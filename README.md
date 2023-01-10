## Install & Setup virtual environment
Build DEV environment (Python Virtual Environment)
Create and activate virtual environment for local development

```bash 
python3 -m venv .venv
echo "export PYTHONPATH=$PWD" >> .venv/bin/activate
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
``` 

## Build custom Docker image

```bash
./scripts/build_image.sh
```

## Run DVC pipeline

```bash
dvc exp run
```