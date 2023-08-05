# Pytest SVN Fixture

Creates an empty SVN repository for testing that cleans up after itself on teardown.

## Installation

Install using your favourite package installer:
```bash
    pip install pytest-svn
    # or
    easy_install pytest-svn
```

Enable the fixture explicitly in your tests or conftest.py (not required when using setuptools entry points):

```python
    pytest_plugins = ['pytest_svn']
```

## Usage

Here's a noddy test case that shows it working:

```python
def test_svn_repo(svn_repo):
    # The fixture derives from `workspace` in `pytest-shutil`, so they contain 
    # a handle to the path.py path object (see https://pythonhosted.org/path.py)
    path = svn_repo.workspace
    file = path / 'hello.txt'
    file.write_text('hello world!')

    # We can also run things relative to the repo
    svn_repo.run('svn add hello.txt')

    # The fixture has a URI property you can use in downstream systems
    assert svn_repo.uri.startswith('file://')
```

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



