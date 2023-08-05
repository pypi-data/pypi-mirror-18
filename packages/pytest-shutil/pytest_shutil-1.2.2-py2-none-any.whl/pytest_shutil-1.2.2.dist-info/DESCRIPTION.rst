# pytest-shutil


This library is a goodie-bag of Unix shell and environment management tools for automated tests.
A summary of the available functions is below, look at the source for the full listing.

## Installation

Install using your favourite package manager::

```bash
    pip install pytest-shutil
    #  or..
    easy_install pytest-shutil
```               

## Workspace Fixture

The workspace fixture is simply a temporary directory at function-scope with a few bells and whistles::

```python
    # Enable the fixture explicitly in your tests or conftest.py (not required when using setuptools entry points)
    pytest_plugins = ['pytest_shutil']

    def test_something(workspace):
        # Workspaces contain a handle to the path.py path object (see https://pythonhosted.org/path.py)
        path = workspace.workspace         
        script = path / 'hello.sh'
        script.write_text('#!/bin/sh\n echo hello world!')

        # There is a 'run' method to execute things relative to the workspace root
        workspace.run('hello.sh')
```

## ``pytest_shutil.env``: Shell helpers

| function  | description
| --------- | -----------
| set_env   | contextmanager to set env vars 
| unset_env | contextmanager to unset env vars 
| no_env    | contextmanager to unset a single env var 
| no_cov    | contextmanager to disable coverage in subprocesses 

## ``pytest_shutil.cmdline``: Command-line helpers

| function  | description
| --------- | -----------
| umask                      | contextmanager to set the umask
| chdir                      | contextmanager to change to a directory
| TempDir                    | contextmanager for a temporary directory
| PrettyFormatter            | simple text formatter for drawing title, paragrahs, hrs. 
| copy_files                 | copy all files from one directory to another
| getch                      | cross-platform read of a single character from the screen
| which                      | analoge of unix ``which``
| get_real_python_executable | find our system Python, useful when running under virtualenv

## ``pytest_shutil.run``: Running things in subprocesses

| function  | description
| --------- | -----------
| run                | run a command, with options for capturing output, checking return codes.
| run_as_main        | run a function as if it was the system entry point
| run_module_as_main | run a module as if it was the system entry point
| run_in_subprocess  | run a function in a subprocess
| run_with_coverage  | run a command with coverage enabled


## Changelog

### 1.2.2 (2016-10-2r70)
 * Python 3 compatibility across most of the modules
 * Fixed deprecated Path.py imports (Thanks to Bryan Moscon)
 * Fixed deprecated multicall in pytest-profiling (Thanks to Paul van der Linden for PR)
 * Added devpi-server fixture to create an index per test function
 * Added missing licence file
 * Split up httpd server fixture config so child classes can override loaded modules easier
 * Added 'preserve_sys_path' argument to TestServer base class which exports the current python sys.path to subprocesses. 
 * Updated httpd, redis and jenkins runtime args and paths to current Ubuntu spec
 * Ignore errors when tearing down workspaces to avoid race conditions in 'shutil.rmtree' implementation

### 1.2.1 (2016-3-1)
 * Fixed pytest-verbose-parametrize for latest version of py.test

### 1.2.0 (2016-2-19)
 * New plugin: git repository fixture

### 1.1.1 (2016-2-16)
 * pytest-profiling improvement: escape illegal characters in .prof files (Thanks to Aarni Koskela for the PR)

### 1.1.0 (2016-2-15)

 * New plugin: devpi server fixture
 * pytest-profiling improvement: overly-long .prof files are saved as the short hash of the test name (Thanks to Vladimir Lagunov for PR)
 * Changed default behavior of workspace.run() to not use a subshell for security reasons
 * Corrected virtualenv.run() method to handle arguments the same as the parent method workspace.run()
 * Removed deprecated '--distribute' from virtualenv args

### 1.0.1 (2015-12-23)

 *  Packaging bugfix

### 1.0.0 (2015-12-21)

 *  Initial public release



