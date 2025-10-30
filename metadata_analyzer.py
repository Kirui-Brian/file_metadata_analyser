#!/usr/bin/env python3
"""
File Metadata Analyzer - Main CLI Application
A comprehensive tool for extracting, analyzing, and managing file metadata.

Author: MST 8407 Course Project
Date: November 2025
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.extractor import MetadataExtractor
from core.analyzer import MetadataAnalyzer
from core.reporter import MetadataReporter
from utils.file_handler import FileHandler
from utils.gps_mapper import GPSMapper
from utils.sanitizer import MetadataSanitizer

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False
    # Define dummy color constants
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


def print_header():
    """Print application header."""
    header = f"""
{'='*80}
    FILE METADATA ANALYZER - Digital Forensics Tool
    MST 8407 Forensic Data Acquisition and Analysis
{'='*80}
"""
    if COLOR_AVAILABLE:
        print(Fore.CYAN + Style.BRIGHT + header)
    else:
        print(header)


def print_success(message):
    """Print success message."""
    if COLOR_AVAILABLE:
        print(Fore.GREEN + "✓ " + message)
    else:
        print(f"[SUCCESS] {message}")


def print_error(message):
    """Print error message."""
    if COLOR_AVAILABLE:
        print(Fore.RED + "✗ " + message)
    else:
        print(f"[ERROR] {message}")


def print_warning(message):
    """Print warning message."""
    if COLOR_AVAILABLE:
        print(Fore.YELLOW + "⚠ " + message)
    else:
        print(f"[WARNING] {message}")


def print_info(message):
    """Print info message."""
    if COLOR_AVAILABLE:
        print(Fore.BLUE + "ℹ " + message)
    else:
        print(f"[INFO] {message}")


def analyze_single_file(args):
    """Analyze a single file."""
    print_header()
    print_info(f"Analyzing file: {args.file}")
    print()
    
    try:
        # Extract metadata
        print_info("Extracting metadata...")
        extractor = MetadataExtractor(args.file)
        metadata = extractor.extract_all()
        print_success("Metadata extraction complete")
        print()
        
        # Analyze metadata if requested
        analysis = None
        if args.analyze or args.report:
            print_info("Analyzing metadata for anomalies and privacy concerns...")
            analyzer = MetadataAnalyzer(metadata)
            analysis = analyzer.analyze()
            print_success(f"Analysis complete - Risk Level: {analysis.get('risk_level', 'N/A')}")
            print()
        
        # Generate report
        reporter = MetadataReporter(metadata, analysis)
        
        if args.report == 'json':
            output_path = args.output or f"metadata_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            reporter.generate_json_report(output_path)
            print_success(f"JSON report saved: {output_path}")
        
        elif args.report == 'csv':
            output_path = args.output or f"metadata_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            reporter.generate_csv_report(output_path)
            print_success(f"CSV report saved: {output_path}")
        
        else:  # text or default
            if args.output:
                reporter.generate_text_report(args.output)
                print_success(f"Text report saved: {args.output}")
            else:
                # Print to console
                report = reporter.generate_text_report()
                print(report)
        
        # Generate GPS map if requested
        if args.map and metadata.get('gps_data'):
            gps_data = metadata['gps_data']
            if 'latitude_decimal' in gps_data:
                mapper = GPSMapper()
                map_path = args.output or f"gps_map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                if map_path.endswith('.txt') or map_path.endswith('.json') or map_path.endswith('.csv'):
                    map_path = map_path.rsplit('.', 1)[0] + '_map.html'
                else:
                    map_path = map_path + '.html' if not map_path.endswith('.html') else map_path
                
                if mapper.create_map(gps_data, map_path):
                    print_success(f"GPS map generated: {map_path}")
                else:
                    print_error("Failed to generate GPS map")
            else:
                print_warning("No GPS coordinates found in file")
        
        # Display quick summary
        if not args.output and args.report != 'text':
            print()
            print(reporter.generate_summary_report())
        
        return True
    
    except FileNotFoundError as e:
        print_error(str(e))
        return False
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def analyze_directory(args):
    """Analyze all files in a directory."""
    print_header()
    print_info(f"Analyzing directory: {args.directory}")
    print()
    
    try:
        # Find all supported files
        print_info("Scanning for supported files...")
        files = FileHandler.find_files_in_directory(args.directory, recursive=True)
        
        if not files:
            print_warning("No supported files found in directory")
            return False
        
        print_success(f"Found {len(files)} supported file(s)")
        print()
        
        # Analyze each file
        results = []
        for i, file_path in enumerate(files, 1):
            print_info(f"[{i}/{len(files)}] Processing: {Path(file_path).name}")
            
            try:
                extractor = MetadataExtractor(file_path)
                metadata = extractor.extract_all()
                
                if args.analyze:
                    analyzer = MetadataAnalyzer(metadata)
                    analysis = analyzer.analyze()
                    metadata['analysis'] = analysis
                
                results.append(metadata)
                print_success(f"  Completed: {Path(file_path).name}")
            
            except Exception as e:
                print_error(f"  Failed: {str(e)}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()
            
            print()
        
        # Generate combined report
        if results:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = Path(args.output or 'output')
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if args.report == 'json':
                import json
                output_path = output_dir / f"batch_report_{timestamp}.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, default=str)
                print_success(f"Batch JSON report saved: {output_path}")
            
            elif args.report == 'csv':
                import csv
                output_path = output_dir / f"batch_report_{timestamp}.csv"
                # Flatten all results
                flat_results = []
                for result in results:
                    reporter = MetadataReporter(result)
                    flat_data = reporter._flatten_dict(result)
                    flat_results.append(flat_data)
                
                if flat_results:
                    keys = set()
                    for data in flat_results:
                        keys.update(data.keys())
                    
                    with open(output_path, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=sorted(keys))
                        writer.writeheader()
                        writer.writerows(flat_results)
                    print_success(f"Batch CSV report saved: {output_path}")
            
            else:  # text
                output_path = output_dir / f"batch_report_{timestamp}.txt"
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write("BATCH METADATA ANALYSIS REPORT\n")
                    f.write("="*80 + "\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Files: {len(results)}\n")
                    f.write("="*80 + "\n\n")
                    
                    for i, result in enumerate(results, 1):
                        reporter = MetadataReporter(result, result.get('analysis'))
                        f.write(f"\n{'='*80}\n")
                        f.write(f"FILE {i} of {len(results)}\n")
                        f.write(f"{'='*80}\n")
                        f.write(reporter.generate_text_report())
                        f.write("\n\n")
                
                print_success(f"Batch text report saved: {output_path}")
        
        return True
    
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def erase_metadata(args):
    """Erase metadata from a file."""
    print_header()
    print_info(f"Sanitizing file: {args.file}")
    print()
    
    try:
        sanitizer = MetadataSanitizer()
        
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            file_path = Path(args.file)
            output_path = str(file_path.parent / f"{file_path.stem}_cleaned{file_path.suffix}")
        
        # Sanitize file
        if sanitizer.sanitize_file(args.file, output_path):
            print_success("Metadata sanitization complete")
            
            # Generate report
            report = MetadataSanitizer.create_sanitization_report(args.file, output_path)
            print(report)
            
            return True
        else:
            print_error("Metadata sanitization failed")
            return False
    
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='File Metadata Analyzer - Extract and analyze file metadata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single image
  python metadata_analyzer.py --file photo.jpg
  
  # Analyze with detailed forensic analysis
  python metadata_analyzer.py --file document.pdf --analyze --report text
  
  # Generate JSON report
  python metadata_analyzer.py --file image.jpg --report json --output report.json
  
  # Create GPS map from image
  python metadata_analyzer.py --file photo.jpg --map
  
  # Analyze all files in a directory
  python metadata_analyzer.py --directory ./samples --analyze --report json
  
  # Remove metadata from a file
  python metadata_analyzer.py --file photo.jpg --erase --output cleaned.jpg
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Path to file to analyze')
    input_group.add_argument('--directory', '-d', help='Path to directory to analyze')
    
    # Operation options
    parser.add_argument('--analyze', '-a', action='store_true',
                       help='Perform deep analysis for anomalies and privacy concerns')
    parser.add_argument('--erase', '-e', action='store_true',
                       help='Remove metadata from the file')
    parser.add_argument('--map', '-m', action='store_true',
                       help='Generate GPS map for images with location data')
    
    # Output options
    parser.add_argument('--report', '-r', choices=['text', 'json', 'csv'],
                       default='text', help='Report format (default: text)')
    parser.add_argument('--output', '-o', help='Output file/directory path')
    
    # Other options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.erase and args.directory:
        print_error("Cannot use --erase with --directory. Use --file instead.")
        return 1
    
    if args.map and args.directory:
        print_warning("--map option is ignored when processing directories")
    
    # Execute appropriate function
    try:
        if args.erase:
            success = erase_metadata(args)
        elif args.directory:
            success = analyze_directory(args)
        else:
            success = analyze_single_file(args)
        
        return 0 if success else 1
    
    except KeyboardInterrupt:
        print()
        print_warning("Operation cancelled by user")
        return 130
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
