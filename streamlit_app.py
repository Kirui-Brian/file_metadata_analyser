#!/usr/bin/env python3
"""
File Metadata Analyzer - Streamlit Web Interface
A user-friendly web GUI for metadata extraction, analysis, and visualization.

Author: Kirui Brian
Date: November 2025
"""

import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime
import tempfile
import os

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.extractor import MetadataExtractor
from core.analyzer import MetadataAnalyzer
from core.reporter import MetadataReporter
from utils.gps_mapper import GPSMapper
from utils.sanitizer import MetadataSanitizer
from utils.file_handler import FileHandler

# Configure page
st.set_page_config(
    page_title="File Metadata Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">🔍 File Metadata Analyzer</div>', unsafe_allow_html=True)
    st.markdown("**Digital Forensics Tool** | MST 8407 Course Project")
    
    # Sidebar
    st.sidebar.title("⚙️ Options")
    
    # Mode selection
    mode = st.sidebar.radio(
        "Select Mode:",
        ["📤 Upload & Analyze", "🧹 Metadata Sanitization", "📚 About"],
        index=0
    )
    
    if mode == "📤 Upload & Analyze":
        analyze_mode()
    elif mode == "🧹 Metadata Sanitization":
        sanitize_mode()
    else:
        about_mode()


def analyze_mode():
    """File upload and analysis mode."""
    
    st.header("📤 Upload & Analyze Files")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose file(s) to analyze",
        type=['jpg', 'jpeg', 'png', 'pdf', 'docx', 'xlsx', 'pptx', 'mp3', 'mp4', 'wav', 'avi'],
        accept_multiple_files=True,
        help="Upload images, documents, or media files for metadata analysis"
    )
    
    # Analysis options
    with st.expander("🔧 Analysis Options", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            perform_analysis = st.checkbox("Perform Forensic Analysis", value=True, 
                                         help="Analyze for anomalies and privacy concerns")
            show_exif = st.checkbox("Show EXIF Data", value=True,
                                   help="Display detailed EXIF metadata for images")
        with col2:
            generate_map = st.checkbox("Generate GPS Map", value=True,
                                      help="Create interactive map if GPS data exists")
            show_hashes = st.checkbox("Show File Hashes", value=True,
                                     help="Display MD5 and SHA-256 hashes")
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
        
        # Analyze button
        if st.button("🔍 Analyze Files", type="primary", use_container_width=True):
            analyze_files(uploaded_files, perform_analysis, show_exif, generate_map, show_hashes)


def analyze_files(uploaded_files, perform_analysis, show_exif, generate_map, show_hashes):
    """Analyze uploaded files."""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Analyzing {uploaded_file.name}...")
        progress_bar.progress((idx + 1) / len(uploaded_files))
        
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            # Extract metadata
            extractor = MetadataExtractor(tmp_path)
            metadata = extractor.extract_all()
            
            # Perform analysis if requested
            analysis = None
            if perform_analysis:
                analyzer = MetadataAnalyzer(metadata)
                analysis = analyzer.analyze()
            
            results.append({
                'filename': uploaded_file.name,
                'metadata': metadata,
                'analysis': analysis,
                'tmp_path': tmp_path
            })
            
        except Exception as e:
            st.error(f"❌ Error analyzing {uploaded_file.name}: {str(e)}")
    
    status_text.text("Analysis complete!")
    progress_bar.progress(100)
    
    # Display results
    st.markdown("---")
    display_results(results, show_exif, generate_map, show_hashes)
    
    # Cleanup temp files
    for result in results:
        try:
            os.unlink(result['tmp_path'])
        except:
            pass


def display_results(results, show_exif, generate_map, show_hashes):
    """Display analysis results."""
    
    # Summary metrics
    st.header("📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Files Analyzed", len(results))
    
    with col2:
        files_with_gps = sum(1 for r in results 
                            if r['analysis'] and r['analysis']['summary'].get('has_gps'))
        st.metric("Files with GPS", files_with_gps)
    
    with col3:
        total_anomalies = sum(r['analysis']['summary']['total_anomalies'] 
                             for r in results if r['analysis'])
        st.metric("Anomalies Found", total_anomalies)
    
    with col4:
        total_privacy = sum(r['analysis']['summary']['total_privacy_concerns'] 
                           for r in results if r['analysis'])
        st.metric("Privacy Concerns", total_privacy)
    
    st.markdown("---")
    
    # Individual file results
    for result in results:
        display_file_result(result, show_exif, generate_map, show_hashes)


def display_file_result(result, show_exif, generate_map, show_hashes):
    """Display result for a single file."""
    
    filename = result['filename']
    metadata = result['metadata']
    analysis = result['analysis']
    
    with st.expander(f"📄 {filename}", expanded=True):
        
        # File Information
        file_info = metadata.get('file_info', {})
        exif_data = metadata.get('exif_data', {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**File Type:**", metadata.get('file_type', 'Unknown').title())
            st.write("**Size:**", file_info.get('size_human', 'N/A'))
        with col2:
            st.write("**MIME Type:**", metadata.get('mime_type', 'N/A'))
        with col3:
            pass
        
        # Display dates with proper context
        st.markdown("---")
        st.markdown("#### 📅 **Date Information**")
        
        # Check if EXIF dates exist (these are the ORIGINAL dates)
        parsed_dates = exif_data.get('parsed_dates', {})
        
        if parsed_dates:
            st.success("✅ **Original Dates (from EXIF metadata - these are accurate!)**")
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                for desc, date_val in parsed_dates.items():
                    st.write(f"**{desc}:**", date_val)
            
            st.warning("⚠️ **File System Dates (when file was copied/moved to this location - may be recent!)**")
            date_col3, date_col4, date_col5 = st.columns(3)
            with date_col3:
                st.write("**Created on disk:**", file_info.get('created', 'N/A')[:19])
            with date_col4:
                st.write("**Modified on disk:**", file_info.get('modified', 'N/A')[:19])
            with date_col5:
                st.write("**Last accessed:**", file_info.get('accessed', 'N/A')[:19])
        else:
            st.info("ℹ️ **File System Dates** (No EXIF dates found - these show when file was created/modified on this computer)")
            date_col1, date_col2, date_col3 = st.columns(3)
            with date_col1:
                st.write("**Created:**", file_info.get('created', 'N/A')[:19])
            with date_col2:
                st.write("**Modified:**", file_info.get('modified', 'N/A')[:19])
            with date_col3:
                st.write("**Accessed:**", file_info.get('accessed', 'N/A')[:19])
        
        # Risk Assessment
        if analysis:
            risk_level = analysis.get('risk_level', 'UNKNOWN')
            risk_colors = {
                'LOW': 'success',
                'MEDIUM': 'warning', 
                'HIGH': 'error',
                'CRITICAL': 'error'
            }
            
            st.markdown("### 🛡️ Risk Assessment")
            st.markdown(f"**Risk Level:** :{risk_colors.get(risk_level, 'info')}[{risk_level}]")
            
            summary = analysis.get('summary', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anomalies", summary.get('total_anomalies', 0))
            with col2:
                st.metric("Privacy Concerns", summary.get('total_privacy_concerns', 0))
            with col3:
                st.metric("Forensic Indicators", summary.get('total_forensic_indicators', 0))
            
            # Anomalies
            anomalies = analysis.get('anomalies', [])
            if anomalies:
                st.markdown("#### ⚠️ Anomalies Detected")
                for anomaly in anomalies:
                    severity = anomaly.get('severity', 'UNKNOWN')
                    description = anomaly.get('description', 'N/A')
                    significance = anomaly.get('forensic_significance', '')
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="warning-box">
                            <b>{severity}:</b> {description}<br>
                            <small><i>Significance: {significance}</i></small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")
            
            # Privacy Concerns
            privacy_concerns = analysis.get('privacy_concerns', [])
            if privacy_concerns:
                st.markdown("#### 🔒 Privacy Concerns")
                for concern in privacy_concerns:
                    severity = concern.get('severity', 'UNKNOWN')
                    description = concern.get('description', 'N/A')
                    recommendation = concern.get('recommendation', '')
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="error-box">
                            <b>{severity}:</b> {description}<br>
                            <small><i>Recommendation: {recommendation}</i></small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.write("")
        
        # GPS Data
        gps_data = metadata.get('gps_data')
        if gps_data and 'latitude_decimal' in gps_data:
            st.markdown("### 📍 GPS Location Data")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Coordinates:**", gps_data.get('coordinates', 'N/A'))
                st.write("**Latitude:**", gps_data.get('latitude_decimal', 'N/A'))
                st.write("**Longitude:**", gps_data.get('longitude_decimal', 'N/A'))
            with col2:
                if 'altitude_meters' in gps_data:
                    st.write("**Altitude:**", f"{gps_data.get('altitude_meters', 'N/A')} meters")
            
            st.warning("⚠️ This file contains GPS coordinates that reveal the exact location!")
            
            # Generate map
            if generate_map:
                with st.spinner("Generating map..."):
                    mapper = GPSMapper()
                    map_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w')
                    if mapper.create_map(gps_data, map_file.name):
                        with open(map_file.name, 'r', encoding='utf-8') as f:
                            map_html = f.read()
                        st.components.v1.html(map_html, height=400, scrolling=True)
                        os.unlink(map_file.name)
        
        # EXIF Data
        if show_exif and 'exif_data' in metadata:
            exif_data = metadata['exif_data']
            if exif_data and 'error' not in exif_data:
                with st.expander("📸 EXIF Data"):
                    # Show important fields first
                    important_fields = ['Make', 'Model', 'DateTime', 'DateTimeOriginal', 
                                      'Software', 'Artist', 'Copyright']
                    
                    for field in important_fields:
                        if field in exif_data:
                            st.write(f"**{field}:**", exif_data[field])
                    
                    # Show all other fields
                    st.write("**Additional EXIF Fields:**")
                    other_fields = {k: v for k, v in exif_data.items() 
                                  if k not in important_fields and len(str(v)) < 200}
                    st.json(other_fields)
        
        # Document Metadata
        if 'document_metadata' in metadata:
            doc_meta = metadata['document_metadata']
            if 'error' not in doc_meta and doc_meta:
                with st.expander("📝 Document Properties"):
                    for key, value in doc_meta.items():
                        if value and key != 'first_page_text_sample':
                            st.write(f"**{key.replace('_', ' ').title()}:**", value)
        
        # File Hashes
        if show_hashes:
            with st.expander("🔐 File Integrity Hashes"):
                st.code(f"MD5:    {file_info.get('md5_hash', 'N/A')}")
                st.code(f"SHA256: {file_info.get('sha256_hash', 'N/A')}")
        
        # Download Report
        st.markdown("### 📥 Export Report")
        col1, col2, col3 = st.columns(3)
        
        reporter = MetadataReporter(metadata, analysis)
        
        with col1:
            json_report = reporter.generate_json_report()
            st.download_button(
                label="📄 Download JSON",
                data=json_report,
                file_name=f"{Path(filename).stem}_report.json",
                mime="application/json"
            )
        
        with col2:
            csv_report = reporter.generate_csv_report()
            st.download_button(
                label="📊 Download CSV",
                data=csv_report,
                file_name=f"{Path(filename).stem}_report.csv",
                mime="text/csv"
            )
        
        with col3:
            text_report = reporter.generate_text_report()
            st.download_button(
                label="📝 Download Text",
                data=text_report,
                file_name=f"{Path(filename).stem}_report.txt",
                mime="text/plain"
            )


def sanitize_mode():
    """Metadata sanitization mode."""
    
    st.header("🧹 Metadata Sanitization")
    
    st.info("""
    **Metadata sanitization** removes sensitive information from files to protect privacy:
    - GPS coordinates from images
    - Author information from documents
    - EXIF data from photos
    - Creation/modification metadata
    """)
    
    uploaded_file = st.file_uploader(
        "Choose a file to sanitize",
        type=['jpg', 'jpeg', 'png', 'pdf', 'docx'],
        help="Upload a file to remove its metadata"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Show original metadata
        with st.expander("🔍 Original Metadata Preview", expanded=True):
            try:
                # Save temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                
                # Extract metadata
                extractor = MetadataExtractor(tmp_path)
                metadata = extractor.extract_all()
                
                file_info = metadata.get('file_info', {})
                st.write("**Original Size:**", file_info.get('size_human', 'N/A'))
                
                # Check what metadata exists
                has_gps = bool(metadata.get('gps_data') and 'latitude_decimal' in metadata.get('gps_data', {}))
                has_exif = bool(metadata.get('exif_data'))
                has_author = bool(metadata.get('document_metadata', {}).get('author'))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("GPS Data", "Yes ⚠️" if has_gps else "No")
                with col2:
                    st.metric("EXIF Data", "Yes" if has_exif else "No")
                with col3:
                    st.metric("Author Info", "Yes" if has_author else "No")
                
                if has_gps:
                    st.warning("⚠️ This file contains GPS coordinates!")
                if has_author:
                    st.warning(f"⚠️ Author: {metadata.get('document_metadata', {}).get('author')}")
                
            except Exception as e:
                st.error(f"Error analyzing file: {str(e)}")
                return
        
        # Sanitize button
        if st.button("🧹 Sanitize Metadata", type="primary", use_container_width=True):
            with st.spinner("Sanitizing metadata..."):
                try:
                    sanitizer = MetadataSanitizer()
                    
                    # Create output file
                    output_tmp = tempfile.NamedTemporaryFile(delete=False, 
                                                             suffix=Path(uploaded_file.name).suffix)
                    output_tmp.close()
                    
                    # Sanitize
                    if sanitizer.sanitize_file(tmp_path, output_tmp.name):
                        st.success("✅ Metadata sanitization complete!")
                        
                        # Verify sanitization
                        cleaned_extractor = MetadataExtractor(output_tmp.name)
                        cleaned_metadata = cleaned_extractor.extract_all()
                        
                        cleaned_file_info = cleaned_metadata['file_info']
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Original Size", file_info.get('size_human', 'N/A'))
                        with col2:
                            st.metric("Cleaned Size", cleaned_file_info.get('size_human', 'N/A'))
                        
                        # Check what was removed
                        has_gps_after = bool(cleaned_metadata.get('gps_data') and 
                                           'latitude_decimal' in cleaned_metadata.get('gps_data', {}))
                        has_exif_after = bool(cleaned_metadata.get('exif_data') and 
                                            len(cleaned_metadata.get('exif_data', {})) > 1)
                        has_author_after = bool(cleaned_metadata.get('document_metadata', {}).get('author'))
                        
                        st.markdown("### ✅ Verification")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("GPS Data Removed", 
                                    "✅ Yes" if has_gps and not has_gps_after else "N/A")
                        with col2:
                            st.metric("EXIF Data Removed", 
                                    "✅ Yes" if has_exif and not has_exif_after else "N/A")
                        with col3:
                            st.metric("Author Removed", 
                                    "✅ Yes" if has_author and not has_author_after else "N/A")
                        
                        # Download cleaned file
                        with open(output_tmp.name, 'rb') as f:
                            cleaned_data = f.read()
                        
                        clean_filename = f"cleaned_{uploaded_file.name}"
                        st.download_button(
                            label="📥 Download Cleaned File",
                            data=cleaned_data,
                            file_name=clean_filename,
                            mime=uploaded_file.type,
                            type="primary",
                            use_container_width=True
                        )
                        
                        # Cleanup
                        os.unlink(output_tmp.name)
                    else:
                        st.error("❌ Sanitization failed")
                
                except Exception as e:
                    st.error(f"❌ Error during sanitization: {str(e)}")
                finally:
                    os.unlink(tmp_path)


def about_mode():
    """About and help mode."""
    
    st.header("📚 About File Metadata Analyzer")
    
    st.markdown("""
    ## 🔍 What is Metadata?
    
    **Metadata** is "data about data" - information about files beyond their visible content.
    This can include:
    - **Timestamps**: When files were created, modified, accessed
    - **Location**: GPS coordinates from photos
    - **Authorship**: Who created or edited documents
    - **Device Info**: Camera model, software used
    - **Technical Details**: Resolution, duration, encoding
    
    ## 🎯 Purpose of This Tool
    
    This tool serves three main purposes:
    
    1. **Digital Forensics** 🔎
       - Extract evidence from file metadata
       - Establish timelines and locations
       - Attribute files to individuals or devices
       - Detect anomalies and tampering
    
    2. **Privacy Protection** 🔒
       - Identify privacy risks in files
       - Remove sensitive metadata before sharing
       - Educate users about information disclosure
       - Prevent unintentional data leaks
    
    3. **Education** 🎓
       - Demonstrate forensic concepts
       - Show real-world applications
       - Raise awareness of metadata
       - Teach digital literacy
    
    ## 🛠️ Features
    
    ### Extraction
    - Images: EXIF data, GPS coordinates, camera info
    - Documents: Author, creation date, revision history
    - Media: Duration, codec, encoding information
    - File System: Timestamps, size, permissions
    
    ### Analysis
    - Timestamp anomaly detection
    - Privacy concern identification
    - Forensic indicator extraction
    - Risk level assessment
    
    ### Visualization
    - Interactive GPS maps
    - Comprehensive reports
    - Multiple export formats
    
    ### Sanitization
    - EXIF data removal
    - Document metadata clearing
    - Privacy-preserving operations
    
    ## ⚖️ Ethical Use
    
    **This tool should be used:**
    - ✅ For authorized investigations
    - ✅ For educational purposes
    - ✅ For personal privacy audits
    - ✅ For research projects
    
    **This tool should NOT be used:**
    - ❌ Without proper authorization
    - ❌ To invade privacy
    - ❌ For malicious purposes
    - ❌ To circumvent security
    
    ## 📖 Forensic Significance
    
    Metadata is crucial in digital investigations:
    
    - **Timeline Analysis**: Establish sequence of events
    - **Location Verification**: GPS coordinates prove presence
    - **Attribution**: Link files to specific individuals
    - **Authenticity**: Detect manipulated or forged files
    - **Pattern Analysis**: Identify behavioral patterns
    
    ## 🔐 Privacy Implications
    
    Files often contain more information than you realize:
    
    - 📸 Photos may reveal exact locations
    - 📄 Documents may disclose authors
    - 🎵 Media files may contain personal info
    - ⏰ Timestamps reveal activity patterns
    
    **Always review metadata before sharing files!**
    
    ## 🎓 Course Information
    
    **Course**: MST 8407 Forensic Data Acquisition and Analysis  
    **Lecturer**: Mr. Nelson Mutua  
    **Project**: File Metadata Analyzer  
    **Date**: November 2025
    
    ## 📞 Getting Help
    
    For detailed documentation:
    - See `README.md` for full documentation
    - See `QUICKSTART.md` for quick start guide
    
    ## ⚠️ Important Disclaimer
    
    This tool is provided for educational and authorized forensic purposes only.
    Users are responsible for complying with applicable laws and obtaining proper
    authorization before analyzing files. Always respect privacy and follow ethical
    guidelines.
    """)
    
    st.markdown("---")
    st.info("**Version**: 1.0.0 | **Author**: Kirui Brian")


if __name__ == '__main__':
    main()
