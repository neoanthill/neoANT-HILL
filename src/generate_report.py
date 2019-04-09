import re
import os
import itertools
import util
import sys


def mutation(sample, mutations, output):

    dir = output + util.MUTATION_DIRECTORY
    directory = os.path.dirname(dir)
    regex = re.compile('[BJOUXZ]')

    if not os.path.exists(directory):
        os.makedirs(directory)

    out = open(dir + sample + ".txt", "w")
    seq_id = 1

    for transcript in mutations.keys():

        canonical_seq = mutations[transcript][0].ref_protein_sequence
        missense_mutations = []

        for mutation in mutations[transcript]:

            r = mutation.mut_protein_sequence

            if mutation.annotation.find(util.MUTATION_MISSENSE) >= 0:
                missense_mutations.append(mutation.mut_protein_sequence)
                missense_annotation = mutation.annotation

            # if r.find("[BJOUXZ]") >= 0:
            if regex.search(r) != None:
                continue
            try:
                if r.find("*") >= 0:
                    s = r[len(r) - 22:len(r) - 1]
                    c = canonical_seq[len(r) - 22:len(r)-1]
                else:
                    m = re.findall(r"[a-z]", r)
                    if not len(m):
                        continue
                    i = r.find(m[0])

                    if i < 10:
                        s = r[i] + r[i + 1:i + 21]
                        c = canonical_seq[i] + canonical_seq[i + 1:i + 21]
                    elif i >= len(r) - 10:
                        s = r[i - 20:i] + r[i]
                        try:
                            c = canonical_seq[i - 20:i] + canonical_seq[i]
                        except:
                            c = canonical_seq[i - 20:i]
                    else:
                        s = r[i - 10:i] + r[i] + r[i + 1:i + 11]
                        c = canonical_seq[i - 10:i] + canonical_seq[i] + canonical_seq[i + 1:i + 11]

            except IndexError:
                c = ""

            if len(s) == 21:
                if c:
                    out.write("|".join([">" + str(mutation),
                                        str(seq_id) + "\n"]))
                    out.write(c + "\n")
                    seq_id += 1

                out.write("|".join([">" + str(mutation),
                                    str(seq_id) + "\n"]))
                out.write(s + "\n")
                seq_id += 1

        if len(missense_mutations) > 1:

            seqs = join_mutations(missense_mutations, canonical_seq)

            if seqs:
                for se in seqs:
                    # if se.find("[BJOUXZ]") >= 0:
                    if regex.search(r) != None:
                        continue
                    try:
                        if se.find("*") >= 0:
                            s = se[len(se) - 22:len(se)-1]
                            c = canonical_seq[len(se) - 22:len(se)-1]
                        else:
                            m = re.findall(r"[a-z]", se)[0]
                            i = se.find(m)

                            if i < 10:
                                s = se[i] + se[i + 1:i + 21]
                                c = canonical_seq[i] + canonical_seq[i + 1:i + 21]
                            elif i >= len(se)-10:
                                s = se[i - 20:i] + se[i]
                                c = canonical_seq[i - 20:i] + canonical_seq[i]
                            else:
                                s = se[i - 10:i] + se[i] + se[i + 1:i + 11]
                                c = canonical_seq[i - 10:i] + canonical_seq[i] + canonical_seq[i + 1:i + 11]
                    except IndexError:
                        c = ""

                    if len(s) == 21:
                        if c:
                            out.write("|".join([">" + str(mutations[transcript][0]),
                                                str(seq_id) + "\n"]))
                            out.write(c + "\n")
                            seq_id += 1

                        out.write("|".join([">" + str(mutations[transcript][0]),
                                            str(seq_id) + "\n"]))
                        out.write(s + "\n")
                        seq_id += 1

    out.close()
    out.close()


def join_mutations(sequence_list, reference_seq):

    mutation = {}
    for seq in sequence_list:
        m = re.findall(r"[a-z]", seq)[0]
        i = seq.find(m)
        mutation[i] = m

    resulted_seqs = []
    prev_i = 0
    combined_sum = 0
    combined_mutations = {}

    for key in sorted(mutation):

        if abs(combined_sum + key - prev_i) <= 10 and prev_i is not 0:
                combined_sum += abs(key - prev_i)
                combined_mutations[key] = mutation[key]
                combined_mutations[prev_i] = mutation[prev_i]
        else:
            if len(combined_mutations.keys()) > 0:
                for i in range(2, len(combined_mutations.keys()) + 1):
                    combinations = itertools.combinations(combined_mutations.keys(), i)
                    for tuple in combinations:
                        resulted_seq = ""
                        prev_index = 0
                        for index in tuple:
                            resulted_seq += reference_seq[prev_index:index] + mutation[index]
                            prev_index = index + 1
                        resulted_seq += reference_seq[prev_index:]
                        resulted_seqs.append(resulted_seq)
            combined_sum = 0
            combined_mutations = {}
        prev_i = key

    if len(combined_mutations.keys()) > 0:
        for i in range(2, len(combined_mutations.keys()) + 1):
            combinations = itertools.combinations(combined_mutations.keys(), i)
            for tuple in combinations:
                resulted_seq = ""
                prev_index = 0
                for index in tuple:
                    resulted_seq += reference_seq[prev_index:index] + mutation[index]
                    prev_index = index + 1
                resulted_seq += reference_seq[prev_index:]
                resulted_seqs.append(resulted_seq)

    return resulted_seqs

