dedup_hash
----------------------------

This is a commandline utility to remove exact duplicate reads
from paired-end fastq files. Reads are assumed to be in 2 separate
files. Read sequences are then concatenated and a short hash is calculated on
the concatenated sequence. If the hash has been previsouly seen the read will
be dropped from the output file.  This means that reads that have the same
start and end coordinate, but differ in lengths will not be removed (but those
will be "flattened" to at most 1 occurence).

This algorithm is very simple and fast, and saves memory as compared to
reading the whole fastq file into memory, such as fastuniq does.

Installation
------------

depdup_city relies on the cityhash python package,
which supports python-2.7 exclusively.

``pip install dedup_hash`

