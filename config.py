from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDER = BASE_DIR / "data"
CHART_FOLDER = BASE_DIR / "charts"
OUTPUT_FOLDER = BASE_DIR / "output"
REFERENCE_FOLDER = BASE_DIR / "reference"
SYMBOL_FOLDER = BASE_DIR / "symbols"

CSV_FILE = SYMBOL_FOLDER / "nifty500.csv"

INTERVAL = "1d"

PERIOD = "6mo"

MAX_WORKERS = 10
NUMBER_OF_CANDLES = 100

CHART_STYLE = "charles"
SIMILARITY_THRESHOLD = 85

TOP_RESULTS = 20

folders = [
    DATA_FOLDER,
    CHART_FOLDER,
    OUTPUT_FOLDER,
    REFERENCE_FOLDER,
]

for folder in folders:
    folder.mkdir(exist_ok=True)