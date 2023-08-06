import contextlib
import os 
import re
import shutil
import string
import tempfile
from configparser import RawConfigParser
from io import StringIO
from subprocess import call, check_output
from tempfile import TemporaryDirectory

class GitMachine():

    def __init__(self, gitdir, tempdir, aliases, tar_url=None):
        '''Initializes a GitMachine, takes a directory to store the gits in,
           a tempdirectory, a dictionary of alias values, and an optional
           url for a tarball server.'''
        self._gitdir = gitdir
        self._tmpdir = tempdir
        os.makedirs(self._gitdir, exist_ok=True)
        os.makedirs(self._tmpdir, exist_ok=True)
        self._aliases = aliases
        self._tar_url = tar_url

    def normalize_repo_url(self, repo):
        '''Takes a repository url and returns a normalized version with the
           aliases replaced with their values.'''
        for alias, url in self._aliases.items():
            repo = repo.replace(alias, url)
        if repo.startswith("http") and not repo.endswith('.git'):
            repo = repo + '.git'
        return repo

    def normalize_repo_name(self, repo):
        '''Takes a repository url and returns a string suitable to use as a
           directory name for storing on a filesystem'''
        def transl(x):
            return x if x in valid_chars else '_'
  
        valid_chars = string.digits + string.ascii_letters + '%_'
        url = self.normalize_repo_url(repo)
        if url.endswith('.git'):
          url = url[:-4]
        return ''.join([transl(x) for x in url])
  
    def get_transport_info(self, repo):
        '''Helper function to generate a dictionary of three useful values from
           a given repository url: the normalized url, the normalized name, and
           the actual location of the repository in the gits directory for this
           GitMachine.'''
        i = { 'url': self.normalize_repo_url(repo),
              'name': self.normalize_repo_name(repo) }
        i.update({'dir': os.path.join(self._gitdir, i['name'])})
        return i

    def get_submodule_details(self, checkout):
        '''Takes a path to a checkout of a repository and reads the
           .gitmodules file.'''
        with self._chdir(checkout):
            if os.path.exists('.gitmodules'):
                with open('.gitmodules', "r") as gmfile:
                    content = '\n'.join(
                        [l.strip() for l in gmfile.read().splitlines()])
                io = StringIO(content)
                parser = RawConfigParser()
                parser.readfp(io)
                return parser

    def submodule_info(self, repo, ref, submodule_mask={}, acc=''):
        '''A generator for returning submodule info for a repository at a given
           ref against a submodule mask. This will loop through child
           submodules recursively, returning a dictionary containing the full
           path of that submodule from the top of the initial repository, as
           well as the url and the commit.'''
        self.mirror_repository(repo)
        with TemporaryDirectory() as tmpdir:
            it = self.get_transport_info(repo)
            self._local_checkout(it['dir'], tmpdir, ref)
            p = self.get_submodule_details(tmpdir)
            if not p:
               return
            for x in p.sections():
                submodule = re.sub(r'submodule "(.*)"', r'\1', x)
                path = p.get(x, 'path')
                try:
                    url = submodule_mask[path]['url']
                except:
                    url = p.get(x, 'url')

                with self._chdir(tmpdir):
                    commit = check_output(['git', 'ls-tree', ref, path]).split()
                fields = list(map(lambda x: x.decode('unicode-escape'), commit))
                if len(fields) >= 2 and fields[1] == 'commit':
                    submodule_commit = fields[2]

                    yield { 'path': os.path.join(acc, path), 'url': url, 'commit': submodule_commit } 
                    yield from self.submodule_info(url, submodule_commit, submodule_mask.get(path, {}).get('submodules', {}), path)

    def arrange_into_folder(self, repo, ref, submodule_mask, folder):
        '''Takes a repository url and ref, a submodule mask, and a target
           folder, and checks out the repository into the folder translating
           urls via the mask.'''
        tree = [ { 'path': '', 'url': repo, 'commit': ref } ] + list(self.submodule_info(repo, ref, submodule_mask))
        os.makedirs(folder, exist_ok=True)
        for x in tree:
            it = self.get_transport_info(x['url']) 
            co = os.path.join(folder, x['path'])
            self._local_checkout(it['dir'], co, x['commit'])

    def mirror_repository(self, repo):
        '''Mirror the repository at the url given into the gits directory
           using the fields provided by get_transport_info.'''
        it = self.get_transport_info(repo)
        tar_file = it['name'] + '.tar'
        if not os.path.exists(it['dir']) and self._tar_url is not None:
            try:
                tmpdir = tempfile.mkdtemp()
                with self._chdir(tmpdir), open(os.devnull, "w") as fnull:
                    t = os.path.join(self._tar_url, tar_file)
                    print("Getting %s" % t)
                    call(['wget', t], stdout=fnull, stderr=fnull)
                    call(['tar', 'xf', tar_file], stderr=fnull)
                    call(['git', 'config', 'gc.autodetach', 'false'], stderr=fnull)
                    os.remove(tar_file)
                shutil.move(tmpdir, it['dir'])
            except:
                pass

        if os.path.exists(it['dir']):
            with self._chdir(it['dir']):
                if call(['git', 'fetch', it['url'], '+refs/*:refs/*', '--prune']):
                    raise Exception("Failed to update mirror for %s" % it['url'])
    
        else:
            tmpdir = tempfile.mkdtemp()
            print("Cloning %s" % it['url'])
            if call(['git', 'clone', '--mirror', '-n', it['url'], tmpdir]):
                raise Exception("Failed to clone %s" % it['url'])
            shutil.move(tmpdir, it['dir'])

    def _local_checkout(self, fromdir, todir, commit):
        '''Clone locally from fromdir into todir and checkout at the commit.'''
        with open(os.devnull, "w") as fnull:
            if call(['git', 'clone', '--quiet', '--no-hardlinks', fromdir, todir],
                    stdout=fnull, stderr=fnull):
                raise Exception('Git clone failed for %s' % todir)
            with self._chdir(todir):
                if call(['git', 'checkout', '--force', commit],
                        stdout=fnull, stderr=fnull):
                    raise Exception('Git checkout failed for %s at %s' % (todir, commit))

    @contextlib.contextmanager
    def _chdir(self, dirname=None):
        '''Change to the specified directory.'''
        currentdir = os.getcwd()
        try:
            if dirname is not None:
                os.chdir(dirname)
            yield
        finally:
            os.chdir(currentdir)
