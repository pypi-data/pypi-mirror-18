import argparse
import gzip
import io
import sys
from itertools import cycle
try:
    from itertools import izip
except ImportError:
    pass  # we can simply use zip in python3


class UniqueFastqBase(object):
    def __init__(self,
                 infiles,
                 outfiles,
                 write_gzip,
                 buffer_size=32768,
                 compresslevel=2,
                 hash_module="smhasher"):
        self.seen_hashes = set()
        self.infiles = infiles
        self.outfiles = outfiles
        self.write_gzip = write_gzip
        self.buffer_size = buffer_size
        self.compresslevel = compresslevel
        self.hash_module = self.import_hash_module(hash_module)
        self.cur_fastq_str_r1 = ""
        self.cur_fastq_str_r2 = ""
        self.cur_uniq = False
        self.fastq_cycle = cycle([self.header_one_action, self.seq_action, self.header_two_action, self.qual_action])
        self.infiles = self.get_inputs()
        self.outfiles = self.get_outputs()
        self.process_files()
        self.close_io()

    def import_hash_module(self, hash_module):
        if hash_module == "smhasher":
            from smhasher import murmur3_x64_64
            return murmur3_x64_64
        if hash_module == "CityHash64":
            from cityhash import CityHash64
            return CityHash64
        if hash_module == "hashxx":
            from pyhashxx import hashxx
            return hashxx

    def get_input(self, infile):
        if self._is_gzip(infile):
            return io.BufferedReader(gzip.GzipFile(infile, 'rb'), buffer_size=self.buffer_size)
        else:
            return open(infile)

    def get_inputs(self):
        return [self.get_input(infile) for infile in self.infiles]

    def get_outputs(self):
        if self.write_gzip:
            return [io.BufferedWriter(gzip.GzipFile(outfile, 'wb', compresslevel=self.compresslevel), buffer_size=self.buffer_size) for outfile in self.outfiles]
        return [open(outfile, 'w') for outfile in self.outfiles]

    def close_io(self):
        [infile.close() for infile in self.infiles]
        [outfile.close() for outfile in self.outfiles]

    def _is_gzip(self, infile):
        gzip_magic_byte = b"\x1f\x8b\x08"
        with open(infile, 'rb') as input:
            return gzip_magic_byte == input.read(len(gzip_magic_byte))

    def process_files(self):
        raise Exception('Not implemented')

    def seq_action(self, lines):
        cur_hash = self.hash_module("".join(lines))
        if cur_hash in self.seen_hashes:
            self.cur_uniq = False
        else:
            self.seen_hashes.add(cur_hash)
            self.cur_uniq = True
            self.cur_fastq_strs = ["".join((prev, cur)) for prev, cur in zip(self.cur_fastq_strs, lines)]

    def header_one_action(self, lines):
        self.cur_uniq = False
        self.cur_fastq_strs = lines

    def header_two_action(self, lines):
        self.cur_fastq_strs = ["".join((prev, cur)) for prev, cur in zip(self.cur_fastq_strs, lines)]

    def qual_action(self, lines):
        if self.cur_uniq:
            self.cur_fastq_strs = ["".join((prev, cur)) for prev, cur in zip(self.cur_fastq_strs, lines)]
            [outfile.write(string) for string, outfile in zip(self.cur_fastq_strs, self.outfiles)]


class UniqueFastqPairsPy2(UniqueFastqBase):

    def process_files(self):
        for items in izip(self.fastq_cycle, *self.infiles):
            fastq_item = items[0]
            lines = items[1:]
            fastq_item(lines)


class UniqueFastqPairsPy3(UniqueFastqBase):

    def process_files(self):
        for items in zip(self.fastq_cycle, *self.infiles):
            fastq_item = items[0]
            lines = items[1:]
            # The following might be slow, rework this to something smarter
            # it it slows down too much.
            fastq_item([l if isinstance(l, str) else l.decode() for l in lines])


def get_args():
    parser = argparse.ArgumentParser(description='Get unique reads from fastq files')
    parser.add_argument('--r1_in', required=True, help='Read1 input fastq file')
    parser.add_argument('--r2_in', required=False, default=None, help='Read2 input fastq file')
    parser.add_argument('--r1_out', required=True, help='Read1 output fastq file')
    parser.add_argument('--r2_out', required=False, help='Read2 output fastq file')
    parser.add_argument('--write_gzip', action='store_true', help="Compress output in gzip format?")
    parser.add_argument('--buffer_size', default=32768, type=int, help="Set buffer size for reading gzip files")
    parser.add_argument('--compresslevel', default=2, type=int, choices=list(range(1, 10)), help="Set compression level (1: fastest, 9: highest compression)")
    parser.add_argument('--algo', default='smhasher', choices=['CityHash64', 'hashxx', 'smhasher'], help='Select hash algorithm')
    return parser.parse_args()


def get_infiles(args):
    if args.r2_in:
        return [args.r1_in, args.r2_in]
    else:
        return [args.r1_in]


def get_outfiles(args):
    if args.r2_out:
        return [args.r1_out, args.r2_out]
    else:
        return [args.r1_out]


def get_unique_fastq_instance():
    if sys.version_info.major == 2:
        return UniqueFastqPairsPy2
    elif sys.version_info.major == 3:
        return UniqueFastqPairsPy3


def main():
    args = get_args()
    UniqueFastqPairs = get_unique_fastq_instance()
    UniqueFastqPairs(infiles=get_infiles(args),
                     outfiles=get_outfiles(args),
                     write_gzip=args.write_gzip,
                     buffer_size=args.buffer_size,
                     compresslevel=args.compresslevel,
                     hash_module=args.algo)


if __name__ == '__main__':
    main()
