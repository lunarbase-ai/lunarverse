#!/usr/bin/env python3
"""
Main CLI interface for the Gene Enrichment Pathway and Biological Process Interpretation Workflow System.
"""

import argparse
import sys
import os
from rich.console import Console

# Add the current directory to Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Handle imports for both module and direct execution
try:
    from .workflow_runner import WorkflowRunner, ValidationError
except ImportError:
    # Fallback for direct execution
    from workflow_runner import WorkflowRunner, ValidationError


def main():
    """Main CLI entry point."""
    console = Console()

    parser = argparse.ArgumentParser(
        description="Gene Enrichment Pathway and Biological Process Interpretation Workflow System"
    )
    parser.add_argument("--input", "-f", type=str,
                        help="Path to JSON input file", required=True)
    parser.add_argument("--output", "-o", type=str,
                        help="Path to save output JSON file")
    parser.add_argument("--consolidated", "-c", type=str,
                        help="Path to save consolidated final analysis JSON file")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")

    args = parser.parse_args()

    try:
        runner = WorkflowRunner(debug=args.debug)
        if args.debug:
            console.print("Debug mode enabled")
            
        results = runner.run_from_json_file(args.input)
        
        if args.output or args.consolidated:
            runner.save_results_to_files(
                results, 
                output_path=args.output,
                consolidated_path=args.consolidated
            )
        elif len(results) > 1:
            # Auto-generate consolidated file if multiple gene sets processed and no explicit paths given
            console.print("[blue]📊 Multiple gene sets analyzed, creating consolidated output[/blue]")
            
    except KeyboardInterrupt:
        console.print("\nOperation cancelled.")
    except ValidationError as e:
        console.print(f"❌ Validation Error: {e}", style="bold red")
        console.print("\n💡 Please ensure your JSON file contains valid 'Context' and 'Question' fields.", style="yellow")
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")


if __name__ == "__main__":
    main()
