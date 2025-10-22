# Folder Structure

This project is organized into the following directories:

## 📁 Directory Organization

```
forensic/
├── reports/                    # Input forensic reports
│   └── sample_report.txt      # Example forensic report
├── outputs/                    # Analysis results
│   ├── summary_*.txt          # Human-readable summary reports
│   └── forensic_analysis_*.json # Detailed JSON analysis results
├── forensic_analyzer.py       # Main analysis script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## 📋 Usage

### Input Reports
- Place your forensic report text files in the `reports/` folder
- Supported formats: `.txt` files
- Example: `reports/incident_report_2024.txt`

### Output Files
- **Summary Reports**: Automatically saved to `outputs/` folder
  - Format: `summary_[filename]_[timestamp].txt`
  - Contains: Attack narrative and kill chain mapping
  - Human-readable format

- **Detailed JSON**: Optional detailed analysis
  - Format: `forensic_analysis_[filename]_[timestamp].json`
  - Contains: Complete artifacts and structured data
  - Use `--output-json` flag to generate

### Examples

```bash
# Analyze a report from the reports folder
python forensic_analyzer.py reports/my_incident.txt

# Generate both summary and detailed JSON
python forensic_analyzer.py reports/my_incident.txt --output-json

# Analyze any report file
python forensic_analyzer.py /path/to/any/report.txt
```

## 🔧 Automatic Features

- **Auto-creates directories**: If `outputs/` doesn't exist, it's created automatically
- **Timestamped files**: All output files include timestamps to prevent overwrites
- **Organized structure**: Clear separation between input and output files
- **Unique filenames**: Each analysis gets a unique filename based on source and timestamp

## 📊 Output Types

1. **Console Output**: Real-time analysis progress and results
2. **Summary Report**: Text file with attack narrative and kill chain mapping
3. **JSON Analysis**: Complete structured data for programmatic use (optional)
