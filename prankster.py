import os
import argparse
import subprocess
import tempfile
import shutil
from distutils.dir_util import copy_tree

from helpers import get_asar_file_path

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PAYLOAD_FILE_PATH = os.path.join(CURRENT_DIR, "payload.txt")
DEFAULT_MP3_FILE_PATH = "https://drive.google.com/uc?export=download&id=1K_RlETR6lkcfSHeDwjSZjYTui0DGZsJq"
INJECTION_POINT = '),q.app.once("ready",function(){'


def run_command(cmd):
    return subprocess.run(cmd, shell=True)


def main(args):
    # download required npm package
    run_command("npm install -g asar")
    asar_file_path = get_asar_file_path()
    # extract Slack app source code
    with tempfile.TemporaryDirectory() as temp_dir:
        run_command(f"asar extract {asar_file_path} {temp_dir}")
        # replace mp3 url with
        target_file_path = os.path.join(temp_dir, "dist", 'main.bundle.js')
        with open(PAYLOAD_FILE_PATH, "r") as payload_file:
            payload = payload_file.read().replace("%MP3_URL%", args.mp3_url)

        with open(target_file_path, "r") as target_file:
            target_file_content = target_file.read()
            if 'mapsut' in target_file_content:
                # Payload is already injected
                print("Payload already injected. Exiting...")
                return

            target_content_with_payload = target_file_content.replace(INJECTION_POINT, INJECTION_POINT + payload)

        with open(target_file_path, "w+") as target_file:
            print(f"Injection payload {INJECTION_POINT} into {target_file_path}")
            target_file.write(target_content_with_payload)

        print(target_file_path)

        # unpacked_asar_location = os.path.join(os.path.dirname(asar_file_path), "app.asar.unpacked")
        # shutil.rmtree(unpacked_asar_location)
        # copy_tree(temp_dir, unpacked_asar_location)
        run_command(f"asar pack {temp_dir} {asar_file_path}")

    print("briut!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replace Slack notification sound with any mp3 you want.\nMake sure you currently use the default knock_brush sound.')
    parser.add_argument('mp3_url', help='mp3 file path to overwrite default sound', nargs="?",
                        default=DEFAULT_MP3_FILE_PATH)
    args = parser.parse_args()
    main(args)
