# Py.test Fixture Configuration

Simple configuration objects for Py.test fixtures. 
Allows you to skip tests when their required config variables aren't set.

## Installation

Install using your favourite package manager:

```bash
    pip install pytest-fixture-config
    #  or..
    easy_install pytest-fixture-config
```

Enable the fixture explicitly in your tests or conftest.py (not required when using setuptools entry points):

```python
    pytest_plugins = ['pytest_fixture_config']
```


## Specifying Configuration

To specify your variables you create a class somewhere in your plugin module,
and a singleton instance of the class which reads the variables from wherever
you want. In this example we read them from the shell environment:

```python
    import os
    from pytest_fixture_config import Config

    class FixtureConfig(Config):
        __slots__ = ('log_dir', 'log_watcher')

    CONFIG=FixtureConfig(
        log_dir=os.getenv('LOG_DIR', '/var/log'),       # This has a default
        log_watcher=os.getenv('LOG_WATCHER'),           # This does not 
    )
```    

## Using Configuration

Simply reference the singleton at run-time in your fixtures:

```python
    import pytest

    @pytest.fixture
    def log_watcher():
        return subprocess.popen([CONFIG.log_watcher, '--log-dir', CONFIG.log_dir])

    def test_log_watcher(watcher):
        watcher.communicate()
```

## Skipping tests when things are missing

There are some decorators that allow you to skip tests when settings aren't set.
This is useful when you're testing something you might not have installed
but don't want your tests suite to fail:

```python
    from pytest_fixture_config import requires_config

    @requires_config(CONFIG, ['log_watcher', 'log_dir'])
    @pytest.fixture
    def log_watcher():
        return subprocess.popen([CONFIG.log_watcher, '--log-dir', CONFIG.log_dir])
```

There is also a version for yield_fixtures:

```python
    from pytest_fixture_config import yield_requires_config

    @yield_requires_config(CONFIG, ['log_watcher', 'log_dir'])
    @pytest.fixture
    def log_watcher():
        watcher = subprocess.popen([CONFIG.log_watcher, '--log-dir', CONFIG.log_dir])
        yield watcher
        watcher.kill()
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



