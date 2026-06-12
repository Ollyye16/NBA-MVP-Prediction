# 🏀 NBA MVP Prediction & Analysis

> 📚 **University Project** — Feng Chia University, Department of Applied Mathematics, 2023

A data analysis project that scrapes historical NBA MVP data, stores it in a database, and provides a REST API for data access and statistical visualization.

## Overview

This project was developed as part of my undergraduate studies at Feng Chia University in 2023. It analyzes historical NBA MVP winners from ESPN data to identify statistical trends and patterns. It includes web scraping, database storage, a Flask REST API, and data visualization.

## Features

- **Web Scraping** — Automatically scrapes NBA MVP history from ESPN
- **Database Storage** — Stores player statistics in SQL database
- **REST API** — Flask-based API endpoints for data access
- **Data Visualization** — Statistical trend analysis using seaborn and matplotlib
  - Field goal percentage trends over the years
  - Points per game (PPG) analysis
  - Rebounds per game (RPG) analysis
  - Assists per game (APG) analysis
  - Blocks per game (BLK) analysis

## Tech Stack

- **Language:** Python
- **Web Scraping:** BeautifulSoup, Requests
- **API:** Flask
- **Database:** SQL Server / SQLite
- **Data Analysis:** Pandas
- **Visualization:** Matplotlib, Seaborn

## Dataset

| File | Description |
|------|-------------|
| `MVP Rankings.csv` | Historical NBA MVP rankings |
| `NBA Data/Player Game Data.csv` | Individual player game statistics |
| `NBA Data/Team Games Played.csv` | Team game records |
| `Top Scorers Per Team.csv` | Top scorers for each team |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/players` | GET | Returns all MVP player data |
| `/api/analysis` | GET | Returns statistical analysis results |

## Installation

```bash
pip install requests beautifulsoup4 flask pandas matplotlib seaborn pyodbc
python nba_analysis.py
```

## Analysis Results

The project analyzes correlations between MVP awards and key statistics:
- How scoring trends have evolved among MVP winners
- The relationship between efficiency (FG%) and MVP selection
- Historical patterns in rebounding and assists for MVP players

## Author

**Chun-Yu Yeh (Olly)**  
Backend Software Engineer | Applied Mathematics  
Feng Chia University, Class of 2023  
GitHub: [Ollyye16](https://github.com/Ollyye16)
