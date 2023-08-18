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

def create_blender_project(data_paths, blender_install_path, target_folder, blender_script_path, program_path):
    print("In create_blender_project function...")
    
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    target_base = os.path.join(target_folder, const.TARGET_NAME)
    target_path = target_base + const.BASE_FORMAT
    target_path = (
        IO.get_next_target_base_name(target_base, target_path) + const.BASE_FORMAT
    )

    print(f"Executing Blender with target path: {target_path}")
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

    outformat = config.get(
        const.SYSTEM_CONFIG_FILE_NAME, "SYSTEM", const.STR_OUT_FORMAT
    ).replace('"', "")
    if outformat != ".blend":
        check_output(
            [
                blender_install_path,
                "-noaudio",
                "--background",
                "--python",
                "./Blender/blender_export_any.py",
                target_path,
                outformat,
                target_base + outformat,
            ]
        )

def process_floorplan(image_path, blender_install_path="/Applications/Blender.app/Contents/MacOS/Blender", config_path="./Configs/default.ini"):
    print("Entering process_floorplan function...")

    # Check if the image exists at the given path
    if not os.path.exists(image_path):
        print(f"Image does NOT exist at path: {image_path}")
        return  # Exit the function early since the image doesn't exist

    print(f"Processing image at path: {image_path}")
    
    data_folder = const.BASE_PATH
    print(f"data_folder: {data_folder}")
    
    target_folder = const.TARGET_PATH
    print(f"target_folder: {target_folder}")
    
    blender_script_path = const.BLENDER_SCRIPT_PATH
    program_path = os.path.dirname(os.path.realpath(__file__))
    data_paths = list()

    floorplans = [floorplan.new_floorplan(config_path)]
    for f in floorplans:
        f.image_path = image_path

    IO.clean_data_folder(data_folder)

    if len(floorplans) > 1:
        data_paths.append(execution.simple_single(f) for f in floorplans)
    else:
        data_paths = [execution.simple_single(floorplans[0])]

    create_blender_project(data_paths, blender_install_path, target_folder, blender_script_path, program_path)
    
    output_filename = os.path.splitext(os.path.basename(image_path))[0] + ".blend"
    return output_filename
