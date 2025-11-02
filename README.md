# CC-Construction-Map
Using AI API's to find and avoid construction in the greater Corpus area. For the 2025 Islander Hackathon.

## Features

- Automatically fetches construction updates from Corpus Christi city website
- Uses OpenAI API to extract structured construction data from webpages
- Automatically generates weekly URLs (adds 7 days for each week)
- Outputs JSON data with location, type, description, dates, impact, and status

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. **Configure API Keys:**
   - **Google Maps API Key**: Edit `index.html` and replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual Google Maps API key
   - **OpenAI API Key**: Either:
     - Edit `extract_construction.py` and replace `YOUR_OPENAI_API_KEY` with your actual key, OR
     - Set environment variable: `export OPENAI_API_KEY="your-key-here"`

## Usage

### Automatic Weekly Mode (Recommended)
Automatically generates URLs for the current week and upcoming weeks:

```bash
python extract_construction.py --auto 4
```

This will generate URLs for the next 4 weeks starting from today.

### Start from Specific Date
Generate URLs starting from a specific date:

```bash
python extract_construction.py --date 2025-10-31 4
```

This generates URLs starting from October 31, 2025, for 4 weeks:
- October 31, 2025
- November 7, 2025
- November 14, 2025
- November 21, 2025

### Manual URL Mode
Process specific URLs manually:

```bash
python extract_construction.py https://www.corpuschristitx.gov/.../street-closures-and-traffic-impacts-october-31-2025/
```

## Output

The script outputs:
- Console output with progress and extracted data
- `construction_data.json` file with all extracted construction information

Each construction project includes:
- **location**: Specific address or intersection
- **type**: Type of construction (road work, building construction, etc.)
- **description**: What work is being done
- **dates**: Timeline information
- **impact**: Traffic impact or detour information
- **status**: Upcoming/ongoing/completed
- **source_url**: URL where the information was found

## Viewing the Map

The HTML map displays all construction locations with color-coded markers:

1. **Run the server** (required for loading JSON data):
   ```bash
   python3 server.py
   ```
   This will automatically open your browser to `http://localhost:8000/index.html`

2. **Color Coding:**
   - 🟠 **Orange** - Road Work
   - 🔴 **Red** - Road Reconstruction  
   - 🔵 **Blue** - Utility Work
   - 🔷 **Cyan** - Storm Water Maintenance
   - 🟣 **Purple** - Building Renovation

3. **Features:**
   - Click any marker to see detailed construction information
   - Legend shows all construction types
   - Markers are automatically positioned using Google Geocoding API
