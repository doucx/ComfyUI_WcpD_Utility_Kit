# import torch
# import torch.nn.functional as F
# import cv2
# import numpy as np
# import multiprocessing as mp
# import time
# import random

BASE_CATEGORY = "WcpD_Kit"

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
                "base_text": ("STRING", {"forceInput": True}),
                # "text1": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge"
    CATEGORY = BASE_CATEGORY

    def merge(self, truncation_symbol: str, **kwargs):
        text = f'{truncation_symbol}'.join(text for text in kwargs.values())
        return (text,)

class StrTuple:
    def __init__(self) -> None:
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Str": ("STRING", {
                    "default":"STRING"
                })
            }
        }

    RETURN_TYPES = ("TUPLE",)
    FUNCTION = "get_tuple"
    CATEGORY = BASE_CATEGORY

    def get_tuple(self, Str):
        return (Str,)

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
    CATEGORY = BASE_CATEGORY

    def exec_str(self, code:str, Tuple:tuple):
        print("Warning: Use `exec()` with caution!")
        RETURN = None
        local_vars = locals()
        exec(code, globals(), local_vars)
        return (local_vars['RETURN'],)

NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings,
    "ExecStrAsCode": ExecStrAsCode,
    "StrTuple": StrTuple
}