import generate_report
import os
import util
import pandas
from mexceptions import ProteinFileNotExistException, TranscriptFileNotExistException, FileHasBeenModified
from collections import defaultdict
from mutation import Mutation


def mutate(vcf_info, opts):

    abs_path = opts[util.ABSOLUTE_PATH_OPTION]
    output = opts[util.OUTPUT_OPTION]

    log_not_found = []
    ################################# RefSeq_human_full.fasta ###################################

    util.print_task(util.TASK_LOAD_PROTEIN_FILE)

    refseq_human = read_protein_file(abs_path)

    util.print_status(util.TASK_SUCCESS)

    #############################################################################################

    ############################# Transcripts_refseq.fasta reading ##############################

    util.print_task(util.TASK_LOAD_TRANSCRIPT_FILE)

    refseq_transc, nm_np_conversor = read_transcript_file(abs_path)

    util.print_status(util.TASK_SUCCESS)

    #############################################################################################

    ################################# vcf info file processing ##################################

    mutations = defaultdict(list)
    samples = set()
    curr_sample = 1

    util.print_task(util.TASK_PROCESS_MUTATION)

    with open(vcf_info, "r") as f:

        f.readline()

        for line in f:

            try:
                mutation = Mutation(line, nm_np_conversor, refseq_transc, refseq_human)
            except KeyError:
                log_not_found.append(line.rstrip())
                continue
            
            samples.add(mutation.sample)

            if mutation.mut_protein_sequence:
                if len(samples) == curr_sample:
                    mutations[mutation.transcript].append(mutation)
                else:
                    generate_report.mutation(mutations[mutations.keys()[0]][0].sample, mutations, output)
                    mutations = defaultdict(list)
                    mutations[mutation.transcript].append(mutation)
                    curr_sample += 1
                
    generate_report.mutation(mutations[mutations.keys()[0]][0].sample, mutations, output)

    util.print_status(util.TASK_SUCCESS)

    #############################################################################################


def read_transcript_file(abs_path):
    transc = {}
    conversor = {}
    t_file = util.REFSEQ_TRANSCRIPTS_FASTA

    if not os.path.isfile(t_file):
        raise TranscriptFileNotExistException()

    with open(t_file, "r") as f:
        try:
            for line in f:
                if line.startswith(">"):
                    nm, np, orf = line.rstrip().split("|")
                    nm = nm.split(".")[0][1:]
                    np = np.split(".")[0]
                    conversor[nm] = np
                    transc[nm] = orf
                else:
                    transc[nm] += "\t" + line.rstrip()
        except Exception as e:
            raise FileHasBeenModified(util.REPORT + str(e))

    if transc and conversor:
        return transc, conversor


def read_protein_file(abs_path):
    protein = {}
    p_file = util.REFSEQ_HUMAN_FASTA
    if not os.path.isfile(p_file):
        raise ProteinFileNotExistException()

    with open(p_file, "r") as f:
        try:
            for line in f:
                if line.startswith(">"):
                    np = line.rstrip().split("|")[3].split(".")[0]
                    protein[np] = ""
                else:
                    protein[np] += line.rstrip()
        except Exception as e:
            raise FileHasBeenModified(util.REPORT + str(e))

    if protein:
        return protein

