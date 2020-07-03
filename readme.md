Installation notes
Microsoft Windows [Version 10.0.18362.900]
(c) 2019 Microsoft Corporation. All rights reserved.
(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>python --version
Python 3.8.3
(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>python -m django --version
C:\Users\issam\Documents\WGU\Capstone\Stella's Choice\venv\Scripts\python.exe: No module named django

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>pip

Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  list                        List installed packages.
  show                        Show information about installed packages.
  check                       Verify installed packages have compatible dependencies.
  config                      Manage local and global configuration.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --isolated                  Run pip in an isolated mode, ignoring environment variables and user configuration.
  -v, --verbose               Give more output. Option is additive, and can be used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output. Option is additive, and can be used up to 3 times (corresponding to WARNING, ERROR, and CRITICAL logging levels).
  --log <path>                Path to a verbose appending log.
  --proxy <proxy>             Specify a proxy in the form [user:passwd@]proxy.server:port.
  --retries <retries>         Maximum number of retries each connection should attempt (default 5 times).
  --timeout <sec>             Set the socket timeout (default 15 seconds).
  --exists-action <action>    Default action when a path already exists: (s)witch, (i)gnore, (w)ipe, (b)ackup, (a)bort).
  --trusted-host <hostname>   Mark this host as trusted, even though it does not have valid or any HTTPS.
  --cert <path>               Path to alternate CA bundle.
  --client-cert <path>        Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
  --cache-dir <dir>           Store the cache data in <dir>.
  --no-cache-dir              Disable the cache.
  --disable-pip-version-check
                              Don't periodically check PyPI to determine whether a new version of pip is available for download. Implied with --no-index.
  --no-color                  Suppress colored output

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>python -m pip install Django
Collecting Django
  Downloading https://files.pythonhosted.org/packages/ca/ab/5e004afa025a6fb640c6e983d4983e6507421ff01be224da79ab7de7a21f/Django-3.0.8-py3-none-any.whl (7.5MB)
    100% |████████████████████████████████| 7.5MB 3.3MB/s
Collecting sqlparse>=0.2.2 (from Django)
  Using cached https://files.pythonhosted.org/packages/85/ee/6e821932f413a5c4b76be9c5936e313e4fc626b33f16e027866e1d60f588/sqlparse-0.3.1-py2.py3-none-any.whl
Collecting pytz (from Django)
  Downloading https://files.pythonhosted.org/packages/4f/a4/879454d49688e2fad93e59d7d4efda580b783c745fd2ec2a3adf87b0808d/pytz-2020.1-py2.py3-none-any.whl (510kB)
    100% |████████████████████████████████| 512kB 7.9MB/s
Collecting asgiref~=3.2 (from Django)
  Downloading https://files.pythonhosted.org/packages/d5/eb/64725b25f991010307fd18a9e0c1f0e6dff2f03622fc4bcbcdb2244f60d6/asgiref-3.2.10-py3-none-any.whl
Installing collected packages: sqlparse, pytz, asgiref, Django
Successfully installed Django-3.0.8 asgiref-3.2.10 pytz-2020.1 sqlparse-0.3.1

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>python -m django --version
3.0.8

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice> django-admin startproject stellachoice

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git init
Initialized empty Git repository in C:/Users/issam/Documents/WGU/Capstone/Stella's Choice/.git/

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .idea/
        manage.py
        stellachoice/
        venv/

nothing added to commit but untracked files present (use "git add" to track)

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   stellachoice/.gitignore

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   stellachoice/.gitignore

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .idea/
        manage.py
        stellachoice/__init__.py
        stellachoice/asgi.py
        stellachoice/settings.py
        stellachoice/urls.py
        stellachoice/wsgi.py
        venv/


(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git add .gitignore

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .gitignore

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        manage.py
        stellachoice/


(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git add *

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>git commit -m "fresh django install"

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"

to set your account's default identity.
Omit --global to set the identity only in this repository.

fatal: unable to auto-detect email address (got 'issam@LAPTOP-50C24O6O.(none)')

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>pip freeze > requirements.txt

(venv) C:\Users\issam\Documents\WGU\Capstone\Stella's Choice>
