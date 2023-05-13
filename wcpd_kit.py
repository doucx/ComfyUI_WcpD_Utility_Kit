# import torch
# import torch.nn.functional as F
# import cv2
# import numpy as np
# import multiprocessing as mp
# import time
# import random


class MergeStrings():
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text0": ("STRING",),
                "text1": ("STRING",),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "merge"
    CATEGORY = "WcpD Kit"

    def merge(self, text0: str, text1: str):
        text = text0 + text1
        return (text,)

NODE_CLASS_MAPPINGS = {
    "MergeStrings": MergeStrings,
}
