# Dock Control
## Installation

python3.12 -m venv .venv
source .venv/bin/activate      (si sur Windows : .venv\Scripts\activate) 
pip install -r requirements.txt

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

Documentation : http://127.0.0.1:8000/docs