import pandas as pd
import random
data = pd.read_table("smallData.txt", index_col=0, header=0)

genes = list(data.index)


def writeSigned(name, fout, genes):
    genes = random.sample(genes, 100);
    genes_pos = genes[:50]
    genes_neg = genes[50:]

    genes_pos.append("UnmatchedGene1")
    genes_neg.append("UnmatchedGene2")

    for g in genes_pos:
        fout.write("\t".join([name, 'plus', g]) + "\n")

    for g in genes_pos:
        fout.write("\t".join([name, 'plus', g]) + "\n")


def writeBoth(name, fout, genes):
    genes = random.sample(genes, 100);

    genes.append("UnmatchedGene1")
    genes.append("UnmatchedGene2")

    for g in genes:
        fout.write("\t".join([name, 'both', g]) + "\n")

def writeUnsigned(name, fout, genes):
    genes = random.sample(genes, 100);

    genes.append("UnmatchedGene1")
    genes.append("UnmatchedGene2")

    for g in genes:
        fout.write("\t".join([name, g]) + "\n")


def writeGMT(name, fout, genes):
    genes = random.sample(genes, 100);

    genes.append("UnmatchedGene1")
    genes.append("UnmatchedGene2")

    row = [name, "Description"] + genes

    fout.write("\t".join(row) + "\n")

def writeGMTSigned(name, fout, genes):
    genes = random.sample(genes, 100);
    genes_pos = genes[:50]
    genes_neg = genes[50:]

    genes_pos.append("UnmatchedGene1")
    genes_neg.append("UnmatchedGene2")

    row_pos = [name+"_plus", "Description"] + genes_pos;
    row_neg = [name+"_minus", "Description"] + genes_neg;

    fout.write("\t".join(row_pos) + "\n")
    fout.write("\t".join(row_neg) + "\n")


fout = open("sigsA.txt", 'w');
for x in range(10):
    writeSigned("Signed"+str(x+1), fout, genes)

for x in range(5):
    writeBoth("Both"+str(x+1), fout, genes)
fout.close();

fout = open("sigsB.txt", 'w');
for x in range(10):
    writeUnsigned("Unsigned"+str(x+1), fout, genes)

fout.close();

fout = open("sigsSmall.gmt", 'w');
for x in range(10):
    writeGMT("GMTUnsigned"+str(x+1), fout, genes)

for x in range(10):
    writeGMTSigned("GMTSigned"+str(x+1), fout, genes)

fout.close();
