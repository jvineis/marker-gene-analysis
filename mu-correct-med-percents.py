#!/usr/bin/env python
import sys
import argparse

parser = argparse.ArgumentParser(description='''The purpose of this script is to correct the MATRIX-PERCENT.txt produced by MED. MED reports the percent relative abundance only for reads that were assigned to a NODE. his is OK if the sequences that were left behind are sequences that represent noise in the data caused by sequencing error etc.  However, in hyperdiverse environments, the sequences not assigned to a MED node can be significant and represent real taxa.  So I made this script to calculate the percent relative abundance of a node from the total quality filtered read counts''')
parser.add_argument('--med_count', help = 'The count table produced by decompose (MED)')
parser.add_argument('--read_counts', help = 'The total number of quality filtered reads for each sample.  The table is produced by MED and found in the HTML-OUTPUT directory. - read_distribution.txt.')
parser.add_argument('--out', help= 'The file to write the corrected table data')
args = parser.parse_args()

#Read in the inputs 

med = open(args.med_count, 'rU')
reads = open(args.read_counts, 'rU')
outfile = open(args.out, 'w')

l = [20,10,18,35,44]
std_num = 200
def trans(l_of_nums, std_num):
    trans_list = []
    trans_ints = []
    all_values_list = []
    for i in l_of_nums:
        trans_list.append(str(float(i)/float(std_num)*100))
        trans_ints.append(float(i)/float(std_num)*100)
        x =  str(100.0 - sum([float(k) for k in trans_ints]))
    all_values_list.append(x)
    for i in trans_list:
        all_values_list.append(i)
    return all_values_list
        
        
    
    print x
#    print sum([float(k) for k in trans_ints])
    print trans_list
    return trans_list


med_dict = {}
for line in med:
    x = line.strip().split('\t')
    med_dict[x[0]] = x[1:len(x)]

reads_dict = {}
with reads as x:
    firstline = x.readline()
    for line in reads:
        x = line.strip().split('\t')
        reads_dict[x[0]] = float(x[1])+float(x[2])+float(x[3])

outfile.write("samples"+'\t'+"unassigned_to_node"+'\t')
for i in med_dict["samples"]:
    outfile.write("%s\t" % i +'\t')
outfile.write('\n')

for key in reads_dict.keys():
    if key in med_dict.keys():
        x = trans(med_dict[key],reads_dict[key])
        outfile.write(key+'\t'+"\t".join(x)+'\t'+'\n')
#        print(trans(med_dict[key],reads_dict[key]))

