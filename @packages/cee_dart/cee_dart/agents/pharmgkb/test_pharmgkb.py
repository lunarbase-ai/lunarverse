#!/usr/bin/env python3
"""
Test script for PharmGKB agents with sample data.
"""

import sys
import os
# Add the parent directory to the path so we can import the pharmGKB_agents module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cee_dart.agents.pharmgkb.workflow_runner import WorkflowRunner

def test_pharmgkb_workflow():
    """Test the pharmGKB workflow with sample data."""
    
    # Sample pharmGKB data in the expected format
    sample_data = {
        'Context': 'Clinical pharmacogenomics study investigating drug response variations',
        'Prompt': 'What are the pharmacogenomic implications of the identified genes for drug therapy?',
        'pharmGKB Analysis': {
            'BCL2': [
                {
                    'Drug(s)': 'carboplatin, docetaxel, paclitaxel',
                    'Sentence': 'Genotype CC is not associated with overall or progression-free survival when treated with carboplatin, docetaxel and paclitaxel in women with Ovarian Neoplasms as compared to genotypes CT + TT.',
                    'Notes': 'No association was seen between SNP and overall or progression-free survival. Please note alleles have been complemented to the plus chromosomal strand.',
                    'PMID': 23963862
                },
                {
                    'Drug(s)': 'interferons, ribavirin',
                    'Sentence': 'Allele T is associated with increased frequency (about double) in non-responder patients compared with responder patients (HCV genotype 4) when treated with interferons and ribavirin in people with Hepatitis C, Chronic as compared to allele C.',
                    'Notes': 'The BCL-2 gene polymorphism at codon 43 (rs1800477 C/T) is a new biological marker to potentially identify responders and non-responders of HCV genotype 4 patients to achieving a sustained virological response to treatment with IFN in combination with ribavirin.',
                    'PMID': 21159314
                }
            ],
            'ESR1': [
                {
                    'Drug(s)': 'tamoxifen',
                    'Sentence': 'Genotype GG is associated with decreased in total cholesterol in postmenopausal woman and increase in triglycerides and decrease in high density lipoprotein in premenopausal women when treated with tamoxifen as compared to genotypes AA + AG.',
                    'Notes': 'The decrease in total cholesterol in postmenopausal woman (P=0.03; GG vs GA/AA) and tamoxifen-induced increase in triglycerides (P=0.002; gene-dose effect) and decrease in high density lipoprotein (P=0.004; gene-dose effect) in premenopausal women.',
                    'PMID': 17713466
                }
            ]
        }
    }
    
    print("Testing PharmGKB Workflow...")
    print("=" * 50)
    
    try:
        # Create workflow runner
        runner = WorkflowRunner(debug=True)
        
        # Run the workflow
        results, consolidated_data = runner.run_from_app_data(sample_data)
        
        print(f"\nWorkflow completed successfully!")
        print(f"Processed {len(results)} genes")
        
        for i, result in enumerate(results, 1):
            gene_name = runner._extract_gene_name_from_evidence(result.user_input.evidence, i)
            print(f"\nGene {i}: {gene_name}")
            print(f"Status: {result.final_status.value}")
            print(f"Iterations: {result.total_iterations}")
            print(f"Final Analysis Preview: {result.final_analysis[:200]}...")
        
        print(f"\nConsolidated data generated with {len(consolidated_data.get('gene_analyses', {}))} gene analyses")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pharmgkb_workflow() 