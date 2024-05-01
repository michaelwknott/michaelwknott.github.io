Title: TIL: Prevent global package installation when using pip 
Date: 2024-05-01 20:00
Category: Python
Tags: TIL, Python, pip
Authors: Michael Knott
Summary: Setting `PIP_REQUIRE_VIRTUALENV=true` to prevent global package installation
Status: Published

## Setting the `PIP_REQUIRE_VIRTUALENV` environment variable

After several instances of accidentally installing packages into the global Python environment, I decided to look for a way to prevent this from happening. A quick Google search revealed that you can set the `PIP_REQUIRE_VIRTUALENV` environment variable to `true` to prevent pip from installing packages globally.

To ensure this runs every time I open a new terminal session, I added the following line to my `.bashrc` file:

```bash
# Prevent global package installation when using pip
export PIP_REQUIRE_VIRTUALENV=true
```

The only thing I'll need to remember is to set `PIP_REQUIRE_VIRTUALENV=false` when installing pipx to each version of Python I install with pyenv.
