# Theory of Computation - Pokemon Web Crawler

This project is a comprehensive Pokémon Pokédex built with FastAPI, created as part of the Theory of Computation course to demonstrate the practical usage and implementation of **Regular Expressions** for web scraping. It scrapes data in real-time from [PokemonDB](https://pokemondb.net/pokedex/) and presents it through a web interface.

**Key Features:**

- **Live Data Crawling:** Fetches the latest Pokémon data on-demand using regular expressions.
- **Interactive Pokédex:** Browse and search for Pokémon with detailed stats, descriptions, and images.
- **CSV Export:** Download the entire Pokémon dataset or a filtered search result as a CSV file.

> **⚠️ Note:** The downloaded CSV data may contain inaccuracies or formatting issues due to special characters (such as é, ♂, ♀, apostrophes, and other unicode characters) in Pokémon names and descriptions. Please verify the data if accuracy is critical for your use case.

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/NongKenKhung/Theory_of_Computation
cd Theory_of_Computation
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:

- `fastapi[standard]` - Web framework
- `requests` - HTTP library for web scraping
- `pandas` - Data manipulation and CSV generation

## Running the Application

### 1. Start the Development Server

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Run the FastAPI development server
fastapi dev main.py
```

### 2. Start the Production Server

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Run the FastAPI production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

> **Note:** In production environments (e.g., Heroku), the port is typically provided via the `PORT` environment variable. The application will automatically use it.

## License

This project is for educational purposes as part of Theory of Computation coursework.

## Data Source

Pokemon data is scraped from [PokemonDB](https://pokemondb.net/pokedex/). Please respect their terms of service and use responsibly.
