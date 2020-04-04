#!/usr/bin/python

import os
from os import listdir
from os import path
from os import system
from collections import defaultdict
import util
from mexceptions import InputFileNotExistException, PreProcessingVariantCallingException, VCFAnnotationFailed


def execute(opts):

    util.print_task(util.TASK_VARIANT_CALLING)
 
    input = opts[util.INPUT_OPTION] 
    output = opts[util.OUTPUT_OPTION] + util.VARIANT_CALLING_DIRECTORY
    gatk = util.GATK
    ref_genome = util.GENOME_FASTA_FILE
    dbsnp = util.DBSNP
    mills = util.MILLS
    known = util.KNOWN
#    gnomad = util.GNOMAD

    variants = os.path.dirname(output)
    if not os.path.exists(variants):
        os.makedirs(variants)

    ids = defaultdict(list)

    for f in input:
        if f.endswith((".sam", ".bam")):
            file =  os.path.split(f)[1]
            sample = file.split(".")[0]
            ids[sample].append(f)
            
    for sample in ids.keys():
        cmd1 = gatk + " AddOrReplaceReadGroups -I " + " ".join(ids[sample]) + " -O " + output + sample + ".sorted.bam --SORT_ORDER coordinate --RGID " + sample + \
               " --RGLB Lib1 --RGPL Illumina --RGPU Barcode --RGSM " + sample
        cmd2 = gatk + " MarkDuplicates -I " + output + sample + ".sorted.bam -O " + output + sample + ".dedupped.bam --CREATE_INDEX true --VALIDATION_STRINGENCY SILENT --METRICS_FILE " + \
               output + sample + ".metrics.txt"
        cmd3 = gatk + " SplitNCigarReads -R " + ref_genome + " -I " + output + sample + ".dedupped.bam -O " + output + sample + ".split.bam"
        cmd4 = gatk + " BaseRecalibrator -R " + ref_genome + " -I " + output + sample + ".split.bam --known-sites " + \
               dbsnp + " --known-sites " + mills + " --known-sites " + known + " -O " + output + sample + ".BaseRecalReport.grp"
        cmd5 = gatk + " ApplyBQSR -R " + ref_genome + " -I " + output + sample + ".split.bam --add-output-sam-program-record --bqsr-recal-file " + \
        output + sample + ".BaseRecalReport.grp -O " + output + sample + ".recalibrated.bam"
        cmd6 = gatk + " Mutect2 -R " + ref_genome + " -I " + output + sample + ".recalibrated.bam -tumor " + sample +  \
        " -stand-call-conf 20 --annotation Coverage --annotation DepthPerAlleleBySample --annotation BaseQuality --annotation ReadPosition --annotation MappingQuality " + \
        "--dont-use-soft-clipped-bases true -O " + output + sample + ".vcf2.gz"			
        cmd7 = gatk + " FilterMutectCalls -V " +  output + sample + ".vcf2.gz --max-alt-allele-count 2 --min-median-read-position 5 -O " +  output + sample + ".vcf.gz"

        try:
            system(cmd1)
            system(cmd2)
            system(cmd3)
            system(cmd4)
            system(cmd5)
            system(cmd6)
            system(cmd7)

        except Exception as e:
       	    raise PreProcessingVariantCallingException(str(e))


    rf = [f for f in listdir(variants) if path.isfile(path.join(variants, f))]

    for a in rf:
        if not a.endswith((".vcf.gz", ".tbi")):
            system("rm -f " + a)

    util.print_task(util.TASK_SUCCESS)

    return variants

def annotate(vcf_info):

    util.print_task(util.TASK_ANNOTATING_VCF)

    snpEff = util.SNPEFF
    snpsift = util.SNPSIFT

    if os.path.isdir(vcf_info):
        file = [path.join(vcf_info, f) for f in listdir(vcf_info) if path.isfile(path.join(vcf_info, f))]
        for i in file:
            if i.endswith((".vcf", ".vcf.gz")):
                vcf_info = vcf_info
                cmd = "java  -Xmx2g -jar " + snpEff + " ann -noLog -canon -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -noStats GRCh37.p13.RefSeq " + i + " > " + i + ".int"
                cmd2 = "java  -Xmx2g -jar " + snpsift + " filter \" (ANN[*].BIOTYPE has 'protein_coding')\" " +  i + ".int > " + i + ".annotated"
                try:
                    system(cmd)
                    system(cmd2)
                except Exception as e:
                        raise VCFAnnotationFailed(str(e))
    else:
        if os.path.isfile(vcf_info):
            cmd = "java -Xmx2g -jar " + snpEff + " ann -noLog -canon -no-downstream -no-intergenic -no-intron -no-upstream -no-utr -noStats GRCh37.p13.RefSeq " + vcf_info + " > " + vcf_info + ".int"
            cmd2 = "java -Xmx2g -jar " + snpsift + " filter \" (ANN[*].BIOTYPE has 'protein_coding')\" " + vcf_info + ".int > " + vcf_info + ".annotated"
            vcf_info = vcf_info + ".annotated"
            try:
                system(cmd)
                system(cmd2)
            except Exception as e:
                raise VCFAnnotationFailed(str(e))
                
    util.print_task(util.TASK_SUCCESS)

    return vcf_info
