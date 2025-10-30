#!/usr/bin/env python3
"""
Demo Script for File Metadata Analyzer
Demonstrates the capabilities of the metadata analyzer tool for class presentation.

This script:
1. Analyzes sample files from different categories
2. Demonstrates GPS coordinate extraction
3. Shows metadata sanitization
4. Displays performance metrics
5. Generates comparison reports
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.extractor import MetadataExtractor
from core.analyzer import MetadataAnalyzer
from core.reporter import MetadataReporter
from utils.gps_mapper import GPSMapper
from utils.sanitizer import MetadataSanitizer

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:
    COLOR_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''


def print_section_header(title):
    """Print a section header."""
    border = "="*80
    if COLOR_AVAILABLE:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{border}")
        print(f"{title.center(80)}")
        print(f"{border}{Style.RESET_ALL}\n")
    else:
        print(f"\n{border}")
        print(title.center(80))
        print(f"{border}\n")


def print_subsection(title):
    """Print a subsection header."""
    if COLOR_AVAILABLE:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'─'*80}")
        print(f"▶ {title}")
        print(f"{'─'*80}{Style.RESET_ALL}\n")
    else:
        print(f"\n{'-'*80}")
        print(f">> {title}")
        print(f"{'-'*80}\n")


def print_success(message):
    """Print success message."""
    if COLOR_AVAILABLE:
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    else:
        print(f"[SUCCESS] {message}")


def print_info(message, indent=0):
    """Print info message."""
    spaces = "  " * indent
    if COLOR_AVAILABLE:
        print(f"{spaces}{Fore.BLUE}{message}{Style.RESET_ALL}")
    else:
        print(f"{spaces}{message}")


def print_warning(message):
    """Print warning message."""
    if COLOR_AVAILABLE:
        print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")
    else:
        print(f"[WARNING] {message}")


def print_error(message):
    """Print error message."""
    if COLOR_AVAILABLE:
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")
    else:
        print(f"[ERROR] {message}")


def print_stat(label, value):
    """Print a statistic."""
    if COLOR_AVAILABLE:
        print(f"{Fore.CYAN}  {label:30s}: {Fore.WHITE}{Style.BRIGHT}{value}{Style.RESET_ALL}")
    else:
        print(f"  {label:30s}: {value}")


def demo_intro():
    """Print demo introduction."""
    print_section_header("FILE METADATA ANALYZER - LIVE DEMONSTRATION")
    
    print("""
This demonstration showcases the File Metadata Analyzer tool, which:

1. Extracts comprehensive metadata from multiple file types
2. Analyzes metadata for forensic significance and anomalies
3. Identifies privacy concerns (GPS coordinates, author info, etc.)
4. Demonstrates metadata sanitization capabilities
5. Generates detailed forensic reports

Let's begin the demonstration...
""")
    
    input("Press Enter to continue...")


def demo_extraction(sample_files):
    """Demonstrate metadata extraction."""
    print_section_header("DEMONSTRATION 1: METADATA EXTRACTION")
    
    results = []
    
    for file_path in sample_files:
        if not Path(file_path).exists():
            print_warning(f"Sample file not found: {file_path}")
            continue
        
        print_subsection(f"Extracting Metadata: {Path(file_path).name}")
        
        start_time = time.time()
        
        try:
            # Extract metadata
            extractor = MetadataExtractor(file_path)
            metadata = extractor.extract_all()
            
            extraction_time = time.time() - start_time
            
            # Display key information
            file_info = metadata.get('file_info', {})
            print_stat("File Name", file_info.get('filename', 'N/A'))
            print_stat("File Type", metadata.get('file_type', 'N/A'))
            print_stat("File Size", file_info.get('size_human', 'N/A'))
            print_stat("Extraction Time", f"{extraction_time:.3f} seconds")
            
            # Type-specific information
            if metadata.get('file_type') == 'image':
                img_meta = metadata.get('image_metadata', {})
                if 'error' not in img_meta:
                    print_stat("Image Dimensions", f"{img_meta.get('width', 'N/A')} x {img_meta.get('height', 'N/A')}")
                
                gps_data = metadata.get('gps_data', {})
                if gps_data and 'latitude_decimal' in gps_data:
                    print_warning(f"GPS COORDINATES FOUND: {gps_data['coordinates']}")
                else:
                    print_info("No GPS data found")
            
            elif metadata.get('file_type') == 'document':
                doc_meta = metadata.get('document_metadata', {})
                if 'error' not in doc_meta:
                    author = doc_meta.get('author') or doc_meta.get('creator')
                    if author:
                        print_warning(f"AUTHOR FOUND: {author}")
                    
                    if 'page_count' in doc_meta:
                        print_stat("Page Count", doc_meta['page_count'])
            
            elif metadata.get('file_type') in ['audio', 'video']:
                media_meta = metadata.get('media_metadata', {})
                mutagen_data = media_meta.get('mutagen_data', {})
                if mutagen_data.get('length'):
                    duration = mutagen_data['length']
                    print_stat("Duration", f"{duration:.2f} seconds")
            
            print_success(f"Metadata extraction completed in {extraction_time:.3f}s")
            
            results.append({
                'file': file_path,
                'metadata': metadata,
                'extraction_time': extraction_time
            })
        
        except Exception as e:
            print_error(f"Failed to extract metadata: {str(e)}")
    
    print(f"\n{Fore.GREEN if COLOR_AVAILABLE else ''}Successfully processed {len(results)} file(s)")
    input("\nPress Enter to continue...")
    
    return results


def demo_analysis(results):
    """Demonstrate metadata analysis."""
    print_section_header("DEMONSTRATION 2: FORENSIC ANALYSIS")
    
    analysis_results = []
    
    for result in results:
        file_name = Path(result['file']).name
        metadata = result['metadata']
        
        print_subsection(f"Analyzing: {file_name}")
        
        start_time = time.time()
        
        try:
            # Analyze metadata
            analyzer = MetadataAnalyzer(metadata)
            analysis = analyzer.analyze()
            
            analysis_time = time.time() - start_time
            
            # Display analysis results
            summary = analysis.get('summary', {})
            print_stat("Risk Level", analysis.get('risk_level', 'N/A'))
            print_stat("Anomalies Detected", summary.get('total_anomalies', 0))
            print_stat("Privacy Concerns", summary.get('total_privacy_concerns', 0))
            print_stat("Forensic Indicators", summary.get('total_forensic_indicators', 0))
            print_stat("Analysis Time", f"{analysis_time:.3f} seconds")
            
            # Show specific findings
            anomalies = analysis.get('anomalies', [])
            if anomalies:
                print_info("\nAnomalies Found:", 0)
                for anomaly in anomalies[:3]:  # Show first 3
                    print_info(f"• [{anomaly['severity']}] {anomaly['description']}", 1)
            
            privacy_concerns = analysis.get('privacy_concerns', [])
            if privacy_concerns:
                print_info("\nPrivacy Concerns:", 0)
                for concern in privacy_concerns[:3]:  # Show first 3
                    print_info(f"• [{concern['severity']}] {concern['description']}", 1)
            
            # Get recommendations
            recommendations = analyzer.get_recommendations()
            if recommendations:
                print_info("\nRecommendations:", 0)
                for rec in recommendations[:3]:
                    print_info(f"• {rec}", 1)
            
            print_success(f"Analysis completed in {analysis_time:.3f}s")
            
            analysis_results.append({
                'file': result['file'],
                'metadata': metadata,
                'analysis': analysis,
                'extraction_time': result['extraction_time'],
                'analysis_time': analysis_time
            })
        
        except Exception as e:
            print_error(f"Failed to analyze: {str(e)}")
    
    input("\nPress Enter to continue...")
    
    return analysis_results


def demo_gps_mapping(analysis_results):
    """Demonstrate GPS mapping."""
    print_section_header("DEMONSTRATION 3: GPS COORDINATE MAPPING")
    
    # Find files with GPS data
    files_with_gps = []
    for result in analysis_results:
        gps_data = result['metadata'].get('gps_data', {})
        if gps_data and 'latitude_decimal' in gps_data:
            files_with_gps.append(result)
    
    if not files_with_gps:
        print_warning("No GPS data found in sample files")
        print_info("GPS mapping feature requires images with embedded GPS coordinates")
        input("\nPress Enter to continue...")
        return
    
    print_info(f"Found {len(files_with_gps)} file(s) with GPS coordinates\n")
    
    for result in files_with_gps:
        file_name = Path(result['file']).name
        gps_data = result['metadata']['gps_data']
        
        print_subsection(f"GPS Data from: {file_name}")
        
        print_stat("Latitude", gps_data['latitude_decimal'])
        print_stat("Longitude", gps_data['longitude_decimal'])
        print_stat("Coordinates", gps_data['coordinates'])
        
        if 'altitude_meters' in gps_data:
            print_stat("Altitude", f"{gps_data['altitude_meters']} meters")
        
        # Generate map
        mapper = GPSMapper()
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        map_file = output_dir / f"gps_map_{Path(file_name).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        print_info(f"\nGenerating interactive map...")
        if mapper.create_map(gps_data, str(map_file)):
            print_success(f"Map saved: {map_file}")
            print_info(f"Open this file in a web browser to view the location")
        else:
            print_error("Failed to generate map")
    
    input("\nPress Enter to continue...")


def demo_sanitization(analysis_results):
    """Demonstrate metadata sanitization."""
    print_section_header("DEMONSTRATION 4: METADATA SANITIZATION")
    
    print("""
Metadata sanitization removes sensitive information from files:
- GPS coordinates from images
- Author information from documents
- Device information from media files

This is important for:
- Privacy protection
- Evidence anonymization (when appropriate)
- Anti-forensics awareness
""")
    
    # Select first file for demo
    if not analysis_results:
        print_warning("No files to sanitize")
        return
    
    result = analysis_results[0]
    file_path = result['file']
    file_name = Path(file_path).name
    
    print_subsection(f"Sanitizing: {file_name}")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Determine output path
    output_path = output_dir / f"cleaned_{file_name}"
    
    print_info("Before Sanitization:")
    file_info = result['metadata']['file_info']
    print_stat("Original Size", file_info['size_human'])
    
    # Count metadata items
    has_gps = bool(result['metadata'].get('gps_data') and 'latitude_decimal' in result['metadata']['gps_data'])
    has_exif = bool(result['metadata'].get('exif_data'))
    has_author = bool(result['metadata'].get('document_metadata', {}).get('author'))
    
    print_stat("Has GPS Data", "Yes" if has_gps else "No")
    print_stat("Has EXIF Data", "Yes" if has_exif else "No")
    print_stat("Has Author Info", "Yes" if has_author else "No")
    
    print_info("\nSanitizing metadata...")
    
    try:
        sanitizer = MetadataSanitizer()
        
        start_time = time.time()
        success = sanitizer.sanitize_file(file_path, str(output_path))
        sanitization_time = time.time() - start_time
        
        if success:
            print_success(f"Sanitization completed in {sanitization_time:.3f}s")
            
            # Re-analyze cleaned file
            print_info("\nVerifying sanitization...")
            cleaned_extractor = MetadataExtractor(str(output_path))
            cleaned_metadata = cleaned_extractor.extract_all()
            
            cleaned_file_info = cleaned_metadata['file_info']
            print_stat("Cleaned Size", cleaned_file_info['size_human'])
            
            # Check if metadata was removed
            has_gps_after = bool(cleaned_metadata.get('gps_data') and 'latitude_decimal' in cleaned_metadata.get('gps_data', {}))
            has_exif_after = bool(cleaned_metadata.get('exif_data') and len(cleaned_metadata.get('exif_data', {})) > 1)
            has_author_after = bool(cleaned_metadata.get('document_metadata', {}).get('author'))
            
            print_stat("GPS Data Removed", "Yes" if has_gps and not has_gps_after else "N/A")
            print_stat("EXIF Data Removed", "Yes" if has_exif and not has_exif_after else "N/A")
            print_stat("Author Info Removed", "Yes" if has_author and not has_author_after else "N/A")
            
            print_success(f"\nCleaned file saved: {output_path}")
        else:
            print_error("Sanitization failed")
    
    except Exception as e:
        print_error(f"Error during sanitization: {str(e)}")
    
    input("\nPress Enter to continue...")


def demo_report_generation(analysis_results):
    """Demonstrate report generation."""
    print_section_header("DEMONSTRATION 5: REPORT GENERATION")
    
    if not analysis_results:
        print_warning("No analysis results to report")
        return
    
    result = analysis_results[0]
    file_name = Path(result['file']).name
    
    print_subsection(f"Generating Reports for: {file_name}")
    
    reporter = MetadataReporter(result['metadata'], result['analysis'])
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = Path(result['file']).stem
    
    # Generate JSON report
    print_info("Generating JSON report...")
    json_path = output_dir / f"report_{base_name}_{timestamp}.json"
    reporter.generate_json_report(str(json_path))
    print_success(f"JSON report: {json_path}")
    
    # Generate CSV report
    print_info("Generating CSV report...")
    csv_path = output_dir / f"report_{base_name}_{timestamp}.csv"
    reporter.generate_csv_report(str(csv_path))
    print_success(f"CSV report: {csv_path}")
    
    # Generate text report
    print_info("Generating text report...")
    text_path = output_dir / f"report_{base_name}_{timestamp}.txt"
    reporter.generate_text_report(str(text_path))
    print_success(f"Text report: {text_path}")
    
    print_info("\nSample Text Report Preview:")
    print("─" * 80)
    summary = reporter.generate_summary_report()
    print(summary)
    print("─" * 80)
    
    input("\nPress Enter to continue...")


def demo_performance_summary(analysis_results):
    """Show performance summary."""
    print_section_header("DEMONSTRATION 6: PERFORMANCE METRICS")
    
    if not analysis_results:
        print_warning("No results to summarize")
        return
    
    # Calculate statistics
    total_files = len(analysis_results)
    total_extraction_time = sum(r['extraction_time'] for r in analysis_results)
    total_analysis_time = sum(r['analysis_time'] for r in analysis_results)
    total_time = total_extraction_time + total_analysis_time
    
    avg_extraction = total_extraction_time / total_files if total_files > 0 else 0
    avg_analysis = total_analysis_time / total_files if total_files > 0 else 0
    
    # Count findings
    total_anomalies = sum(r['analysis']['summary']['total_anomalies'] for r in analysis_results)
    total_privacy = sum(r['analysis']['summary']['total_privacy_concerns'] for r in analysis_results)
    total_indicators = sum(r['analysis']['summary']['total_forensic_indicators'] for r in analysis_results)
    
    files_with_gps = sum(1 for r in analysis_results if r['analysis']['summary'].get('has_gps'))
    files_with_author = sum(1 for r in analysis_results if r['analysis']['summary'].get('has_author_info'))
    
    print_subsection("Processing Statistics")
    print_stat("Total Files Processed", total_files)
    print_stat("Total Processing Time", f"{total_time:.3f} seconds")
    print_stat("Avg Extraction Time", f"{avg_extraction:.3f} seconds/file")
    print_stat("Avg Analysis Time", f"{avg_analysis:.3f} seconds/file")
    
    print_subsection("Findings Summary")
    print_stat("Total Anomalies", total_anomalies)
    print_stat("Total Privacy Concerns", total_privacy)
    print_stat("Total Forensic Indicators", total_indicators)
    print_stat("Files with GPS Data", f"{files_with_gps}/{total_files}")
    print_stat("Files with Author Info", f"{files_with_author}/{total_files}")
    
    print_subsection("File Type Distribution")
    type_counts = {}
    for r in analysis_results:
        file_type = r['metadata'].get('file_type', 'unknown')
        type_counts[file_type] = type_counts.get(file_type, 0) + 1
    
    for file_type, count in type_counts.items():
        print_stat(file_type.title(), count)
    
    input("\nPress Enter to continue...")


def demo_conclusion():
    """Print demo conclusion."""
    print_section_header("DEMONSTRATION COMPLETE")
    
    print("""
The File Metadata Analyzer has demonstrated:

✓ Comprehensive metadata extraction from multiple file formats
✓ Forensic analysis identifying anomalies and privacy concerns
✓ GPS coordinate extraction and mapping capabilities
✓ Metadata sanitization for privacy protection
✓ Multiple report format generation (JSON, CSV, Text)
✓ Performance metrics and batch processing

FORENSIC SIGNIFICANCE:
• Metadata provides crucial evidence in digital investigations
• Timestamps can establish timelines of events
• GPS coordinates can verify locations
• Author information can attribute document creation
• Anomalies may indicate tampering or anti-forensic activities

PRIVACY IMPLICATIONS:
• Files often contain more information than users realize
• GPS coordinates in photos can reveal sensitive locations
• Document metadata can expose organizational information
• Metadata sanitization is important before sharing files

ETHICAL CONSIDERATIONS:
• Tools can be used for legitimate investigations
• Always obtain proper authorization
• Consider privacy implications
• Document chain of custody
• Follow legal and ethical guidelines

Thank you for attending this demonstration!
""")
    
    print_info("All reports and maps have been saved to the 'output' directory")
    print_info("You can review the generated files for your presentation\n")


def main():
    """Main demo execution."""
    # Sample files to analyze (create these or use existing ones)
    sample_files = [
        "samples/image.jpg",
        "samples/document.pdf",
        "samples/audio.mp3",
        "samples/photo.jpg"
    ]
    
    # Check for sample directory
    samples_dir = Path("samples")
    if not samples_dir.exists():
        print_warning("Sample directory not found. Creating...")
        samples_dir.mkdir(exist_ok=True)
        print_info(f"Please add sample files to: {samples_dir.absolute()}")
        print_info("Supported formats: JPG, PNG, PDF, DOCX, MP3, MP4, etc.")
        return
    
    # Find existing sample files
    existing_samples = list(samples_dir.glob("*"))
    existing_samples = [str(f) for f in existing_samples if f.is_file()]
    
    if not existing_samples:
        print_warning("No sample files found in samples directory")
        print_info("Please add sample files for demonstration")
        return
    
    sample_files = existing_samples[:5]  # Use up to 5 samples
    
    try:
        # Run demonstration
        demo_intro()
        
        results = demo_extraction(sample_files)
        
        if results:
            analysis_results = demo_analysis(results)
            demo_gps_mapping(analysis_results)
            demo_sanitization(analysis_results)
            demo_report_generation(analysis_results)
            demo_performance_summary(analysis_results)
        
        demo_conclusion()
    
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        return 1
    except Exception as e:
        print_error(f"Demo error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
