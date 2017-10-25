
from __future__ import unicode_literals

from numpy import arange, sin, pi
import a
import sys
import os
import random
import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import torch
from torchvision import utils as vutils

class Oracle():
    # for visualization
    def __init__(self):
        pass

    def visualize_tensors(self, tensor_list, file="./sandbox_results/temp"):

        # Visualize tensor list (concatenating vertically) and save them in a file
        # accepts a list of tensors of the form batch x channels x (size1 x size2)

        # max channel dimension
        cmax = -1
        proper_size = None

        t_vis = []
        for tensor in tensor_list:
            t_size = tensor.size()[1]
            if cmax < t_size:
                cmax = t_size
            proper_size = tensor.size()

        # expand channels for all tensors with less channels
        for tensor in tensor_list:
            if tensor.size()[1] < cmax:
                t_vis.append(tensor.expand((proper_size[0], cmax, proper_size[2], proper_size[3])))
            else:
                t_vis.append(tensor)

        vis = torch.cat(t_vis, 0)

        if "png" not in file:
            file += ".png"

        # visualize all tensors (greyscale and colored together)
        vutils.save_image(vis,file, nrow=proper_size[0], pad_value=1.0, normalize=False)

class Historian():
    # for logging
    def __init__(self):
        pass

class Chamber():

    def __init__(self):
        pass

