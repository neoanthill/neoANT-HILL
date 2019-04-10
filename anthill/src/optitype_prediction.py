#!/usr/bin/python

import os
import util
import time
from os import listdir
from os import path
from mexceptions import QuantifyingExpressionException, ExpressionInputIsEmpty, InputExpressionDataWrongFormat
from collections import defaultdict
from os import system
import sys


def execute(opts):

    util.print_task(util.TASK_ALLELE_TYPING)

    input = opts[util.FASTQ_INPUT_OPTION]
    output = opts[util.OUTPUT_OPTION] + util.ALLELE_DIRECTORY

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    fls = defaultdict(list)

    for f in input:
        sample = f.split("/")[-1].split("_")[0]
        fls[sample].append(f)

    for i in fls.keys():
        cmd = "OptiTypePipeline.py -i " + " ".join(fls[sample]) + " -r -p " + sample + " -o " + output
        try:
            time.sleep(5)
            system(cmd)
            time.sleep(5)
        except Exception as e:
            raise AllelePredictionException(str(e))
    a = set()

    with open(output + sample + "_result.tsv", "r") as r:
        r.readline()
        for line in r:
            line = line.rstrip().split("\t")
            for i in line[1:7]:
                a.add(i.replace("A*", "HLA-A*").replace("B*", "HLA-B*").replace("C*", "HLA-C*"))

    out = open(output + sample + ".tsv", "w")
    out.write(("allele") + "\n")
    out.write("\n".join(a))
    out.close()
    
    system("rm -f " + output + sample + "_result.tsv")
    
    for p, d, files in os.walk(output):
        for y in files:
            if not y.endswith(".tsv"):
                system("rm -f " + os.path.join(p, y))
   
    util.print_status(util.TASK_SUCCESS)
