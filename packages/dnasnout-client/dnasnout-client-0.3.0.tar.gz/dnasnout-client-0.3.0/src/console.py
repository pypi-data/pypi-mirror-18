from . import __version__

import os, subprocess
import sys, logging
import warnings
def goodbye(message):
    sys.stderr.write('\n')
    sys.stderr.write(message)
    sys.stderr.write('\n')
    sys.stderr.flush()
    sys.exit(0)

if sys.version_info[0] == 3:
    if sys.version_info[1] < 3:
        warnings.warn("Error: Python >= 3.3 is required for this to work.")
else:
    goodbye("Error: Python >= 3.3 is required for this to work.")

import shutil, random, gzip, pickle
import json, urllib, urllib.request, urllib.parse, urllib.error, http.client
import socket
from collections import namedtuple, OrderedDict
    
try:
    import ngs_plumbing.fastq as fastq
    import ngs_plumbing.parsing
    from ngs_plumbing.sampling import ReservoirSample, ReservoirSampleBloom
except ImportError as ie:
    goodbye("""
    Error: The package 'ngs_plumbing' cannot be imported because of:

    %s

    Missing modules are available on Pypi, and installing them can be as simple
    as running `pip install <module name>`.
    Note: the optional dependency on h5py 
    coming with ngs_plumbing is _not_ required.""" % ie)
    
from . import match
from .align import Bowtie2, BWAmem

Entry = namedtuple('Entry', 'header sequence quality')


def avgqual_phred(qualstring):
    """ Average quality in a quality string from Phred scores.
    Return zero (0) if string of length 0. """
    l = len(qualstring)
    if l == 0:
        return 0
    else:
        return sum(ord(x)-33 for x in qualstring) / l

# FIXME: rewrite as a custom logger ?
def _message(msg, logger, msg_func):
    if logger is not None:
        logger.info(msg);
    if msg_func is not None:
        try:
            msg_func(msg)
        except curses.error as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            print(e)
            if logger is not None:
                logger.error(e)

def _filter_passthrough(logger, msg_func, entryname):
    def f(entries):
        count = int(0); inc = int(1)
        for entry in entries:
            yield entry
            if count % 10000 == 0:
                msg = "Read {:,} {:s} entries".format(count, entryname)
                _message(msg, logger, msg_func)
            count += inc
        msg = "Read {:,} {:s} entries".format(count, entryname)
        _message(msg, logger, msg_func)
    return f

def _filter_bam(logger, msg_func):
    """ Filter bam entries """
    LMIN = 32
    PNMAX = 0.05
    AQMIN = 30
    def f(entries):
        count = int(0); inc = int(1)
        for read in entries:
            # filter the read out if either:
            # - already mapped
            # - read length < LMIN
            # - percentage of 'N's in the read > PNMAX
            # - average quality score > AQMIN
            if (not read.is_unmapped) or \
                    (len(read.seq) < LMIN) or \
                    ((1.0 * read.seq.count('N') / len(read.seq)) > PNMAX) or \
                    avgqual_phred(read.qual) > AQMIN:
                pass 
            else:
                yield Entry(read.tags[2][1], read.seq, None) # empty quality
            if count % 10000 == 0:
                msg = "Read {0:,} unmapped BAM entries (l >= {1})".format(count, LMIN)
                _message(msg, logger, msg_func)
                status_win.refresh()
            count += inc
        msg = "Read {0:,} unmapped BAM entries (l >= {1})".format(count, LMIN)
        _message(msg, logger, _message(msg, logger, msg_func))
        status_win.refresh()
    return f

def _sample_entries(entries, spl, entryname = '', screen=None):
    for entry in entries:
        spl.add(entry)
    return count
    
def _tofastq_reads_bam(input_file, output_file):
    LMIN = 32
    PNMAX = 0.05
    AQMIN = 30
    f = pysam.Samfile(input_file.name, "rb")
    count_ok = int(0)
    count_total = int(0)
    inc = int(1)
    for read in f:
        # filter the read out if either:
        # - already mapped
        # - read length < LMIN
        # - percentage of 'N's in the read > PNMAX
        # - average quality score > AQMIN
        count_total += inc
        if (not read.is_unmapped) or \
                (len(read.seq) < LMIN) or \
                ((1.0 * read.seq.count('N') / len(read.seq)) > PNMAX) or \
                avgqual_phred(read.qual) > AQMIN:
            continue
        output_file.writelines(('@'+read.tags[2][1], '\n', read.seq, '\n+\n', read.qual, '\n'))
        if count_total % 10000 == 0:
            sys.stdout.write("\rWrote {0:,}/{1:,} unmapped BAM entries into FASTQ".format(count_ok, count_total));
            sys.stdout.flush()
        count_ok += inc
    sys.stdout.write("\rWrote {0:,}/{1:,} unmapped BAM entries into FASTQ.\n".format(count_ok, count_total));
    sys.stdout.flush()
    f.close()
    return (count_ok, count_total)

FFORMAT_OPENER = OrderedDict((('AUTO', ngs_plumbing.parsing.open),
                              ('FASTQ', fastq.FastqFile), 
                              ('FASTQ.gz', fastq.GzipFastqFile), 
                              ('BAM', None))) #FIXME

def _makeparser():
    _N = 300
    import argparse
    parser = argparse.ArgumentParser(
        description = '''
DNA-snout <pig-noise>, a simple client.

The communication protocol with server is likely to change
without prior notice. Make sure that you are using the latest
version of this script.

By default the script is querying our server "tapir"
(http://tapir.cbs.dtu.dk). This is a relatively modest server,
and one should be gentle with it - hitting it too heavily may
result in having your IP banned.

Consider running your own DNAsnout server if this is a limitation.
''',
        epilog = 'Version {0} - Laurent Gautier(2013, 2016) <laurent@cbs.dtu.dk, lgautier@gmail.com>'.format(__version__)
        )

    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input-file',
                          required = True,
                          nargs = '+',
                          type = argparse.FileType('rb'),
                          dest = 'input_files',
                          help = 'Input file')
    required.add_argument('-d', '--output-directory',
                          dest = 'out_d',
                          metavar = '<directory>',
                        required = True,
                          help = 'Output directory')
    required.add_argument('-P', '--n-processes',
                          dest = 'n_processes',
                          type = int,
                          default = 1,
                          help = 'Number of processes to use (note: each bowtie instance in a process can itself use several threads) [currently not doing anything useful]')
    optional_files = parser.add_argument_group('optional arguments for files and storage')
    optional_files.add_argument('-f', '--input-format',
                                metavar = '<file format>',
                                dest = 'input_format',
                                choices = FFORMAT_OPENER.keys(),
                                default = 'AUTO',
                                help = 'Input format, as one of {%(choices)s}. If AUTO, an educated guess will be made from the file extension. (default: %(default)s)')
    optional_files.add_argument('--ref-directory',
                                dest = 'refdir',
                                metavar = '<directory>',
                                help = 'Directory in which to find reference sequences and indexes, or add them whenever necessary. This allows to reuse reference sequences and bowtie2 indexes across several DNA sequencing data sets.')
    optional_files.add_argument('-l', '--log-file',
                                dest = 'log_file',
                                metavar = '<file name>',
                                type = argparse.FileType('wb'),
                                help = 'Log file')
    optional_files.add_argument('--file-buffering',
                                dest = 'file_buffering',
                                default = int(2**23),
                                type = int,
                                help = 'Buffer size for I/O (in bytes - default: %(default)s)')
    optional_sampling = parser.add_argument_group('optional arguments for the sampling')
    optional_sampling.add_argument('--seed',
                                   dest = 'seed',
                                   default = None,
                                   type = int,
                                   metavar = 'Random seed',
                                   help = 'Set the random set for sampling')
    optional_sampling.add_argument('-n', '--sample-size',
                                   dest = 'sample_size',
                                   metavar = '<sample size>',
                                   type = int,
                                   default = _N,
                                   help = 'Sample size. '
                                   'Increase this value if suspected "garbage" '
                                   'reads obtained from sequencing '
                                   '(default: %(default)s)')
    optional_sampling.add_argument('--bloom-filter',
                                   dest = 'bloom_filter',
                                   action = 'store_true',
                                   help = 'Use a Bloom filter-based '
                                   'reservoir sampling. This could(*) be '
                                   'helpful with highly redundant sequencing data '
                                   '(clonal artefact or else) while '
                                   'an identification based on diversity '
                                   'is wanted. (*: speculative and not verified)')
    optional_sampling.add_argument('--bloom-m',
                                   dest = 'bloom_m',
                                   type = int,
                                   default = int(10E6),
                                   help = 'Number of bits in the Bloom filter. '
                                   'Increasing it prevents the filter from '
                                   'saturating with larger/diverse datasets '
                                   'but also consummes more memory. '
                                   '(only used if --bloom-filter - '
                                   'default: %(default)s)')
    optional_sampling.add_argument('--bloom-k',
                                   dest = 'bloom_k',
                                   type = int,
                                   default = int(10),
                                   help = 'Number of hashing function in the Bloom filter '
                                   '(only used if --bloom-filter - '
                                   'default: %(default)s)')

    optional_mapping = parser.add_argument_group('optional arguments for the alignment')
    optional_mapping.add_argument('--no-mapping',
                                  dest = 'nomap',
                                  action = "store_true",
                                  help = "Do not perform mapping with the aligner. "
                                  "This forces the number of iterations to one.")
    optional_mapping.add_argument('-a', '--aligner',
                                  dest = 'aligner',
                                  default = "bowtie2",
                                  choices = ["bowtie2", ],
                                  help = "Excutable for the aligner"
                                  "(full path to the executable is needed if "
                                  "it cannot be found in the PATH). "
                                  'Possible values are {%(choices)s} '
                                  "(default: %(default)s)")
    ## dynamically add options for the aligner(s)
    for cls in [Bowtie2, BWAmem]:
        for p in cls._default_align_params:
            optional_mapping.add_argument('--%s-%s' % (cls._name, p.name.replace('_', '-')),
                                          dest = '%s_%s' % (cls._name, p.name),
                                          default = p.default_value,
                                          help = ''.join(('%s.' % p.doc,
                                                          '(defaut: %(default)s). ',
                                                          'Check the documentation of %s ' % cls._name,
                                                          'for further details.')))
    parser.add_argument('--iter-max',
                        dest = 'itermax',
                        type = int,
                        default = 3,
                        help = 'Maximum number of iterations. Increase this number when working on metagenomics samples (default: %(default)s)')
    parser.add_argument('--pause',
                        dest = 'pause',
                        type = int,
                        default = 0,
                        help = 'Number of seconds to pause before exiting. (default: %(default)s)')
    parser.add_argument('--n-matches',
                          dest = 'nmatches',
                          type = int,
                          default = 5,
                          help = 'Maximum number of matches to retrieve (default: %(default)s)')
    parser.add_argument('-s', '--server',
                        dest = 'server',
                        default = "http://tapir.cbs.dtu.dk",
                        help = 'URL for the server (default: %(default)s). CAUTION: be gentle with our little server - hitting it too heavily may result in having your IP banned.')
    parser.add_argument('-p', '--port',
                        dest = 'port',
                        type = int,
                        default = 80,
                        help = 'Port on the server (default: %(default)s)')


    return parser



def ensure_reference_dir(reference_dir, out_d, refid):
    """ 
    :param reference_dir: reference directory
    :param out_d: output directory (used only if reference_dir not None)
    :param refid: reference id (used only if reference_dir not None)
    """
    if reference_dir is None:
        reference_dir = os.path.join(out_d, '..', 'references')
        # can raise FileNotFoundError or PermissionError
        os.mkdir(reference_dir)
        reference_dir = os.path.join(out_d, '..', 'references', 
                                     'refid_{0}'.format(refid))
    else:
        reference_dir = os.path.join(reference_dir, 'refid_{0}'.format(refid))

    # only create directory with reference information 
    # (bowtie2 index and so on...) if not already there
    if not os.path.isdir(reference_dir):
        # can raise FileNotFoundError or PermissionError
        os.mkdir(reference_dir)
    return reference_dir


class NoReferenceSentError(Exception):
    pass

def ensure_reference(reference_dir, out_d, refid, description,
                     server,
                     logger = None, msg_func = None):
    """ 
    Ensure that a reference is present, downloading it if necessary.

    :param reference_dir: reference directory
    :param out_d: output directory (used only if reference_dir not None)
    :param refid: reference id (used only if reference_dir not None)
    :param description: description
    :param server: URL for the DNAsnout server
    :param logger: logger
    :param screen: curses screen
    """
    reference_dir = ensure_reference_dir(reference_dir, out_d, refid)
    # only download the reference if not already there
    reference_fa = os.path.join(reference_dir, 'ref.fa')
    if not os.path.isfile(reference_fa):
        con = urllib.request.urlopen(server + '/reference/{0}'.format(refid))
        ref = json.loads(con.read().decode('ASCII'))
        if ref['seq'] == '':
            raise NoReferenceSentError("No reference sent for reference ID %s" % str(refid))
        with open(reference_fa, 'w') as seq_out:
            seq_out.write('>{0}:{1}'.format(refid, description.lstrip('>'))); seq_out.write('\n')
            seq_out.write(ref['seq']); seq_out.write('\n')
            seq_out.flush();seq_out.close();

    return reference_fa

def mapreads(m_i, m, unmapped_fn, out_d, server,
             aligner,
             aligner_params = None,
             reference_dir = None,
             gz_tag='',
             status_win=None, match_win=None,
             logger=None):
    
    """ Map reads 

    :param m_i: rank of the match in the list
    :param m: match returned by DNA snout (:class:`dict` from JSON structure)
    :param unmapped_fn: file name for unmapped reads
    :param out_d: output directory
    :param aligner: an aligner (a concrete class inheriting from the abstract :class:`Aligner`)
    :param reference_dir: directory with reference sequences
    :param gz_tag: tag for compression
    :param status_win: 
    :param match_win: 
    :param logger: logger (or None)"""

    msg = 'Match #{i}: fetching ref. DNA...'.format(i=m_i)
    _message(msg, logger, status_win.set_action)
    status_win.refresh()

    refid = m['refid']
        
    reference_dir = ensure_reference_dir(reference_dir, out_d, refid)

    reference_fa = None
    try:
        reference_fa = ensure_reference(reference_dir, out_d, refid, 
                                        m['description'], server,
                                        logger, status_win.set_action)
    except urllib.error.URLError as ue:
        if logger is not None:
            logger.info(str(ue)+"\n")
        msg = 'Error: URL Error'
        _message(msg, logger, status_win.set_action)
    except urllib.error.HTTPError as ue:
        if logger is not None:
            logger.info(str(ue)+"\n")
        msg = 'Error: HTTP Error'
        _message(msg, logger, status_win.set_action)
    except NoReferenceSentError as nrse:
        msg = 'Error: Did not get the sequence from the server (presumably because too long).'
        _message(msg, logger, status_win.set_action)
    except Exception as e:
        if logger is not None:
            logger.info(str(ue)+"\n")
        msg = 'Error: Retrieving reference sequence from the server'
        _message(msg, logger, status_win.set_action)
        
    status_win.refresh()

    if reference_fa is not None:
        bt_idx = aligner.ensure_index(reference_dir,
                                      reference_fa,
                                      logger=None, msg_func=None)
        if bt_idx is not None:
            # error occurred, return it
            return bt_idx

        new_unmapped_fn, \
            countaligned = aligner.align(refid, 
                                         reference_fa, unmapped_fn,
                                         out_d, gz_tag,
                                         parameters = aligner_params,
                                         logger = None,
                                         status_win = status_win,
                                         match_win = match_win)
        msg = None
    else:
        new_unmapped_fn = unmapped_fn
        countaligned = None
        
    return (reference_dir, new_unmapped_fn, countaligned, msg)

# "Screen object
#Screen = namedtuple('Screen', 'stdscr x y')

class StatusWindow(object):
    SCR_ITERATION_ROW = 1
    SCR_DATA_ROW = 2
    SCR_ACTION_ROW = 4
    SCR_NET_ROW = 3

    def __init__(self, win, box=True):
        self._win = win
        self._box = box

    def set_iteration(self, msg):
        self._win.addstr(self.SCR_ITERATION_ROW, 1, msg)
        self._win.clrtoeol()

    def set_data(self, msg):
        self._win.addstr(self.SCR_DATA_ROW, 1, msg)
        self._win.clrtoeol()
        
    def set_action(self, msg):
        self._win.addstr(self.SCR_ACTION_ROW, 1, msg)
        self._win.clrtoeol()
        
    def set_net(self, msg):
        self._win.addstr(self.SCR_NET_ROW, 1, msg)
        self._win.clrtoeol()

    def refresh(self):
        self._win.refresh()
        if self._box:
            self._win.box()

class MatchWindow(object):

    def __init__(self, win, maxrows, ncol):
        self._win = win
        self._n = 0
        self._ncol = ncol
        self._header()
        self.refresh()
        self._maxrows = maxrows
        self._full = False

    def _header(self):
        self._win.addstr(0, 0, 'CURRENT CANDIDATE MATCHES:')
        self._win.clrtoeol()

    def _addstr(self, row, col, s):
        if len(s) >= self._ncol:
            s = s[:(self._ncol-5)] + '...'
        self._win.addstr(row, col, s)
        self._win.clrtoeol()
        
    def add_match(self, l1=None, l2=None):
        
        if self._n >= (self._maxrows // 2):
            self._win.addstr(self._n*2, 1, '...', curses.A_REVERSE)
            self._win.clrtoeol()
            self._full = True
            return
        
        if l1 is not None:
            self._addstr(self._n*2+1, 1, l1)
            self._win.clrtoeol()
        if l2 is not None:
            self._addstr(self._n*2+1+1, 1, l2)
            self._win.clrtoeol()
        self._n += 1

    def amend(self, l1=None, l2=None):
        if self._full:
            return
        n = self._n - 1
        if l1 is not None:
            self._addstr(n*2+1, 1, l1)
            self._win.clrtoeol()
        if l2 is not None:
            self._addstr(n*2+1+1, 1, l2)
            self._win.clrtoeol()

    def refresh(self):
        self._win.refresh()

    def clear(self):
        self._n = 0
        self._full = False
        # clear
        y, x = self._win.getmaxyx()
        s = ' ' * (x - 1)
        for l in range(y):
            self._win.addstr(l, 0, s)
        # put the header back
        self._header()
        self.refresh()

class IterationWindow(object):

    def __init__(self, win, maxrows, ncol):
        self._win = win
        self._n = 0
        self._ncol = ncol
        self._maxrows = maxrows
        self._header()
        self.refresh()
        self._full = False

    def _addstr(self, row, col, s):
        if len(s) >= self._ncol:
            s = s[:(self._ncol - 5)] + '...'
        self._win.addstr(row, col, s)
        self._win.clrtoeol()

    def _header(self):
        self._addstr(0, 0, 'RESULTS:')
        
    def add_result(self, m):
        if self._n >= self._maxrows:
            self._addstr(self._n-1, 1, '...')
            self._full = True
            return
        self._addstr(self._n+1, 1, str(m))
        self._n += 1

    def refresh(self):
        self._win.refresh()


def process_fastq(unmapped_file, options, aligner, aligner_params,
                  status_win, iteration_win, match_win,
                  total_upload=0, logger=None):
    """

    Process a FASTQ file

    :param unmapped_file: Python file handle to FASTQ file 
    :param options: command line options in a namespace
    :param stdscr:
    :param total_upload: 
    :param logger: A Python logger

    :return: a tuple with the results and the total uploaded
    :rtype: :class:`tuple` with 2 elements :class:`Result` and :class:`int`

    """

    reference_dir = options.refdir

    count_threshold = 0
    entries = None
    try:
        entries = ngs_plumbing.parsing.open(unmapped_file.name, 
                                            buffering = options.file_buffering)
    except ImportError as ie:
        return (Result(None,
                       str(ie)),
                total_upload)
    except ngs_plumbing.parsing.FileFormatError:
        return (Result(None,
                       "File format error with %s" % unmapped_file.name),
                total_upload)

    try:
        initial_data_size = '{:,.2f}KB'.format(os.stat(unmapped_file.name).st_size / 1000)
    except:
        initial_data_size = 'NA'

    if unmapped_file.name.lower().endswith('.gz'):
        gz_tag = '-gz'
    else:
        gz_tag = ''

    inputfile_path = os.path.join(options.out_d, 
                                  os.path.splitext(os.path.basename(unmapped_file.name))[0])
    os.mkdir(inputfile_path)
    if logger is not None:
        logger.info('Created directory %s' % inputfile_path)

    iteration = 0
    iterinfo = []
    prevp = 1
    notmapped = set()

    while os.stat(unmapped_file.name).st_size > 0 and iteration < options.itermax:

        match_win.clear()

        if logger is not None:
            logger.info("Iteration %i" % iteration)

        iteration += 1
        iteration_path = os.path.join(inputfile_path, 
                                      "iteration_%i" % iteration)
        os.mkdir(iteration_path)
        if entries is not None:
            entries = ngs_plumbing.parsing.open(unmapped_file.name,
                                                buffering = options.file_buffering)
        if unmapped_file.name.lower().endswith('.bam'):
            msg = "Converting BAM to FASTQ..."
            status_win.set_action(msg)
            status_win.refresh()
            if logger is not None:
                logger.info(msg)
            unmapped_fn = unmapped_file.name
            output_fn = unmapped_fn[:-3] + 'fq'
            sys.stdout.write(output_fn); sys.stdout.flush()
            output_file = open(output_fn, 'w',
                               buffering = options.file_buffering)
            _tofastq_reads_bam(unmapped_file, output_file)
            unmapped_file.close()
            unmapped_fn = output_fn
            unmapped_file = open(unmapped_fn, 'rb',
                                 buffering = options.file_buffering)
        status_win.set_iteration(
            'Iteration %i / %i' % (iteration, options.itermax))
        entries = ngs_plumbing.parsing.open(unmapped_file.name,
                                            buffering = options.file_buffering)
        if options.bloom_filter:
            spl = ReservoirSampleBloom(options.sample_size,
                                       bloom_m = options.bloom_m,
                                       bloom_k = options.bloom_k)
        else:
            spl = ReservoirSample(options.sample_size)
        #candidate_entries = filter(None, entries)

        def _ui_update(*args, **kwargs):
            status_win.set_data(*args, **kwargs)
            status_win.refresh()

        read_filter = _filter_passthrough(logger,
                                          _ui_update,
                                          '')
        if logger is not None:
            logger.info(str(type(entries)))
        candidate_entries = read_filter(entries)
        for entry in candidate_entries:
            spl.add(entry)
        tmp = open(os.path.join(iteration_path, "spl.pkl"), "wb") # small. no point buffering
        pickle.dump(spl, tmp)
        tmp.close()
        msg = "Sending a request to %s..." % options.server
        status_win.set_action(msg)
        status_win.refresh()

        data = match._prep_data(spl._l)
        total_upload += len(data)    
        msg = "Total uploaded: {:,.2f}KB (local input data: {})".format(total_upload/1000, initial_data_size)
        status_win.set_net(msg)
        try:
            matchres = match.sniff_samples(spl._l,
                                           options.server)
        except urllib.error.URLError as ue:
            return (Result(None, str(ue)+"\n"),
                    total_upload)
        except http.client.BadStatusLine as bsl:
            return (Result(None, str(bsl)+"\n"),
                    total_upload)
        except socket.timeout as sto:
            return (Result(None, 
                           'Connection with the server timed out.'),
                    total_upload)
        except Exception as e:
            if logger is not None:
                logger.exception(e)
            return (Result(None, str(e)),
                    total_upload)

        f = open(os.path.join(iteration_path, "res.json"), "w") # small. no point buffering
        json.dump(matchres._d, f)
        f.close()
        unmapped_file.close()
        #unmapped_fn = None

        if options.nomap:
            msg = "No mapping performed. No need to iterate further."
            status_win.set_action(msg)
            return (Result(None, None),
                    total_upload)

        status_win.refresh()
        msg = "{0} matches (considering the first {1})".\
              format(len(matchres.matches), 
                     options.nmatches)
        status_win.set_action(msg)
        status_win.refresh()

        if logger is not None:
            logger.info(msg)
        best_countaligned = 0
        best_i = None
        res_list = []
        for m_i, m in enumerate(matchres.matches):
            match_offset = m_i*2
            if m_i == options.nmatches:
                break
            msg = m['description']
            match_win.add_match(l1=msg)
            match_win.refresh()
            if logger is not None:
                logger.info(msg)
            try:
                (reference_dir, unmapped_fn, countaligned, map_msg)\
                    = mapreads(m_i, m, unmapped_file.name,
                               iteration_path,
                               options.server,
                               aligner,
                               aligner_params = aligner_params,
                               reference_dir = reference_dir,
                               gz_tag = gz_tag,
                               status_win = status_win,
                               match_win = match_win,
                               logger = logger)
            except Exception as e:
                import traceback
                msg = ''.join(traceback.format_tb(e.__traceback__))
                msg += str(e)
                #msg = str(e)
                return (Result(None, msg),
                        total_upload)
            res_list.append((unmapped_fn, countaligned, m_i))

            if logger is not None:
                logger.info('    %s %% of the reads\n' % str(countaligned))


            if countaligned is None:
                try:
                    match_win.amend(l1=None, l2='NA (alignment not performed)')
                except curses.error as e:
                    pass
                notmapped.add(m['description'])
            else:
                try:
                    match_win.amend(l1=None, l2='%8.5f%%' % countaligned)
                except curses.error as e:
                    pass
                if countaligned > best_countaligned:
                    best_i = m_i
                    best_countaligned = countaligned

            iteration_win.refresh()

        if (best_i is None):
            msg = "No read matching."
            if logger is not None:
                logger.info(msg)
            break
        else:                
            p = prevp * res_list[best_i][1]
            iteration_win.add_result('%8.5f%% - %s' % \
                                     (p, matchres.matches[best_i]['description']))
            iteration_win.refresh()
            if logger is not None:
                logger.info('Best is: %s\n  with %f %% of the reads\n' % (matchres.matches[best_i]['description'], p))
            unmapped_fn = res_list[best_i][0]
            iterinfo.append((res_list[best_i], matchres.matches[best_i], p))
            prevp *= 1-(res_list[best_i][1]/100.0)
            # clearing the directories for the other mappings
            for i, elt in enumerate(res_list):
                if i == best_i:
                    continue
                tmp = 'refid_{0}'.format(matchres.matches[i]['refid'])
                try:
                    shutil.rmtree(os.path.join(iteration_path,
                                               tmp))
                except FileNotFoundError:
                    # if not there, don't remove it then...
                    pass
            res_list.append((unmapped_fn, countaligned, m_i))
            if logger is not None:
                logger.info('Unmapped reads: %s' % unmapped_fn)
        unmapped_file = open(unmapped_fn, 'rb',
                             buffering = options.file_buffering)
    import time
    time.sleep(options.pause)
    return (Result((unmapped_file.name, iterinfo, notmapped), None), total_upload)


def runall(stdscr, options, parser, pool, logger = None):
    height, width = stdscr.getmaxyx()
    banner_win = curses.newwin(1, width-1, 0, 0)
    banner_win.erase()
    #banner_win.box()
    banner_win.addstr(0, 0,
                      'DNA-Snout v. %s' % __version__,
                      curses.A_REVERSE)
    banner_win.refresh()

    path_aligner = shutil.which(options.aligner)
    if path_aligner is None:
        return Result(None,
                      "Error: No executable '%s' could be found." % options.aligner)

    if os.path.basename(options.aligner) == 'bowtie2':
        aligner = Bowtie2(path_aligner)
    elif os.path.basename(options.aligner) == 'bwa':
        aligner = BWAmem(path_aligner)
    else:
        return Result(None,
                      'Error: No class for aligner %s' % options.aligner)

    # extract the aligner parameters
    aligner_params = dict()
    opts_prefix = '--' + aligner._name
    for a in parser._optionals._actions:
        is_param = False
        param_name = None
        if hasattr(a, 'option_strings'): 
            for s in a.option_strings:
                if s.startswith(opts_prefix):
                    is_param = True
                    break
        if is_param:
            param_name = a.dest[(len(aligner._name)+1):]
            aligner_params[param_name] = getattr(options, a.dest)
    try:
        os.mkdir(options.out_d)
    except FileExistsError:
        return Result(None,
                      "Error: The output directory '%s' already exists. Use a different directory name, or remove it if its content is not needed." % options.out_d)        

    status_win = StatusWindow(curses.newwin(6,
                                            width-1,
                                            1, 0))
    status_win.refresh()

    iteration_win_height = min(5, max(options.itermax+2, 5))
    iteration_win = IterationWindow(curses.newwin(iteration_win_height,
                                                  width-1,
                                                  6+1, 0),
                                    iteration_win_height,
                                    width-2)
    iteration_win.refresh()

    match_win_height = height - (1 + 8 + iteration_win_height + 1)
    match_win = MatchWindow(curses.newwin(match_win_height,
                                          width-1,
                                          iteration_win_height+6+2+1, 0),
                            match_win_height, width-2)
    match_win.refresh()

    #prev_count = sys.maxsize
    total_upload = 0
    res_allinputs = list()
    for unmapped_file in options.input_files:
        res, total_upload = process_fastq(unmapped_file,
                                          options,
                                          aligner,
                                          aligner_params,
                                          status_win,
                                          iteration_win,
                                          match_win,
                                          total_upload=total_upload,
                                          logger=logger)
        res_allinputs.append(res)
    return res_allinputs


if __name__ == '__main__':
    import curses
    parser = _makeparser()
    options = parser.parse_args()

    if options.seed is not None:
        random.seed(options.seed)

    Result = namedtuple('Result', 'result error')
    
    import multiprocessing
    pool = multiprocessing.Pool(processes=options.n_processes)

    if (options.refdir is not None) and (not os.path.exists(options.refdir)):
        os.mkdir(options.refdir)
        
    if options.log_file is not None:
        options.log_file.close()
        logger = logging.getLogger("dnasnout_logger")
        logger.setLevel(logging.DEBUG)
        log_file = logging.FileHandler(options.log_file.name)
        log_file.setLevel(logging.DEBUG)
        logger.addHandler(log_file)
    else:
        logger = None
    res_allinputs = curses.wrapper(runall, options, parser, pool, logger=logger)
    if type(res_allinputs) is Result and res_allinputs.error is not None:
        if logger is not None:
            logger.error(res_allinputs.error)
        goodbye(res_allinputs.error)

    for res in res_allinputs:
        if res.error is not None:
            if logger is not None:
                logger.error(res.error)
            print(res.error)
            continue
        print('Summary for %s' % os.path.basename(res[0][0]))
        import csv
        with open(os.path.join(options.out_d, "results.csv"), "w") as fh_out:
            csv_w = csv.writer(fh_out)
            csv_w.writerow(('Description', 'percentage'))
            if len(res[0][1]) == 0:
                print('No read matching.')
            else:
                for elt in res[0][1]:
                    print(elt[1]['description'])
                    print('    %f %%' % (elt[2]))
                    csv_w.writerow((elt[1]['description'], elt[2]))
            if len(res[0][2]) > 0:
                print('We suggest looking also at')
                for elt in res[0][2]:
                    print(elt)
