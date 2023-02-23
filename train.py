from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import pickle
import subprocess as sp
from collections import defaultdict

genos = defaultdict(dict)

# get genotypes for all samples at all positions in the vcf
for l in sp.Popen(r"bcftools query -f '[%POS\t%SAMPLE\t%GT\n]' snps.vcf.gz",shell=True,stdout=sp.PIPE).stdout:
    # l is a byte string, so we need to decode it to a string and strip the newline character at the end
    pos,sample,gt = l.decode().strip().split()
    # convert the position to an integer
    pos = int(pos)
    # if the genotype is missing or reference, set it to 0 (otherwise set it to 1)
    if gt=="./." or gt=="0/0":
        gt = 0
    else:
        gt = 1
    # add the genotype to the dictionary
    genos[sample][pos] = gt




# get the phenotype for each sample
pheno = {}
for l in open("pheno.txt"):
    row = l.strip().split()
    pheno[row[0]] = int(row[1])

# convert the genotype dictionary to a list of lists
X = [list(genos[s].values()) for s in pheno] 
y = [pheno[s] for s in pheno]
# use scikit-learn to train a random forest classifier
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)

# dump the model and the positions to a pickle file
positions = list(list(genos.values())[0])
pickle.dump({"model":clf,"positions":positions}, open("model.pkl","wb"))