 <img src="https://github.com/neoanthill/neoANT-HILL/blob/master/ant_hill/static/images/logo_index.png" style="max-width:20%;">

<p align="justify" > neoANT-HILL is a python toolkit that integrates several pipelines for fully automated identification of potential neoantigens (pNeoAgs) which could be used in personalized immunotherapy due to their ability to elicit and boosting T-cell immune response. It is available as a Docker pre-built image and allows the analysis of single- or multiple samples. As input files is required RNA sequencing reads and/or somatic DNA mutations derived from Next Generating Sequencing.</p>


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

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>4. Output Files </h2>

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
<li>IEDB</li>
<p align="justify">
 
#By using the IEDB software, you are consenting to be bound by and become a "Licensee" for the use of IEDB tools and are consenting to the terms and conditions of the Non-Profit Open Software License ("Non-Profit OSL") version 3.0

Please read these two license agreements <a href="http://tools.iedb.org/mhci/download/">here</a> before proceeding. If you do not agree to all of the terms of these two agreements, you must not install or use the product. Companies (for-profit entities) interested in downloading the command-line versions of the IEDB tools or running the entire analysis resource locally, should contact us (license@iedb.org) for details on licensing options.

Citing the IEDB All publications or presentations of data generated by use of the IEDB Resource Analysis tools should include citations to the relevant reference(s), found <a href="http://tools.iedb.org/mhci/reference/">here</a>.

</p>
<li>MHCflurry </li>  
<li>Kallisto</li>
<li>Optitype</li>
<li>quanTIseq</li>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>References </h2>

<p align="justify">1.	DePristo MA, Banks E, Poplin R, Garimella KV, Maguire JR, Hartl C, Philippakis AA, del Angel G, Rivas MA, Hanna M, McKenna A, Fennell TJ, Kernytsky AM, Sivachenko AY, Cibulskis K, Gabriel SB, Altshuler D, Daly MJ. A framework for variation discovery and genotyping using next-generation DNA sequencing data. Nature Genetics. 2011;43(5):491-498.</p>

<p align="justify">2.	Van der Auwera GA, Carneiro MO, Hartl C, Poplin R, del Angel G, Levy-Moonshine A, Jordan T, Shakir K, Roazen D, Thibault J, Banks E, Garimella KV, Altshuler D, Gabriel S, DePristo MA. From FastQ Data to High-Confidence Variant Calls: The Genome Analysis Toolkit Best Practices Pipeline. Current Protocols in Bioinformatics. 2013;:11.10.1-11.10.33.</p>

<p align="justify">3. CINGOLANI, Pablo et al. A program for annotating and predicting the effects of single nucleotide polymorphisms, SnpEff: SNPs in the genome of Drosophila melanogaster strain w1118; iso-2; iso-3. Fly, v. 6, n. 2, p. 80-92, 2012.</p>

<p align="justify">4. VITA, Randi et al. The immune epitope database (IEDB): 2018 update. Nucleic acids research, v. 47, n. D1, p. D339-D343, 2018.</p>

<p align="justify">5. O'DONNELL, Timothy J. et al. MHCflurry: open-source class I MHC binding affinity prediction. Cell systems, v. 7, n. 1, p. 129-132. e4, 2018.</p>

<p align="justify">6. BRAY, Nicolas L. et al. Near-optimal probabilistic RNA-seq quantification. Nature biotechnology, v. 34, n. 5, p. 525, 2016.</p>

<p align="justify">7. SZOLEK, András et al. OptiType: precision HLA typing from next-generation sequencing data. Bioinformatics, v. 30, n. 23, p. 3310-3316, 2014.</p>

<p align="justify">8. FINOTELLO, Francesca et al. Molecular and pharmacological modulators of the tumor immune contexture revealed by deconvolution of RNA-seq data. Genome medicine, v. 11, n. 1, p. 34, 2019.</p>

<h2><a id="user-content-installation-pip" class="anchor" aria-hidden="true" href="#installation-pip"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Limitations </h2>

This release only supports the human genome version GRCh37.
