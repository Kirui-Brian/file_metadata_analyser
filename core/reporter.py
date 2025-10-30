"""
Metadata Reporter Module
Generates reports in various formats (JSON, CSV, Text) from extracted and analyzed metadata.
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
from io import StringIO


class MetadataReporter:
    """
    Generates formatted reports from metadata extraction and analysis.
    Supports JSON, CSV, and human-readable text formats.
    """
    
    def __init__(self, metadata: Dict[str, Any], analysis: Optional[Dict[str, Any]] = None):
        """
        Initialize the reporter with metadata and optional analysis results.
        
        Args:
            metadata (Dict): Raw metadata from MetadataExtractor
            analysis (Dict, optional): Analysis results from MetadataAnalyzer
        """
        self.metadata = metadata
        self.analysis = analysis
        self.report_time = datetime.now()
    
    def generate_json_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a JSON report.
        
        Args:
            output_path (str, optional): Path to save the report
            
        Returns:
            str: JSON string
        """
        report_data = {
            'report_info': {
                'generated_at': self.report_time.isoformat(),
                'report_type': 'File Metadata Analysis',
                'version': '1.0.0'
            },
            'metadata': self.metadata,
            'analysis': self.analysis if self.analysis else {}
        }
        
        json_str = json.dumps(report_data, indent=2, default=str)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    def generate_csv_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a CSV report (flattened metadata).
        
        Args:
            output_path (str, optional): Path to save the report
            
        Returns:
            str: CSV string
        """
        # Flatten the metadata structure
        flat_data = self._flatten_dict(self.metadata)
        
        # Add analysis data if available
        if self.analysis:
            analysis_flat = self._flatten_dict(self.analysis, prefix='analysis')
            flat_data.update(analysis_flat)
        
        output = StringIO()
        if flat_data:
            writer = csv.DictWriter(output, fieldnames=flat_data.keys())
            writer.writeheader()
            writer.writerow(flat_data)
        
        csv_str = output.getvalue()
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_str)
        
        return csv_str
    
    def generate_text_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a human-readable text report.
        
        Args:
            output_path (str, optional): Path to save the report
            
        Returns:
            str: Formatted text report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("FILE METADATA ANALYSIS REPORT")
        lines.append("=" * 80)
        lines.append(f"Generated: {self.report_time.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # File Information Section
        file_info = self.metadata.get('file_info', {})
        lines.append("FILE INFORMATION")
        lines.append("-" * 80)
        lines.append(f"  Filename:        {file_info.get('filename', 'N/A')}")
        lines.append(f"  Full Path:       {file_info.get('full_path', 'N/A')}")
        lines.append(f"  File Size:       {file_info.get('size_human', 'N/A')}")
        lines.append(f"  File Type:       {self.metadata.get('file_type', 'N/A')}")
        lines.append(f"  MIME Type:       {self.metadata.get('mime_type', 'N/A')}")
        lines.append("")
        
        # Timestamps
        lines.append("TIMESTAMPS")
        lines.append("-" * 80)
        lines.append(f"  Created:         {file_info.get('created', 'N/A')}")
        lines.append(f"  Modified:        {file_info.get('modified', 'N/A')}")
        lines.append(f"  Accessed:        {file_info.get('accessed', 'N/A')}")
        lines.append("")
        
        # Hash Values
        lines.append("FILE INTEGRITY")
        lines.append("-" * 80)
        lines.append(f"  MD5:             {file_info.get('md5_hash', 'N/A')}")
        lines.append(f"  SHA-256:         {file_info.get('sha256_hash', 'N/A')}")
        lines.append("")
        
        # Image Metadata
        if 'image_metadata' in self.metadata:
            img_meta = self.metadata['image_metadata']
            if 'error' not in img_meta:
                lines.append("IMAGE PROPERTIES")
                lines.append("-" * 80)
                lines.append(f"  Format:          {img_meta.get('format', 'N/A')}")
                lines.append(f"  Dimensions:      {img_meta.get('width', 'N/A')} x {img_meta.get('height', 'N/A')}")
                lines.append(f"  Mode:            {img_meta.get('mode', 'N/A')}")
                lines.append("")
        
        # GPS Data
        if 'gps_data' in self.metadata and self.metadata['gps_data']:
            gps_data = self.metadata['gps_data']
            if 'error' not in gps_data and 'latitude_decimal' in gps_data:
                lines.append("GPS LOCATION DATA")
                lines.append("-" * 80)
                lines.append(f"  Coordinates:     {gps_data.get('coordinates', 'N/A')}")
                lines.append(f"  Latitude:        {gps_data.get('latitude_decimal', 'N/A')}")
                lines.append(f"  Longitude:       {gps_data.get('longitude_decimal', 'N/A')}")
                if 'altitude_meters' in gps_data:
                    lines.append(f"  Altitude:        {gps_data.get('altitude_meters', 'N/A')} meters")
                lines.append("  ⚠️  WARNING: This file contains GPS coordinates!")
                lines.append("")
        
        # EXIF Data
        if 'exif_data' in self.metadata:
            exif_data = self.metadata['exif_data']
            if 'error' not in exif_data and exif_data:
                lines.append("EXIF DATA (Selected Fields)")
                lines.append("-" * 80)
                
                # Prioritize important fields
                important_fields = [
                    'Make', 'Model', 'DateTime', 'DateTimeOriginal', 
                    'Software', 'Artist', 'Copyright'
                ]
                
                for field in important_fields:
                    if field in exif_data:
                        lines.append(f"  {field:20s}: {exif_data[field]}")
                
                # Show count of additional fields
                additional = len(exif_data) - len([f for f in important_fields if f in exif_data])
                if additional > 0:
                    lines.append(f"  ... and {additional} more EXIF fields")
                lines.append("")
        
        # Document Metadata
        if 'document_metadata' in self.metadata:
            doc_meta = self.metadata['document_metadata']
            if 'error' not in doc_meta:
                lines.append("DOCUMENT PROPERTIES")
                lines.append("-" * 80)
                
                for key in ['author', 'title', 'subject', 'creator', 'keywords', 
                           'created', 'modified', 'last_modified_by', 'page_count']:
                    if key in doc_meta and doc_meta[key]:
                        lines.append(f"  {key.replace('_', ' ').title():20s}: {doc_meta[key]}")
                lines.append("")
        
        # Media Metadata
        if 'media_metadata' in self.metadata:
            media_meta = self.metadata['media_metadata']
            if 'error' not in media_meta:
                lines.append("MEDIA PROPERTIES")
                lines.append("-" * 80)
                
                mutagen_data = media_meta.get('mutagen_data', {})
                if mutagen_data:
                    for key, value in mutagen_data.items():
                        if value is not None:
                            lines.append(f"  {key.replace('_', ' ').title():20s}: {value}")
                lines.append("")
        
        # Analysis Results
        if self.analysis:
            lines.append("=" * 80)
            lines.append("FORENSIC ANALYSIS")
            lines.append("=" * 80)
            lines.append("")
            
            summary = self.analysis.get('summary', {})
            lines.append("SUMMARY")
            lines.append("-" * 80)
            lines.append(f"  Risk Level:              {self.analysis.get('risk_level', 'N/A')}")
            lines.append(f"  Anomalies Found:         {summary.get('total_anomalies', 0)}")
            lines.append(f"  Privacy Concerns:        {summary.get('total_privacy_concerns', 0)}")
            lines.append(f"  Forensic Indicators:     {summary.get('total_forensic_indicators', 0)}")
            lines.append(f"  Has GPS Data:            {'Yes' if summary.get('has_gps') else 'No'}")
            lines.append(f"  Has Author Info:         {'Yes' if summary.get('has_author_info') else 'No'}")
            lines.append("")
            
            # Anomalies
            anomalies = self.analysis.get('anomalies', [])
            if anomalies:
                lines.append("ANOMALIES DETECTED")
                lines.append("-" * 80)
                for i, anomaly in enumerate(anomalies, 1):
                    lines.append(f"  [{i}] {anomaly.get('type', 'UNKNOWN')}")
                    lines.append(f"      Severity: {anomaly.get('severity', 'N/A')}")
                    lines.append(f"      Description: {anomaly.get('description', 'N/A')}")
                    if 'forensic_significance' in anomaly:
                        lines.append(f"      Significance: {anomaly['forensic_significance']}")
                    lines.append("")
            
            # Privacy Concerns
            privacy_concerns = self.analysis.get('privacy_concerns', [])
            if privacy_concerns:
                lines.append("PRIVACY CONCERNS")
                lines.append("-" * 80)
                for i, concern in enumerate(privacy_concerns, 1):
                    lines.append(f"  [{i}] {concern.get('type', 'UNKNOWN')}")
                    lines.append(f"      Severity: {concern.get('severity', 'N/A')}")
                    lines.append(f"      Description: {concern.get('description', 'N/A')}")
                    if 'recommendation' in concern:
                        lines.append(f"      Recommendation: {concern['recommendation']}")
                    lines.append("")
            
            # Forensic Indicators
            indicators = self.analysis.get('forensic_indicators', [])
            if indicators:
                lines.append("FORENSIC INDICATORS")
                lines.append("-" * 80)
                for i, indicator in enumerate(indicators, 1):
                    lines.append(f"  [{i}] {indicator.get('type', 'UNKNOWN')}")
                    lines.append(f"      Value: {indicator.get('value', 'N/A')}")
                    if 'significance' in indicator:
                        lines.append(f"      Significance: {indicator['significance']}")
                    lines.append("")
        
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        report_text = "\n".join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
        
        return report_text
    
    def generate_summary_report(self) -> str:
        """Generate a brief summary report."""
        lines = []
        lines.append("QUICK SUMMARY")
        lines.append("=" * 60)
        
        file_info = self.metadata.get('file_info', {})
        lines.append(f"File: {file_info.get('filename', 'N/A')}")
        lines.append(f"Type: {self.metadata.get('file_type', 'N/A')}")
        lines.append(f"Size: {file_info.get('size_human', 'N/A')}")
        
        if self.analysis:
            lines.append(f"Risk Level: {self.analysis.get('risk_level', 'N/A')}")
            summary = self.analysis.get('summary', {})
            lines.append(f"GPS Data: {'Yes ⚠️' if summary.get('has_gps') else 'No'}")
            lines.append(f"Anomalies: {summary.get('total_anomalies', 0)}")
            lines.append(f"Privacy Concerns: {summary.get('total_privacy_concerns', 0)}")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _flatten_dict(self, d: Dict[str, Any], prefix: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten a nested dictionary.
        
        Args:
            d (Dict): Dictionary to flatten
            prefix (str): Prefix for keys
            sep (str): Separator for nested keys
            
        Returns:
            Dict: Flattened dictionary
        """
        flat = {}
        
        for key, value in d.items():
            new_key = f"{prefix}{sep}{key}" if prefix else key
            
            if isinstance(value, dict):
                flat.update(self._flatten_dict(value, new_key, sep))
            elif isinstance(value, (list, tuple)):
                flat[new_key] = str(value)
            else:
                flat[new_key] = value
        
        return flat
