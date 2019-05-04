import argparse
from imagemetadata import MetadataProcessor
import projection
import os
from typing import Callable
from datetime import datetime

IMAGE_FORMATS = ('.bmp', '.jpg', '.png')
PROJECTOR = projection.ImageProjection()
PROCESSOR = MetadataProcessor()


def get_args():
    parser = argparse.ArgumentParser(description='Pre-process folder to ensure \
                                                  valid metadata and correct \
                                                  time')
    parser.add_argument('-i', '--input_dir', help='specify input directory',
                        required=True)
    return parser.parse_args()


def run(input_folder_path: str):
    images_with_bad_metadata = set()

    run_on_each_file(input_dir_path,
                     lambda path: images_with_bad_metadata.add(path)
                     if metadata_does_not_exist_or_invalid(path)
                     else None)

    if responded_yes(f'Encountered {len(images_with_bad_metadata)} images with \
invalid metadata would you like to remove them?'):
        for path in images_with_bad_metadata:
            os.remove(path)

    while True:
        if not responded_yes("Would you like to remove a time interval?"):
            break

        try:
            start = get_time(input("start time: ") + "-000")
            end = get_time(input("end time: ") + "-000")

            if start >= end:
                print("Start time before end time try again!")
                break

            remove_files_inside_of_time_range(input_folder_path, start, end)
        except ValueError as e:
            print(e, "Should be of the form 2019-04-13_13-45-55(i.e. \
            2019 April 13th at 1:45 pm 55 seconds)")

    images_with_bad_projection = set()
    run_on_each_file(input_dir_path,
                     lambda path: images_with_bad_projection.add(path)
                     if exist_unprojectable_point(path)
                     else None)

    if responded_yes(f'Encountered {len(images_with_bad_projection)} images\
with possible bad projections would you like to remove them?'):
        for path in images_with_bad_projection:
            os.remove(path)


def remove_files_inside_of_time_range(input_folder_path: str, start: datetime,
                                       end: datetime):
    out_of_range = set()

    def check_time(path: str):
        text = PROCESSOR.ReadFromImageFilePath(path)
        metadata = PROCESSOR.Process(text)
        timestamp = get_time(metadata["corrected"]["gps"]["timestamp"])
        if start < timestamp < end:
            out_of_range.add(path)
    run_on_each_file(input_folder_path, check_time)

    if responded_yes(f'Encountered {len(out_of_range)} images with \
out of time range given would you like to remove them?'):
        for path in out_of_range:
            os.remove(path)


def metadata_does_not_exist_or_invalid(path: str) -> bool:
    try:
        get_metadata(path)
    except ValueError as e:
        print_exception_in_processing(e, path)
        return True
    return False


def exist_unprojectable_point(path: str) -> bool:
    metadata = get_metadata(path)
    longitude = float(metadata["corrected"]["gps"]["longitude"])
    latitude = float(metadata["corrected"]["gps"]["latitude"])
    altitude = float(metadata["corrected"]["gps"]["altitude_agl"])
    roll = float(metadata["corrected"]["attitude"]["roll_angle"])
    pitch = float(metadata["corrected"]["attitude"]["pitch_angle"])
    yaw = float(metadata["corrected"]["attitude"]["yaw_angle"])

    try:
        for pixel in [(0, 0), (0, 5119), (5119, 0), (5119, 5119)]:
            PROJECTOR.get_pixel_coords(pixel, yaw, pitch, roll,
                                       latitude, longitude, altitude)
    except Exception as e:
        print_exception_in_processing(e, path)
        return True
    return False


def run_on_each_file(input_folder_path, f: Callable[[str], None]):
    walk = os.walk(input_folder_path)
    for root, _, files in walk:
        for file in files:
            path = os.path.join(root, file)
            if not file.lower().endswith(IMAGE_FORMATS):
                continue
            f(path)


def get_metadata(path) -> dict:
    text = PROCESSOR.ReadFromImageFilePath(path)
    return PROCESSOR.Process(text)


def print_exception_in_processing(e: Exception, path: str):
    print(f'encountered exception {e} when processing image {path}')


def get_time(string: str) -> datetime:
    return datetime.strptime(string + '000', "%Y-%m-%d_%H-%M-%S-%f")


def responded_yes(string: str) -> bool:
    return input(string + "(Y/n)").lower() == 'y'


args = get_args()
input_dir_path = args.input_dir
run(input_dir_path)
