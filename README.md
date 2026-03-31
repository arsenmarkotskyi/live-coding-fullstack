# Live coding - Full Stack Engineer

![work-smart-not-hard.svg](assets/work-smart-not-hard.svg)

Task: complete the following steps:

* Create the front-end for the application - visualize the database with alerts: `db.sqlite`.
* API: allow filtering alerts database by column `project`.
* Front-end: add filtering to frontend by connecting backend instead of usage mocked data.

---

## Backend (FastAPI)

### Run

```bash
python -m venv .venv
# On Unix/MacOS:
source .venv/bin/activate 
# On Windows: 
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

---
## Frontend (Vue.js)

### Run

```bash
npm install
npm run dev
```
