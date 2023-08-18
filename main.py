from subprocess import check_output
from FloorplanToBlenderLib import (
    IO,
    config,
    const,
    execution,
    dialog,
    floorplan,
    stacking,
)
import os

def create_blender_project(data_paths):
    if not os.path.exists("." + target_folder):
        os.makedirs("." + target_folder)

    target_base = target_folder + const.TARGET_NAME
    target_path = target_base + const.BASE_FORMAT
    target_path = (
        IO.get_next_target_base_name(target_base, target_path) + const.BASE_FORMAT
    )

    print("Executing Blender command for project creation...")
    check_output(
        [
            blender_install_path,
            "-noaudio",
            "--background",
            "--python",
            blender_script_path,
            program_path,
            target_path,
        ]
        + data_paths
    )
    print("Blender command for project creation executed successfully!")

    outformat = config.get(
        const.SYSTEM_CONFIG_FILE_NAME, "SYSTEM", const.STR_OUT_FORMAT
    ).replace('"', "")
    if outformat != ".blend":
        print("Executing Blender command for format conversion...")
        check_output(
            [
                blender_install_path,
                "-noaudio",
                "--background",
                "--python",
                "./Blender/blender_export_any.py",
                "." + target_path,
                outformat,
                target_base + outformat,
            ]
        )
        print("Blender command for format conversion executed successfully!")

def process_floorplan(image_path, blender_install_path, config_path="./Configs/default.ini"):
    data_folder = const.BASE_PATH
    target_folder = const.TARGET_PATH
    blender_script_path = const.BLENDER_SCRIPT_PATH
    program_path = os.path.dirname(os.path.realpath(__file__))
    data_paths = list()

    print(f"Blender Installation Path: {blender_install_path}")

    floorplans = [floorplan.new_floorplan(config_path)]
    for f in floorplans:
        f.image_path = image_path

    IO.clean_data_folder(data_folder)

    if len(floorplans) > 1:
        data_paths.append(execution.simple_single(f) for f in floorplans)
    else:
        data_paths = [execution.simple_single(floorplans[0])]

    create_blender_project(data_paths)
    
    output_filename = os.path.splitext(os.path.basename(image_path))[0] + ".blend"
    return output_filename
