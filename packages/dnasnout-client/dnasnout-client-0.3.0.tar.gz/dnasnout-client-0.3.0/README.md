# About

This code is supplementary material for the peer-reviewed publication:

http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0083784

(also in [GenomeWeb](https://www.genomeweb.com/sequencing/danish-duo-introduces-microbe-identification-scheme-based-random-subset-raw-sequ))


It requires:

- Python >= 3.3+ (currently tested with Python 3.5)

- `bowtie2` in the PATH (parameter `-a`, try `--help`)

- It is self-documented (try `-h` or `--help`).

It is working on FASTQ or gzipped-FASTQ files, possibly on BAM files.

Be gentle and please do not hammer the server like there is no tomorrow.

The latest released versions of the package will always be on Pypi.

The terminal-based UI is looking like this:

![Screenshot](screenshot.png)


The code is shipping with test data:

- Phage Lambda DNA sequence from ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/840/245/GCF_000840245.1_ViralProj14204
  

# Installation

This installs as a regular Python package with:

```bash
	  
python setup.py install

```

It is also available in a Docker container. The current release is version 0.3.0.

```bash

docker pull lgautier/dnasnout-client:0.3.0

```

**Note about the docker image:** the default user is called `docker_user`,
so the container is not running an in-container root. We are providing
a way to map the in-container user to the host user below, making
the execution of the software as an in-container command line
a practical option.

   
# Usage


```bash

alias dnasnout="python -m dnasnout_client.console"

```

Declaring an alias that runs a container from our Docker image
that can access the current working directory with the host's user and group ID
can be done with:

```bash
alias dnasnout="docker run \
                --rm -t \
                -v `pwd`:/shared \
                -u $(id -u):$(id -g) \
                -w /shared \
                lgautier/dnasnout-client:0.3.0 \
                python3 -m dnasnout_client.console"

```

Once the alias is declared, we can use it as a regular command:

```bash

wget http://tapir.cbs.dtu.dk/static/iontorrent_head400.fq
dnasnout -i iontorrent_head400.fq -d iontorrent_test

```

A more difficult dataset is a metagenome sample from anterior nares in
the HMP Core Microbiome Sampling Protocol A (HMP-A).

We use read data available on the CloVR website: http://data.clovr.org/

```bash

wget http://clovr.org/files/Diginorm_sample_input.zip
unzip Diginorm_sample_input.zip

dnasnout -i Diginorm_sample_input/SRS018671.denovo_duplicates_marked.trimmed.1.fastq \
         -d diginorm_test \
	 -n 600 --bloom-filter --seed 123 --n-matches=8

```

Unsurprising results are:

- /Staphilococcus epidermidis/ is found
- possible human (not suprising) or mouse DNA (probable artefact from our sample strategy that alignment would clear up)

Unfortunately, the human and mouse references genomes are not downloaded
(our server is geared toward serving larger genomes) but the general idea is that one would
first align the reads in such samples against the human (or mouse) genome and use dnasnout
on the unmapped reads.

More surprising results are unplaced genomic scaffold from:

- /Harpegnathos saltator/
- /Volvox carteri f. nagariensis/

These are either artefacts from our scoring, from the reference sequence (contamination
when the references where sequenced).



Help is available with:

```bash

dnasnout --help

```

**note:** To update the Docker image to the latest version, `docker pull` is required each time
(otherwise Docker will use the local image available).

```bash

docker pull lgautier/dnasnout-client:latest

```


