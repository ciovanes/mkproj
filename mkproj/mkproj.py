
""" 
Created on Sat Aug 28 21:31:44 2021
@author: spanishkukli
@summary: Make your projects more easyer and faster.
"""

""""
@usage:
    py mkproj.py <-f, --folder [foldername]>, <-l, --local>, <-r, --remote>, <-p, --path [custom path]>
    py mkproj.py --help
"""



def status():
    return ["\033[31m" + "[ERROR]" + "\033[39m ", 
            "\033[32m" + "[DONE]" + "\033[39m ",
            "\033[33m" + "[WARNING]" + "\033[39m ",
            "\033[39m "]
    
ERROR, DONE, WARNING, RESET = status()


try:
    import os
    import sys
    import json
    from github import Github
    import argparse
    from datetime import datetime
       
except ImportError as err:
	modulename = err.args[0].partition("'")[-1].rpartition("'")[0]
	print(ERROR +  f"It was not possible to import the module: {modulename}")
	sys.exit(-1)
 
 
# Get o.s
opsys = os.name

# Decorator to get func execution time 
def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        func(*args, **kwargs)
        end_time = datetime.now()
        time = end_time - start_time
        print("\033[32m" + "[DONE] in {0:.2f} seconds".format(time.total_seconds()) + RESET)
    
    return wrapper


def yesno(text):
    yes = ["yes", "y", ""]
    no = ["no", "n"]
    while True:
        answer = input(text + "[Y/n]").lower()
        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            print("Invalid answer")

# Get all script args
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", type=str, help="Add a name to your folder project",  required=True)
    parser.add_argument("-l", "--local", help="Create all local files (github and vevn)", action='store_true')
    parser.add_argument("-r", "--remote", help="Create a repository and upload all the files in your github",  action='store_true')
    parser.add_argument("-p", "--path", type=str, help="Custom path for your project")
    args = parser.parse_args()
    
    return args

# Get path to save files
def get_path(args):
    with open("config.json") as f:
        data = json.load(f)
        custom_path = data["custom_filepath"]
      
    #Check if there is a custom file in config.json and path arg at the same time  
    if len(custom_path) > 0 and args.path:
        keep_it = yesno(WARNING + f"You already have an custom path on config.json, you want to keep it? \n config.json -> {custom_path}")
        if keep_it is True:
            path = data["custom_filepath"]
        else:
            path = args.path
    elif len(custom_path) > 0:
        path = data["custom_filepath"]
    elif args.path:
        path = args.path 
    else:
        path = os.getcwd()
   
    foldername = str(args.folder)
    _dir = path + "{}".format('\\' if opsys == 'nt' else '/') + foldername
        
    return foldername, path, _dir
    
# Get github data from config.json
def get_gh_data():
    with open("config.json") as f:
        data = json.load(f)
        token = data["token"]
        privacity = bool(data["private_repo"])
        
    return token, privacity

# Create all local files
class Local:
    def __init__(self, foldername, path, _dir, opsys):
        self.foldername = foldername
        self.path = path
        self._dir = _dir
        self.opsys = opsys

        
    def make_dir(self):
        try:
            os.mkdir(self._dir)
            os.chdir(self._dir)
        except FileExistsError:
            print(ERROR + f"Cannot create a file when that file already exists:{self._dir}")
            sys.exit(-1)
        
    
    def create_local_git(self):
        git_local = ["git init",
                f"echo # {self.foldername} > README.md",
                "echo venv/ > .gitignore"
                ]

        for command in git_local:
            os.system(command)
    
        print(DONE + f"Created git local files in {self._dir}")
    
    
    def create_venv(self):
        os.system("python -m venv venv")
        print(DONE + f"Created venv local files in {self._dir}")
    
    
    def activate_venv(self):
        if self.opsys == "nt":
            os.chdir(self._dir + "\\venv\\Scripts")
            os.system("echo cmd /k >> activate.bat")
            os.system("activate.bat")
        else:
            print(WARNING + f"It`s not possible to activate venv on {opsys}, actually only available on windows")
        
# Create git repository and upload all files
class Remote:
    def __init__(self, token, privacity, user, login, repos, foldername):
        self.token = token
        self.privacity = privacity
        self.user = user
        self.login = login
        self. repos = repos
        self.foldername = foldername        
        
    def create_repo(self):
        if self.repos == 0:
            print(ERROR + "This repo already exist!")
            sys.exit(-1)
        else:
            self.user.create_repo(self.foldername, private=self.privacity)    
            print(DONE + f"All files will be uploaded to https://github.com/{self.login}/{self.foldername}")
    
    
    def push_files(self):
        push = [f"git remote add origin https://github.com/{self.login}/{self.foldername}.git",
            "git add *",
            'git commit -m "Initial commit"',
            "git push -u origin master"]

        for i in push:
            os.system(i)
            
        print(DONE + f"All files pushed at https://github.com/{self.login}/{self.foldername}")


@execution_time
def local_func(local):
    local.make_dir()
    local.create_local_git()
    local.create_venv()
    

@execution_time
def remote_func(local, remote):
    remote.create_repo()
    local.make_dir()
    local.create_local_git()
    local.create_venv()
    remote.push_files()
    
  
    
def main():
    args = get_args()
    
    if not args.local and not args.remote:
        print(ERROR + "You need to specify where you want to create your files <-l, --local> or <-r, --remote>")
        sys.exit(-1)
    
    if args.local and args.remote:
        print(ERROR + "You only can choose one arg <-l, --local> or <-r, --remote>")
        sys.exit(-1)
    
    foldername, path, _dir = get_path(args)
    local = Local(foldername, path, _dir, opsys)
    
    if args.local:
        local_func(local)
        local.activate_venv()
        sys.exit(0)
    
    if args.remote:
        token, privacity = get_gh_data()
        g = Github(token)
        user = g.get_user()
        login = user.login
        repos = os.system(f"git ls-remote https://github.com/{login}/{foldername}")
        remote = Remote(token, privacity, user, login, repos, foldername)
        
        remote_func(local, remote)
        local.activate_venv()
        sys.exit(0)  



if __name__ == "__main__":
    main()
