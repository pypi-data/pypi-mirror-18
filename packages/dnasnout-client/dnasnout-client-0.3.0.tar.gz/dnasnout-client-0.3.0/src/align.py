""" Interface to (short) read aligners """

from collections import namedtuple
import os
import subprocess
import signal
import asyncio
import asyncio.subprocess
import tempfile

Param = namedtuple('Param', 'name cls default_value doc')

# FIXME: rewrite as a custom logger ?
# FIXME: duplicated in console.py
def _message(msg, logger, msg_func):
    if logger is not None:
        logger.info(msg);
    if msg_func is not None:
        try:
            msg_func(msg)
        except curses.error as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            if logger is not None:
                logger.error(e)

class Aligner(object):
    def __init__(self, aligner):
        """
        :param aligner: aligner (executable to align reads, full path if necessary)
        """
        self._aligner = aligner
        

class Bowtie2(Aligner):
    _name = 'bowtie2'
    _default_align_params = (Param('preset', str, "--very-sensitive",
                                   'parameter preset for command-line bowtie2'),
                             Param('n_threads', int, 1,
                                   'number of threads used by bowtie2'),
                             Param('inputformat', str, '-q',
                                   'input format for bowtie2'))
    

    def index_template(self, reference_fa):
        return reference_fa[:-3]

    def ensure_index(self, reference_dir,
                     reference_fa,
                     logger=None, msg_func=None):
        """
        :param reference_dir: directory with reference sequences
        :param reference_fa: FASTA file name for reference sequence
        :param logger: logger (or None)
        :param msg_func: call to display messages (or None)
        """
        res = None
        # only build bowtie index if missing
        reference_idx = os.path.join(reference_dir, 'ref.1.bt2')
        if not os.path.isfile(reference_idx):
            msg = 'building bowtie index...'
            _message(msg, logger, msg_func)

            cmd = (os.path.join(os.path.dirname(self._aligner),
                                'bowtie2-build'), '--quiet',
                   reference_fa, 
                   self.index_template(reference_fa)) # clip the suffix '.fa'
            _message(' '.join(cmd), logger, None)

            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError:
                sys.stdout.write('error with bowtie2.\n'); sys.stdout.flush()
                res = (reference_dir, None, 0)
        return res

    def align(self, refid,
              reference_fa, unmapped_fn, out_d, gz_tag,
              parameters = None,
              logger = None, status_win = None, match_win=None):

        if parameters is None:
            parameters = dict()
            for p in self._default_align_params:
                parameters[p.name] = p.cls(p.default_value)
            
        matchref_dir = os.path.join(out_d, 'refid_{0}'.format(refid))
        # can raise errors
        os.mkdir(matchref_dir)

        msg = 'Aligning reads with bowtie2...'
        _message(msg, logger, status_win.set_action)
        new_unmapped_fn = os.path.join(matchref_dir, 'un.fq')
        if gz_tag == '-gz':
            new_unmapped_fn += ".gz"

        ref_index = self.index_template(reference_fa)

        res = self._align(parameters, ref_index, matchref_dir, unmapped_fn, new_unmapped_fn)
        
        for row in res.split(b'\n'):
            row = row.decode('ASCII')
            if row.endswith('overall alignment rate'):
                percent = float(row[:row.index('%')])
        countaligned = percent
        #sys.stdout.write('\n{0}\n'.format(cmd)); sys.stdout.flush()
        msg = 'Complete'
        _message(msg, logger, None)
        return (new_unmapped_fn, countaligned)
        
    def _align(self, parameters, ref_index, matchref_dir, reads_fn, unmapped_fn, gz_tag='', logger=None):
        
        cmd = (self._aligner,
               parameters['inputformat'],
               parameters['preset'], "-X", '2000',
               "-x", ref_index, # clip the suffix '.fa'
               "-U", reads_fn,
               "-S", os.path.join(matchref_dir, 'ref.sam'),
               '--un'+gz_tag, unmapped_fn,
               '--threads', str(parameters['n_threads']))
        if logger is not None:
                logger.info(' '.join(cmd))

        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return res
    
        
class BWAmem(Aligner):
    _name = 'bwa'
    _default_align_params = (Param('n_threads', int, 1,
                                   'number of threads used by bwa'),)

    def index_template(self, reference_fa):
        return reference_fa[:-3]
        
    def ensure_index(self, reference_dir,
                     reference_fa,
                     logger=None, msg_func=None):
        """
        :param reference_dir: directory with reference sequences
        :param reference_fa: FASTA file name for reference sequence
        :param logger: logger (or None)
        :param msg_func: call to display messages (or None)
        """
        res = None
        # only build index if missing
        ref_idx_template = self.index_template(reference_fa)
        reference_idx = os.path.join(reference_dir, '%s.bwt' % ref_idx_template)
        if not os.path.isfile(reference_idx):
            msg = 'building %s index...' % self._name
            _message(msg, logger, msg_func)

            cmd = (self._aligner, 'index',
                   '-p', ref_idx_template, # clip the suffix '.fa'
                   reference_fa)
                   
            _message(' '.join(cmd), logger, None)

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            if proc.returncode != 0:
                print('error with %s.\n' % self._name)
                res = (reference_dir, None, 0)
        return res

    def _align(self, parameters, ref_index, matchref_dir, reads_fn, unmapped_fn,
               gz_tag='', logger=None):
        
        if logger is not None:
                logger.info(' '.join(cmd_align))

        with tempfile.NamedTemporaryFile(dir=matchref_dir, mode='w+b') as fh_out:
            cmd_align = (self._aligner,
                         'mem',
                         '-t', str(parameters['n_threads']),
                         ref_index,
                         reads_fn)
            proc_align = subprocess.Popen(cmd_align,
                                          stdout=fh_out)
            proc_align.wait()
            fh_out.flush()
            
            # samtools view to the rescue
            with open(unmapped_fn, 'wb') as fh_fq:
                cmd_unaligned = 'samtools view -f 4 - | samtools view -bS - | samtools bam2fq'
                proc_unaligned = subprocess.Popen(cmd_unaligned,
                                                  stdin = fh_out,
                                                  stdout= fh_fq,
                                                  shell=True)
                proc_unaligned.communicate()
            
            cmd_aligned = 'samtools view -F 4 - |  grep ^@ | wc -l'
            proc_aligned = subprocess.Popen(cmd_aligned,
                                            stdin = fh_out,
                                            stdout = subprocess.PIPE,
                                            shell=True)
            res = proc_aligned.communicate()[0]
            
        return res
        
        
    def align(self, refid,
              reference_fa, unmapped_fn, out_d, gz_tag,
              parameters = None,
              logger = None, status_win = None, match_win=None):

        if parameters is None:
            parameters = dict()
            for p in self._default_align_params:
                parameters[p.name] = p.cls(p.default_value)
            
        matchref_dir = os.path.join(out_d, 'refid_{0}'.format(refid))
        # can raise errors
        os.mkdir(matchref_dir)

        msg = 'Aligning reads with %s...' % self._name
        _message(msg, logger, status_win.set_action)
        new_unmapped_fn = os.path.join(matchref_dir, 'un.fq')
        if gz_tag == '-gz':
            new_unmapped_fn += ".gz"

        reference_index = self.index_template(reference_fa)
        res = self._align(parameters, reference_index, matchref_dir, reads_fn, unmapped_fn,
                          gz_tag='', logger=None)

        for row in res.split(b'\n'):
            row = row.decode('ASCII')
            if row.endswith('overall alignment rate'):
                percent = float(row[:row.index('%')])
        countaligned = percent
        #sys.stdout.write('\n{0}\n'.format(cmd)); sys.stdout.flush()
        msg = 'Complete'
        _message(msg, logger, None)
        return (new_unmapped_fn, countaligned)


def extract_unaligned(bam_fn, unaligned_fq):
    with open(bam_fn, 'rb') as fh_in, open(bam_fn, 'wb') as fh_out:
        cmd_unaligned = 'samtools view -f 4 - | samtools view -bS - | samtools bam2fq'
        proc_unaligned = subprocess.Popen(cmd_unaligned,
                                          stdin = fh_in,
                                          stdout= fh_out,
                                          shell=True)
        proc_unaligned.communicate()
