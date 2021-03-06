###############################################################################
#Dockerfile
#
#Version: 1.0
#Software: neoANT-HILL
#Description: Neoantigen NGS-based detector
#Tags: (Immuno)Genomics
#Build cmd = docker build -t neoanthill:1.0 <path-to-dockerfile>
#Run cmd = docker run -v /path-to-docker-input:/biodocker/
###############################################################################

# Source Image
FROM biocontainers/biocontainers:latest

USER root

# install
RUN apt-get clean all && \
apt-get update && \
apt-get upgrade -y && \
apt-get install -y software-properties-common && \
apt-get install -y \
gcc-4.9        \
g++-4.9        \
coinor-cbc     \
zlib1g-dev     \
libbz2-dev     \
nano           \
gawk           \
parallel       \
tcsh           \
r-base         \
r-base-core    \
&& update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.9 \
&& apt-get clean \
&& apt-get purge \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --upgrade pip

RUN pip install \
numpy==1.15 \
pyomo \
pysam \
matplotlib \
tables \
pandas \
flask \
future \
mygene \
mhctools \
markdown==3.0.1

### Installing samtools/htslib/tabix/bgzip

ENV VERSIONH 1.2.1-254-6462e34
ENV NAMEH htslib
ENV SHA1H "6462e349d16e83db8647272e4b98d2a92992071f"

ENV VERSION 1.2-242-4d56437
ENV NAME "samtools"
ENV SHA1 "4d56437320ad370eb0b48c204ccec7c73f653393"

RUN git clone https://github.com/samtools/htslib.git && \
    cd ${NAMEH} && \
    git reset --hard ${SHA1H} && \
    make -j 4 && \
    cd .. && \
    cp ./${NAMEH}/tabix /usr/local/bin/ && \
    cp ./${NAMEH}/bgzip /usr/local/bin/ && \
    cp ./${NAMEH}/htsfile /usr/local/bin/ && \
    strip /usr/local/bin/tabix; true && \
    strip /usr/local/bin/bgzip; true && \
    strip /usr/local/bin/htsfile; true && \

git clone https://github.com/samtools/samtools.git && \
    cd ${NAME} && \
    git reset --hard ${SHA1} && \
    make -j 4 && \
    cp ./${NAME} /usr/local/bin/ && \
    cd .. && \
    strip /usr/local/bin/${NAME}; true && \
    rm -rf ./${NAMEH}/ && \
    rm -rf ./${NAME}/ && \
    rm -rf ./${NAMEH}

#mhcflurry download
ENV MHCFLURRY_DOWNLOADS_CURRENT_RELEASE=1.2.0
ENV MHCFLURRY_DATA_DIR=/tmp/
RUN mhcflurry-downloads fetch

#HLA Typing
#OptiType dependecies
RUN curl -O https://support.hdfgroup.org/ftp/HDF5/current18/bin/hdf5-1.8.21-Std-centos7-x86_64-shared_64.tar.gz \
    && tar -xvf hdf5-1.8.21-Std-centos7-x86_64-shared_64.tar.gz \
    && mv hdf5/bin/* /usr/local/bin/ \
    && mv hdf5/lib/* /usr/local/lib/ \
    && mv hdf5/include/* /usr/local/include/ \
    && mv hdf5/share/* /usr/local/share/man/ \
    && rm -rf hdf5/ \
    && rm -r hdf5-1.8.21-Std-centos7-x86_64-shared_64.tar.gz

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH
ENV HDF5_DIR /usr/local/
    
#installing optitype form git repository (version Dec 09 2015) and wirtig config.ini
RUN git clone https://github.com/FRED-2/OptiType.git \
&& sed -i -e '1i#!/usr/bin/env python\' OptiType/OptiTypePipeline.py \
&& mv OptiType/ /usr/local/bin/ \
&& chmod 777 /usr/local/bin/OptiType/OptiTypePipeline.py \
&& echo "[mapping]\n\
razers3=/usr/local/bin/razers3 \n\
threads=1 \n\
\n\
[ilp]\n\
solver=cbc \n\
threads=1 \n\
\n\
[behavior]\n\
deletebam=true \n\
unpaired_weight=0 \n\
use_discordant=false\n" >> /usr/local/bin/OptiType/config.ini

#installing razers3
RUN git clone https://github.com/seqan/seqan.git seqan-src \
&& cd seqan-src \
&& cmake -DCMAKE_BUILD_TYPE=Release \
&& make razers3 \
&& cp bin/razers3 /usr/local/bin \
&& cd .. \
&& rm -rf seqan-src

ENV PATH=/usr/local/bin/OptiType:$PATH

#installing kallisto
RUN conda install -y kallisto

WORKDIR /home/biodocker/

#installing GATK
RUN wget https://github.com/broadinstitute/gatk/releases/download/4.1.0.0/gatk-4.1.0.0.zip \
&& unzip gatk-4.1.0.0.zip 

#installing SNPEFF
RUN wget http://sourceforge.net/projects/snpeff/files/snpEff_latest_core.zip \ 
&& unzip snpEff_latest_core.zip \
&& rm snpEff_latest_core.zip

#installing QUANTISEQ
RUN git clone https://github.com/icbi-lab/quanTIseq.git

RUN ln -s /usr/lib/x86_64-linux-gnu/libgfortran.so.3 /usr/lib/libgfortran.so
RUN ln -s /usr/lib/x86_64-linux-gnu/libquadmath.so.0 /usr/lib/libquadmath.so

RUN Rscript quanTIseq/dependencies.R
RUN sed -i 's/\/opt/\/home\/biodocker/g' quanTIseq/quantiseq/deconvolution/*
RUN cp -r quanTIseq/quantiseq /home/biodocker

RUN mkdir iedb
WORKDIR /home/biodocker/iedb/

#installing iedb prediction class I
RUN wget https://downloads.iedb.org/tools/mhci/2.17/IEDB_MHC_I-2.17.tar.gz \
&& tar -xzvf IEDB_MHC_I-2.17.tar.gz \
&& rm IEDB_MHC_I-2.17.tar.gz

#installing iedb prediction class II
RUN wget https://downloads.iedb.org/tools/mhcii/2.17.5/IEDB_MHC_II-2.17.5.tar.gz \
&& tar -xzvf IEDB_MHC_II-2.17.5.tar.gz \
&& rm IEDB_MHC_II-2.17.5.tar.gz

COPY ant_hill /home/biodocker/neoanthill/

WORKDIR /home/biodocker/neoanthill/

RUN gunzip data/protein_refseq.fasta.gz \
&& gunzip data/transcript_refseq.fasta.gz 

##download-data

RUN wget https://github.com/pachterlab/kallisto-transcriptome-indices/releases/download/ensembl-96/homo_sapiens.tar.gz -O data/homo_sapiens.tar.gz \
&& tar -xvzf data/homo_sapiens.tar.gz --strip-components 1 \
&& mv transcriptome.idx data/human_transcript_index \
&& rm Homo_sapiens.* && rm transcripts_to_genes.txt \
&& rm data/homo_sapiens.tar.gz

RUN wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/Mills_and_1000G_gold_standard.indels.b37.vcf.gz -P data/ \
&& gunzip data/Mills_and_1000G_gold_standard.indels.b37.vcf.gz && bgzip data/Mills_and_1000G_gold_standard.indels.b37.vcf \
&& wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/dbsnp_138.b37.vcf.gz -P data/ \
&& gunzip data/dbsnp_138.b37.vcf.gz && bgzip data/dbsnp_138.b37.vcf \
&& wget ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/b37/1000G_phase1.indels.b37.vcf.gz -P data/ \
&& gunzip data/1000G_phase1.indels.b37.vcf.gz && bgzip data/1000G_phase1.indels.b37.vcf \
&& wget ftp://ftp.ensembl.org/pub/grch37/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh37.dna.primary_assembly.fa.gz -O data/Homo_sapiens.GRCh37.fa.gz \
&& gunzip data/Homo_sapiens.GRCh37.fa.gz

#RUN wget http://www.bioinformatics-brazil.org/~carolcoelho/neoanthill/protein_refseq.fasta -O /home/biodocker/neoanthill/data/protein_refseq.fasta
#RUN wget http://www.bioinformatics-brazil.org/~carolcoelho/neoanthill/transcript_refseq.fasta -O /home/biodocker/neoanthill/data/transcript_refseq.fasta

EXPOSE 80


