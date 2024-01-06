import torch
import numpy as np
import os
import io
import sys
import yaml
import subprocess
import json
import random
import pyperclip
from PIL.PngImagePlugin import PngInfo
from PIL import Image, ImageOps, ImageSequence
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

import folder_paths
import comfy
from nodes import common_ksampler, SaveImage

BASE_CATEGORY = "WcpD_Kit"
MAX_RESOLUTION=8192

class MergeStrings:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "truncation_symbol": ("STRING", {
                    "default":", ",
                    "multiline": False,
                    }),
                # "base_text": ("STRING", {"forceInput": True}),
                "index": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                # "text": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge"
    CATEGORY = BASE_CATEGORY + "/text"

    def merge(self, truncation_symbol: str, **kwargs):
        kwargs.pop("index")
        kwargs.pop("truncation_symbol")
        text = f'{truncation_symbol}'.join(kwargs.values())
        return (text,)

class ExecStrAsCode:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "code": ("STRING", {
                    "default":
'''# RETURN is what you want to return
# import torch
RETURN = Tuple
''',
                "multiline": True,
                }),
                "Tuple":("TUPLE", {
                })
                ,
            },
        }

    RETURN_TYPES = ("TUPLE",)
    FUNCTION = "exec_str"
    CATEGORY = BASE_CATEGORY + "/debug"

    def exec_str(self, code:str, Tuple:tuple):
        print("Warning: Use `exec()` with caution!")
        RETURN = None
        local_vars = locals()
        exec(code, globals(), local_vars)
        r = local_vars['RETURN']
        if isinstance(r, tuple):
            return r
        else:
            raise TypeError("Output must be tuple")

class YamlToPrompt:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {
                "multiline": True,
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "to_prompt"
    CATEGORY = BASE_CATEGORY + "/text"

    def flatten_data(self, data):
        result = []
        if isinstance(data, list):
            for item in data:
                result.extend(self.flatten_data(item))
        elif isinstance(data, dict):
            for key, value in data.items():
                result.extend(self.flatten_data(value))
        elif isinstance(data, str):
            result.append(data)
        return result

    def to_prompt(self, text:str):
        text_yaml = yaml.load(text, yaml.FullLoader)
        if text_yaml == None:
            return []
        text_list = self.flatten_data(text_yaml)
        text_formatted = ", ".join(text_list)
        return (text_formatted,)

class CopyImageWayland():
    def __init__(self):
        pass
    RETURN_TYPES = ()
    CATEGORY = BASE_CATEGORY + "/image"
    FUNCTION = "copy_img"
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(s):
        XDG_RUNTIME_DIR=os.environ.get('XDG_RUNTIME_DIR')
        return {"required":
                    {"images": ("IMAGE", ), 
                    "num": ("INT", {"default": 1, "min": 1, "max": 4096}),
                    "XDG_RUNTIME_DIR": ("STRING", {"multiline": False, "default": XDG_RUNTIME_DIR if XDG_RUNTIME_DIR is not None else "/run/user/1000"}),
                    },
                }

    def is_wl_copy_available(self):
        try:
            # 尝试运行 wl-copy 命令
            subprocess.run(['wl-copy', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            # 如果命令执行失败，则说明 wl-copy 不可用
            return False

    def copy_img(self, images, num, XDG_RUNTIME_DIR):

        if not self.is_wl_copy_available():
            print("error: wl-copy is unavailable")
            return {}
        elif os.environ.get('XDG_RUNTIME_DIR')==None:
            print("warn: cannot get XDG_RUNTIME_DIR, try user input.")

        if len(images) < num: 
            num=len(images)
        img = images[num-1]
        i = 255. * img.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        with io.BytesIO() as bio:
            # 将 PIL 图像保存到临时文件
            img.save(bio, format='PNG')
            # 使用 pyclip 复制文件内容到剪贴板
            subprocess.run('wl-copy', input=bio.getvalue(), shell=True, env={"XDG_RUNTIME_DIR":XDG_RUNTIME_DIR})
        return {}

class BlackImage():
    def __init__(self):
        pass

    RETURN_TYPES = ("IMAGE",)
    CATEGORY = BASE_CATEGORY + "/image"
    FUNCTION = "empty_img"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "width": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                              "height": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096})}}

    def empty_img(self, width, height, batch_size):
        images = [np.zeros([width,height]) for i in range(batch_size)]
        return images

NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings,
    "ExecStrAsCode": ExecStrAsCode,
    "YamlToPrompt":YamlToPrompt,
    "CopyImage(Wayland)":CopyImageWayland,
    "BlackImage":BlackImage
}
