import argparse
import box
import json
import logging
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from typing import List, Set,Text
import yaml

from src.utils.config import load_config
from src.utils.logging import get_logger


def prepare_data(config_path: Text) -> None:

    config: box.ConfigBox  = load_config(config_path)
    logger: logging.Logger = get_logger('PREPARE_DATA', config.base.log_level)
    class_names_set: Set = set()

    logger.info('Load annotations')
    datasets_dir: Path = Path(config.data.datasets_dir)
    dataset_path: Path = datasets_dir / config.data.dataset
    # It's assumed that annotations:
    # 1) are located in directory <dataset_dir>/labels
    # 2) are in Label Studio JSON format (https://labelstud.io/guide/export.html#Label-Studio-JSON-format-of-annotated-tasks)
    annotations_dir: Path = dataset_path / 'labels'
    annotations_path: Path = annotations_dir / 'annotations.json'
    
    with open(annotations_path) as annotations_f:
        annotations = json.load(annotations_f)

    logger.info('Build class names set')
    for img_annots in map(box.ConfigBox, annotations):
        detected_objects: List[box.ConfigBox] = img_annots.annotations[0].result
        for obj in detected_objects:
            # Update dataset class names set
            class_names_set.update(obj.value.rectanglelabels)

    class_names: List = sorted(list(class_names_set))
    
    logger.info('Parse annotations')
    for img_annots in map(box.ConfigBox, annotations):

        image_name: Text = Path(img_annots.data.image).stem
        detected_objects: List[box.ConfigBox] = img_annots.annotations[0].result

        with open(annotations_dir / f'{image_name}.txt', 'w') as img_objs_f:
            for obj in detected_objects:
                
                # Read coordinates and sizes
                original_width: int = obj.original_width
                original_height: int = obj.original_height
                x: float = obj.value.x
                y: float = obj.value.y
                width: float = obj.value.width
                height: float = obj.value.height

                # Convert image coordinates and sizes to pixels
                pixel_x: float = x / 100.0 * original_width
                pixel_y: float = y / 100.0 * original_height
                pixel_width: float = width / 100.0 * original_width
                pixel_height: float = height / 100.0 * original_height

                # Convert images coordinates and sizes to YOLO format
                pixel_x2: float = pixel_x + pixel_width
                pixel_y2: float = pixel_y + pixel_height

                b_center_x: float = (pixel_x + pixel_x2) / 2
                b_center_y: float = (pixel_y + pixel_y2) / 2
                b_width: float = (pixel_x2 - pixel_x)
                b_height: float = (pixel_y2 - pixel_y)

                b_center_x /= original_width
                b_center_y /= original_height
                b_width /= original_width
                b_height /= original_height

                # It's assumed that each object corresponds to one label
                class_name: Text = obj.value.rectanglelabels[0]
                class_idx: int = class_names.index(class_name)

                img_objs_f.write(f'{class_idx} {b_center_x} {b_center_y} {b_width} {b_height}\n')
    
    logger.info('Create train/val indices')
    images_dir: Path = dataset_path / 'images'
    images: List[Text] = os.listdir(images_dir)
    images.sort()

    if config.prepare_data.is_validate:
        val_size: float = config.prepare_data.val_size
        train_images, val_images = train_test_split(
            images, test_size=val_size, shuffle=False, random_state=42
        )
    else:
        train_images, val_images = images, images

    with open(dataset_path / 'train.txt', 'w') as train_index_f:
        for img in train_images:
            train_index_f.write(f'./images/{img}\n')

    with open(dataset_path / 'val.txt', 'w') as val_index_f:
        for img in val_images:
            val_index_f.write(f'./images/{img}\n')

    logger.info('Create YOLO data config')
    yolo_config = {
        'path': (Path('..') / dataset_path).as_posix(),
        'train': 'train.txt',
        'val': 'val.txt',
        'names': dict(zip(range(len(class_names)), class_names))
    }
    
    data_config_path = Path(config.data.data_configs_dir) / f'{config.data.dataset}.yaml'
    with open(data_config_path, 'w') as yolo_conf_f:
        yaml.safe_dump(yolo_config, yolo_conf_f, sort_keys=False)


if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config', dest='config', required=True)
    args = args_parser.parse_args()

    prepare_data(config_path=args.config)
