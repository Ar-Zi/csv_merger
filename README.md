# CSV File Merger

A web application to combine multiple CSV files while preserving the header from the first file.

## Features

- 📁 Upload multiple CSV files
- 🔗 Combine them while preserving the first file's header
- 💾 Download the merged CSV instantly
- ⚡ Handles quoted fields, embedded line breaks, and multiple line endings
- 🌐 Web-based interface via Streamlit

## Installation

### Local Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd scopus_csv_merger
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Local Development

Run the app locally:
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Streamlit Community Cloud

1. Push your code to a GitHub repository
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repository
3. Select the branch and file: `streamlit_app.py`
6. Click "Deploy"

The app will be live at `https://<your-username>-<repo-name>.streamlit.app`

## How to Use

1. Click "Upload CSV files to combine"
2. Select 2 or more CSV files
3. (Optional) Change the output filename
4. Click "Combine Files"
5. Click "Download Combined CSV" to get your merged file

## Technical Details

The merger:
- Preserves the header row from the first file
- Skips headers in subsequent files
- Maintains original encoding and line endings
- Handles quoted fields with embedded commas and line breaks
- Properly escapes double quotes

## Requirements

- Python 3.7+
- Streamlit 1.28.0+

## License

MIT License
