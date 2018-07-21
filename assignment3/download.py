#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloader for unsup tutorial

@author: zeyi
"""
import os
import requests
import gzip

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

DATA_DIR = 'data'

def download_file(url, destination):
    """Wrapper for downloading file with progress bar"""
    r = requests.get(url, stream=True)
    
    # Get file size
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0
    if tqdm is None:
        dl_iter = r.iter_content(block_size)
    else:
        dl_iter = tqdm(r.iter_content(block_size), 
                         total=block_size//block_size,
                         unit='KB',
                         unit_divisor=1024,
                         unit_scale=True)
    with open(destination, 'wb') as f:
        for data in dl_iter:
            wrote += len(data)
            f.write(data)
    if total_size > 0 and wrote != total_size:
        raise(ValueError)
    return
    
def retrieve_BlueCoat(path=DATA_DIR):
    """Downloads BlueCoat Proxy Data, and prepares data for analysis"""
        
    full_path = os.path.join(path, 'bluecoat')
    if not os.path.exists(full_path):
        os.makedirs(full_path, exist_ok=True)
    
    #Check if data already exists
    zip_file = os.path.join(full_path, 'bluecoat_proxy_big.zip')
    if not os.path.isfile(zip_file):
        print('Downloading bluecoat data')
        url = 'http://log-sharing.dreamhosters.com/bluecoat_proxy_big.zip'
        download_file(url, zip_file)
    else:
        print("File already exists: %s" % zip_file)
        return
    
    #Unpack zip file
    #unzip(zip_file)
    return

def retrieve_SotM30(path=DATA_DIR):
    """SoTM30 download"""
    full_path = os.path.join(path, 'SotM30')
    if not os.path.exists(full_path):
        os.makedirs(full_path, exist_ok=True)
    
    #Check if data already exists
    zip_file = os.path.join(full_path, 'SotM30-anton.log.gz')
    if not os.path.isfile(zip_file):
        print('Downloading SoTM30 data')
        url = 'http://log-sharing.dreamhosters.com/SotM30-anton.log.gz'
        download_file(url, zip_file)
    else:
        print("File already exists: %s" % zip_file)
        return
    
    #Unpack file
    unzip_gzip(zip_file, os.path.join(full_path, 'honeynet-Feb1_FebXX.log'))
    return

def unzip_gzip(filename, dst_file=None):
    assert(filename.endswith('.gz'))
    if dst_file is None and len(filename) > 3:
        dst_file = filename[:-3]

    with gzip.open(filename, 'rb') as f_gz:
        with open(dst_file, 'wb') as f:
            f.write(f_gz.read())

def retrieve_IDS(path=DATA_DIR):
    raise(NotImplementedError)
    
if __name__ == "__main__":
    #etrieve_BlueCoat()
    retrieve_SotM30()

