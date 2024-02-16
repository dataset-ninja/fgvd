import os
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/IDD_FGVD"
    images_folder = "images"
    bboxes_folder = "annos"
    batch_size = 30
    images_ext = ".jpg"
    bboxes_ext = ".xml"

    def create_ann(image_path):
        labels = []

        ann_path = image_path.replace(images_folder, bboxes_folder).replace(images_ext, bboxes_ext)

        if file_exists(ann_path):
            tree = ET.parse(ann_path)
            root = tree.getroot()

            img_height = int(root.find(".//height").text)
            img_wight = int(root.find(".//width").text)

            all_objects = root.findall(".//object")

            for curr_object in all_objects:
                tags = []
                all_name = curr_object.find(".//name").text
                split_name = all_name.split("_")
                class_name = split_name[0]
                if len(split_name) == 3:
                    model = sly.Tag(model_meta, value=split_name[2])
                    manufacturer = sly.Tag(manufacturer_meta, value=split_name[1])
                    tags.extend([manufacturer, model])
                elif len(split_name) == 2:
                    manufacturer = sly.Tag(manufacturer_meta, value=split_name[1])
                    tags.append(manufacturer)
                obj_class = meta.get_obj_class(class_name)
                coords_xml = curr_object.findall(".//bndbox")
                for curr_coord in coords_xml:
                    left = float(curr_coord[0].text)
                    top = float(curr_coord[1].text)
                    right = float(curr_coord[2].text)
                    bottom = float(curr_coord[3].text)

                    rect = sly.Rectangle(
                        left=int(left), top=int(top), right=int(right), bottom=int(bottom)
                    )
                    label = sly.Label(rect, obj_class, tags=tags)
                    labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    mini = sly.ObjClass("mini-bus", sly.Rectangle)
    car = sly.ObjClass("car", sly.Rectangle)
    autorickshaw = sly.ObjClass("autorickshaw", sly.Rectangle)
    bus = sly.ObjClass("bus", sly.Rectangle)
    scooter = sly.ObjClass("scooter", sly.Rectangle)
    motorcycle = sly.ObjClass("motorcycle", sly.Rectangle)
    truck = sly.ObjClass("truck", sly.Rectangle)

    manufacturer_meta = sly.TagMeta("manufacturer", sly.TagValueType.ANY_STRING)
    model_meta = sly.TagMeta("model", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[mini, car, autorickshaw, bus, scooter, motorcycle, truck],
        tag_metas=[manufacturer_meta, model_meta],
    )
    api.project.update_meta(project.id, meta.to_json())

    for ds_name in os.listdir(dataset_path):

        images_path = os.path.join(dataset_path, ds_name, images_folder)
        bboxes_path = os.path.join(dataset_path, ds_name, bboxes_folder)

        images_names = os.listdir(images_path)

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(images_path, image_name) for image_name in images_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
