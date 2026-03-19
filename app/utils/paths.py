import os
import sys

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(APP_DIR)
SERVER_SCRIPT = os.path.join(APP_DIR, "server.py")

PYTHON_EXE = os.path.join(BASE_DIR, "venv", "bin", "python3")
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = sys.executable

FAISS_DIR = os.path.join(APP_DIR, "faiss_index")
FAISS_INDEX_PATH = os.path.join(FAISS_DIR, "index.faiss")

DATABASE_FILE = os.path.join(APP_DIR, "modules", "database", "crm.db")
