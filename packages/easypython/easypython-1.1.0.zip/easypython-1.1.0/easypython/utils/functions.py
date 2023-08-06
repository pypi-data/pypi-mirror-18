#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division
import os
import re
import hashlib
import urllib
import zipfile

def zipdir(dirname, zipfilename):
    try:
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)

        else :
            for root, dirs, files in os.walk(dirname):
                for name in files:
                    filelist.append(os.path.join(root, name))
             
        zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            #print arcname
            zf.write(tar, arcname)
        zf.close()

        return True
    except:
        pass
    return False

def unzip(zip_path, folder, name=None, pwd=None):
    if not os.path.isfile(zip_path):
        return False

    if not os.path.exists(folder):
        os.makedirs(folder)

    zfobj = zipfile.ZipFile(zip_path)

    if pwd is not None:
        zfobj.setpassword(pwd)

    for zfname in zfobj.namelist():
        zfname = zfname.replace('\\', '/')

        if zfname.endswith('/'):
            os.makedirs(os.path.join(folder, zfname))
            continue

        if name is not None and name != zfname:
            continue

        ext_filename = os.path.join(folder, zfname)
        ext_dir = os.path.dirname(ext_filename)
        if not os.path.exists(ext_dir):
            os.makedirs(ext_dir)

        with open(ext_filename, 'wb') as fs:
            fs.write(zfobj.read(zfname))

    return True