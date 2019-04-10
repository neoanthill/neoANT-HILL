#!/usr/bin/python

import util
import mygene
import os
import pandas as pd
from mexceptions import VCFWrongFormat

def extract(vcf_info):

    util.print_task(util.TASK_EXTRACT_VCF_INFO)

    mg = mygene.MyGeneInfo()

    out_file = vcf_info + ".ExtractedInfo.txt"
    out_string = []

    if os.path.isdir(vcf_info):
        files = [f for f in listdir(vcf_info) if path.isfile(path.join(vcf_info, f))]
    else:
        files = []
        files.append(vcf_info)

    for vcf in files:
        if vcf.endswith(".annotated"): 
            with open(vcf, "r") as f:
                samples = {}
                line_count = 1
 
                for line in f:
                    try:
                        if line.startswith("##"):
                            line_count += 1
                            continue

                        linesplit = line.rstrip().split("\t")
                        if line.startswith("#"):
                            for i in range(9, len(linesplit)):
                                samples[i] = linesplit[i]
                        else:
                            try:
                                infos = linesplit[7].split(",")
                                for i in infos:
                                    mut = i.split("ANN=")[-1]
                                    infosplit = mut.split("|")
                                    for key in samples.keys():
                                        if linesplit[key].split(":")[0].find("1") >= 0:
                                            out_string.append("\t".join([samples[key], infosplit[1], infosplit[3], infosplit[6], infosplit[9], infosplit[10], linesplit[2], linesplit[key].split(":")[0]]))
                            except:
                                continue

                    except Exception as e:
                        util.print_status(util.TASK_ERROR)
                        msg = util.REPORT + str(e) + "\n\tline: " + str(line_count) + " | \"" + line.rstrip() + "\"\n"
                        raise VCFWrongFormat(msg)

                    line_count += 1

    sorted_out_string = sorted(out_string)
    df = pd.DataFrame([sub.split("\t") for sub in sorted_out_string], columns=["Sample", "Annotation", "Gene", "Transcript", "HGVS.c", "HGVS.p", "Variant", "Genotype"]).drop_duplicates()
    df = df[df['Transcript'].str.contains('NM')]
    df['Transcript'] = df['Transcript'].str.split('.').str[0]
    df.to_csv(out_file, sep='\t', index=False) 

    util.print_status(util.TASK_SUCCESS)

    return out_file


