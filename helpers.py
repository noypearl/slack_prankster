import sys
import os
import glob
from pathlib import Path


def get_asar_file_path():
    if sys.platform == "win32":
        slack_folder = os.path.expandvars(os.path.join("%LOCALAPPDATA%", "slack"))
    elif sys.platform == "darwin":
        slack_folder = os.path.expanduser("~/Applications/Slack.app/Contents/Resources/")
        pass
    else:
        raise NotImplementedError

    [slack_asar_file] = glob.glob(slack_folder + "/*/resources/app.asar")
    return slack_asar_file

