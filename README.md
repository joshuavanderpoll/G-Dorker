# G-Dorker
**A Python3 script for automating Google search queries.**
This script attempts to request search queries to Google by disguising as a MacBook Chrome browser. All found links from Google are stored in a `output.json` file.

## Installation
```
$ git clone https://github.com/joshuavanderpoll/G-Dorker.git
$ cd G-Dorker/
$ virtualenv -p python3 .venv  # Setup virtual environment (OPTIONAL)
$ source .venv/bin/activate    # Start virtual environment (OPTIONAL)
$ pip3 install -r requirements.txt
$ python3 gdorker.py -h
```

## Usage
```
$ python3 gdorker.py --query="intitle:\"Index of /backup\"" --pages=100
```

## Troubleshooting
**You are sending too many requests**
This happens when Google receives to much suspicious requests. Because we run this as a Python script we can't complete the Captcha thats given. You can prevent this by changing the `--sleep` argument to a higher number or using mutiple proxies.

## Future
- [ ] Add more decoy browser information
- [ ] More dynamic script arguments
    - [x] Output path/type
    - [x] Proxy support