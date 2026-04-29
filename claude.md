# 📱 Screen Time Dashboard — Project Documentation

## 📌 Project Summary
A **Streamlit web application** that visualizes iPhone screen time data.
The user enters weekly screen time data via CSV files, and the app analyzes and visualizes the data over the semester.

---

## 📁 Project Structure
```
project/
│
├── data/
│   ├── woche_1.csv
│   ├── woche_2.csv
│   ├── woche_3.csv
│   └── woche_4.csv
│
├── app.py               ← Main Streamlit application
├── requirements.txt     ← Required libraries
└── claude.md            ← This file
```

---

## 📊 CSV Format
One CSV file per week. Each row = 1 day.

```
datum, gesamte bildschirmzeit, app1_adi, app1_sure, app2_adi, app2_sure, app3_adi, app3_sure, app4_adi, app4_sure, app5_adi, app5_sure
```

| Column | Description | Example |
|---|---|---|
| `datum` | Date (YYYY-MM-DD) | 2025-03-16 |
| `gesamte bildschirmzeit` | Daily total screen time (minutes) | 356 |
| `app1_adi` | Most used app of the day (1st) | Instagram |
| `app1_sure` | Usage time of that app (minutes) | 106 |
| ... | (app2 → app5 same logic) | ... |

---

## 🖥️ App Pages

### 1️⃣ Overview (All Weeks)
- Daily screen time across all weeks → **line chart** 📈
- Weekly total screen time comparison → **bar chart** 📊
- Average daily usage, longest/shortest day → **metric cards** 🃏

### 2️⃣ Weekly Detail
- Select week via dropdown (Week 1, 2, 3...)
- Daily breakdown for that week → **bar chart**
- Top 5 apps for that week → **horizontal bar chart**
- Daily app distribution → **stacked bar chart**

### 3️⃣ App Analysis
- Which apps appeared most across all weeks → **bar chart**
- Time trend per app → **line chart**

---

## 🛠️ Libraries Used

```txt
streamlit
pandas
plotly
glob
logging
black
```

---

## 🔧 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the app
streamlit run app.py
```

---

## 🔄 Development Workflow

> For every task: **Develop → Format → Commit → Push → Merge → Next task**

1. Create a new branch: `git checkout -b feature/task-name`
2. Develop the feature
3. Format code: `python -m black app.py`
4. Test the app: `streamlit run app.py`
5. Commit: `git add app.py && git commit -m "..."`
6. Push branch: `git push origin feature/task-name`
7. Merge to main: `git checkout main && git merge --no-ff feature/task-name`
8. Push main: `git push origin main`
9. Move to next sprint

---

## 🏃 Sprint Plan

| Sprint | Branch | Task | Status |
|---|---|---|---|
| 0 | `feature/data-loading` | Data loading + helper functions | ✅ Done |
| 0 | `feature/charts` | All charts and visualizations | ✅ Done |
| 0 | `feature/weekly-viewer` | Weekly raw data viewer | ✅ Done |
| 1 | `feature/csv-upload` | CSV file upload via UI | ✅ Done |
| 2 | `feature/error-handling` | try/except error handling | ✅ Done |
| 3 | `feature/logging` | Python logging module | ✅ Done |
| 4 | `feature/formatting` | Code formatting with Black | ✅ Done |

---

## 📋 To-Do List

- [x] Define CSV format
- [x] Enter data for Weeks 1–4
- [x] Write `app.py` → Streamlit application
- [x] Write `requirements.txt`
- [x] Build Overview page
- [x] Build Weekly Detail page
- [x] Build App Analysis page
- [x] Test the app
- [x] CSV file upload via UI
- [x] Error handling (try/except)
- [x] Logging
- [x] Code formatting (Black)

---

## ⚠️ Notes
- All durations are stored in **minutes** in the CSV
- The app automatically converts minutes → hours + minutes for display (e.g. 185 min → 3h 5min)
- The app UI language is **German**
- Each week's CSV file must follow the `woche_X.csv` naming format
- When a new CSV is added to the `data/` folder, the app reads it automatically
- Keep the code simple and easy to understand — no unnecessary complexity
