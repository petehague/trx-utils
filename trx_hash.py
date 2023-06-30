#!/usr/bin/env python3

import h5py
import numpy as np
import sys
import hashlib
import pandas as pd
import os


def process_trx(filename):
    result = {}
    local = h5py.File(filename)
    
    localpath = ''
    for item in local[local['trx']['full_path'][0][0]]:
        localpath += chr(item[0])

    result["Internal Path"] = localpath
    result["Larvae"] = local['trx']['numero_larva_num'].shape[1]
    result["Keys"] = len(local['trx'].keys())-1
    
    keylist = list(local['trx'].keys())
    keylist.sort()
    trx_hash = hashlib.sha256()
    for tag in keylist:
        if tag == 'full_path':
            continue
        local_data = local[local['trx'][tag][0][0]]
        #print(tag, trx_hash.hexdigest())
        for n, local_seq in enumerate(local_data):
            for i in range(len(local_seq)):
                if type(local_seq[i]) == np.float64  or type(local_seq[i]) == np.uint16:
                    if local_seq[i] != local_seq[i]:
                        continue # NaN check
                    cropped_local = np.round(local_seq[i], 10)
                    trx_hash.update(str(cropped_local).encode('utf-8'))
                else:
                    newlocal_seq = np.array(local[local_seq[i]]).flatten()
                    for j in range(len(newlocal_seq)):
                        trx_hash.update(str(newlocal_seq[j]).encode('utf-8'))

    result["Hash"] = trx_hash.hexdigest()
    return result


if __name__ == "__main__":
    filename = 'trx.mat' if len(sys.argv) < 2 else sys.argv[1]
    if filename[-4:] == ".mat":
        print(process_trx(filename))
    else:
        if len(sys.argv) < 3:
            print("Usage: trx_hash.py <list of trx.mat files> <output csv file>")
        else:
            df = pd.DataFrame(columns=["Filename", "Larvae", "Keys", "Hash","Internal Path"])
            with open(filename, 'r') as f:
                for line in f:
                    cleanline = line.strip()
                    if not os.path.exists(cleanline):
                        print("File not found:", cleanline)
                        row = {"Filename": cleanline, "Larvae": 0, "Keys": 0, "Hash": "", "Internal Path": ""}
                    else:
                        print(cleanline)
                        row = process_trx(cleanline)
                        row["Filename"] = cleanline
                    df.loc[len(df)] = row
            df.to_csv(sys.argv[2], index=False)