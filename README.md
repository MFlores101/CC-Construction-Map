# 🚦 2025 Islander Hackathon Project  
## 🧠 Corpus Christi Road Construction AI  

### 👥 Team Information  
**Team Name:** MRRC  
**Team Members:** Christian Estrada, Michael Flores, Rean Supena, Ricardo Vela  

---

### 📍 Project Overview  
For the **2025 Islander Hackathon**, our team developed a program addressing the ongoing issue of **road construction across Corpus Christi**. 🏗️  

This project leverages **AI-powered APIs** 🤖 to **detect and help users avoid construction zones** throughout the greater Corpus area. By improving public awareness of road closures, the system aims to **reduce traffic congestion** 🚗💨 and enhance **commute efficiency** 🚦.  

---

### 💼 Purpose  
Our solution performs a valuable **civic service** by integrating the capabilities of **OpenAI** 🧠 and **Geocode** 🗺️ APIs — combining intelligent language processing with geospatial mapping technology to deliver accurate, real-time information to users.  

---

### ⚙️ Challenges  
One of the most significant challenges encountered during development was managing **false positives** ⚠️ produced by OpenAI’s API when interpreting Geocode data. This proved difficult because the two systems did not initially integrate as smoothly as anticipated.  

---

### 🚀 Future Plans  
Looking ahead 🔭, our team plans to **further refine and expand** the project to achieve its full potential. Due to the **limited timeframe** ⏳ of the hackathon, we simplified several planned features to ensure functionality and meet submission requirements.  

Despite these limitations, we are committed to **continuing development** and realizing the complete vision for this application. 💪✨  
---

### 🎥 Project Demo Video

[![Watch the video](https://img.youtube.com/vi/X_HlqYLm7Xk/0.jpg)](https://youtu.be/X_HlqYLm7Xk)

---

### 🏁 Summary  
This project demonstrates how **AI and mapping technologies** can be combined to provide real-world, practical solutions that improve community mobility and public awareness. 🌎💡  

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
