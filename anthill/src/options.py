#!/usr/bin/python

import os
import sys
import re
import getopt
import util
import datetime
import time
from mexceptions import OptNotHandledException, InputFileNotExistException, TooMuchArgumentsException
from mexceptions import InputMissingException, InvalidPeptideLengthException, PeptideLengthMissingException
from mexceptions import InvalidFilterCutOffException, InvalidCoreNumberException, InvalidFunction
from mexceptions import InvalidMethodException, ClassMissingException, InvalidClassException


def handle(argv):

    util.print_task(util.TASK_ANALYZE_PARAMETERS)

    absolute_path = util.ABSOLUTE_PATH

    functions = argv.getlist("function[]")
    type = argv.get("type")

    if type:
        options = {util.ABSOLUTE_PATH_OPTION: absolute_path}

        options[util.TYPE_OPTION] = argv.get("type")
        
        if options[util.TYPE_OPTION] == "vcf":
            options[util.INPUT_OPTION] = input_validation(argv.get("input"), argv.get("type"))
        else:
            options[util.INPUT_OPTION] = input_validation(argv.getlist("input[]"), argv.get("type"))

        options[util.OUTPUT_OPTION] = output_validation(argv.get("output"))

    elif functions:
        options = additional_processing_handler(absolute_path, argv)
        options[util.ADD_PROCESSING_OPTION] = functions
    else:
        options = binding_prediction_handler(absolute_path, argv)

    util.print_status(util.TASK_SUCCESS)

    return options

def binding_prediction_handler(absolute_path, bpoptions):

    try:
        options = {util.ABSOLUTE_PATH_OPTION: absolute_path}

        options[util.OUTPUT_OPTION] = output_validation(bpoptions.get("output"))
    	options[util.CLASS_OPTION] = int(bpoptions.get("class"))
    	options[util.METHOD_OPTION] = bpoptions.get("method")
    	options[util.PARALLEL_OPTION] = parallel_validation(bpoptions.get("parallel"))
    	options[util.LENGTH_OPTION] = length_validation(options[util.CLASS_OPTION], bpoptions.getlist("length[]"))
    	options[util.ALLELE_OPTION] = allele_validation(bpoptions.getlist("allele[]"))

    except Exception as e:
        raise e

    with open("/home/biodocker/iedb/mhc_i/src/setupinfo.py", "r+") as f:
        lines = f.readlines()
        lines[6] = "\tself.path_main = '/home/biodocker/iedb/mhc_i'\n"
    sout = open("/home/biodocker/iedb/mhc_i/src/setupinfo.py", "w")
    sout.write("".join(lines))
    sout.close()

    return options

def additional_processing_handler(absolute_path, parameters):

    try:
        options = {util.ABSOLUTE_PATH_OPTION: absolute_path}
        options[util.FASTQ_INPUT_OPTION] = apinput_validation(parameters.getlist("fastq[]"))
        options[util.OUTPUT_OPTION] = output_validation(parameters.get("output"))
    except Exception as e:
        raise e

    return options


# HELP


def usage():
    a = 0

# VALIDATION


def function_validation(function):

    if not function:
        raise InvalidFunction

    return function


def apinput_validation(input):
    i = []
    for fastq in input:
    	if os.path.isfile(util.INPUT_PATH + fastq):
    	    i.append(util.INPUT_PATH + fastq)
        if not i:
        	raise InputFileNotExistException(input)

    return i

def input_validation(input, type):
    i = []
    if type == "vcf":
    	if os.path.isfile(util.INPUT_PATH + input):
    	    i.append(util.INPUT_PATH + input)
            
    else:
    	for bam in input:
            if os.path.isfile(util.INPUT_PATH + bam):
                i.append(util.INPUT_PATH + bam)

    return i

def output_validation(output):

    if not output:
        ts = time.time()
        output = util.OUTPUT_PATH + datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
    else:
        output = util.OUTPUT_PATH + output

    return output

def index_validation(index):
    if not index:
	index = util.HUMAN_TRANSCRIPTS_INDEX
    else:
    	input = util.INPUT_PATH + index
    if not os.path.isfile(index):
        raise InputFileNotExistException(index)

    return index

def parallel_validation(parallel):
    if int(parallel) == 1:
	parallel = None
    return parallel

def length_validation(pclass, length):
    if pclass == 1:
	if not length:
	    raise PeptideLengthMissingException
    	peptide_len = list(map(int, length))
    	length = sorted(peptide_len)
    else:
	length = [15]

    return length

def allele_validation(allele):
    if not allele:
        allele = util.read_list(util.DEFAULT_ALLELE_LIST[1])

    return allele

