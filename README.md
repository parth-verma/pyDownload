# PyDownload

This package aims to provide the functionality to download large files from the internet using chunked and multithreaded downloads.

# Index
 - [Command Line Usage](#command-line-usage)
 - [Installation](#installation)
 - [Usage](#usage)
 - [Developer Guide](#developer-guide)
 - [SayThanks](#saythanks)

# Command Line usage

The package can be used to perform multithreaded downloads via the CLI.

### Usage

```bash
pyDownload https://github.com/party98/Python-Parallel-Downloader/archive/master.zip
```

### Config Options
```bash
positional arguments:
  url                   list of urls to download

optional arguments:
  -h, --help            show this help message and exit
  -o FILENAME, --output FILENAME
                        output file
  -t NUM_THREADS, --threads NUM_THREADS
                        number of threads to use
  -c CHUNK_SIZE, --chunk-size CHUNK_SIZE
                        chunk size (in bytes)
  --single-multithreaded
                        use multithreading to download file.
  --version             display the version of pyDownload being used
```

# Installation

```bash
pip install pydownload
```

# Usage

```python
import time
from pyDownload import Downloader

url = 'https://github.com/party98/Python-Parallel-Downloader/archive/master.zip'
downloader = Downloader(url=url)
if downloader.is_running:
    time.sleep(1)
print('File downloaded to %s' % downloader.file_name)
```



# Developer Guide

## Setting Up The Environment
 - ### Setup VirtualEnv (Recommended But Optional)
   ```bash
   pip install virtualenv
   virtualenv env
   source ./env/bin/activate
   ```
 - ### Install Dependencies
   ```bash
   pip install .[dev]
   ```
 -  ### Install pre-commit hooks
    The project uses various pre-commit hooks to enforce code quality and standards. Therefore, it is really necessary for all the contributors to install these and run before every commit else the contributions will be rejected.

    ##### Steps
    ```bash
    pre-commit install
    ```

## Running Tests
 - ### Install Dependencies
   ```bash
   pip install .[test]
   ```
 - ### Run the Tests
   - #### With Coverage Report (Recommended)
     ```
     nosetests --cover-erase --cover-package=pyDownload --with-coverage --cover-branches
     ```
   - #### Without Coverage Report
     ```
     nosetests --cover-erase --cover-package=pyDownload  --cover-branches
     ```


# SayThanks

You can thank the team [here](https://saythanks.io/to/party98).
