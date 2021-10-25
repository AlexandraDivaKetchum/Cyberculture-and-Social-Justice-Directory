# How to run the "markdown to HTML" script?

_This guide is assuming that you are using OS X or Linux_

**This should only be necessary IF the automated script is not working**

## How to set up project locally
### 1. Install git
[How to install git?](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 2. Copy source code locally

1. Open terminal: [How to open terminal on Os X](https://support.apple.com/en-ca/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)
2. "Clone" repository locally on your machine: 
   1. [How to clone a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
   2. Select a folder and clone source code: e.g. `git clone https://github.com/AlexandraDivaKetchum/Cyberculture-and-Social-Justice-Directory.git /Users/<myUserName>/Documents/cyberculture`
   
### 3. Setup python 3.9.0

1. Download installer from [here](https://www.python.org/downloads/release/python-390/) (scroll to the bottom and find Mac OS installer)
2. Launch installer
3. Open a terminal ([How to open terminal on Os X](https://support.apple.com/en-ca/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac))
4. Install project dependencies:
   1. In the terminal, go to the project root (where you cloned the project documents): `cd /path/of/project` (e.g. `cd /Users/<myUserName>/Documents/cyberculture`)
   2. Then run `pip3 install -r requirements.txt`

## How to run script

_NB: The script will transform the .html files based on the .md files, make sure you are done with your .md changes before running_ 

1. Open terminal: [How to open terminal on Os X](https://support.apple.com/en-ca/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)
2. In the terminal, go to the project root (where you cloned the project documents): `cd /path/of/project` (e.g. `cd /Users/<myUserName>/Documents/cyberculture`)
3. Run the script `python3 markdown_to_html.py`
4. You can preview the changes by opening `index.html` file in your browser

## Uploading modified HTML files

### Option 1: Upload using git with your terminal

_NB: You might be prompted to login into GitHub directly in the terminal_

1. Navigate to the project root using the terminal
2. Sync your local repository with the remote repository: 
   1. `git fetch`
   2. `git pull`
3. Make changes to .md files then run script
4. Prepare changes to be "saved": To add all changed files `git add .` or `git add <file1> <file2> <fileN>` to select only certain files
5. Create a "commit" or save (/!\ This will only be local until pushed): `git commit -m "<Message to describe changes>"`
6. Upload changes online: `git push`

### Option 2: Apply changes online directly

1. Go to the GitHub repository
2. Copy your **final** local changes onto the files using the GitHub file editor (so `index.html` and `about.html`)
3. Save changes

**NB:** Do not change files other that `.html` and `.md` files
