import argparse
from imagemetadata import MetadataProcessor
import projection
import os

IMAGE_FORMATS = ('.bmp', '.jpg', '.png')
PROJECTOR = projection.ImageProjection()
PROCESSOR = MetadataProcessor()

def get_args():
    parser = argparse.ArgumentParser(description='Preprocess folder to ensure \
                                                  valid metadata and correct time')
    parser.add_argument('-i', '--input_dir', help='specify input directory',
                        required=True)
    return parser.parse_args()


def run(input_folder_path):
    images_with_bad_metadata = set()
    walk = os.walk(input_folder_path)
    for root, _, files in walk:
        for file in files:
            path = os.path.join(root, file)
            if not file.lower().endswith(IMAGE_FORMATS):
                continue
            if not check_metadata_exists_and_valid(path):
                images_with_bad_metadata.add(path)

    if input(f'encountered {len(images_with_bad_metadata)} images with \
invalid metadata would you like to remove them? (Y/n)').lower() == 'y':
        for path in images_with_bad_metadata:
            os.remove(path)

    images_with_bad_projection = set()
    walk = os.walk(input_folder_path)
    for root, _, files in walk:
        for file in files:
            path = os.path.join(root, file)
            if not file.lower().endswith(IMAGE_FORMATS):
                continue
            text = PROCESSOR.ReadFromImageFilePath(path)
            metadata = PROCESSOR.Read(text)
            if not check_projection(metadata, path):
                images_with_bad_projection.add(path)

    if input(f'encountered {len(images_with_bad_projection)} images with \
possible bad projections would you like to remove them? (Y/n)').lower() == 'y':
        for path in images_with_bad_metadata:
            os.remove(path)


def check_metadata_exists_and_valid(path: str) -> bool:
    try:
        text = PROCESSOR.ReadFromImageFilePath(path)
    except ValueError as e:
        print_exception_in_processing(e, path)
        return False
    try:
        PROCESSOR.Process(text)
    except ValueError as e:
        print_exception_in_processing(e, path)
        return False
    return True

def check_projection(metadata: dict, path: str) -> bool:
    longitude = metadata["corrected"]["gps"]["longitude"]
    latitude = metadata["corrected"]["gps"]["latitude"]
    altitude = metadata["corrected"]["gps"]["altitude_agl"]
    roll = metadata["corrected"]["attitude"]["roll_angle"]
    pitch = metadata["corrected"]["attitude"]["pitch_angle"]
    yaw = metadata["corrected"]["attitude"]["yaw_angle"]

    try:
        PROJECTOR.get_pixel_coords((0, 0), yaw, pitch, roll, latitude, longitude, altitude)
    except Exception as e:
        print_exception_in_processing(e, path)


def print_exception_in_processing(e: Exception, path: str):
    print(f'encountered exception {e} when processing image {path}')


args = get_args()
input_dir_path = args.input_dir
run(input_dir_path)
