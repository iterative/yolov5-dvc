## Install & Setup virtual environment
Build DEV environment (Python Virtual Environment)
Create and activate virtual environment for local development

```bash 
python3 -m venv .venv
echo "export PYTHONPATH=$PWD" >> .venv/bin/activate
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
# git clone https://github.com/ultralytics/yolov5.git
# pip install -r yolov5/requirements.txt

``` 

## Build custom Docker image

```bash
./scripts/build_image.sh
```

## Run DVC pipeline

```bash
dvc exp run
```

## Setup CI/CD

Config `.github/workflows/cml_vision_detection.yml` implements [`CML`](https://cml.dev/) CI pipeline (GitHub Actions workflow).

Preparation steps:

1. create `GitHub` **Personal Access Token** (**PAT**): https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

2. create `GitHub Action` *secret* with **PAT**: 
    - instruction how to add encrypted secrets: https://docs.github.com/en/actions/security-guides/encrypted-secrets
    - secret's name and value:
        ```dotenv
        PERSONAL_ACCESS_TOKEN=<PAT>
        ```

3. (Optional) test the workflow locally:
- download, configure and run self-hosted runner: https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners
**Notes**: 
    - the runner configuration script will ask additional info - add additional label `cml-runner`
    - alternative option - you can add label `cml-runner` manually or using the configuration script parameter: https://docs.github.com/en/actions/hosting-your-own-runners/using-labels-with-self-hosted-runners
- create new branch starts with ***exp-cloud*** and push it into your repository fork
- open tab `Actions` in the repository on `GitHub` to observe the workflow execution