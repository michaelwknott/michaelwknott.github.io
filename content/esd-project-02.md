Title: Monitoring and Prescribing Individualised Conditioning Sessions: Part 2
Date: 2023-07-04 13:30
Category: ESD
Tags: projects, esd
Authors: Michael Knott
Summary: Project Set-up
Status: Draft

In [part 1](https://michaelwknott.github.io/monitoring-and-prescribing-individualised-conditioning-sessions:-part-1.html) I outlined the rationale for the project and my plans for structuring the project using a three-layered architecture. Today's post will focus on my project set-up workflow.


## Project Set-up

1. Create a new virtual environment for the project and upgrade pip, setuptools and wheel.

```
esd$ python -m venv .venv --prompt .

esd/$ source .venv/bin/activate

(esd) esd/$ python -m pip install -U pip setuptools wheel
```

2. Initiate a git repository in the project directory for version control and add a `.gitignore` file. Add the `.venv` directory to the `.gitignore` file to avoid commiting the virtual environment to version control.

```
(esd) esd/$ git init

(esd) esd/$ echo .venv > .gitignore
```
3. Install `pip-tools` to manage dependencies. I use pip-tools as it provides a detailed requirements file outlining the source of each dependency installed in the project.

```
(esd) esd/$ python -m pip install pip-tools
```

4. Create a `requirements.in` and `requirements-dev.in` file for project and development dependencies respectively.

```
(esd) esd/$ touch requirements.in requirements-dev.in
```

5.  Constrain the development dependencies with the main project dependencies to avoid dependency conflicts.

```
(esd) esd/$ echo -c requirements.txt >> requirements-dev.in
```

6. Add the required development dependencies to `requirements-dev.in`.

```
(esd) esd/$ echo -e "pre-commit\nblack\nruff\nmypy\npytest" >> requirements-dev.in
```

7. Add the required project dependencies to `requirements.in`.

```
(esd) esd/$ echo -e "fastapi[all]\nSQLAlchemy" >> requirements.in
```

8. Compile the requirements.txt and requirements-dev.txt files. Ensure to compile the requirements.txt first as requirements-dev.in will use this as the constraint file.

```
(esd) esd/$ pip-compile requirements.in
(esd) esd/$ pip-compile requirements-dev.in
```

9. Install dependencies within the virtual environment.

```
(esd) esd/$ python -m pip install -r requirements.txt -r requirements-dev.txt
```

10. Create a `pyproject.toml` file and configure development dependencies. I've included defaults from Ruff in the `pyproject.toml` configuration to be explicit about settings. 

```
(esd) esd/$ touch pyproject.toml

```
```
# pyproject.toml

[tool.mypy]
python_version = 3.11
warn_unused_configs = true
warn_return_any = true
disallow_untyped_defs = true
warn_unused_ignores = true
warn_redundant_casts = true
show_error_context = true
pretty = true

[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
# Enable pycodestyle (`E`), Pyflakes (`F`), pycodestyle warnings (`W`),
# McCabe complexity (`C901`), pep8-naming (`N`), pydocstyle (`D`),
# pyupgrade (`UP`) and pylint (`PL`).
select = ["E", "F", "W", "C901", "N", "D", "UP", "PL"]
ignore = []

# Allow autofix for all enabled rules (when `--fix`) is provided.
fixable = ["ALL"]
unfixable = []

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "venv",
]
per-file-ignores = {}

# Same as Black.
line-length = 88

# Allow unused variables when underscore-prefixed.
dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

# Assume Python 3.11.
target-version = "py311"

[tool.ruff.isort]
# Placeholder for future configuration.

[tool.ruff.mccabe]
# Flag errors (`C901`) whenever the complexity level exceeds 10.
max-complexity = 10

[tool.ruff.pep8-naming]
# Placeholder for future configuration.

[tool.ruff.pydocstyle]
# Use Google-style docstrings.
convention = "google"

[tool.ruff.pylint]
# Placeholder for future configuration.

[tool.ruff.pyupgrade]
# Placeholder for future configuration.
```

11. Create a `.pre-commit-config.yaml` to configure `pre-commit`. Running `pre-commit` before each git commit ensures code quality and consistency across the project.

```
# .pre-commit-config.yaml

repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: check-yaml
    -   id: end-of-file-fixer
    -   id: trailing-whitespace
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        args: ['--config=./pyproject.toml']
-   repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.276
    hooks:
      - id: ruff
-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: 'v1.4.1'
    hooks:
    -   id: mypy
        args: [--no-strict-optional, --ignore-missing-imports]
        additional_dependencies: [
          fastapi==0.99.1,
          sqlalchemy==2.0.17,
          typing-extensions==4.7.1
        ]
```

12. Use the `pre-commit` autoupdate command to update hooks to the latest version and install the git hook scripts.

```
(esd) esd/$ pre-commit autoupdate

(esd) esd/$ pre-commit install
```

13. Create a `.editorconfig` file to ensure consistency in formatting when collaborating with other developers.

```
(esd) esd/$ touch .editorcongig

# .editorconfig
root = true
[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
trim_trailing_whitespace = true
insert_final_newline = true
[*.html]
indent_size = 2
```

14. Configure local settings for VSCode. I currently use VSCode as my text editor/IDE.

```
(esd) esd/$ touch .vscode/settings.json

# .vscode/settings.json

{
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true,
    },
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "editor.rulers": [
        88,
    ],
    "python.analysis.typeCheckingMode": "strict",
}
```

15. Create project structure. I add `athlete.py` and `test_athlete.py` files as placeholders in the `esd` and `tests` directories respectively.

```
(esd) esd/$  mkdir esd tests && touch esd/athlete.py tests/test_athlete.py
# Project tree after adding esd and tests directories

esd
├── .venv
├── .vscode
│   └──settings.json 
├── esd
│   └──athlete.py
├── tests
│   └──test_athlete.py
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements-dev.in
├── requirements-dev.txt
├── requirements.in
└── requirements.txt
```

16. Create a GitHub repository with `README.md` and `LICENSE` files.

```
![Creating a GitHub Repository]({static}/images/create-github-repo.png "Creating a GitHub repository"){style="display: block; margin: 0 auto"}
```

17.  Link `esd` project to GitHub repository, add and commit project set-up changes and push changes to GitHub.

```
# Add files to staging in local repo
(esd) esd/$ git add .

# Commit files in local repo
(esd) esd/$ git commit -m "Project set-up"

# Link local repository with remote repository on GitHub
(esd) esd/$ git remote add origin git@github.com:michaelwknott/esd.git

# Check the link between repositories has worked
(esd) esd/$ git remote -v

# Change the name of `master` to `main`
(esd) esd/$ git branch -m main

# Rebase local repository with the remote main branch. The local repository doesn't have `README.md` and `LICENSE` and needs these changes before pushing to the remote repository 
(esd) esd/$ git pull origin main --rebase

# Push changes in local repository to GitHub
(esd) esd/$ git push origin main 
```

The final project structure looks as follows:

```
esd
├── .venv
├── .vscode
│   └──settings.json 
├── esd
│   └──athlete.py
├── tests
│   └──test_athlete.py
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements-dev.in
├── requirements-dev.txt
├── requirements.in
└── requirements.txt
```