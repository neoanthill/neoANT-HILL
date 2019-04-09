# neoANT-HILL

neoANT-HILL is a python toolkit that integrates several pipelines for fully automated identification of potential neoantigens (pNeoAgs) which could be used in personalized immunotherapy due to their ability to elicit and boosting T-cell immune response. It is available as a Docker pre-built image and allows the analysis of single- or multiple samples. As input files is required RNA sequencing reads and/or somatic DNA mutations derived from Next Generating Sequencing.


<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>1. Quick Start Guide </h2>

<p>After cloning the repository, build the container:</p>

<pre><code>$ docker build -t neoanthill:1.0 /path/to/Dockerfile
</code></pre>

<p>Running the container:</p>

<pre><code>$ docker run -v path/to/input:/home/biodocker/input -v path/to/output:/home/biodocker/output -p host:80 -it neoanthill:1.0 /bin/bash
</code></pre>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>2. Running neoANT-HILL </h2>

<p>To execute neoANT-HILL, run the following command:</p>

<pre><code>$ python app.py
</code></pre>

<p>Then, open the web browser and type the following address to start the interface:</p>

<pre><code> <strong>localhost:[host]</strong>
</code></pre>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>3. Input Files </h2>

<li>Somatic Variant List (.VCF format) and/<strong>OR</strong> </li>
<li>RNA-seq (Aligned and/or Raw) </li>  

<p></p>
<p>Note: RNA-seq files should match the following naming convention:  <em><strong>sampleID{_1,2}.extension</strong></em></p>

<p><em>where:</em></p>
<pre><code>
<li><strong>sampleID</strong> is the identifier of the sample;</li>
<li><strong>{_1,2}</strong> is the read pair in the paired-end samples (FASTQ)</li>
<li><strong>extension</strong> is the file extension eg. sam, bam, fastq, fastq.gz, etc.</li>
</code></pre>

<p>Note: The sampleID from VCF should match the sampleID from RNA-seq FASTQ.</p>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>4.Output Files </h2>

<p>For each sample the pipeline creates a generic diretory specified by the user (default: <code>datestamp</code>). Inside this directory there will be folders named sampleID.</p>

<p>For each sample the following  output files can be created:</p>

<table>
<thead>
<tr>
<th>Output</th>
<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>variant_calling</code></td>
<td>Somatic mutations called from the RNAseq data</td>
</tr>
<tr>
<td><code>mutations</code></td>
<td>FASTA sequences (WT and MT)</td>
</tr>
<tr>
<td><code>allele_prediction</code></td>
<td>HLA predicted haplotypes</td>
</tr>
<tr>
<td><code>gene_expression</code></td>
<td>Gene expression abundance</td>
</tr>
<tr>
<td><code>immune_infiltrating</code></td>
<td>Quantification of tumor-infiltrating immune cells</td>
</tr>
</tbody>
</table>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Contents </h2>

<p>neoANT-HILL uses the following software components and tools:</p>

<li>GATK 4.0</li>
<li>snpEff</li>  
<li>IEDB class I</li>
<li>IEDB class II</li>
<li>MHCflurry </li>  
<li>Kallisto</li>
<li>Optitype</li>
<li>quanTIseq</li>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Limitations </h2>

This release only supports the human genome version GRCh37.
