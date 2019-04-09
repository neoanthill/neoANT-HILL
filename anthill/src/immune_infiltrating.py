#!/usr/bin/python

import os
import util
from os import listdir
from os import path
from collections import defaultdict
from os import system
import sys


def execute(opts):

    util.print_task(util.TASK_TUMOR_IMMUNE_PROFILE)

    input_exp = opts[util.OUTPUT_OPTION] + util.GENE_EXPRESSION
    output = opts[util.OUTPUT_OPTION] + util.IMMUNE_INFILTRATING

    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    exp = defaultdict(dict)
    samples = []

    files_input_exp = [f for f in listdir(input_exp) if path.isfile(path.join(input_exp, f))]

    print files_input_exp

    for f in files_input_exp:
        if not f.endswith('.tsv'):
                continue
        sample = f.split(".tsv")[0]
        samples.append(sample)
        with open(input_exp + f, 'r') as fname:
            fname.readline()
            for line in fname:
                genes, transcript, tpm = line.rstrip().split("\t")
                try:
                    exp[genes][sample] += float(tpm)
                except:
                    exp[genes][sample] = 0
                    exp[genes][sample] += float(tpm)

    with open(output + 'tempInput.txt', 'w') as outfile:
        outfile.write("GENE\t" + "\t".join(sorted(samples)) + "\t" + "SAMPLE" + "\n")
        for genes in exp.keys():
            outfile.write(genes)
            for sample in sorted(samples):
                try:
                    outfile.write("\t" + str(exp[genes][sample]))
                except:
                    outfile.write("\t0")
                outfile.write("\t1" + "\n")
        outfile.close()

    prefix = "neoANT-HILL"
    expr = "TRUE"
    pipelinestart = "decon"
    arrays = "FALSE"
    signame = "TIL10"
    tumor = "FALSE"
    mRNAscale = "TRUE"
    method = "lsei"
    btotalcells = "FALSE"
    rmgenes = "unassigned"
    cmd = util.QUANTISEQ + " ".join([output + "tempInput.txt", output, expr, arrays, signame, tumor, mRNAscale, method, prefix, btotalcells, rmgenes])

    try:
        system(cmd)
    except Exception as e:
        raise QuantifyingImmuneInfiltratingException(str(e))

    smp = {}

    with open(output + 'neoANT-HILL_cell_fractions.txt', 'r') as f:
        header = f.readline()
        for line in f:
            smp[line.split("\t")[0]] = line

    for key in smp.keys():
        out = open(output + key + ".tsv", "w")
        out.write(header)
        out.write(smp[key])
        out.close()

    system("rm -r " + output + "tempInput.txt")
    system("rm -f " + output + "SAMPLE.tsv")
    system("rm -f " + output + "neoANT-HILL_cell_fractions.txt")

    util.print_status(util.TASK_SUCCESS)
