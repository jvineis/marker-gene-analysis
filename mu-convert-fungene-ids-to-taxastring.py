#!/usr/bin/env python

import sys
import re
## This script is designed to take a list of node hits that were obtained from a vsearch of fungene dna or protein seqs
## and convert the names to the taxonomic string associated with the assigned species id in the header.  Here are the steps to 
## generate the necessary infiles.
##
#   1. Run vsearch on the MED output NODE-REPRESENTATIVES.fasta ( note , you need to remove the "-" pads on the seqs prior to vsearch
#    vsearch --usearch_global NODE-REPRESENTATIVES.fa --db ~/Dropbox/oxygen_gradient/dsrB-references/dsrB-nuclotide.fa --blast6out NODE-HITS.txt --id 0.6
#
#   2.  Return the NODE-HITS using the following unix commands
#    cut -f 1 -d "|" NODE-HITS.txt > NODE-HITS-1.txt
#    cut -f 2 NODE-HITS.txt > NODE-HITS-2.txt
#    paste NODE-HITS-1.txt NODE-HITS-2.txt > NODE-HITS-1-2.txt
#    rm NODE-HITS-1.txt
#    rm NODE-HITS-2.txt
#    mv NODE-HITS-1-2.txt NODE-HITS.txt 
#    
#    file looks like this
#     NODE-ID    fungene-id    
#     000008777    CP007518
#     000008635    LZFM01000013
#     000001533    CP000142
#     000002489    AKFT01000013
#

#
#   3.  Use taxize (an R library) to determine the string of taxonomy associated with each species in the header
#    Here is an example to use taxize in R. The variable "d" (below) was generated using unix and text editing to return
#    just the genus name.
#
#    library("taxize")
#    d <- c("Acetonema","Acidobacteria","Actinobacillus","Actinomyces")
#    work = tax_name(d, get = c("phylum","class","order","family","genus"), db = "ncbi")
#    write.table(work, "~/Dropbox/oxygen_gradient/nrfA-references/raw_taxit.txt")
#
#    needed to fix the table a bit
#    sed 's/"//g' raw_taxit.txt | sed 's/ / /g' > fix
#    mv fix raw_taxit.txt    
#
#
#   4. Now we come to the utility of this baby script.  we need to create a table where the file contains the following fields
#
#     node Domain Phylum Class Order Family Genus Species
#    
#. %^ * ~ ~ . %^ * ~ ~ . LETS GET DOWN TO BUSINESS AND MAKE THIS HAPPEN . %^ * ~ ~ . %^ * ~ ~ .

# Read in the node hits
node_hits = open(sys.argv[1], 'rU')
# Read in the fungene reference file - headers for each of the fungene reference headers.  It was created like this
# grep ">" nrfA-fungene.fa | sed 's/\>//g' > fungene_ids.txt
node_refs = open(sys.argv[2], 'rU')
# Read in the taxize table
taxa = open(sys.argv[3], 'rU')

hits_dict = {}
for node in node_hits:
    x = node.strip().split('\t')
    hits_dict[x[0]] = x[1]

taxa_dict = {}
for id in taxa:
    x = id.strip().split(' ')

    #genus is the key
    taxa_dict[x[2]] = x[2],x[3],x[4],x[5],x[6] 
for key in taxa_dict.keys():
    print taxa_dict[key][1]

refs_dict = {}
for ref in node_refs:
    x = ref.strip()
    x = re.split(',| |=', x)
    refs_dict[x[0]] = x[5],x[6]

hits_refs_dict = {}
for key in hits_dict.keys():
    hits_refs_dict[key] = hits_dict[key], refs_dict[hits_dict[key]][0], refs_dict[hits_dict[key]][1]


output = open('fungene.tax', 'w')
#output.write('node'+";"+'Phylum'+";"+'Class'+";"+'Order'+";"+'Family'+";"+'Genus'+";"+'Species'+";"+"\n")


for key in hits_refs_dict.keys():
    print hits_refs_dict[key], key
    if hits_refs_dict[key][1] in taxa_dict.keys():
       # output.write(key+';'+taxa_dict[hits_refs_dict[key][1]][0]+';'+taxa_dict[hits_refs_dict[key][1]][1]+';'+taxa_dict[hits_refs_dict[key][1]][2]+';'+taxa_dict[hits_refs_dict[key][1]][3]+';'+taxa_dict[hits_refs_dict[key][1]][4]+';'+hits_refs_dict[key][2]+'\n')
        output.write(hits_refs_dict[key][0]+'\t'+taxa_dict[hits_refs_dict[key][1]][1]+';'+taxa_dict[hits_refs_dict[key][1]][2]+';'+taxa_dict[hits_refs_dict[key][1]][3]+';'+taxa_dict[hits_refs_dict[key][1]][4]+';'+taxa_dict[hits_refs_dict[key][1]][0]+';'+hits_refs_dict[key][2]+'\n')
    else:
        output.write(hits_refs_dict[key][0]+'\t'+"unknown"+';'+"unknown"+';'+"unknown"+';'+"unknown"+';'+"unknown"+';'+"unknown"+'\n')
