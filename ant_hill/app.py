#!/usr/bin/python

from flask import Flask, render_template, request
import time
import os
import sys
import socket
import json
import pandas
import multiprocessing
from collections import defaultdict
import src.vcf_extractor as vcf_extractor
import src.variant_calling as variant_calling
import src.generate_protein as generate_protein
import src.iedb_prediction as iedb_prediction
import src.optitype_prediction as optitype_prediction
import src.kallisto_expression as kallisto_expression
import src.immune_infiltrating as immune_infiltrating
import src.options as options
import src.util as util

app = Flask(__name__)
core_number = multiprocessing.cpu_count()


@app.route("/")
def index():

    if request.args.get('status'):
        return render_template('index.html', app_name=util.PIPELINE_NAME, value=core_number, files=list_results(), status=request.args.get('status'))

    return render_template('index.html', app_name=util.PIPELINE_NAME, value=core_number, files=list_results())


@app.route('/input_processing', methods = ['POST'])
def input_processing():
	if request.method == 'POST':
		try:
			opts = options.handle(request.form)

			if opts[util.TYPE_OPTION] == "vcf":
				vcf_info = opts[util.INPUT_OPTION][0]
			elif opts[util.TYPE_OPTION] == "bam":
				vcf_info = variant_calling.execute(opts)

                        vcf_info = variant_calling.annotate(vcf_info) 
			vcf_info = vcf_extractor.extract(vcf_info)
			generate_protein.mutate(vcf_info, opts)

			message = { "status":"success" }
			util.save_log(opts)

		except Exception as e:
			message = { "status":"fail",
				"message":str(e) }
	        
	        finally:
		    return json.dumps(message), 200


@app.route('/additional_processing', methods = ['POST'])
def additional_processing():

    if request.method == 'POST':

		opts = options.handle(request.form)

		try:
		    if util.ADD_PROCESS[util.APREDICTION_PROCESS] in opts[util.ADD_PROCESSING_OPTION]:
		    	optitype_prediction.execute(opts)

		    if util.ADD_PROCESS[util.EQUANTIFICATION_PROCESS] in opts[util.ADD_PROCESSING_OPTION]:
		    	kallisto_expression.execute(opts)

		    if util.ADD_PROCESS[util.LINFILTRATES_PROCESS] in opts[util.ADD_PROCESSING_OPTION]:
		    	immune_infiltrating.execute(opts)

		    message = { "status":"success",
			        "message":util.read_predicted_alleles(opts[util.OUTPUT_OPTION]) }

		    util.save_log(opts)

		except Exception as e:
		    message = { "status":"fail",
	                    "message":str(e) }

		finally:
			return json.dumps(message), 200


@app.route('/binding_prediction', methods = ['POST'])
def binding_prediction():

	if request.method == 'POST':

		try:
			opts = options.handle(request.form)

			iedb_prediction.execute(opts)
			iedb_prediction.filter(opts)

			message = { "status": "success" }
			util.save_log(opts)

		except Exception as e:
		    message = { "status": "fail",
						"message":str(e) }

		finally:
                    return json.dumps(message), 200


@app.route('/sample_result', methods = ['POST', 'GET'])
def sample_result():

    if request.method == 'GET':

		out = request.args.get('out')
		sample = request.args.get('sample')

		params = ""
		try:
		    params = util.read_log(out)
		except:
			None

		c1_lines = pandas.DataFrame()
		try:
		    c1_lines = util.read_c1_binding_results(out, sample)
		except:
		    None

		c2_lines = pandas.DataFrame()
		try:
		    c2_lines = util.read_c2_binding_results(out, sample)
		except:
			None

		result_path = util.OUTPUT_PATH + out + "/allele_prediction/" + sample + ".tsv"
		allele_lines =[]
		try:
			with open(result_path, "r") as f:
				allele_lines = f.readlines()[1:]
		except:
			None

		expquant_lines = pandas.DataFrame()
		try:
			expquant_lines = util.read_gene_exp(out, sample)
		except:
			None

		immune = pandas.DataFrame()
		try:
			immune = util.read_immune_inf(out, sample)
		except:
			None

		return render_template('sample_result.html', sample=sample, params=params, c1_lines=c1_lines, c2_lines=c2_lines, allele_lines=allele_lines, expquant_lines=expquant_lines, immune=immune)


def list_results():

	base = util.OUTPUT_PATH
	samples = defaultdict(set)

	for dir in os.listdir(base):
		try:
			cur_dir = base + "/" + dir + "/c1_predictions/not_filtered/"
			for sample in os.listdir(cur_dir):
				samples[dir].add(sample.split(".txt")[0])
		except:
			None

		try:
			cur_dir = base + "/" + dir + "/c2_predictions/not_filtered/"
			for sample in os.listdir(cur_dir):
				samples[dir].add(sample.split(".txt")[0])
		except:
			None

		try:
			cur_dir = base + "/" + dir + "/allele_prediction/"
			for sample in os.listdir(cur_dir):
				samples[dir].add(sample.split(".tsv")[0])
		except:
			None

		try:
			cur_dir = base + "/" + dir + "/gene_expression/"
			for sample in os.listdir(cur_dir):
				samples[dir].add(sample.split(".tsv")[0])
		except:
			None

	return samples

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
