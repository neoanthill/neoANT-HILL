#!/usr/bin/python

import sys
from collections import defaultdict
from os import listdir, path
import pandas
import json


PIPELINE_NAME =  "neoANT-HILL"

LOG_FILE = "/params.log"

PICARD = "/home/biodocker/picard.jar"
GATK = "/home/biodocker/gatk-4.1.0.0/gatk"
SNPEFF = "/home/biodocker/snpEff/snpEff.jar"
SNPSIFT = "/home/biodocker/snpEff/SnpSift.jar"
QUANTISEQ = "Rscript /home/biodocker/quantiseq/deconvolution/quanTIseq_decon.R "


ABSOLUTE_PATH = "/home/biodocker/neoanthill/"
OUTPUT_PATH = "/home/biodocker/output/"
INPUT_PATH = "/home/biodocker/input/"

#FUNCTIONS
ADD_PROCESS = ["aprediction", "equantification", "linfiltrates"]
APREDICTION_PROCESS = 0
EQUANTIFICATION_PROCESS = 1
LINFILTRATES_PROCESS = 2

# GENERIC OPTIONS
ABSOLUTE_PATH_OPTION = "absolute_path"
ADD_PROCESSING_OPTION = "aprocessing"
INPUT_OPTION = "input"
FASTQ_INPUT_OPTION = "fastq"
OUTPUT_OPTION = "output"

# BP OPTIONS
TYPE_OPTION = "type"
CLASS_OPTION = "class"
METHOD_OPTION = "method"
PARALLEL_OPTION = "parallel"
LENGTH_OPTION = "length"
ALLELE_OPTION = "allele"

# DIRECTORIES
MUTATION_DIRECTORY = "/mutations/"
PREDICTION_FILTERED_DIRECTORY = "predictions/filtered/"
PREDICTION_NOT_FILTERED_DIRECTORY = "predictions/not_filtered/"
PREDICTION_RAW_DIRECTORY = "predictions/raw/"
ALLELE_DIRECTORY = "/allele_prediction/"
VARIANT_CALLING_DIRECTORY = "/variant_calling/"
GENE_EXPRESSION = "/gene_expression/"
IMMUNE_INFILTRATING = "/immune_infiltrating/"

# MUTATIONS
MUTATION_MISSENSE = "missense_variant"
MUTATION_FRAMESHIFT = "frameshift_variant"
MUTATION_INFRAME = ["conservative_inframe_insertion", "disruptive_inframe_insertion", "conservative_inframe_deletion", "disruptive_inframe_deletion"]

# TASKS
TASK_ANALYZE_PARAMETERS = "analysing parameters"
TASK_EXTRACT_VCF_INFO = "extracting vcf info"
TASK_LOAD_PROTEIN_FILE = "loading protein refseqs"
TASK_LOAD_TRANSCRIPT_FILE = "loading transcript refseqs"
TASK_PROCESS_MUTATION = "processing mutations"
TASK_WRITE_REPORT_FILE = "writting report files"
TASK_PREDICT_BINDING = "predicting bindings"
TASK_FILTER_BINDING = "filtering predictions"
TASK_GENE_EXPRESSION = "quantifying transcript expression"
TASK_ANNOTATING_VCF = "annotating vcf"
TASK_VARIANT_CALLING = "calling variants"
TASK_TUMOR_IMMUNE_PROFILE = "profiling tumor-immune cells"
TASK_ALLELE_TYPING = "typing HLA alleles"

# TASK STATUS
TASK_ERROR = "er"
TASK_SUCCESS = "ok"

# DATA
DBSNP = ABSOLUTE_PATH + "data/dbsnp_138.b37.vcf.gz"
MILLS = ABSOLUTE_PATH + "data/Mills_and_1000G_gold_standard.indels.b37.vcf.gz"
KNOWN = ABSOLUTE_PATH + "data/1000G_phase1.indels.b37.vcf.gz"
GENOME_FASTA_FILE = ABSOLUTE_PATH + "data/Homo_sapiens.GRCh37.fa"
REFSEQ_TRANSCRIPTS_FASTA = ABSOLUTE_PATH + "data/transcript_refseq.fasta"
REFSEQ_HUMAN_FASTA = ABSOLUTE_PATH + "data/protein_refseq.fasta"
HUMAN_TRANSCRIPTS_INDEX = ABSOLUTE_PATH +"data/human_transcript_index"
DEFAULT_ALLELE_LIST = [0, ABSOLUTE_PATH + "data/hla_class_i.alleles", ABSOLUTE_PATH + "data/hla_class_ii.alleles"]

# PREDICT METHODS
PREDIC_METHODS = [0,
                ["IEDB_recommended",
                    "ann",
                    "comblib_sidney2008",
                    "consensus",
                    "netmhcstabpan",
                    "netmhcpan",
                    "smm",
                    "smmpmbec",
                    "pickpocket",
                    "netmhccons"],
                ["IEDB_recommended",
                    "comblib",
                    "consensus3",
                    "NetMHCIIpan",
                    "nn_align",
                    "smm_align",
                    "sturniolo"]
                ]

# FILTERS
FILTER_LIST = {"percentile_rank": 7, "ann_ic50": 8, "smm_ic50": 10, "comblib_sidney2008_score": 12, "netmhcpan_ic50": 14, "ic50": 6, }

REPORT = "report: "
GENERAL_USAGE = "general usage: ./main [-opt] [arg] [inputfile]"

AMINO = {'Ala': 'a', 'Arg': 'r', 'Asn': 'n', 'Asp': 'd', 'Cys': 'c', 'Gln': 'q',
         'Glu': 'e', 'Gly': 'g', 'His': 'h', 'Ile': 'i', 'Leu': 'l', 'Lys': 'k',
         'Met': 'm', 'Phe': 'f', 'Pro': 'p', 'Ser': 's', 'Thr': 't', 'Trp': 'w',
         'Tyr': 'y', 'Val': 'v', 'Ter': '*'}

CODON = {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'CTT': 'L',
      'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'ATT': 'I', 'ATC': 'I',
      'ATA': 'I', 'ATG': 'M', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V',
      'GTG': 'V', 'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
      'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'ACT': 'T',
      'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'GCT': 'A', 'GCC': 'A',
      'GCA': 'A', 'GCG': 'A', 'TAT': 'Y', 'TAC': 'Y', 'CAT': 'H',
      'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q', 'AAT': 'N', 'AAC': 'N',
      'AAA': 'K', 'AAG': 'K', 'GAT': 'D', 'GAC': 'D', 'GAA': 'E',
      'GAG': 'E', 'TGT': 'C', 'TGC': 'C', 'TGG': 'W', 'CGT': 'R',
      'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'AGT': 'S', 'AGC': 'S',
      'AGA': 'R', 'AGG': 'R', 'GGT': 'G', 'GGC': 'G', 'GGA': 'G',
      'GGG': 'G', 'TAA': 'STOP', 'TAG': 'STOP', 'TGA': 'STOP'}


DEFAULT_METHOD = "IEDB_recommended"

PREDICTION_CLASS_COMMAND = [0, "/home/biodocker/iedb/mhc_i/src/predict_binding.py ", "/home/biodocker/iedb/mhc_ii/mhc_II_binding.py "]


def print_task(task):
    repetition = 40 - len(task)
    print ("[ -> " + task + " " + ("." * repetition)),
    sys.stdout.flush()


def print_status(status):

    if status == TASK_SUCCESS:
        print (status + " ]")
    else:
        print (status + " ]")


def save_log(ops):
  output = ops[OUTPUT_OPTION]

  if CLASS_OPTION in ops.keys():
    p_class = str(ops[CLASS_OPTION])
    ops[p_class + METHOD_OPTION] = ops[METHOD_OPTION]
    ops[p_class + ALLELE_OPTION] = ops[ALLELE_OPTION]
    ops[p_class + LENGTH_OPTION] = ops[LENGTH_OPTION]
    ops.pop(METHOD_OPTION, None)
    ops.pop(ALLELE_OPTION, None)
    ops.pop(LENGTH_OPTION, None)
  
  if path.isfile(output + LOG_FILE):
    with open(output + LOG_FILE, "r") as f:
      dic = json.load(f)

      dic.update(ops)
      ops = dic
      
  with open(output + LOG_FILE, "w") as f:
    json.dump(ops, f)


def read_log(out):
  
  params = None
  
  with open(OUTPUT_PATH + out + LOG_FILE, "r") as f:
    params = json.load(f)
  
  return params


def read_list(filepath):

    elements = []
    with open(filepath, "r") as f:
        for row in f:
            row = row.strip("\r")
            row = row.strip("\n")
            elements.append(row)
    return elements

def read_predicted_alleles(outpath):

    outpath += ALLELE_DIRECTORY
    files = [f for f in listdir(outpath) if path.isfile(path.join(outpath, f))]

    p_allele = defaultdict(list)
    str_result = ""
    for file in files:
        if file.endswith("_result.tsv"):
            sample = file.split("_result.tsv")[0]
            with open(outpath + file, "r") as f:
                f.readline()
                for line in f:
                  p_allele[line.rstrip()].append(sample)
        else:
            continue

    for allele in sorted(p_allele.keys()):
        str_result += allele + " ("
        for sample in p_allele[allele]:
            str_result += sample + ", "
        str_result = str_result[0:-2] + ")\n"

    return str_result

def read_c1_binding_results(out, sample):

    result_path = OUTPUT_PATH + out + "/c1_predictions/not_filtered/" + sample + ".txt"
    
    try:
        c1_lines = pandas.read_csv(result_path, sep='\t')
    except:
        c1_lines = pandas.DataFrame()

    return c1_lines


def read_c2_binding_results(out, sample):

    result_path = OUTPUT_PATH + out + "/c2_predictions/not_filtered/" + sample + ".txt"
    
    try:
        c2_lines = pandas.read_csv(result_path, sep='\t')
    except:
        c2_lines = pandas.DataFrame()

    return c2_lines

def read_gene_exp(out, sample):

    result_path = OUTPUT_PATH + out + "/gene_expression/" + sample + ".tsv"
    
    try:
        gene_exp = pandas.read_csv(result_path, sep='\t')
    except:
        gene_exp = pandas.DataFrame()

    return gene_exp

def read_immune_inf(out, sample):

    result_path = OUTPUT_PATH + out + "/immune_infiltrating/" + sample + ".tsv"
    
    try:
        immune = pandas.read_csv(result_path, sep='\t')
    except:
        immune = pandas.DataFrame()

    return immune

def read_ct_genes():

  ctfile = ABSOLUTE_PATH + 'data/ct_genes'
  ctgenes = []
  with open(ctfile, 'r') as f:
    f.readline()
    for line in f:
      ctgenes.append(line.rstrip())

  return ctgenes



