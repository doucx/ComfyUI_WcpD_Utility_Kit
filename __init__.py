# Modified from Davemane42#0042's Node

import os
# import subprocess
# import importlib.util
# import sys
import filecmp
import shutil

import __main__
from .wcpd_kit import NODE_CLASS_MAPPINGS

JS_DEV_MODE = False #True

print(f'\033[34mWcpD Utility Kit: \033[93mLoading{" with JS_DEV_MODE" if JS_DEV_MODE else ""}\033[0m')
extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                 "web" + os.sep + "extensions" + os.sep + "WcpD_Kit")
javascript_folder = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "js")

if not JS_DEV_MODE and not os.path.exists(extentions_folder):
    print('- Making the "web\extensions\WcpD_Kit" folder')
    os.mkdir(extentions_folder)

result = filecmp.dircmp(javascript_folder, extentions_folder)

if not JS_DEV_MODE and (result.left_only or result.diff_files):
    print('- Update to javascripts files detected')
    file_list = list(result.left_only)
    file_list.extend(x for x in result.diff_files if x not in file_list)

    for file in file_list:
        print(f'- Copying {file} to extensions folder')
        src_file = os.path.join(javascript_folder, file)
        dst_file = os.path.join(extentions_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        # print("disabled")
        shutil.copy(src_file, dst_file)

__all__ = ["NODE_CLASS_MAPPINGS"]

print('\033[34mWcpD Utility Kit: \033[92mLoaded\033[0m')
