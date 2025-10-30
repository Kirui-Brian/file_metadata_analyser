# Sample Files Guide

## Overview
This directory should contain sample files for testing and demonstration purposes.

## Required Sample Files

To fully demonstrate the tool's capabilities, please add the following types of files:

### 1. Images with GPS Data
- **Photo taken with smartphone** (contains GPS coordinates)
- Preferred formats: `.jpg`, `.jpeg`
- Example: `photo_with_gps.jpg`

### 2. Images without GPS Data
- **Any regular image**
- Formats: `.jpg`, `.png`, `.tiff`
- Example: `image.jpg`

### 3. PDF Documents
- **Any PDF file** (preferably with author information)
- Format: `.pdf`
- Example: `document.pdf`

### 4. Word Documents
- **DOCX file with metadata**
- Format: `.docx`
- Example: `report.docx`

### 5. Excel Spreadsheets (Optional)
- **XLSX file**
- Format: `.xlsx`
- Example: `data.xlsx`

### 6. Audio Files (Optional)
- **MP3 or WAV file**
- Formats: `.mp3`, `.wav`
- Example: `audio.mp3`

### 7. Video Files (Optional)
- **MP4 or AVI file**
- Formats: `.mp4`, `.avi`
- Example: `video.mp4`

## How to Get Sample Files

### Option 1: Use Your Own Files
1. Take a photo with your smartphone (will likely have GPS data)
2. Create a Word document with your name as author
3. Save any PDF you have

### Option 2: Create Test Files
Run the sample creation script:
```bash
python create_samples.py
```

### Option 3: Download Sample Files
- **Unsplash**: Free images (no GPS data)
- **Sample Documents**: Create in Microsoft Office
- **Test Media**: Use any personal media files

## Important Notes

⚠️ **Privacy Warning**: 
- Do NOT use files with sensitive personal information
- Remove any confidential data before using as samples
- These files will be analyzed and reports generated

✓ **Best Practice**:
- Use files specifically created for testing
- Verify files don't contain sensitive information
- Consider using publicly available sample files

## File Naming Convention

For easy identification, use descriptive names:
- `photo_with_gps.jpg` - Photo containing GPS coordinates
- `photo_no_gps.jpg` - Photo without GPS data
- `document_with_author.pdf` - PDF with author metadata
- `anonymous_document.pdf` - PDF with minimal metadata

## Testing Checklist

- [ ] At least one image with GPS data
- [ ] At least one image without GPS data
- [ ] At least one PDF document
- [ ] At least one DOCX document
- [ ] (Optional) Audio file
- [ ] (Optional) Video file

## Current Contents

```
samples/
├── (Add your sample files here)
```

## After Adding Files

Run the demo to test:
```bash
python demo.py
```

Or analyze a specific file:
```bash
python metadata_Analyser.py --file samples/your_file.jpg --analyze
```
