from mexceptions import NoMutatedFileWasFoundException, NoBindingPredictionFileWasFoundException, BindingPredictionException
from os import listdir, path, makedirs, system, remove
from collections import defaultdict
import util
import sys


def execute(opts):

    util.print_task(util.TASK_PREDICT_BINDING)

    abs_path = opts[util.ABSOLUTE_PATH_OPTION]
    pep_len = opts[util.LENGTH_OPTION]
    method = opts[util.METHOD_OPTION]
    hlas = opts[util.ALLELE_OPTION]
    parallel = opts[util.PARALLEL_OPTION]
    p_class = opts[util.CLASS_OPTION]
    input_path = opts[util.OUTPUT_OPTION]

    mutations_path = input_path + util.MUTATION_DIRECTORY
    raw_predictions_path = input_path + "/c" + str(p_class) + "_" + util.PREDICTION_RAW_DIRECTORY

    directory = path.dirname(raw_predictions_path)
    if not path.exists(directory):
        makedirs(directory)

    files = [f for f in listdir(mutations_path) if path.isfile(path.join(mutations_path, f))]

    if not files:
        raise NoMutatedFileWasFoundException

    cmds = []

    for f in files:

        if f.startswith("."):
            continue

	
	if method == "mhcflurry":
	    with open(mutations_path + f, "r") as st:
	        line_fasta = []
                for line in st:
                    if line.startswith(">"):
		        text = line.replace(".", "_")
		    else:
		        text = line
		    line_fasta.append(text)
	        pfasta_file = mutations_path + f
                pfasta_out = open(pfasta_file, "w")
                pfasta_out.write("".join(line_fasta))
                pfasta_out.close()


        output_file = raw_predictions_path + f

        for i in pep_len:
            pl = [str(i)] * len(hlas)
            if p_class == 1:
		if method == "mhcflurry":
			cmds.append("mhctools --mhc-predictor mhcflurry --input-fasta-file " +  mutations_path + f + " --extract-subsequences --mhc-alleles "  + ",".join(hlas) + " --mhc-peptide-lengths " +  ",".join(pl) + " --output-csv " + output_file)
		else:
                	cmds.append("python " + util.PREDICTION_CLASS_COMMAND[p_class] + method.split("iedb_")[1] + " \"" + ",".join(hlas) + \
                        	    "\" " + ",".join(pl) + " " + mutations_path + f + " >> " + output_file)
            else:
                cmds.append("python " + util.PREDICTION_CLASS_COMMAND[p_class] + method.split("iedb_")[1] + " " + ",".join(hlas) + \
                            " " + mutations_path + f + " >> " + output_file)

    if parallel:
        p_file = "temp_par_cmd.txt"
        p_out = open(p_file, "w")
        p_out.write("\n".join(cmds))
        p_out.close()

        cmd = "parallel --no-notice -j " + str(parallel) + " <" + p_file

        try:
            system(cmd)
        except Exception as e:
            raise BindingPredictionException(str(e))
        remove(p_file)

    else:
        for cmd in cmds:
            try:
                system(cmd)
            except Exception as e:
                raise BindingPredictionException(str(e))
    util.print_status(util.TASK_SUCCESS)


def filter(opts):

    util.print_task(util.TASK_FILTER_BINDING)

    method = opts[util.METHOD_OPTION]
    input_path = opts[util.OUTPUT_OPTION]
    p_class = opts[util.CLASS_OPTION]

    mutations_path = input_path + util.MUTATION_DIRECTORY
    nf_predictions_path = input_path + "/c" + str(p_class) + "_" + util.PREDICTION_NOT_FILTERED_DIRECTORY
    raw_predictions_path = input_path + "/c" + str(p_class) + "_" + util.PREDICTION_RAW_DIRECTORY

    directory = path.dirname(nf_predictions_path)
    if not path.exists(directory):
        makedirs(directory)

    id_to_gene = defaultdict(dict)
    files = [f for f in listdir(raw_predictions_path) if path.isfile(path.join(raw_predictions_path, f))]

    if not files:
        raise NoBindingPredictionFileWasFoundException

    filtered_results = False
	
    for f in files:
        header_to_id = {}
        filtered_results = set()
        not_filtered_results = set()

        if f.startswith("."):
            continue

        with open(raw_predictions_path + f, "r") as st:
            prediction_header = st.readline()
            for line in st:
	 	if method == "mhcflurry":
		    if line.startswith("source_sequence_name"):
		        continue
                    lsplit = line.rstrip().split(",")
		    lsplit2 = lsplit[0].rstrip().split("|")
		    p_key = lsplit2[-1]
		else:
		    if line.startswith("allele"):
                        continue
		    lsplit = line.rstrip().split("\t")
		    p_key = lsplit[1]

                if len(lsplit) < 5:
                    continue

		if method == "mhcflurry":
		    s_key = "|".join([lsplit[3], lsplit[1], lsplit[-1]])
                elif p_class == 1:
                    s_key = "|".join([lsplit[0], lsplit[2], lsplit[4]])
                else:
                    s_key = "|".join([lsplit[0], lsplit[2]])
              
                id_to_gene[p_key][s_key] = line.rstrip()

        with open(mutations_path + f, "r") as st:
            for line in st:
                if line.startswith(">"):
                    k = "|".join(line.rstrip().split("|")[0:-1])
                    try:
                        header_to_id[k].append(int(line.rstrip().split("|")[-1]))
                    except:
                        header_to_id[k] = []
                        header_to_id[k].append(int(line.rstrip().split("|")[-1]))

        for key in header_to_id.keys():
            sample, nm, np, annotation, gene, hgvs_c, hgvs_p, variant, genotype = key.split("|")

            if len(header_to_id[key]) % 2 == 0:
                for i in range(0, len(header_to_id[key]), 2):

                    hti = header_to_id[key][i:i+2]
                    ref_id = min(hti)
                    alt_id = max(hti)

                    ref = id_to_gene[str(ref_id)]
                    alt = id_to_gene[str(alt_id)]

                    for prediction in alt.keys():
                        if prediction not in ref.keys() or prediction not in alt.keys():
                            continue
			
		 	if method == "mhcflurry":
			    ref_prediction = ref[prediction].split(",")
                            alt_prediction = alt[prediction].split(",")
			    ic50 = 4
			else:
                            ref_prediction = ref[prediction].split("\t")
                            alt_prediction = alt[prediction].split("\t")
			    ic50 = 6

                        if float(ref_prediction[ic50]) < 500:
                                continue

                        if p_class == 1:
                            if ref_prediction[5] == alt_prediction[5]:
                                continue
                        else:
                            if ref_prediction[4] == alt_prediction[4]:
                                continue

                        if float(alt_prediction[ic50]) < 50:
                            rank = "STRONG BINDER"
                        elif float(alt_prediction[ic50]) >= 50 and float(alt_prediction[ic50]) < 250:
                            rank = "INTERMEDIATE BINDER"
                        elif float(alt_prediction[ic50]) >= 250 and float(alt_prediction[ic50]) < 500:
                            rank = "WEAK BINDER"
                        else:
                            rank = "NON BINDER"
                      
                        dai = float(ref_prediction[ic50]) - float(alt_prediction[ic50])

			if method == "mhcflurry":
			    merged_report = "\t".join([sample[1:], gene, variant, genotype, hgvs_c, hgvs_p, nm, np, annotation, alt_prediction[3], alt_prediction[-1], ref_prediction[2]])
			    merged_report += "\t" + "\t".join([ref_prediction[ic50], alt_prediction[2], alt_prediction[ic50], str(dai), rank])
                        elif p_class == 1:
                            merged_report = "\t".join([sample[1:], gene, variant, genotype, hgvs_c, hgvs_p, nm, np, annotation, alt_prediction[0], alt_prediction[4], ref_prediction[5]])
                            merged_report += "\t" + "\t".join([ref_prediction[ic50], alt_prediction[5], alt_prediction[ic50], str(dai), rank])
                        else:
                            merged_report = "\t".join([sample[1:], gene, variant, genotype, hgvs_c, hgvs_p, nm, np, annotation, alt_prediction[0], ref_prediction[4]])
                            merged_report += "\t" + "\t".join([ref_prediction[ic50], alt_prediction[4], alt_prediction[ic50], str(dai), rank])
                        
                        not_filtered_results.add(merged_report)

            else:
                alt_id = max(header_to_id[key])
                alt = id_to_gene[str(alt_id)]

                for prediction in alt.keys():

                    alt_prediction = alt[prediction].split("\t")
		    if method == "mhcflurry":
		        merged_report = "\t".join([sample[1:], gene, variant, genotype, hgvs_c, hgvs_p, nm, np, annotation, alt_prediction[3], alt_prediction[-1], "NA"])
		    else:
                    	merged_report = "\t".join([sample[1:], gene, variant, genotype, hgvs_c, hgvs_p, nm, np, annotation, alt_prediction[0], alt_prediction[4], "NA"])

                    ic50 = 6
                        
                    if float(alt_prediction[ic50]) < 50:
                        rank = "STRONG BINDER"
                    elif float(alt_prediction[ic50]) >= 50 and float(alt_prediction[ic50]) < 250:   
                        rank = "INTERMEDIATE BINDER"
                    elif float(alt_prediction[ic50]) >= 250 and float(alt_prediction[ic50]) < 500:
                        rank = "WEAK BINDER"
                    else:
                        rank = "NON BINDER"
                  
                    dai = "NA"
                    merged_report += "\t" + "\t".join(["NA", alt_prediction[5], alt_prediction[ic50], str(dai), rank])

                    not_filtered_results.add(merged_report)

        if p_class == 1:
            nf_header = "\t".join(["sample", "gene", "variant", "genotype", "hgvs_c", "hgvs_p", "nm", "np", "annotation", "allele", "len", "ref_peptide", "ref_ic50", "alt_peptide", "alt_ic50", "dai", "classification"])
        else:
            nf_header = "\t".join(["sample", "gene", "variant", "genotype", "hgvs_c", "hgvs_p", "nm", "np", "annotation", "allele", "ref_peptide", "ref_ic50", "alt_peptide", "alt_ic50", "dai", "classification"])

        if not_filtered_results:
            out = open(nf_predictions_path + f, "w")
            out.write(nf_header + "\n")
            out.write("\n".join(not_filtered_results))
            out.close()
	    filtered_results = True

    system("rm -rf " + raw_predictions_path)

    if filtered_results:
    	util.print_status(util.TASK_SUCCESS)
	return True
    else:
	return False


