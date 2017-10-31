import sys, os, random

import torch
from torchvision import utils as vutils

import bokeh
import vispy
from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d
import collections 

class Commander():
    def __init__(self, historian=None, debug=False):
        self.debug = debug
        self.historian = historian
        self.command_help_string = ""
        self.command_help_string += "\n->plotlog <logfile>"
        self.command_help_string += "\n->addlogline <logline pattern>, [provide logline function in execute]"
        self.command_help_string += "\n->findloglines"
        self.command_help_string += "\n->resetlog"
        self.log_patterns = []

    def help(self):
        self.historian.log("help for commander -> list of acceptable commands: {}".format(self.command_help_string))

    def execute(self, command, function=None):
        if self.historian != None:
            self.historian.log("executing command -> "+str(command))
        command_type = command.split(" ")[0]
        pattern = ' '.join(command.split(" ")[1:])
        if command_type == "plotlog":
            self.logfile = pattern
            self.historian.log("logging from file {}".format(self.logfile))
        if command_type == "addlogline":
            self.log_patterns.append((pattern, function))
        if command_type == "findloglines":
            with open(self.logfile) as f:
                lines = f.readlines()
                for line in lines:
                    for pattern in self.log_patterns:
                        if pattern[0] in line:
                            pattern[1](pattern[0],line)

        if command_type == "resetlog":
            self.log_patterns = []
            self.logfile = None

class Misc():

    def __init__(self, historian=None, debug=False):
        self.historian = historian
        self.debug=debug

    def slicer(self, s, pattern):
        if pattern in s:
            return s[s.index(pattern)+len(pattern):]
        else:
            return None

class Oracle():

    # for visualization
    def __init__(self, historian=None, debug=False):
        self.historian = historian
        self.debug = debug
        
    def vis3d():
        pass

    def plotadd(self, **vals):

        '''
        Example usage: plotadd(x=5) or plotadd(y=[0,3,2,4])
        x is a list of x-axis values
        y is a list of entire datalines for y-axis
        '''

        for key, value in vals.items():
            self.datapoints[str(key)].append(value)

    def plotinit(self,command="2dplot"):
        if command == "2dplot":
            self.datapoints = {'x':[], 'y':[]}
            self.command = command
            self.styles={'colors':['navy'], 'alphas':[0.5]}

    def plotstyle(self, **style_parameters):
        for key, value in style_parameters.items():
            self.styles[key] = value

    def plotlog(self,title,xaxis,yaxis):

        if self.command == "2dplot":
            p = figure(plot_width=600, plot_height=600, title=title)
            p.xaxis.axis_label = xaxis
            p.yaxis.axis_label = yaxis

            for i, y_line in enumerate(self.datapoints['y']):
                try:
                    p.line(self.datapoints['x'], y_line, line_color=self.styles['colors'][i], line_alpha=self.styles['alphas'][i], line_width=3)
                    p.circle(self.datapoints['x'], y_line, color=self.styles['colors'][i], fill_color='white', size=4)
                except:
                    try:
                        p.line(self.datapoints['x'], y_line, line_color=self.styles['colors'][0], line_alpha=self.styles['alphas'][0], line_width=3)
                        p.circle(self.datapoints['x'], y_line, color=self.styles['colors'][0], fill_color='white', size=4)
                    except:
                        p.line(self.datapoints['x'], y_line, line_color='navy', line_alpha=0.5, line_width=3)
                        p.circle(self.datapoints['x'], y_line, color='navy', fill_color='white', size=4)

            p.x_range = Range1d(0, len(self.datapoints['x']))
            p.y_range = Range1d(0, 1)
            show(p)


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
        self.logfile = None

    def logger(self, logfile=None):
        if logfile != None:
            self.logfile = logfile
            f = open(self.logfile,"w")
            f.close()
        else:
            logfile = None

    def log(self, o):
        s = "Historian -> {}\n".format(str(o))
        if self.logfile is None:
            print(s,end='')
        else:
            f = open(self.logfile,"a")
            f.write(s)
            f.close()

class Chamber():

    def __init__(self):
        pass

