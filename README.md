# File Metadata Analyser

## Project Overview

**File Metadata Analyser** is a comprehensive Python-based digital forensics tool designed to extract, analyze, and manipulate metadata from various file types including images, documents, videos, and audio files. This tool demonstrates the critical role of metadata in digital investigations and highlights how metadata can be manipulated or erased to conceal evidence.

## Objectives

1. **Extract Metadata**: Retrieve comprehensive metadata from multiple file formats
2. **Analyze Metadata**: Identify anomalies, timestamps, authorship, and embedded information
3. **Detect Manipulation**: Flag suspicious patterns in metadata
4. **Metadata Sanitization**: Demonstrate metadata removal for privacy purposes
5. **Generate Reports**: Create detailed forensic reports in multiple formats

## Features

- ✅ **Multi-format Support**: Images (JPEG, PNG, TIFF), Documents (PDF, DOCX), Media (MP4, MP3, WAV)
- ✅ **EXIF Data Extraction**: Including GPS coordinates from images
- ✅ **Document Properties**: Author, creation date, modification history
- ✅ **Media Information**: Codec, duration, resolution, bitrate
- ✅ **Anomaly Detection**: Identify suspicious timestamp patterns
- ✅ **Metadata Sanitization**: Remove sensitive metadata
- ✅ **Multiple Report Formats**: JSON, CSV, and human-readable text
- ✅ **CLI Interface**: Easy command-line operation
- ✅ **GPS Mapping**: Visual representation of location data

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone or download the project**:
   ```bash
   cd "b:\MSc\Module IV\MST 8407 Forensic Data Acquisition and Analysis, DF - Mr Nelson Mutua\Course Project"
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python metadata_Analyser.py --help
   ```

## Usage

### Basic Command Structure

```bash
python metadata_Analyser.py --file <path_to_file> [options]
```

### Examples

#### 1. Extract metadata from an image
```bash
python metadata_Analyser.py --file samples/image.jpg --report json
```

#### 2. Analyze a PDF document
```bash
python metadata_Analyser.py --file samples/document.pdf --report text
```

#### 3. Extract metadata from multiple files
```bash
python metadata_Analyser.py --directory samples/ --report csv
```

#### 4. Remove metadata from a file
```bash
python metadata_Analyser.py --file samples/image.jpg --erase --output cleaned_image.jpg
```

#### 5. Generate GPS map from image metadata
```bash
python metadata_Analyser.py --file samples/photo.jpg --map
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--file PATH` | Path to the file to analyze |
| `--directory PATH` | Analyze all files in a directory |
| `--report FORMAT` | Output report format: `json`, `csv`, or `text` (default: text) |
| `--output PATH` | Output file path for reports or cleaned files |
| `--erase` | Remove metadata from the file |
| `--map` | Generate GPS map for images with location data |
| `--analyze` | Perform deep analysis for anomalies |
| `--verbose` | Enable verbose output |

## Running the Demo

Execute the demonstration script to see the tool in action:

```bash
python demo.py
```

This will:
- Analyze sample files from different formats
- Extract and display metadata
- Demonstrate GPS coordinate extraction
- Show metadata sanitization
- Generate comparison reports
- Display performance metrics

## Project Structure

```
Course Project/
│
├── metadata_Analyser.py       # Main CLI application
├── core/
│   ├── __init__.py
│   ├── extractor.py           # Metadata extraction classes
│   ├── Analyser.py            # Metadata analysis engine
│   └── reporter.py            # Report generation
│
├── utils/
│   ├── __init__.py
│   ├── file_handler.py        # File operations
│   ├── gps_mapper.py          # GPS coordinate mapping
│   └── sanitizer.py           # Metadata removal
│
├── samples/                   # Sample files for testing
│   ├── images/
│   ├── documents/
│   └── media/
│
├── output/                    # Generated reports and results
│
├── demo.py                    # Demonstration script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── PRESENTATION.md            # Presentation talking points
```

## Supported File Types

### Images
- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- HEIF (.heif, .heic)

### Documents
- PDF (.pdf)
- Microsoft Word (.docx, .doc)
- Microsoft Excel (.xlsx)
- Microsoft PowerPoint (.pptx)

### Media Files
- Video: MP4, AVI, MOV, MKV
- Audio: MP3, WAV, FLAC, AAC

## Extracted Metadata Types

### File System Metadata
- File name and path
- File size
- Creation time
- Modification time
- Access time
- File permissions

### Image Metadata (EXIF)
- Camera make and model
- Date/time taken
- GPS coordinates (latitude, longitude, altitude)
- Image dimensions
- ISO, aperture, shutter speed
- Software used

### Document Metadata
- Author
- Title
- Subject
- Keywords
- Creation date
- Modification date
- Application used
- Revision history

### Media Metadata
- Duration
- Codec information
- Resolution
- Bitrate
- Frame rate
- Audio channels

## Forensic Analysis Features

### Anomaly Detection
- **Timestamp Inconsistencies**: Detect when access time is before creation time
- **Missing Metadata**: Flag files with suspiciously absent metadata
- **Modified EXIF**: Identify edited or tampered EXIF data
- **GPS Anomalies**: Detect impossible travel distances/times

### Privacy Concerns
- Identify files containing personal information
- Flag embedded GPS coordinates
- Detect author/organization information

## Educational Value

This tool demonstrates:

1. **Metadata Importance**: How seemingly hidden data can reveal critical information
2. **Digital Evidence**: The role of metadata in forensic investigations
3. **Privacy Risks**: What information files inadvertently expose
4. **Anti-Forensics**: How perpetrators might attempt to hide evidence
5. **Ethical Considerations**: Balancing investigation needs with privacy rights

## Presentation Topics

1. **Introduction to File Metadata**
   - What is metadata?
   - Types of metadata
   - Where metadata is stored

2. **Forensic Significance**
   - Case studies of metadata in investigations
   - Timeline reconstruction
   - Author attribution

3. **Tool Demonstration**
   - Live extraction examples
   - GPS mapping demonstration
   - Anomaly detection showcase

4. **Metadata Manipulation**
   - Techniques for altering metadata
   - Detection methods
   - Sanitization for privacy

5. **Ethical and Legal Implications**
   - Privacy concerns
   - Admissibility in court
   - Best practices for investigators

## Future Enhancements

- [ ] GUI interface using Streamlit
- [ ] Database storage for large-scale analysis
- [ ] Machine learning for anomaly detection
- [ ] Cloud storage metadata extraction
- [ ] Blockchain-based evidence chain
- [ ] Mobile app metadata support

## Technical Stack

- **Python 3.10+**: Core language
- **Pillow**: Image processing
- **exifread**: EXIF data extraction
- **PyPDF2/PyMuPDF**: PDF metadata
- **python-docx**: Word document metadata
- **mutagen**: Audio metadata
- **ffmpeg-python**: Video metadata
- **folium**: GPS mapping
- **pandas**: Data analysis and reporting

## License

This project is created for educational purposes as part of MST 8407 Forensic Data Acquisition and Analysis course.

## Author

**Course**: MST 8407 Forensic Data Acquisition and Analysis, DF  
**Instructor**: Mr. Nelson Mutua  
**Date**: November 2025

## Troubleshooting

### FFmpeg Not Found
If you encounter FFmpeg errors, install it:
- **Windows**: Download from https://ffmpeg.org/ and add to PATH
- **Linux**: `sudo apt-get install ffmpeg`
- **macOS**: `brew install ffmpeg`

### Permission Errors
Run the script with appropriate permissions or use files you own.

### Missing Dependencies
Reinstall requirements: `pip install -r requirements.txt --upgrade`

## Contact & Support

For questions or issues, please refer to the course materials or consult the instructor.

---

**Important**: This tool is for educational and authorized forensic analysis only. Always obtain proper authorization before analyzing files.
