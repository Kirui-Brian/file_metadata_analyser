"""
File Metadata Analyzer - Core Package
This package contains the core functionality for metadata extraction, analysis, and reporting.
"""

__version__ = "1.0.0"
__author__ = "MST 8407 Course Project"

from .extractor import MetadataExtractor
from .analyzer import MetadataAnalyzer
from .reporter import MetadataReporter

__all__ = [
    'MetadataExtractor',
    'MetadataAnalyzer',
    'MetadataReporter'
]
