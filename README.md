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

## Data configs

Create or copy `YOLOv5` dataset config and put it to directory `data_configs/`.

**Note**: `data_configs/` contains examples of configs using you can create or generate custom configs.

## Configure datasets directory path

Specify value of parameter *data.datasets_dir*:

`params.yaml`
```yaml
data:
  datasets_dir: <datasets_dir_path>
```

**Note**: datasets directory is a directory which contains dataset subdirectories:
```
<datasets_dir>
├── <dataset_1>
├── <dataset_2>
├── <....>
└── <dataset_N>
```

Dataset directory path can be:

- directory in the repo, example:
    
    `params.yaml`
    ```yaml
    data:
        datasets_dir: $(pwd)/datasets
    ```
    
  **Note**: in this case the path starts with `$(pwd)` because this path will be used for mounting to `Docker` environment and it must be absolute

- directory outside the repo, example:

    `params.yaml`
    ```yaml
    data:
        datasets_dir: /home/user/datasets
    ```

- environment variable, example:

    `params.yaml`
    ```yaml
    data:
        datasets_dir: ${DATASETS_DIR}
    ```

    In this case you have to define environment variable before pipeline execution, example:

    ```bash
    export DATASET_DIR=/home/user/datasets
    dvc exp run
    ```

    Main advantage of this approach: each member of the team can specify custom path but value of *data.datasets_dir*  in `params.yaml` will be the same for all members.


## Run DVC pipeline

```bash
dvc exp run
```