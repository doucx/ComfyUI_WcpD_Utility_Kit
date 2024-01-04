import torch
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))
import comfy
from nodes import common_ksampler
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
        r = local_vars['RETURN']
        if isinstance(r, tuple):
            return r
        else:
            raise TypeError("Output must be tuple")

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

# class KSamplerAdvancedWithDenoise:
#     @classmethod
#     def INPUT_TYPES(s):
#         return {"required":
#                     {"model": ("MODEL",),
#                     "add_noise": (["enable", "disable"], ),
#                     "noise_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
#                     "steps": ("INT", {"default": 20, "min": 1, "max": 10000}),
#                     "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.5, "round": 0.01}),
#                     "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
#                     "scheduler": (comfy.samplers.KSampler.SCHEDULERS, ),
#                     "positive": ("CONDITIONING", ),
#                     "negative": ("CONDITIONING", ),
#                     "latent_image": ("LATENT", ),
#                     "start_at_step": ("INT", {"default": 0, "min": 0, "max": 10000}),
#                     "end_at_step": ("INT", {"default": 10000, "min": 0, "max": 10000}),
#                     "return_with_leftover_noise": (["disable", "enable"], ),
#                     "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
#                      }
#                 }

#     RETURN_TYPES = ("LATENT",)
#     FUNCTION = "sample"

#     CATEGORY = BASE_CATEGORY + "sampler"

#     def sample(self, model, add_noise, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, start_at_step, end_at_step, return_with_leftover_noise, denoise):
#         force_full_denoise = True
#         if return_with_leftover_noise == "enable":
#             force_full_denoise = False
#         disable_noise = False
#         if add_noise == "disable":
#             disable_noise = True
#         return common_ksampler(model, noise_seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise, disable_noise=disable_noise, start_step=start_at_step, last_step=end_at_step, force_full_denoise=force_full_denoise)

NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings,
    "ExecStrAsCode": ExecStrAsCode,
    "RandnLatentImage": RandnLatentImage,
    # "KSamplerAdvancedWithDenoise": KSamplerAdvancedWithDenoise,
    # "StrTuple": StrTuple
}
