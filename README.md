# MKPROJ 

<p align="center">
  <img src="https://github.com/spanishkukli/mkproj/blob/master/mkproj/img/example.gif">
</p>

## Install:

    git clone https://github.com/spanishkukli/mkproj.git
    cd mkproj 
    pip install -r requirements.txt  
    
#### Or use:

    clone_proj.bat

## Get github token:

    https://github.com/settings/tokens
    Only give repo, workflow, write:packages and delete:packages permissions
    
## Config.json:

    {
    "token":"YOUR TOKEN HERE",
    "private_repo":"True or False",
    "custom_filepath": ".:\\...\\..."
    }

## Usage:

    python mkproj.py [-h] [-f FOLDER] [-l ] [-r] [-p PATH]
    
    optional arguments:
      -h, --help            show this help message and exit
      -f FOLDER, --folder FOLDER Add a name to your folder project
      -l, --local           Create all local files (github and vevn)
      -r, --remote          Create a repository and upload all the files in your github
      -p PATH, --path PATH  Custom path for your project
      
## Contributing
- [Pull requests](https://github.com/spanishkukli/mkproj/pulls) and stars are always welcome.
- For major changes, please open an [issue](https://github.com/spanishkukli/mkproj/issues) first to discuss what you would like to change.
- Please make sure to update tests as appropriate.
