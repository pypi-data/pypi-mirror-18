import hashlib
import inspect
import os
import subprocess
import sys
import tempfile


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(currentdir)
sys.path.insert(0, os.path.join(parent_dir, 'dedup_hash/'))
import dedup_hash


TEST_DATA_DIR = os.path.join(parent_dir, 'test-data/')
UNCOMPRESSED_IN = ['r1.fastq', 'r2.fastq']
COMPRESSED_IN = ['r1.fastq.gz', 'r2.fastq.gz']
UNCOMPRESSED_OUT = ['r1_dedup.fastq', 'r2_dedup.fastq']
SINGLE_IN = ['r1.fastq']
SINGLE_OUT = ['r1_dedup.fastq']



def run(input):
    args = prepare_args(input)
    run_dedup(args)
    compare_output(args)


def compare_output(args):
    ref_out1 = os.path.join(TEST_DATA_DIR, 'r1_dedup.fastq')
    try:
        assert md5(args['outfiles'][0]) == md5(ref_out1)
    except AssertionError:
        cmd = "diff -Nru %s %s" % (args['outfiles'][0], ref_out1)
        subprocess.check_call(cmd.split(' '))
    print('all good')


def prepare_args(test_files):
    infiles = [os.path.join(TEST_DATA_DIR, test_file) for test_file in test_files]
    outfiles = [tempfile.NamedTemporaryFile(delete=False).name for test_file in test_files]  # Same number of output files as input files
    kwargs = {'infiles': infiles,
              'outfiles': outfiles,
              'write_gzip': False}
    return kwargs


def run_dedup(kwargs):
    fastq_pairs_instance = dedup_hash.get_unique_fastq_instance()
    fastq_pairs_instance(**kwargs)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == '__main__':
    run(UNCOMPRESSED_IN)
    run(COMPRESSED_IN)
    run(SINGLE_IN)
