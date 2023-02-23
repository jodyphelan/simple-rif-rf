""" read in genotypes from VCF file and predict outcome """
import sys
import os
import argparse
import pickle
import subprocess as sp

# parse command line arguments
parser = argparse.ArgumentParser(description='Predict outcome from VCF file')
parser.add_argument('--vcf', help='VCF file', required=True)
parser.add_argument('--model', help='model file', required=True)
args = parser.parse_args()

# load model
items = pickle.load(open(args.model, "rb"))
clf = items['model']
positions = items['positions']



# extract genotypes
genos = {}
for l in sp.Popen(r"bcftools query -f '%POS[\t%GT\n]' "+ args.vcf,shell=True,stdout=sp.PIPE).stdout:
    row = l.decode().strip().split()
    if row[1]!="0/0":
        genos[int(row[0])] = 1
    else:
        genos[int(row[0])] = 0

# fill in missing genotypes with 0 (ref)
for p in positions:
    if p not in genos:
        genos[p] = 0

genos = [[genos[p] for p in positions]]

# predict outcome
pred = clf.predict(genos)
# write output
sys.stdout.write("drug,prediction\nrifampicin,%s\n" % pred[0])