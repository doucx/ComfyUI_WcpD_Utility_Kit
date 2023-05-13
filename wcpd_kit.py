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

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings
}