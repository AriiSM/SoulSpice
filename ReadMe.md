## Configurare și instalare

### Backend (FastAPI)

1. Navighează în server:
```bash
cd Server
```

2. Creează un mediu virtual Python și activează-l:
```bash
python -m venv venv
source venv/bin/activate        # Pentru Linux/macOS
venv\Scripts\activate           # Pentru Windows
```

3. Instalează dependințele:
```bash
pip install -r requirements.txt
```

4. Pornește serverul:
```bash
python main.py
```

Serverul va rula la adresa http://localhost:8000. Poți accesa documentația API la http://localhost:8000/docs.

### Frontend (React)

1. Instalează dependințele:
```bash
cd Client
npm install
```

2. Pornește aplicația React:
```bash
npm start
```
