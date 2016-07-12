__author__ = 'theep_000'

import os
import tempfile

testbed = open('testbed', 'r')

class Gene:

    GC_percent = 0
    LowerCasePercent = 0
    NucleotideTrackLength = 0
    eighteenmer_count = 0

    def __init__(self, GCpercent, LowerCasePercent, NucleotideTracklength, EighteenMer_Count):
        self.GC_percent = GCpercent
        self.LowerCasePercent = LowerCasePercent
        self.NucleotideTrackLength = NucleotideTracklength
        self.eighteenmer_count = EighteenMer_Count

def extract_sequence_from_genome(chromosome, start, stop,
                                 human_genome = os.environ["ARCHER_GENOME"]):
    """Extracts a sequence from the human genome given a chromosom, start and stop

    :param str chromosome: Chromsome to extract from
    :param int start: Bed coordinate start of the sequence
    :parm int stop: Bed coordinate stop of the sequence
    """

    # Create a dummy bed line to use fastaFromBed of bedtools
    bed_lines = ["\t".join([chromosome, str(start), str(stop), "Name", "0", "+"])]

    temp_output_fasta = tempfile.NamedTemporaryFile()
    result = extract_fasta_using_bed(bed_lines, human_genome, temp_output_fasta.name)

    # Grab the resulting output file
    output_file = result['output_file']
    output_fasta = output_file.readlines()

    # The sequence will be the second line in the result
    return \
        "".join(output_fasta[1:]).replace.strip()

def GC_Content_entgene(extracted_seq):
    gc_counter = 0
    total_base = 0
    for line in extracted_seq:
        if '>' not in line:
            for base in line:
                if base != '\n':
                    total_base += 1
                if base == 'g':
                    gc_counter += 1
                if base == 'c':
                    gc_counter += 1
                if base == 'G':
                    gc_counter += 1
                if base == 'C':
                    gc_counter += 1
    GC_percent = float(gc_counter)/float(total_base)
    return GC_percent

def Lower_case_count_entgene(extraced_seq):
    lower_count = 0
    total = 0
    for line in extraced_seq:
        for base in line:
            total += 1
            if base.islower():
                lower_count += 1
    percent_lower = lower_count/total
    return percent_lower

def bed_analyzer(bed):
    gene_num = 0
    for line in bed:
        gene_num += 1
        bed_data = line.split()
        single_gene = extract_sequence_from_genome(bed_data[0], int(bed_data[1]), int(bed_data[2]))
        single_gene_clone = single_gene
        Lower_case_count_entgene(single_gene)
        GC_Content_entgene(single_gene_clone)

bed_analyzer(testbed)