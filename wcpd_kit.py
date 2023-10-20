import torch
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
                "base_text": ("STRING", {"forceInput": True}),
                "index": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                # "text": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge"
    CATEGORY = BASE_CATEGORY + "/text"

    def merge(self, truncation_symbol: str, **kwargs):
        kwargs.pop("index")
        text = f'{truncation_symbol}'.join(kwargs.values())
        return (text,)

# class StrTuple:
#     def __init__(self) -> None:
#         pass

#     @classmethod
#     def INPUT_TYPES(s):
#         return {
#             "required": {
#                 "Str": ("STRING", {
#                     "default":"STRING"
#                 })
#             }
#         }

#     RETURN_TYPES = ("TUPLE",)
#     FUNCTION = "get_tuple"
#     CATEGORY = BASE_CATEGORY

#     def get_tuple(self, Str):
#         return (Str,)

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
        return (local_vars['RETURN'],)

class RandnLatentImage:
    def __init__(self, device="cpu"):
        self.device = device

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "width": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                              "height": ("INT", {"default": 512, "min": 16, "max": MAX_RESOLUTION, "step": 8}),
                              "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096})}}
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"

    CATEGORY = BASE_CATEGORY+"/latent"

    def generate(self, width, height, batch_size=1):
        latent = torch.randn([batch_size, 4, height // 8, width // 8])
        return ({"samples":latent}, )

NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings,
    "ExecStrAsCode": ExecStrAsCode,
    "RandnLatentImage":RandnLatentImage,
    # "StrTuple": StrTuple
}
