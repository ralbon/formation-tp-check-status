# Formation TP check status

This project allows you to check status of an TP environment.

Note: 
- API, developped in Python, uses a `checks.yaml` (list of tasks to execute)
- API will run locally on port 4000

# Prerequisites

## Tools: 
- Python3

Note that depending on taks you want to run to check status, you might need to install extra tools.

# Installation

Go to `src` directory:
```bash
cd src
```

(OPTIONAL) Use a python virtual environment with `pyenv`:
```bash
pyenv install 3.10.9
pyenv virtualenv 3.10.9 formation-tp-check-status
pyenv local formation-tp-check-status
```

Update list of tasks that you want to execute to check status: 
```
vi checks.yaml
```

Run application locally:
```
python3 app.py
```

# Usage
Once API is deployed locally, you can access to application data:
```
curl http://localhost:4000
```

