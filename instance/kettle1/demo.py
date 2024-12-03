# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-1-1
# Description:
# *****************************************************************


import os
import shutil

def clean_file(file_name):
    if os.path.isdir(file_name):
        shutil.rmtree(file_name)
        os.makedirs(file_name)
    else:
        os.makedirs(file_name)


clean_file(r'/Users/linghuchong/Downloads/51/Python/project/instance/kettle1/f2')









