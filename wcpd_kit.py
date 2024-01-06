import torch
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))
import comfy
from nodes import common_ksampler
import yaml
# import torch.nn.functional as F
# import cv2
# import numpy as np
# import multiprocessing as mp
# import time
# import random

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
                    "default":
                        '''# YamlToPrompt
                        ''',
                "multiline": True,
                }),
            },
        }

    RETURN_TYPES = ("TUPLE",)
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
        text = yaml.load(text, yaml.FullLoader)
        text = ", ".join(self.flatten_data(text))
        return text


NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings,
    "ExecStrAsCode": ExecStrAsCode,
    "YamlToPrompt":YamlToPrompt
}
