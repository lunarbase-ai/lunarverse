#!/usr/bin/env python3
"""
Evidence Integration Workflow CLI

This script provides a command-line interface for running the evidence integration workflow
that integrates evidence from CIVIC, PharmGKB, and Gene Enrichment analyses.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import from the novelty_agents package
sys.path.append(str(Path(__file__).parent.parent))

from cee_dart.agents.evidence_integration.workflow_runner import NoveltyWorkflowRunner, ValidationError

def main():
    """Main entry point for the evidence integration workflow."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py <config.json>")
        print("  python main.py <civic_file> <pharmgkb_file> <gene_enrichment_file> <context> <question>")
        print("\nExample:")
        print("  python main.py evidence_integration_config.json")
        return
    
    runner = NoveltyWorkflowRunner(debug=True)
    
    try:
        if len(sys.argv) == 2:
            # Run from config file
            config_file = sys.argv[1]
            print(f"Running evidence integration from config file: {config_file}")
            
            result = runner.run_from_json_file(config_file)
            
            print(f"EVIDENCE INTEGRATION WORKFLOW COMPLETED SUCCESSFULLY!")
            print(f"Final status: {result.final_status.value}")
            print(f"Total iterations: {result.total_iterations}")
            print(f"Evidence sources: CIVIC({result.consolidated_evidence.total_genes_civic}), "
                  f"PharmGKB({result.consolidated_evidence.total_genes_pharmgkb}), "
                  f"Gene sets({result.consolidated_evidence.total_gene_sets_enrichment})")
            
            # Display final report sections
            print(f"\nFinal Unified Report:")
            print(f"- Potential Novel Biomarkers: {len(result.unified_report.potential_novel_biomarkers)} chars")
            print(f"- Implications: {len(result.unified_report.implications)} chars")
            print(f"- Well-Known Interactions: {len(result.unified_report.well_known_interactions)} chars")
            print(f"- Conclusions: {len(result.unified_report.conclusions)} chars")
            
        elif len(sys.argv) == 6:
            # Run with individual arguments
            civic_file, pharmgkb_file, gene_enrichment_file, context, question = sys.argv[1:6]
            
            print(f"Running evidence integration with individual files:")
            print(f"CIVIC: {civic_file}")
            print(f"PharmGKB: {pharmgkb_file}")
            print(f"Gene Enrichment: {gene_enrichment_file}")
            print(f"Context: {context[:100]}...")
            print(f"Question: {question}")
            
            result = runner.run_from_files(
                civic_file=civic_file,
                pharmgkb_file=pharmgkb_file,
                gene_enrichment_file=gene_enrichment_file,
                context=context,
                question=question
            )
            
            print(f"EVIDENCE INTEGRATION WORKFLOW COMPLETED SUCCESSFULLY!")
            print(f"Final status: {result.final_status.value}")
            print(f"Total iterations: {result.total_iterations}")
            
        else:
            print("Invalid number of arguments. See usage above.")
            return
            
    except (ValidationError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
