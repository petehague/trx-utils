# TRX utilites

Where I keep utilities for manipulating trx.mat files produced by behaviour pipelines

## trx_hash.py

Create a hash of the data content of the file, regardless of some mess that various programs make in there. Use either like

`trx_hash.py trx.mat`

to view data for an individual file or

`trx_hash.py <file containing list of trx.mat files> <output csv file>`

if you have a list of files.
