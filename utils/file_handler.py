"""
File Handler Utility
Handles file operations, validation, and batch processing.
"""

import os
from pathlib import Path
from typing import List, Optional
import mimetypes


class FileHandler:
    """Utility class for file operations and validation."""
    
    SUPPORTED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.heic', '.heif'],
        'document': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
        'video': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
    }
    
    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """
        Check if file type is supported.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if supported, False otherwise
        """
        ext = Path(file_path).suffix.lower()
        all_supported = []
        for exts in FileHandler.SUPPORTED_EXTENSIONS.values():
            all_supported.extend(exts)
        return ext in all_supported
    
    @staticmethod
    def get_file_category(file_path: str) -> Optional[str]:
        """
        Get the category of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: Category name or None
        """
        ext = Path(file_path).suffix.lower()
        for category, extensions in FileHandler.SUPPORTED_EXTENSIONS.items():
            if ext in extensions:
                return category
        return None
    
    @staticmethod
    def find_files_in_directory(directory: str, recursive: bool = True) -> List[str]:
        """
        Find all supported files in a directory.
        
        Args:
            directory (str): Directory path
            recursive (bool): Whether to search recursively
            
        Returns:
            List[str]: List of file paths
        """
        directory_path = Path(directory)
        if not directory_path.exists() or not directory_path.is_dir():
            raise ValueError(f"Invalid directory: {directory}")
        
        files = []
        pattern = '**/*' if recursive else '*'
        
        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and FileHandler.is_supported_file(str(file_path)):
                files.append(str(file_path.absolute()))
        
        return files
    
    @staticmethod
    def validate_output_path(output_path: str, create_dirs: bool = True) -> Path:
        """
        Validate and prepare output path.
        
        Args:
            output_path (str): Output file path
            create_dirs (bool): Create parent directories if they don't exist
            
        Returns:
            Path: Validated path object
        """
        path = Path(output_path)
        
        if create_dirs and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        
        return path
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """
        Create a safe filename by removing invalid characters.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Safe filename
        """
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        return filename
    
    @staticmethod
    def ensure_unique_path(file_path: str) -> str:
        """
        Ensure file path is unique by adding suffix if needed.
        
        Args:
            file_path (str): Desired file path
            
        Returns:
            str: Unique file path
        """
        path = Path(file_path)
        if not path.exists():
            return file_path
        
        stem = path.stem
        suffix = path.suffix
        parent = path.parent
        counter = 1
        
        while True:
            new_path = parent / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                return str(new_path)
            counter += 1
