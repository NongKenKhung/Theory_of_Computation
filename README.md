# Theory of Computation - Pokemon Web Crawler

A FastAPI web application that crawls Pokemon data from [PokemonDB](https://pokemondb.net/pokedex/) and provides CSV download functionality.

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
