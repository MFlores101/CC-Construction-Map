#!/usr/bin/env python3
"""
Construction Data Extractor using OpenAI API
Reads webpages and extracts construction information for Corpus Christi area.
"""

import requests
from openai import OpenAI
import json
import sys
import os
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class ConstructionExtractor:
    def __init__(self, openai_api_key: str):
        """Initialize the extractor with OpenAI API key."""
        self.client = OpenAI(api_key=openai_api_key)
        
    def fetch_webpage(self, url: str) -> str:
        """
        Fetch webpage content and extract text.
        
        Args:
            url: The URL of the webpage to fetch
            
        Returns:
            Extracted text content from the webpage
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML and extract text
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except requests.RequestException as e:
            print(f"Error fetching webpage: {e}", file=sys.stderr)
            return ""
    
    def extract_construction_data(self, webpage_text: str, url: str = "") -> List[Dict]:
        """
        Use OpenAI API to extract construction data from webpage text.
        
        Args:
            webpage_text: The text content from the webpage
            url: Optional URL for context
            
        Returns:
            List of dictionaries containing construction data
        """
        if not webpage_text:
            return []
        
        # Truncate text if too long (OpenAI has token limits)
        max_chars = 10000  # Roughly ~2500 tokens
        if len(webpage_text) > max_chars:
            webpage_text = webpage_text[:max_chars] + "... [content truncated]"
        
        prompt = f"""Analyze the following webpage content and extract all construction-related information for Corpus Christi, Texas area.

Extract the following information for each construction project/update mentioned:
- Location/Address (be as specific as possible, include street names, intersections, etc.)
- Type of construction (road work, building construction, utility work, etc.)
- Description of the work
- Dates/Timeline (start date, end date, duration if mentioned)
- Impact/Traffic information (lane closures, detours, etc.)
- Status (upcoming, ongoing, completed)

Webpage content:
{webpage_text}

Return the data as a JSON array of objects. Each object should have these fields:
- location: string (specific address or intersection)
- type: string (type of construction)
- description: string (what work is being done)
- dates: string (timeline information if available)
- impact: string (traffic impact or detour information)
- status: string (upcoming/ongoing/completed)

If no construction information is found, return an empty array [].
Return ONLY valid JSON, no other text."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts construction and traffic information from web content. Always return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            # Sometimes OpenAI wraps JSON in markdown code blocks
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            construction_data = json.loads(result_text)
            
            # Add source URL if provided
            if url and isinstance(construction_data, list):
                for item in construction_data:
                    if isinstance(item, dict):
                        item["source_url"] = url
            
            return construction_data if isinstance(construction_data, list) else []
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}", file=sys.stderr)
            print(f"Response was: {result_text}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"Error calling OpenAI API: {e}", file=sys.stderr)
            return []
    
    def process_url(self, url: str) -> List[Dict]:
        """
        Fetch a webpage and extract construction data.
        
        Args:
            url: The URL to process
            
        Returns:
            List of construction data dictionaries
        """
        print(f"Fetching webpage: {url}")
        webpage_text = self.fetch_webpage(url)
        
        if not webpage_text:
            print("Failed to fetch webpage content", file=sys.stderr)
            return []
        
        print(f"Extracted {len(webpage_text)} characters from webpage")
        print("Analyzing content with OpenAI...")
        
        construction_data = self.extract_construction_data(webpage_text, url)
        
        return construction_data


def generate_corpus_christi_url(date: datetime) -> str:
    """
    Generate Corpus Christi street closures URL for a given date.
    
    Args:
        date: The date to generate the URL for
        
    Returns:
        URL string in format: ...street-closures-and-traffic-impacts-[month]-[day]-[year]/
    """
    # Format date as: month-day-year (e.g., october-31-2025)
    month_name = date.strftime("%B").lower()
    # Remove leading zero from day (e.g., "31" not "31", but "7" not "07")
    day = str(date.day)  # This automatically removes leading zeros
    year = date.strftime("%Y")
    
    base_url = "https://www.corpuschristitx.gov/department-directory/public-works/street-closures-and-traffic-impacts"
    url = f"{base_url}/street-closures-and-traffic-impacts-{month_name}-{day}-{year}/"
    
    return url


def generate_weekly_urls(start_date: datetime = None, weeks_ahead: int = 4) -> List[str]:
    """
    Generate weekly URLs for Corpus Christi street closures.
    
    Args:
        start_date: Starting date (defaults to today)
        weeks_ahead: Number of weeks to generate URLs for (default 4 weeks)
        
    Returns:
        List of URLs
    """
    if start_date is None:
        start_date = datetime.now()
    
    urls = []
    current_date = start_date
    
    for week in range(weeks_ahead):
        url = generate_corpus_christi_url(current_date)
        urls.append(url)
        current_date += timedelta(days=7)
    
    return urls


def main():
    """Main function to run the construction extractor."""
    # OpenAI API key
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"
    
    extractor = ConstructionExtractor(OPENAI_API_KEY)
    all_construction_data = []
    urls_to_process = []
    
    # Check if user wants automatic weekly URLs or manual URLs
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Automatic mode: generate weekly URLs
        weeks = 4
        if len(sys.argv) > 2:
            try:
                weeks = int(sys.argv[2])
            except ValueError:
                print(f"Invalid number of weeks: {sys.argv[2]}. Using default: 4", file=sys.stderr)
        
        print(f"Generating weekly URLs for the next {weeks} weeks...")
        urls_to_process = generate_weekly_urls(weeks_ahead=weeks)
        
        print("\nGenerated URLs:")
        for url in urls_to_process:
            print(f"  - {url}")
    
    elif len(sys.argv) > 1 and sys.argv[1] == "--date":
        # Date mode: generate URLs starting from a specific date
        if len(sys.argv) < 3:
            print("Usage: python extract_construction.py --date YYYY-MM-DD [weeks_ahead]")
            print("Example: python extract_construction.py --date 2025-10-31 4")
            sys.exit(1)
        
        try:
            start_date = datetime.strptime(sys.argv[2], "%Y-%m-%d")
            weeks = int(sys.argv[3]) if len(sys.argv) > 3 else 4
            urls_to_process = generate_weekly_urls(start_date, weeks)
            
            print(f"\nGenerated URLs starting from {start_date.strftime('%B %d, %Y')}:")
            for url in urls_to_process:
                print(f"  - {url}")
        except ValueError as e:
            print(f"Error parsing date: {e}", file=sys.stderr)
            print("Date format should be YYYY-MM-DD (e.g., 2025-10-31)")
            sys.exit(1)
    
    elif len(sys.argv) > 1:
        # Manual mode: process provided URLs
        urls_to_process = sys.argv[1:]
    else:
        # Default: use auto mode with 4 weeks
        print("No arguments provided. Using automatic weekly URL generation (4 weeks).")
        print("Usage options:")
        print("  python extract_construction.py --auto [weeks]           # Auto-generate weekly URLs")
        print("  python extract_construction.py --date YYYY-MM-DD [weeks] # Start from specific date")
        print("  python extract_construction.py <url1> [url2] ...        # Manual URLs")
        print("\nRunning with --auto 4...")
        urls_to_process = generate_weekly_urls(weeks_ahead=4)
    
    # Process each URL
    for url in urls_to_process:
        print(f"\n{'='*60}")
        print(f"Processing: {url}")
        print('='*60)
        
        data = extractor.process_url(url)
        all_construction_data.extend(data)
        
        print(f"Found {len(data)} construction project(s)")
    
    # Output results
    print(f"\n{'='*60}")
    print(f"Total construction projects found: {len(all_construction_data)}")
    print('='*60)
    
    if all_construction_data:
        print("\nConstruction Data:")
        print(json.dumps(all_construction_data, indent=2, ensure_ascii=False))
        
        # Save to file
        output_file = "construction_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_construction_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to: {output_file}")
    else:
        print("No construction data found.")


if __name__ == "__main__":
    main()

