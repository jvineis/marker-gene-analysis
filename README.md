# marker-gene-analysis
The baby scripts and steps used to filter reads, assign taxonomy, analyze phylogeny, and visualize: nrfA, nirS, dsrB

### Gather reference sequences from [fungene](http://fungene.cme.msu.edu/) for nirS, nrfA(—Allana Welsh), and dsrB by manually selecting sequences.  Its freakin painful, but its the only way until I figure out something better through biomartr.  I collected 8774 sequences for nirS, 9585 for nrfA, and 1292 for dsrB (obtained from pelikan et al).  

### parse out the genus name from the resulting fasta files donig something like this

    grep ">" nirS-fungene.fa | cut -f 2 -d "," | cut -f 2 -d "=" | cut -f 1 -d " " | sort | uniq > genus_names.txt

### You will also need to make a file called fungene_ids.txt like this from the file that you downladed from fungene and renamed "nrfA-fungene.fa" (at least in this example).

    grep ">" nrfA-fungene.fa | sed 's/\>//g' > fungene_ids.txt

### run taxize - an R package to determine the matching taxonomic string for each of your genus_names.txt.  I use ncbi
taxa strings to do this.

    library(taxize)
    d <- c("Alphaproteobacteria","Anabaena","Betaproteobacteria","Candidatus","Gammaproteobacteria","Parcubacteria","Phormidesmis","Pseudomonas","Rhodobacteraceae","Sulfurovum")
    work = tax_name(d, get = c("phylum","class","order","family","genus"), db = "ncbi")
    write.table(work, "~/Dropbox/oxygen_gradient/nrfA-references/raw_taxit.txt")

##### first you have to fix up the "raw_taxit.txt" table

    sed 's/"//g' raw_taxit.txt > fix
    mv fix raw_taxit.txt

### Then use the mu-convert-fungene-ids-to-taxastring.py to create a tax reference for the marker gene that will allow you to identify taxonomic strings.  for nrfA.  I ran this command from the nrfA-reference directory that contained the raw_taxit.txt and fungene_ids.txt files.  But you can modify the paths to run it from where ever you like

    python ~/scripts/mu-convert-fungene-ids-to-taxastring.py ~/Dropbox/oxygen_gradient/nrfA-MED-analysis/sequences-to-decompose-padded-m0.10-A0-M0-d4/NODE-HITS.txt fungene_ids.txt raw_taxit.txt

### Now you must use mu-silva-ids_to_phyloseq.py wich will convert the separate elements for med node hits, fungene ids that contain species information, and taxize taxonomy strings to obtain the correct taxonomy string for each node. Lots of fun!

    python ~/scripts/mu-silva_ids_to_phyloseq.py fungene.tax NODE-HITS.txt NODE-IDs.txt


#### the output of the mu-convert-fungene-ids-to-taxonomy is named fungene.tax.  We use this file to run this script to produce a phyloseq readable object (with a little unix magic).  The name of the file produced is PHYLOSEQ-TAX-OBJECT which we will use in R. to discover amazing evolutionary trends and cool things to test with radical hypotheses.  

### You need to fix the file a bit first.  

    sort PHYLOSEQ-TAX-OBJECT.txt > fix
    mv fix PHYLOSEQ-TAX-OBJECT.txt
    create a copy of the PHYLOSEQ-TAX-OBJECT
    cp PHYLOSEQ-TAX-OBJECT.txt PHYLOSEQ-TAX-OBJECT-CORRECTED.txt

    add the following lines to the top of the PHYLOSEQ-TAX-OBJECT.txt
    A;B;C;D;E;F;G
    
    add the following lines to the top of the file PHYLOSEQ-TAX-OBJECT-CORRECTED.txt
    A;B;C;D;E;F;G
    unassigned_to_node

### I also wrote something to correct for the fact that MED doesn't correct the MATRIX-PERCENT to include the reads removed due to "M" and "V" and any other filters that you might have set.  To reincorportate this information to create a more accurate picture of the percent relative abundance.  On second thought it might not be totally more accurate.  There could be importnat reasons why the nodes/sequences weren't retained like sequencing error or PCR error and stochastic forces that wish to runin you science.  - Mordor

####  Here is the script that works on the MATRIX-COUNT.txt and HTML-OUTPUT/read_distribution.txt files produced by MED - "decompose" - it converts the table to a file (I call mine MATRIX-PERCENT-CORRECTED.txt) and inserts a column[1] that represents the percentage of sequences removed during the MED process.

      mu-correct-med-percents.py --med_count MATRIX-COUNT.txt --read_counts HTML-OUTPUT/read_distribution.txt --out MATRIX-PERCENT-CORRECTED.txt


### Now we can get things going with R - using phyloseq to visualize some barplots.  We can also run some stats.  The inputs here are the mapping files (similar to those produced for the devil (I mean qiime6 or whateves version they call it now)).

    




    
