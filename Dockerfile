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
ADD dependencies.R /tmp/
RUN ln -s /usr/lib/x86_64-linux-gnu/libgfortran.so.3 /usr/lib/libgfortran.so
RUN ln -s /usr/lib/x86_64-linux-gnu/libquadmath.so.0 /usr/lib/libquadmath.so
RUN Rscript /tmp/dependencies.R
COPY quantiseq /home/biodocker/quantiseq

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

#RUN wget http://www.bioinformatics-brazil.org/~carolcoelho/neoanthill/protein_refseq.fasta -O /home/biodocker/neoanthill/data/protein_refseq.fasta
#RUN wget http://www.bioinformatics-brazil.org/~carolcoelho/neoanthill/transcript_refseq.fasta -O /home/biodocker/neoanthill/data/transcript_refseq.fasta

EXPOSE 80


