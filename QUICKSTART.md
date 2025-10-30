# Quick Start Guide - File Metadata Analyser

## Installation

### Step 1: Navigate to Project Directory
```powershell
cd "b:\MSc\Module IV\MST 8407 Forensic Data Acquisition and Analysis, DF - Mr Nelson Mutua\Course Project"
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

**Note**: Some dependencies are optional. If you encounter errors, install minimal set:
```powershell
pip install Pillow exifread PyPDF2 PyMuPDF python-docx mutagen pandas folium colorama
```

### Step 3: Install FFmpeg (Optional, for video analysis)
- **Windows**: Download from https://ffmpeg.org/ and add to PATH
- Or skip if you don't need video analysis

## Creating Sample Files

### Option 1: Use Your Own Files
Place your test files in the `samples/` directory:
- Images (`.jpg`, `.png`) - preferably photos from smartphone with GPS
- Documents (`.pdf`, `.docx`)
- Media files (`.mp3`, `.mp4`) - optional

### Option 2: Generate Test Files
```powershell
python create_samples.py
```

This creates basic test files in the `samples/` directory.

## Running the Tool

### Basic Usage - Single File Analysis
```powershell
# Analyze an image
python metadata_Analyser.py --file samples/photo.jpg

# Analyze a PDF document
python metadata_Analyser.py --file samples/document.pdf

# Analyze with detailed forensic analysis
python metadata_Analyser.py --file samples/photo.jpg --analyze
```

### Generate Reports
```powershell
# JSON report
python metadata_Analyser.py --file samples/photo.jpg --report json --output report.json

# CSV report
python metadata_Analyser.py --file samples/photo.jpg --report csv --output report.csv

# Text report (saved to file)
python metadata_Analyser.py --file samples/photo.jpg --report text --output report.txt
```

### GPS Mapping
```powershell
# Generate GPS map from image with location data
python metadata_Analyser.py --file samples/photo.jpg --map

# This creates an HTML file - open it in your browser to see the map
```

### Batch Processing
```powershell
# Analyze all files in a directory
python metadata_Analyser.py --directory samples/ --analyze --report json
```

### Metadata Removal
```powershell
# Remove metadata from a file
python metadata_Analyser.py --file samples/photo.jpg --erase --output cleaned_photo.jpg

# The original file is backed up automatically
```

## Running the Demo

The demo script provides an interactive demonstration of all features:

```powershell
python demo.py
```

This will:
1. Extract metadata from sample files
2. Perform forensic analysis
3. Generate GPS maps (if applicable)
4. Demonstrate metadata sanitization
5. Create comprehensive reports
6. Show performance metrics

## Understanding the Output

### Console Output
- **Green ✓**: Successful operation
- **Red ✗**: Error
- **Yellow ⚠**: Warning or important information
- **Blue ℹ**: Informational message

### Report Files
All reports are saved to the `output/` directory:
- `*.json` - Machine-readable JSON format
- `*.csv` - Spreadsheet-compatible format
- `*.txt` - Human-readable text format
- `*.html` - Interactive GPS maps

### Reading Reports

**Text Report Sections:**
1. **File Information**: Basic file details
2. **Timestamps**: Creation, modification, access times
3. **File Integrity**: MD5 and SHA-256 hashes
4. **Type-Specific Metadata**: EXIF, document properties, media info
5. **Forensic Analysis**: Anomalies, privacy concerns, indicators

**Key Findings:**
- **Risk Level**: LOW / MEDIUM / HIGH / CRITICAL
- **Anomalies**: Suspicious patterns in metadata
- **Privacy Concerns**: Information that could compromise privacy
- **Forensic Indicators**: Evidence-relevant metadata

## Common Use Cases

### 1. Verify Image Location
```powershell
python metadata_Analyser.py --file photo.jpg --map
```
Opens a map showing where the photo was taken.

### 2. Check Document Author
```powershell
python metadata_Analyser.py --file document.pdf --analyze
```
Shows author, organization, and revision information.

### 3. Timeline Analysis
```powershell
python metadata_Analyser.py --directory evidence/ --report csv
```
Creates a CSV with timestamps for timeline reconstruction.

### 4. Privacy Check Before Sharing
```powershell
# Check what metadata exists
python metadata_Analyser.py --file myfile.jpg --analyze

# Remove sensitive metadata
python metadata_Analyser.py --file myfile.jpg --erase --output safe_file.jpg
```

### 5. Batch Analysis for Investigation
```powershell
python metadata_Analyser.py --directory case_files/ --analyze --report json --output case_report.json
```

## Troubleshooting

### "File not found" error
- Check file path is correct
- Use quotes around paths with spaces
- Use absolute path or ensure you're in the correct directory

### "Module not found" error
- Run: `pip install -r requirements.txt`
- Install missing package individually: `pip install <package-name>`

### FFmpeg errors (video files)
- Install FFmpeg or skip video files
- Video analysis is optional

### No GPS data found
- Not all images have GPS data
- Camera/phone must have GPS enabled when photo was taken
- Some apps strip GPS data

### "Permission denied" error
- Ensure you have read permission on input files
- Ensure you have write permission on output directory
- Don't analyze system files

## Tips for Presentation

1. **Prepare Sample Files in Advance**
   - Use diverse file types
   - Include at least one image with GPS data
   - Have documents with author information

2. **Pre-generate Some Reports**
   - Have backup reports ready
   - Show different formats (JSON, text, map)

3. **Test All Commands**
   - Run through the demo before presenting
   - Ensure all dependencies work

4. **Have Backup**
   - Take screenshots of expected output
   - Save sample reports

5. **Explain As You Go**
   - Don't just run commands
   - Explain what each output means
   - Relate to forensic significance

## Getting Help

### View Help
```powershell
python metadata_Analyser.py --help
```

### Verbose Mode
```powershell
python metadata_Analyser.py --file samples/photo.jpg --verbose
```
Shows detailed error messages and stack traces.

## Project Structure Reference

```
Course Project/
├── metadata_Analyser.py     # Main CLI application
├── demo.py                   # Interactive demonstration
├── create_samples.py         # Sample file generator
│
├── core/                     # Core modules
│   ├── extractor.py         # Metadata extraction
│   ├── Analyser.py          # Forensic analysis
│   └── reporter.py          # Report generation
│
├── utils/                    # Utility modules
│   ├── file_handler.py      # File operations
│   ├── gps_mapper.py        # GPS mapping
│   └── sanitizer.py         # Metadata removal
│
├── samples/                  # Test files
├── output/                   # Generated reports
│
├── requirements.txt          # Dependencies
├── README.md                # Full documentation
├── QUICKSTART.md            # This file
└── PRESENTATION.md          # Presentation guide
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Create or add sample files
3. ✅ Run basic analysis
4. ✅ Try different report formats
5. ✅ Run the demo script
6. ✅ Review generated reports
7. ✅ Prepare for presentation

---

**Ready to begin!** Start with a simple command:
```powershell
python metadata_Analyser.py --file samples/test_image.jpg --analyze
```

Good luck with your project! 🎓
