"""
Metadata Analyser Module
Analyzes extracted metadata for anomalies, inconsistencies, and forensic indicators.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import re


class MetadataAnalyser:
    """
    Analyzes metadata for forensic significance, anomalies, and privacy concerns.
    """
    
    def __init__(self, metadata: Dict[str, Any]):
        """
        Initialize the Analyser with extracted metadata.
        
        Args:
            metadata (Dict): Metadata dictionary from MetadataExtractor
        """
        self.metadata = metadata
        self.findings = []
        self.anomalies = []
        self.privacy_concerns = []
        self.forensic_indicators = []
    
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of the metadata.
        
        Returns:
            Dict containing analysis results
        """
        self._analyze_timestamps()
        self._analyze_file_system()
        self._analyze_document_properties()
        self._analyze_gps_data()
        self._analyze_media_properties()
        self._check_privacy_concerns()
        self._generate_forensic_indicators()
        
        return {
            'summary': self._generate_summary(),
            'anomalies': self.anomalies,
            'privacy_concerns': self.privacy_concerns,
            'forensic_indicators': self.forensic_indicators,
            'findings': self.findings,
            'risk_level': self._calculate_risk_level(),
        }
    
    def _analyze_timestamps(self):
        """Analyze file timestamps for inconsistencies."""
        file_info = self.metadata.get('file_info', {})
        
        try:
            created = datetime.fromisoformat(file_info.get('created', ''))
            modified = datetime.fromisoformat(file_info.get('modified', ''))
            accessed = datetime.fromisoformat(file_info.get('accessed', ''))
            
            # Check for impossible timestamp sequences
            if modified < created:
                self.anomalies.append({
                    'type': 'TIMESTAMP_ANOMALY',
                    'severity': 'HIGH',
                    'description': 'Modified time is before creation time',
                    'details': f"Created: {created}, Modified: {modified}",
                    'forensic_significance': 'Possible timestamp manipulation or system clock issues'
                })
            
            if accessed < created:
                self.anomalies.append({
                    'type': 'TIMESTAMP_ANOMALY',
                    'severity': 'HIGH',
                    'description': 'Access time is before creation time',
                    'details': f"Created: {created}, Accessed: {accessed}",
                    'forensic_significance': 'Strong indicator of timestamp tampering'
                })
            
            # Check for same timestamps (suspicious for edited files)
            if created == modified:
                self.findings.append({
                    'type': 'TIMESTAMP_MATCH',
                    'severity': 'LOW',
                    'description': 'Creation and modification times are identical',
                    'forensic_significance': 'File may never have been edited, or timestamps were synchronized'
                })
            
            # Check if file is very old but recently accessed
            now = datetime.now()
            file_age = (now - created).days
            last_access_age = (now - accessed).days
            
            if file_age > 365 and last_access_age < 1:
                self.findings.append({
                    'type': 'OLD_FILE_RECENT_ACCESS',
                    'severity': 'MEDIUM',
                    'description': f'File is {file_age} days old but was accessed recently',
                    'forensic_significance': 'May indicate recent interest in old evidence'
                })
        
        except (ValueError, KeyError) as e:
            self.findings.append({
                'type': 'TIMESTAMP_ERROR',
                'severity': 'LOW',
                'description': f'Error analyzing timestamps: {str(e)}'
            })
    
    def _analyze_file_system(self):
        """Analyze file system metadata."""
        file_info = self.metadata.get('file_info', {})
        
        # Check file size
        size_bytes = file_info.get('size_bytes', 0)
        if size_bytes == 0:
            self.anomalies.append({
                'type': 'EMPTY_FILE',
                'severity': 'MEDIUM',
                'description': 'File is empty (0 bytes)',
                'forensic_significance': 'Possible data wiping or placeholder file'
            })
        
        # Check for suspicious file names
        filename = file_info.get('filename', '')
        suspicious_patterns = [
            r'copy\s+of',
            r'backup',
            r'tmp',
            r'temp',
            r'~\$',
            r'^\.',  # Hidden files on Unix
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                self.findings.append({
                    'type': 'SUSPICIOUS_FILENAME',
                    'severity': 'LOW',
                    'description': f'Filename contains suspicious pattern: {pattern}',
                    'forensic_significance': 'May indicate temporary, backup, or hidden file'
                })
                break
    
    def _analyze_document_properties(self):
        """Analyze document metadata for forensic indicators."""
        doc_metadata = self.metadata.get('document_metadata', {})
        
        if not doc_metadata or 'error' in doc_metadata:
            return
        
        # Check for author information
        author = doc_metadata.get('author') or doc_metadata.get('creator')
        if author:
            self.privacy_concerns.append({
                'type': 'AUTHOR_INFORMATION',
                'severity': 'MEDIUM',
                'description': f'Document contains author information: {author}',
                'recommendation': 'Remove author metadata before sharing'
            })
            
            self.forensic_indicators.append({
                'type': 'AUTHORSHIP',
                'value': author,
                'significance': 'Can be used to attribute document creation'
            })
        
        # Check for organization/company information
        for key in ['company', 'organization', 'category']:
            if key in doc_metadata and doc_metadata[key]:
                self.privacy_concerns.append({
                    'type': 'ORGANIZATION_INFO',
                    'severity': 'MEDIUM',
                    'description': f'Document contains organization info: {doc_metadata[key]}',
                    'recommendation': 'Remove organizational metadata'
                })
        
        # Check for revision history
        revision = doc_metadata.get('revision')
        if revision and int(revision) > 1:
            self.forensic_indicators.append({
                'type': 'REVISION_COUNT',
                'value': revision,
                'significance': f'Document has been revised {revision} times'
            })
        
        # Check for comments or keywords
        comments = doc_metadata.get('comments')
        keywords = doc_metadata.get('keywords')
        
        if comments:
            self.privacy_concerns.append({
                'type': 'EMBEDDED_COMMENTS',
                'severity': 'HIGH',
                'description': 'Document contains embedded comments',
                'recommendation': 'Review and remove sensitive comments'
            })
        
        if keywords:
            self.forensic_indicators.append({
                'type': 'KEYWORDS',
                'value': keywords,
                'significance': 'May reveal document classification or purpose'
            })
    
    def _analyze_gps_data(self):
        """Analyze GPS data from images."""
        gps_data = self.metadata.get('gps_data')
        
        if not gps_data or 'error' in gps_data:
            return
        
        if 'latitude_decimal' in gps_data and 'longitude_decimal' in gps_data:
            lat = gps_data['latitude_decimal']
            lon = gps_data['longitude_decimal']
            
            self.privacy_concerns.append({
                'type': 'GPS_LOCATION',
                'severity': 'CRITICAL',
                'description': f'Image contains GPS coordinates: {lat}, {lon}',
                'recommendation': 'Remove GPS data before sharing to protect location privacy'
            })
            
            self.forensic_indicators.append({
                'type': 'GEOLOCATION',
                'value': f'{lat}, {lon}',
                'significance': 'Can pinpoint exact location where photo was taken'
            })
            
            # Check altitude
            if 'altitude_meters' in gps_data:
                altitude = gps_data['altitude_meters']
                self.forensic_indicators.append({
                    'type': 'ALTITUDE',
                    'value': f'{altitude} meters',
                    'significance': 'Additional location context (elevation)'
                })
    
    def _analyze_media_properties(self):
        """Analyze media file metadata."""
        media_metadata = self.metadata.get('media_metadata', {})
        
        if not media_metadata or 'error' in media_metadata:
            return
        
        # Check for duration (for potential deleted content)
        mutagen_data = media_metadata.get('mutagen_data', {})
        duration = mutagen_data.get('length')
        
        if duration is not None:
            self.forensic_indicators.append({
                'type': 'MEDIA_DURATION',
                'value': f'{duration:.2f} seconds',
                'significance': 'Original recording length'
            })
        
        # Check for embedded tags
        tags = media_metadata.get('tags', {})
        if tags:
            # Look for artist, album, etc.
            for key in ['artist', 'album', 'title', 'comment']:
                if key in tags:
                    self.forensic_indicators.append({
                        'type': 'MEDIA_TAG',
                        'value': f'{key}: {tags[key]}',
                        'significance': 'Embedded metadata may reveal origin'
                    })
    
    def _check_privacy_concerns(self):
        """Identify overall privacy concerns."""
        # Check for personal identifiable information
        exif_data = self.metadata.get('exif_data', {})
        
        # Camera/device information
        camera_make = exif_data.get('Make') or exif_data.get('EXIF Make')
        camera_model = exif_data.get('Model') or exif_data.get('EXIF Model')
        
        if camera_make or camera_model:
            self.privacy_concerns.append({
                'type': 'DEVICE_INFORMATION',
                'severity': 'LOW',
                'description': f'File contains device info: {camera_make} {camera_model}',
                'recommendation': 'Device information can be used for fingerprinting'
            })
        
        # Software information
        software = exif_data.get('Software') or exif_data.get('EXIF Software')
        if software:
            self.privacy_concerns.append({
                'type': 'SOFTWARE_INFORMATION',
                'severity': 'LOW',
                'description': f'File contains software info: {software}',
                'recommendation': 'Software metadata can reveal editing tools used'
            })
    
    def _generate_forensic_indicators(self):
        """Generate summary of forensic indicators."""
        # Add hash values as forensic indicators
        file_info = self.metadata.get('file_info', {})
        
        for hash_type in ['md5_hash', 'sha256_hash']:
            if hash_type in file_info:
                self.forensic_indicators.append({
                    'type': 'FILE_HASH',
                    'value': f'{hash_type.upper()}: {file_info[hash_type]}',
                    'significance': 'Cryptographic fingerprint for file integrity verification'
                })
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate analysis summary."""
        return {
            'total_anomalies': len(self.anomalies),
            'total_privacy_concerns': len(self.privacy_concerns),
            'total_forensic_indicators': len(self.forensic_indicators),
            'total_findings': len(self.findings),
            'file_type': self.metadata.get('file_type'),
            'has_gps': bool(self.metadata.get('gps_data') and 
                           'latitude_decimal' in self.metadata.get('gps_data', {})),
            'has_author_info': bool(self.metadata.get('document_metadata', {}).get('author')),
            'analyzed_at': datetime.now().isoformat(),
        }
    
    def _calculate_risk_level(self) -> str:
        """Calculate overall privacy risk level."""
        critical_count = sum(1 for concern in self.privacy_concerns 
                            if concern.get('severity') == 'CRITICAL')
        high_count = sum(1 for concern in self.privacy_concerns 
                        if concern.get('severity') == 'HIGH')
        
        high_anomalies = sum(1 for anomaly in self.anomalies 
                            if anomaly.get('severity') == 'HIGH')
        
        if critical_count > 0 or high_anomalies > 2:
            return 'CRITICAL'
        elif high_count > 0 or high_anomalies > 0:
            return 'HIGH'
        elif len(self.privacy_concerns) > 0:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_recommendations(self) -> List[str]:
        """Get privacy and security recommendations."""
        recommendations = []
        
        if any('GPS_LOCATION' == c.get('type') for c in self.privacy_concerns):
            recommendations.append('Remove GPS coordinates before sharing photos online')
        
        if any('AUTHOR_INFORMATION' == c.get('type') for c in self.privacy_concerns):
            recommendations.append('Strip author metadata from documents before distribution')
        
        if any('TIMESTAMP_ANOMALY' in a.get('type', '') for a in self.anomalies):
            recommendations.append('Investigate potential timestamp manipulation')
        
        if len(self.privacy_concerns) > 5:
            recommendations.append('Consider using metadata sanitization tools')
        
        if not recommendations:
            recommendations.append('No critical privacy concerns detected')
        
        return recommendations
