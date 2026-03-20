# London Rent Scraper

A simple Python project for scraping rental listings from OpenRent, extracting rent and bedroom data, and generating a PDF report.

## Features

- Scrape rental listings by area
- Extract rent price and bedroom count
- Save raw data to CSV
- Analyze average and median rent by area
- Generate a PDF report

## Project Structure

- `main.py` — runs the scraper and analysis
- `src/scraper.py` — collects listing data from OpenRent
- `src/parser.py` — extracts rent and bedroom information
- `src/analysis.py` — analyzes the data and creates the PDF report

## Requirements

Install dependencies with:

    pip install -r requirements.txt

## How to Run

    python main.py

## Output

- Raw scraped data: `data/raw_data.csv`
- PDF report: `output/bedroom_rent_report.pdf`