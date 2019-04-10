#!/usr/bin/python

import util
import re

class Mutation:

    @property
    def sample(self):
        return self.__sample

    @property
    def annotation(self):
        return self.__annotation

    @property
    def gene(self):
        return self.__gene

    @property
    def transcript(self):
        return self.__transcript

    @property
    def hgvs_c(self):
        return self.__hgvs_c

    @property
    def hgvs_p(self):
        return self.__hgvs_p

    @property
    def variant(self):
        return self.__variant

    @property
    def genotype(self):
        return self.__genotype

    @property
    def protein(self):
        return self.__protein

    @property
    def ref_protein_sequence(self):
        return self.__ref_protein_sequence

    @property
    def ref_transcript_sequence(self):
        return self.__ref_transcript_sequence

    def __init__(self, line, nm_np_conversor, refseq_transc, refseq_human):
        ls = line.rstrip().split("\t")
        self.sample = ls[0]
        self.annotation = ls[1]
        self.gene = ls[2]
        self.transcript = ls[3]
        self.hgvs_c = ls[4]
        self.hgvs_p = ls[5]
        self.variant = ls[6]
        self.genotype = ls[7]

        try:
            self.protein = nm_np_conversor[self.transcript]
            self.ref_protein_sequence = refseq_human[self.protein]
            self.ref_transcript_sequence = refseq_transc[self.transcript]
        except KeyError as e:
            raise e

        if self.annotation == util.MUTATION_MISSENSE >= 0:
            self.mut_protein_sequence = self._missense(self.ref_protein_sequence, self.hgvs_p)
        elif self.annotation == util.MUTATION_FRAMESHIFT  >= 0:
            self.mut_protein_sequence = self._frameshift(self.ref_transcript_sequence, self.hgvs_c)
        elif self.annotation in util.MUTATION_INFRAME >= 0:
            self.mut_protein_sequence = self._inframe(self.ref_transcript_sequence, self.hgvs_c)
        else:
            self.hgvs_p = "."

        if len(self.hgvs_p.split(".")[1]) == 0:
            self.mut_protein_sequence = ""
        else:
            pos_prot = int(re.findall(r'\d+', self.hgvs_p.split(".")[1])[0])
            aux = self.mut_protein_sequence[0:pos_prot - 1] + \
                  self.mut_protein_sequence[pos_prot - 1:pos_prot].lower() + \
                  self.mut_protein_sequence[pos_prot:]
            self.mut_protein_sequence = aux

    def __str__(self):
        s = "|".join([ 
            self.sample, self.transcript, self.protein, self.annotation, self.gene, 
            self.hgvs_c.replace(">", "*"), self.hgvs_p.replace(">", "*"), self.variant, 
            self.genotype
        ])
        return s

    def _missense(self, seq_protein, hgvs_p):

        translated_sequence = ""
        ref_prot, alt_prot = re.split(r'\d+', hgvs_p.split(".")[1])
        alt_prots = []

        for i in range(0, len(alt_prot), 3):
            alt_prots.append(alt_prot[i:i + 3])

        pos_prot = int(re.findall(r'\d+', hgvs_p.split(".")[1])[0])

        if util.AMINO[ref_prot].upper() != seq_protein[pos_prot - 1]:
            return translated_sequence

        translated_sequence = seq_protein[0:pos_prot - 1]
        for ap in alt_prots:
            translated_sequence += util.AMINO[ap]
        translated_sequence += seq_protein[pos_prot + len(alt_prots) - 1:]

        return translated_sequence

    def _inframe(self, refseq_transcript, hgvs_c):

        translated_sequence = ""
        orf, transc_seq = refseq_transcript.split("\t")
        orf = int(orf)
        hgvs_c = hgvs_c.split(".")[1]

        if hgvs_c.find("-") >= 0:
            return translated_sequence

        if hgvs_c.find("_") >= 0:
            pos, mutations = hgvs_c.split("_")
            pos = int(re.findall(r"[0-9]+", pos)[0])

            if hgvs_c.find("ins") >= 0 and hgvs_c.find("del") >= 0:
                deletion, insertion = re.findall(r"[A-Z]+", mutations)
                mutation_type = "del_ins"

            else:
                mutation_type = re.findall(r"[a-z]+", mutations)[0]
                if mutation_type.find("dup") >= 0:
                    pos = int(re.findall(r"[0-9]+", mutations)[0])
                mutation = re.findall(r"[A-Z]+", mutations)[0]

        else:
            pos = int(re.findall(r"\d+", hgvs_c)[0])

            if hgvs_c.find("ins") >= 0 and hgvs_c.find("del") >= 0:
                deletion, insertion = re.findall(r"[A-Z]+", hgvs_c)
                mutation_type = "del_ins"

            else:
                mutation_type = re.findall(r"[a-z]+", hgvs_c)[0]
                mutation = re.findall(r"[A-Z]+", hgvs_c)[0]

        if orf > 0:
            if mutation_type == "ins" or mutation_type == "dup":
                aux = transc_seq[0:pos + orf] + mutation + transc_seq[pos + orf:]
            else:
                if mutation_type == "del_ins":
                    aux = transc_seq[0:pos + orf - 1] + insertion + transc_seq[(pos + orf - 1) + len(deletion):]
                else:
                    aux = transc_seq[0:pos + orf - 1] + transc_seq[(pos + orf - 1) + len(mutation):]

            for i in range(orf, len(aux), 3):

                codon = aux[i:i + 3].upper()

                if len(codon) < 3:
                    break

                if codon in util.CODON.keys() and util.CODON[codon] != "STOP":
                    translated_sequence += util.CODON[codon]
                elif util.CODON[codon] == "STOP":
                    if pos + orf >= i and pos + orf <= i + 3:
                        translated_sequence += util.AMINO["Ter"]
                    break

        return translated_sequence

    def _frameshift(self, refseq_transcript, hgvs_c):

        translated_sequence = ""
        orf, transc_seq = refseq_transcript.split("\t")
        orf = int(orf)
        hgvs_c = hgvs_c.split(".")[1]

        if hgvs_c.find("-") >= 0:
            return translated_sequence

        if hgvs_c.find("_") >= 0:
            pos, mutations = hgvs_c.split("_")
            pos = int(re.findall(r"\d+", pos)[0])

            if hgvs_c.find("ins") >= 0 and hgvs_c.find("del") >= 0:
                deletion, insertion = re.findall(r"[A-Z]+", mutations)
                mutation_type = "del_ins"

            else:
                mutation_type = re.findall(r"[a-z]+", mutations)[0]
                if mutation_type.find("dup") >= 0:
                    pos = int(re.findall(r"[0-9]+", mutations)[0])
                mutation = re.findall(r"[A-Z]+", mutations)[0]

        else:
            pos = int(re.findall(r"\d+", hgvs_c)[0])

            if hgvs_c.find("ins") >= 0 and hgvs_c.find("del") >= 0:
                deletion, insertion = re.findall(r"[A-Z]+", hgvs_c)
                mutation_type = "del_ins"

            else:
                mutation_type = re.findall(r"[a-z]+", hgvs_c)[0]
                mutation = re.findall(r"[A-Z]+", hgvs_c)[0]

        if orf > 0:
            if mutation_type == "ins" or mutation_type == "dup":
                aux = transc_seq[0:pos + orf] + mutation + transc_seq[pos + orf:]
            else:
                if mutation_type == "del_ins":
                    aux = transc_seq[0:pos + orf - 1] + insertion + transc_seq[(pos + orf - 1) + len(deletion):]
                else:
                    aux = transc_seq[0:pos + orf - 1] + transc_seq[(pos + orf - 1) + len(mutation):]

            for i in range(orf, len(aux), 3):

                codon = aux[i:i + 3].upper()

                if len(codon) < 3:
                    break

                if codon in util.CODON.keys() and util.CODON[codon] != "STOP":
                    translated_sequence += util.CODON[codon]
                elif util.CODON[codon] == "STOP":
                    if pos + orf >= i and pos + orf <= i + 3:
                        translated_sequence += util.AMINO["Ter"]
                    break

        return translated_sequence

