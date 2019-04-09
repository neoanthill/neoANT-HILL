#!/usr/bin/python

import os
import util
from os import listdir
from os import path
from mexceptions import QuantifyingExpressionException, ExpressionInputIsEmpty, InputExpressionDataWrongFormat
from collections import defaultdict
from os import system
import mygene
import pandas as pd
import sys


def execute(opts):

    input = opts[util.FASTQ_INPUT_OPTION]
    output = opts[util.OUTPUT_OPTION] + util.GENE_EXPRESSION
    index = util.HUMAN_TRANSCRIPTS_INDEX

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    util.print_task(util.TASK_GENE_EXPRESSION)

    ids = defaultdict(list)

    for f in input:
        sample = f.split("/")[-1].split("_")[0]
        ids[sample].append(f)

    for sample in ids.keys():
        if ids[sample][0].find("read") >= 0:
            end = " --single -l " + str(200) + " -s " + str(20) + " "
        else:
            end = " "

        files = " ".join(ids[sample])
        cmd = "kallisto quant -i " + index + " -o " + output + end + files

        try:
            system(cmd)
        except Exception as e:
            raise QuantifyingExpressionException(str(e))

        mg = mygene.MyGeneInfo()

        symbols = pd.read_csv(output + "abundance.tsv", sep='\t', header=0, usecols=['target_id', 'tpm'])       
        symbols['target_id'] = symbols['target_id'].str.split('.').str[0]
        
        sy = mg.querymany(symbols['target_id'], scopes='all', fields='symbol', species='human', verbose=False, as_dataframe=True)
        df = pd.merge(symbols, sy, left_on="target_id", right_on="query").drop(columns=['_id', '_score', 'notfound']).drop_duplicates()
        df2 = df.groupby(['symbol', 'target_id'])['tpm'].sum().reset_index(name='tpm').drop_duplicates()
        df2.columns = ['symbol', 'transcript', 'tpm']
        
        df2['tpm'] = pd.to_numeric(df2['tpm'])
        df2[df2['tpm'] > 1].to_csv(output + sample + ".tsv", sep = '\t', index=False) 

        os.remove(output + "abundance.tsv")
        os.remove(output + "abundance.h5")
        os.remove(output + "run_info.json")
                
        util.print_status(util.TASK_SUCCESS)

