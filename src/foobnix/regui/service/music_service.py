#-*- coding: utf-8 -*-
'''
Created on 25 сент. 2010

@author: ivan
'''
import os
from foobnix.util.fc import FC
from foobnix.util.file_utils import file_extenstion
from foobnix.util import LOG
from foobnix.regui.model import FModel
from foobnix.regui.id3 import update_id3_wind_filtering
    
def get_all_music_by_path(path):
    return _scanner(path, None) 

def get_all_music_with_id3_by_path(path):
    all = _scanner(path, None)
    return update_id3_wind_filtering(all)

def _scanner(path, level):
    results = []
    if not os.path.exists(path):
        return None
    dir = os.path.abspath(path)
    list = os.listdir(dir)
    list = sort_by_name(path, list)

    for file in list:
        full_path = os.path.join(path, file)
        
        if os.path.isfile(full_path) and file_extenstion(file) not in FC().support_formats:
            continue;
        
        if is_dir_with_music(full_path):
            b_bean = FModel(file, full_path).add_parent(level).add_is_file(False)
            results.append(b_bean)
            results.extend(_scanner(full_path, b_bean.get_level()))
        elif os.path.isfile(full_path):
            results.append(FModel(file, full_path).add_parent(level).add_is_file(True))
    return results

def sort_by_name(path, list):
    files = []
    directories = []
    for file in list:
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            directories.append(file)
        else:
            files.append(file)

    return sorted(directories) + sorted(files)

def is_dir_with_music(path):
    if os.path.isdir(path):
        list = None
        try:
            list = os.listdir(path)
        except OSError, e:
            LOG.info("Can'r get list of dir", e)

        if not list:
            return False

        for file in list:
            full_path = os.path.join(path, file)
            if os.path.isdir(full_path):
                if is_dir_with_music(full_path):
                    return True
            else:
                if file_extenstion(file) in FC().support_formats:
                    return True
    return False