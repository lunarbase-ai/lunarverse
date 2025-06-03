import pandas as pd
from pathlib import Path
import os

# Load the CSV file into a DataFrame
file_path = r'C:\Users\owysocky\Documents\GitHub\CCE_scGeneRAI\resources\pharmgkb'  # Replace with your CSV file path

study_parameters_name = 'study_parameters.tsv'
var_drug_ann_name = 'var_drug_ann.tsv'
var_fa_ann_name = 'var_fa_ann.tsv'
var_pheno_ann_name = 'var_pheno_ann.tsv'
# Join file paths with the directory
study_parameters_path = os.path.join(file_path, study_parameters_name)
var_drug_ann_path = os.path.join(file_path, var_drug_ann_name)
var_fa_ann_path = os.path.join(file_path, var_fa_ann_name)
var_pheno_ann_path = os.path.join(file_path, var_pheno_ann_name)

# Load all files to separate DataFrames
study_parameters = pd.read_csv(study_parameters_path, sep='\t')
var_drug_ann = pd.read_csv(var_drug_ann_path, sep='\t')
var_fa_ann = pd.read_csv(var_fa_ann_path, sep='\t')
var_pheno_ann = pd.read_csv(var_pheno_ann_path, sep='\t')


var_pheno_ann = var_pheno_ann[['Gene', 'Drug(s)','Sentence','Notes','PMID']]
var_drug_ann = var_drug_ann[['Gene', 'Drug(s)','Sentence','Notes','PMID']]
var_fa_ann = var_fa_ann[['Gene', 'Drug(s)','Sentence','Notes','PMID']]

var_pheno_ann.to_csv('var_pheno_ann_simple.csv', index=False)
var_drug_ann.to_csv('var_drug_ann_simple.csv', index=False)
var_fa_ann.to_csv('var_fa_ann_simple.csv', index=False)



