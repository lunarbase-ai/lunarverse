#!/usr/bin/env python3
"""
Main CLI interface for the PharmGKB Drug Interaction and Pharmacogenomics Interpretation Workflow System.
"""

import argparse
from rich.console import Console
from cee_dart.agents.pharmgkb.workflow_runner import WorkflowRunner


def main():
    """Main CLI entry point."""
    console = Console()

    parser = argparse.ArgumentParser(
        description="PharmGKB Drug Interaction and Pharmacogenomics Interpretation Workflow System"
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
            # Auto-generate consolidated file if multiple genes processed and no explicit paths given
            console.print("[blue]📊 Multiple genes analyzed, creating consolidated output[/blue]")
            
    except KeyboardInterrupt:
        console.print("\nOperation cancelled.")
    except Exception as e:
        console.print(f"Error: {e}", style="bold red")


if __name__ == "__main__":
    main()
