import pytest

import os
import shutil
import tempfile
import dnasnout_client.align

demo_data_path = os.path.join(os.path.dirname(dnasnout_client.__path__[0]), 'data')
fasta_fn = 'GCF_000840245.1_ViralProj14204_genomic.fna'
fastq_fn = 'iontorrent_head400.fq'

def test_bowtie2_index():

    bowtie2 = dnasnout_client.align.Bowtie2('bowtie2')
    with tempfile.TemporaryDirectory() as tmp_d:
        shutil.copy(os.path.join(demo_data_path, fasta_fn), tmp_d)
        fasta_path = os.path.join(tmp_d, fasta_fn)
        res = bowtie2.ensure_index(tmp_d, fasta_path)

        # success ?
        assert res is None
                             
        # added index files ?
        fns = os.listdir(tmp_d)
        assert len(tmp_d) > 1

def test_bowtie2_align():

    bowtie2 = dnasnout_client.align.Bowtie2('bowtie2')
    with tempfile.TemporaryDirectory() as tmp_d:
        shutil.copy(os.path.join(demo_data_path, fasta_fn), tmp_d)
        fasta_path = os.path.join(tmp_d, fasta_fn)
        res = bowtie2.ensure_index(tmp_d, fasta_path)

        parameters = dict((key, value) for key, cls, value, doc in bowtie2._default_align_params)
        ref_index = os.path.join(tmp_d, bowtie2.index_template(fasta_fn))
        matchref_dir = tmp_d
        reads_fn = os.path.join(demo_data_path, fastq_fn)
        unmapped_fn = os.path.join(tmp_d, 'un.fq')
        assert not os.path.exists(unmapped_fn)
        res = bowtie2._align(parameters, ref_index, matchref_dir,
                             reads_fn,
                             unmapped_fn)
        assert os.path.exists(unmapped_fn)
        assert os.path.getsize(unmapped_fn) > 0        

def test_bwa_index():
    
    bwamem = dnasnout_client.align.BWAmem('bwa')
    with tempfile.TemporaryDirectory() as tmp_d:
        shutil.copy(os.path.join(demo_data_path, fasta_fn), tmp_d)
        fasta_path = os.path.join(tmp_d, fasta_fn)
        res = bwamem.ensure_index(tmp_d, fasta_path)

        # success ?
        assert res is None
                             
        # added index files ?
        fns = os.listdir(tmp_d)
        assert len(tmp_d) > 1

def test_bwa_align():

    bwa = dnasnout_client.align.BWAmem('bwa')
    with tempfile.TemporaryDirectory() as tmp_d:
        shutil.copy(os.path.join(demo_data_path, fasta_fn), tmp_d)
        fasta_path = os.path.join(tmp_d, fasta_fn)
        res = bwa.ensure_index(tmp_d, fasta_path)

        parameters = dict((key, value) for key, cls, value, doc in bwa._default_align_params)
        ref_index = os.path.join(tmp_d, bwa.index_template(fasta_fn))
        matchref_dir = tmp_d
        reads_fn = os.path.join(demo_data_path, fastq_fn)
        unmapped_fn = os.path.join(tmp_d, 'un.fq')
        assert not os.path.exists(unmapped_fn)
        res = bwa._align(parameters, ref_index, matchref_dir,
                         reads_fn,
                         unmapped_fn)
        assert os.path.exists(unmapped_fn)
        assert os.path.getsize(unmapped_fn) > 0
