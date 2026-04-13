import glob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# Data Loading
# ============================================================

def load_data() -> pd.DataFrame:
    """Read all woche_X.csv files and combine into one DataFrame."""
    files = sorted(glob.glob("woche_*.csv"))
    frames = []
    for f in files:
        df = pd.read_csv(f)
        week_num = int(f.split("_")[1].split(".")[0])
        df["woche"] = week_num
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    combined["datum"] = pd.to_datetime(combined["datum"])
    combined = combined.sort_values("datum").reset_index(drop=True)
    return combined


# ============================================================
# Helper Functions
# ============================================================

def fmt_duration(minutes: int) -> str:
    """Convert minutes to a readable string, e.g. 185 → '3h 5min'."""
    h, m = divmod(int(minutes), 60)
    if h and m:
        return f"{h}h {m}min"
    if h:
        return f"{h}h"
    return f"{m}min"


WEEKDAY_LABELS = {
    0: "Montag", 1: "Dienstag", 2: "Mittwoch", 3: "Donnerstag", 4: "Freitag", 5: "Samstag", 6: "Sonntag"
}

# Varied, pleasant palette for categorical use
PALETTE = [
    "#5B8DB8", "#E07B54", "#6BAE75", "#C97CB4",
    "#E8C84A", "#7ECECA", "#D47575", "#9B7FD4",
]


# ============================================================
# Data Processing
# ============================================================

def melt_apps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reshape the wide app columns into a long DataFrame with one row
    per (date, app) combination.

    Returns columns: datum, woche, app, minutes
    """
    records = []
    for _, row in df.iterrows():
        for i in range(1, 6):
            app = row.get(f"app{i}_name")
            mins = row.get(f"app{i}_zeit")
            if pd.notna(app) and pd.notna(mins):
                records.append({
                    "datum": row["datum"],
                    "woche": row["woche"],
                    "app": str(app).strip(),
                    "minutes": int(mins),
                })
    return pd.DataFrame(records)


def filter_by_week(df: pd.DataFrame, week: str) -> pd.DataFrame:
    """Return rows matching the selected week filter ('Alle' = no filter)."""
    if week == "Alle":
        return df
    week_num = int(week.split(" ")[1])
    return df[df["woche"] == week_num]


def top_apps(app_df: pd.DataFrame, n: int = 8) -> pd.DataFrame:
    """Aggregate total minutes per app, return top-n sorted descending."""
    return (
        app_df.groupby("app", as_index=False)["minutes"]
        .sum()
        .sort_values("minutes", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def weekly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """Total and average daily screen time per week."""
    return (
        df.groupby("woche")["gesamte bildschirmzeit"]
        .agg(gesamt="sum", durchschnitt="mean")
        .reset_index()
    )


def weekday_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """Average screen time by day of week (0=Mo … 6=So)."""
    tmp = df.copy()
    tmp["weekday"] = tmp["datum"].dt.dayofweek
    agg = tmp.groupby("weekday")["gesamte bildschirmzeit"].mean().reset_index()
    agg["label"] = agg["weekday"].map(WEEKDAY_LABELS)
    return agg.sort_values("weekday")


# ============================================================
# Charts
# ============================================================

_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=10, b=10),
)


def chart_daily(df: pd.DataFrame) -> go.Figure:
    """Area chart of daily total screen time."""
    fig = px.area(
        df,
        x="datum",
        y="gesamte bildschirmzeit",
        labels={"datum": "", "gesamte bildschirmzeit": "Minuten"},
        color_discrete_sequence=["#5B8DB8"],
    )
    # Custom hover using formatted duration
    durations = [fmt_duration(int(v)) for v in df["gesamte bildschirmzeit"]]
    fig.update_traces(
        customdata=durations,
        hovertemplate="<b>%{x|%d. %b}</b><br>%{customdata}<extra></extra>",
        line_color="#3a6d9a",
        fillcolor="rgba(91,141,184,0.25)",
    )
    fig.update_layout(
        **_LAYOUT,
        yaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
    )
    return fig


def chart_top_apps(app_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of top apps — each app gets its own color."""
    data = top_apps(app_df)
    data["label"] = data["minutes"].apply(fmt_duration)
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(data))]
    fig = go.Figure(go.Bar(
        x=data["minutes"],
        y=data["app"],
        orientation="h",
        text=data["label"],
        textposition="outside",
        marker_color=colors,
        customdata=data["label"],
        hovertemplate="<b>%{y}</b><br>%{customdata}<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT,
        yaxis=dict(autorange="reversed"),
        xaxis=dict(
            gridcolor="rgba(128,128,128,0.15)",
            title="Minuten",
        ),
    )
    return fig


def chart_weekly_comparison(df: pd.DataFrame) -> go.Figure:
    """Bar chart for weekly totals + line for daily average."""
    wt = weekly_totals(df)
    labels = [f"Woche {w}" for w in wt["woche"]]

    fig = go.Figure()
    gesamt_labels = [fmt_duration(v) for v in wt["gesamt"]]
    avg_labels = [fmt_duration(round(v)) for v in wt["durchschnitt"]]
    fig.add_bar(
        x=labels,
        y=wt["gesamt"],
        name="Gesamt",
        marker_color="#5B8DB8",
        text=gesamt_labels,
        textposition="outside",
        customdata=gesamt_labels,
        hovertemplate="<b>%{x}</b><br>Gesamt: %{customdata}<extra></extra>",
        yaxis="y1",
    )
    fig.add_scatter(
        x=labels,
        y=wt["durchschnitt"],
        name="Tagesdurchschnitt",
        mode="lines+markers+text",
        line=dict(color="#E07B54", width=2.5),
        marker=dict(size=8),
        text=avg_labels,
        textposition="top center",
        textfont=dict(color="#E07B54"),
        customdata=avg_labels,
        hovertemplate="<b>%{x}</b><br>Ø pro Tag: %{customdata}<extra></extra>",
        yaxis="y2",
    )
    fig.update_layout(
        **_LAYOUT,
        barmode="group",
        yaxis=dict(
            title="Gesamt (Min.)",
            gridcolor="rgba(128,128,128,0.15)",
        ),
        yaxis2=dict(
            title="Ø pro Tag (Min.)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def chart_weekday_pattern(df: pd.DataFrame) -> go.Figure:
    """Bar chart of average screen time by weekday, colored by intensity."""
    wd = weekday_pattern(df)
    vals = wd["gesamte bildschirmzeit"].tolist()
    # Map values to a blue color scale (lighter = less, darker = more)
    min_v, max_v = min(vals), max(vals)
    def intensity_color(v):
        t = (v - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        r = int(91 + (28 - 91) * t)
        g = int(141 + (80 - 141) * t)
        b = int(184 + (154 - 184) * t)
        return f"rgb({r},{g},{b})"

    colors = [intensity_color(v) for v in vals]
    dur_labels = [fmt_duration(round(v)) for v in vals]
    fig = go.Figure(go.Bar(
        x=wd["label"],
        y=vals,
        text=dur_labels,
        textposition="outside",
        marker_color=colors,
        customdata=dur_labels,
        hovertemplate="<b>%{x}</b><br>Ø %{customdata}<extra></extra>",
    ))
    fig.update_layout(
        **_LAYOUT,
        xaxis=dict(title=""),
        yaxis=dict(
            title="Ø Minuten",
            gridcolor="rgba(128,128,128,0.15)",
        ),
    )
    return fig


def chart_app_trend(app_df: pd.DataFrame, top_n: int = 5) -> go.Figure:
    """Line chart showing weekly minutes for the top-N apps overall."""
    overall_top = top_apps(app_df, n=top_n)["app"].tolist()
    filtered = app_df[app_df["app"].isin(overall_top)]
    weekly = filtered.groupby(["woche", "app"], as_index=False)["minutes"].sum()
    weekly["duration"] = weekly["minutes"].apply(fmt_duration)
    fig = px.line(
        weekly,
        x="woche",
        y="minutes",
        color="app",
        markers=True,
        custom_data=["app", "duration"],
        labels={"woche": "Woche", "minutes": "Minuten", "app": "App"},
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Woche %{x}<br>%{customdata[1]}<extra></extra>"
    )
    fig.update_layout(
        **_LAYOUT,
        xaxis=dict(
            tickvals=[1, 2, 3, 4],
            ticktext=["Woche 1", "Woche 2", "Woche 3", "Woche 4"],
        ),
        yaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def chart_app_share(app_df: pd.DataFrame) -> go.Figure:
    """Pie chart of app share by total minutes (top 7 + Sonstige)."""
    data = top_apps(app_df, n=7)
    total = app_df["minutes"].sum()
    top_total = data["minutes"].sum()
    rest = total - top_total
    if rest > 0:
        data = pd.concat([
            data,
            pd.DataFrame([{"app": "Sonstige", "minutes": rest}])
        ], ignore_index=True)
    fig = go.Figure(go.Pie(
        labels=data["app"],
        values=data["minutes"],
        hole=0.4,
        textinfo="label+percent",
        marker=dict(colors=PALETTE[:len(data)]),
    ))
    hover_durations = [fmt_duration(int(v)) for v in data["minutes"]]
    fig.update_traces(
        customdata=hover_durations,
        hovertemplate="<b>%{label}</b><br>%{customdata}<br>%{percent}<extra></extra>",
    )
    fig.update_layout(
        **_LAYOUT,
        showlegend=False,
    )
    return fig


# ============================================================
# Weekly File Viewer
# ============================================================

def show_weekly_raw(df_raw: pd.DataFrame) -> None:
    """Dropdown to pick a week and display its CSV data in German."""
    st.subheader("Wochendaten")
    woche_nr = st.selectbox(
        "Woche auswählen",
        options=[1, 2, 3, 4],
        format_func=lambda w: f"Woche {w}",
        key="raw_woche_select",
    )
    week_df = df_raw[df_raw["woche"] == woche_nr].copy()
    week_df["datum"] = week_df["datum"].dt.strftime("%d.%m.%Y")

    # Build a readable table: date + gesamtzeit + top-5 apps as "App (min)" strings
    rows = []
    for _, r in week_df.iterrows():
        apps = []
        for i in range(1, 6):
            name = r.get(f"app{i}_name")
            mins = r.get(f"app{i}_zeit")
            if pd.notna(name) and pd.notna(mins):
                apps.append(f"{name} ({fmt_duration(int(mins))})")
        rows.append({
            "Datum": r["datum"],
            "Bildschirmzeit": fmt_duration(int(r["gesamte bildschirmzeit"])),
            "Top Apps": " · ".join(apps),
        })

    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


# ============================================================
# Streamlit UI
# ============================================================

st.set_page_config(
    page_title="Bildschirmzeit",
    page_icon="📱",
    layout="wide",
)

st.title("📱 Bildschirmzeit Dashboard")
st.caption("16. März – 12. April 2025 · 4 Wochen Bildschirmzeit-Daten")

# --- Daten laden ---
df_raw = load_data()
app_df_all = melt_apps(df_raw)

# --- Seitenleiste ---
with st.sidebar:
    st.header("Filter")
    week_options = ["Alle"] + [f"Woche {i}" for i in sorted(df_raw["woche"].unique())]
    selected_week = st.selectbox("Woche", week_options)

df = filter_by_week(df_raw, selected_week)
app_df = filter_by_week(app_df_all, selected_week)

# --- Kennzahlen ---
total_mins = int(df["gesamte bildschirmzeit"].sum())
avg_daily = df["gesamte bildschirmzeit"].mean()
max_row = df.loc[df["gesamte bildschirmzeit"].idxmax()]
top_app = app_df.groupby("app")["minutes"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Gesamte Bildschirmzeit", fmt_duration(total_mins))
col2.metric("Tagesdurchschnitt", fmt_duration(round(avg_daily)))
col3.metric("Längster Tag", f"{max_row['datum'].strftime('%d. %b')} · {fmt_duration(int(max_row['gesamte bildschirmzeit']))}")
col4.metric("Meist genutzte App", top_app)

st.divider()

# --- Tägliche Bildschirmzeit ---
st.subheader("Tägliche Bildschirmzeit")
st.plotly_chart(chart_daily(df), width="stretch")

st.divider()

# --- App-Aufteilung + Wochentag-Muster ---
left, right = st.columns(2)

with left:
    st.subheader("App-Aufteilung")
    st.plotly_chart(chart_app_share(app_df), width="stretch")

with right:
    st.subheader("Ø Bildschirmzeit pro Wochentag")
    st.plotly_chart(chart_weekday_pattern(df), width="stretch")

st.divider()

# --- Top Apps ---
st.subheader("Top Apps")
st.plotly_chart(chart_top_apps(app_df), width="stretch")

st.divider()

# --- Wochenvergleich & Trends (nur bei "Alle") ---
if selected_week == "Alle":
    left2, right2 = st.columns(2)

    with left2:
        st.subheader("Wochenvergleich")
        st.plotly_chart(chart_weekly_comparison(df_raw), width="stretch")

    with right2:
        st.subheader("App-Trends nach Woche")
        st.plotly_chart(chart_app_trend(app_df_all), width="stretch")

    st.divider()

# --- Wochendaten ---
show_weekly_raw(df_raw)
