# Streamlit GUI Guide - File Metadata Analyser

## 🎨 Web Interface Overview

The File Metadata Analyser now includes a **beautiful, user-friendly web interface** built with Streamlit!

## 🚀 Quick Start

### 1. Install Streamlit (if not already installed)
```powershell
pip install streamlit
```

Or install all requirements:
```powershell
pip install -r requirements.txt
```

### 2. Launch the Web Interface
```powershell
streamlit run streamlit_app.py
```

Your default browser will automatically open to `http://localhost:8501`

## 🖥️ Interface Features

### 📤 **Upload & Analyze Mode**

This is the main mode for analyzing files:

#### Features:
- **Drag & Drop Upload**: Simply drag files into the upload area
- **Multiple File Support**: Analyze several files at once
- **Real-time Analysis**: Instant results as files are processed
- **Interactive Visualizations**: Beautiful charts and metrics
- **GPS Mapping**: Embedded interactive maps in the browser
- **Customizable Options**: Choose what to analyze

#### Analysis Options:
- ✅ **Forensic Analysis**: Detect anomalies and privacy concerns
- ✅ **Show EXIF Data**: Display detailed camera/photo metadata
- ✅ **Generate GPS Map**: Create interactive location maps
- ✅ **Show File Hashes**: Display MD5 and SHA-256 hashes

#### What You'll See:
1. **Summary Dashboard**
   - Total files analyzed
   - Files with GPS coordinates
   - Anomalies detected
   - Privacy concerns found

2. **Individual File Results**
   - File information (type, size, dates)
   - Risk assessment with color-coded levels
   - Anomaly warnings
   - Privacy concern alerts
   - GPS maps (if location data exists)
   - EXIF data viewer
   - Document properties

3. **Export Options**
   - Download JSON report
   - Download CSV report
   - Download text report

### 🧹 **Metadata Sanitization Mode**

Clean metadata from your files:

#### Features:
- **Before/After Comparison**: See what metadata exists and what gets removed
- **Privacy Protection**: Remove GPS, author info, EXIF data
- **File Size Comparison**: See storage impact of metadata removal
- **Download Cleaned File**: Get sanitized version instantly

#### Process:
1. Upload file to sanitize
2. Review original metadata
3. Click "Sanitize Metadata"
4. Verify what was removed
5. Download cleaned file

### 📚 **About Mode**

Educational information about:
- What is metadata?
- Why it matters for forensics
- Privacy implications
- Ethical guidelines
- Tool features and capabilities

## 🎯 Use Cases

### For Presentations
- **Live Demo**: More impressive than command line
- **Visual Appeal**: Professional, polished interface
- **Easy Navigation**: No commands to remember
- **Interactive**: Audience can follow along

### For Class Projects
- **User-Friendly**: Easy for classmates to test
- **Professional**: Shows modern web development skills
- **Accessible**: Works on any device with a browser
- **Shareable**: Send link for others to view

### For Investigations
- **Quick Analysis**: Upload and get results fast
- **Multiple Files**: Batch processing with progress tracking
- **Export Reports**: Download professional reports
- **Visual Evidence**: Maps and charts for presentations

## 🎨 Interface Highlights

### Color-Coded Risk Levels
- 🟢 **LOW**: Green - minimal concerns
- 🟡 **MEDIUM**: Yellow - some issues found
- 🔴 **HIGH**: Orange - significant concerns
- ⚫ **CRITICAL**: Red - serious privacy risks

### Interactive Elements
- 📊 **Metrics Cards**: Key statistics at a glance
- 📍 **GPS Maps**: Interactive Folium maps embedded
- 🔍 **Expandable Sections**: Click to show/hide details
- 📥 **Download Buttons**: Export reports with one click

### Responsive Design
- Works on desktop, tablet, and mobile
- Adapts to screen size
- Professional layout
- Easy navigation

## 💡 Tips for Best Results

### For Demonstrations
1. **Prepare Files in Advance**
   - Have diverse file types ready
   - Include photos with GPS data
   - Use documents with author info

2. **Show Different Features**
   - Upload multiple files at once
   - Demonstrate GPS mapping
   - Show metadata sanitization
   - Export various report formats

3. **Highlight Key Points**
   - Point out privacy risks (GPS, author)
   - Show anomaly detection
   - Explain forensic significance
   - Demonstrate sanitization

### For Daily Use
1. **Privacy Audits**: Check files before sharing
2. **Quick Analysis**: Upload and analyze in seconds
3. **Batch Processing**: Analyze entire folders
4. **Report Generation**: Professional output for documentation

## 🔧 Advanced Features

### Sidebar Options
- **Mode Selection**: Switch between analyze/sanitize/about
- **Collapsible**: Maximize screen space when needed

### Analysis Options Panel
- **Customizable**: Toggle features on/off
- **Tooltips**: Hover for explanations
- **Persistent**: Settings maintained during session

### Export Features
- **Multiple Formats**: JSON, CSV, Text
- **Instant Download**: One-click export
- **Proper Naming**: Files named after source

## 📱 Browser Compatibility

Works on all modern browsers:
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari
- ✅ Opera

## 🌐 Network Access

### Local Mode (Default)
```powershell
streamlit run streamlit_app.py
```
- Accessible only on your computer
- URL: `http://localhost:8501`

### Network Mode (Share with Others)
```powershell
streamlit run streamlit_app.py --server.address=0.0.0.0
```
- Accessible on local network
- Share your IP address with others
- Good for classroom demos

### Cloud Deployment (Optional)
Deploy to Streamlit Cloud for public access:
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click
4. Get public URL to share

## 🎓 For Your Presentation

### Why GUI is Better for Demo
- ✅ **Visual Impact**: More engaging than CLI
- ✅ **Easy to Follow**: Audience can see everything
- ✅ **Professional**: Modern, polished look
- ✅ **Interactive**: Can demonstrate live
- ✅ **No Typos**: Click buttons instead of typing

### Demo Flow Suggestion
1. **Open interface** - Show clean, modern design
2. **Upload image** - Drag and drop demonstration
3. **Show results** - Walk through analysis
4. **Show GPS map** - Interactive map display
5. **Sanitize file** - Before/after comparison
6. **Export report** - Download JSON example

### Presentation Tips
1. **Full Screen**: Press F11 for immersive view
2. **Clear Cache**: Start fresh before demo
3. **Test Upload**: Verify files work beforehand
4. **Backup Files**: Have multiple samples ready
5. **Practice**: Run through demo at least once

## 🔍 Comparison: CLI vs GUI

| Feature | CLI | GUI |
|---------|-----|-----|
| **Ease of Use** | Requires commands | Point and click |
| **Visual Appeal** | Text-based | Colorful, modern |
| **Learning Curve** | Steeper | Gentle |
| **Batch Processing** | Fast with scripts | Upload multiple |
| **Presentation** | Technical | Professional |
| **Reports** | File-based | Download buttons |
| **Maps** | Separate HTML | Embedded |
| **Best For** | Scripts, automation | Demos, exploration |

**Both interfaces are valuable!**
- Use **CLI** for automation and scripting
- Use **GUI** for presentations and exploration

## 🐛 Troubleshooting

### Port Already in Use
```powershell
streamlit run streamlit_app.py --server.port=8502
```

### Browser Doesn't Open
- Manually navigate to `http://localhost:8501`
- Check firewall settings

### Upload Fails
- Check file size (Streamlit has 200MB default limit)
- Verify file format is supported
- Try clearing browser cache

### Maps Don't Display
- Check internet connection (for map tiles)
- Ensure Folium is installed
- Try refreshing the page

## 📖 Additional Resources

### Streamlit Documentation
- Official docs: https://docs.streamlit.io
- Gallery of examples
- Component library

### Customization
The `streamlit_app.py` file can be customized:
- Change colors in CSS section
- Modify layout structure
- Add new features
- Adjust styling

## 🎉 Benefits of GUI Version

### For Students
- ✅ Learn modern web development
- ✅ More impressive in presentations
- ✅ Easier to share with classmates
- ✅ Portfolio-worthy project

### For Investigators
- ✅ Quick file analysis
- ✅ No command-line knowledge needed
- ✅ Visual presentation of evidence
- ✅ Easy to demonstrate findings

### For Privacy Users
- ✅ Check files before sharing
- ✅ Clean metadata easily
- ✅ No technical skills required
- ✅ Instant feedback

## 🚀 Getting Started Now

**Open terminal in project directory:**
```powershell
cd "b:\MSc\Module IV\MST 8407 Forensic Data Acquisition and Analysis, DF - Mr Nelson Mutua\Course Project"
```

**Launch the web interface:**
```powershell
streamlit run streamlit_app.py
```

**Your browser should open automatically!**

If not, navigate to: `http://localhost:8501`

---

## 📝 Quick Reference

### Start GUI
```powershell
streamlit run streamlit_app.py
```

### Stop GUI
Press `Ctrl+C` in the terminal

### Restart GUI
Press `R` in the browser or `Ctrl+C` then restart

### Clear Cache
Press `C` in the browser or click "Clear cache" in settings

---

**Enjoy the modern web interface! 🎨✨**

Perfect for:
- 🎓 Class presentations
- 🔍 Quick analysis
- 🧹 Metadata cleaning
- 📊 Professional reports
