import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# MEDISYNTH | Hospital Discharge Intelligence
# Built for the NY State SPARCS Inpatient Discharges dataset
# ============================================================

st.set_page_config(
    page_title="MEDISYNTH | Hospital Intelligence",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual system ----------
BG = "#080F18"
PANEL = "#111D29"
PANEL_2 = "#152432"
BORDER = "#263747"
CYAN = "#22D3D0"
BLUE = "#438BFA"
LIME = "#B9E769"
VIOLET = "#9B83F6"
TEXT = "#EAF2F7"
MUTED = "#91A3B3"
PALETTE = [CYAN, BLUE, VIOLET, LIME, "#F3A76B", "#E879A8"]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {{ color-scheme: dark; }}
    html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
    .stApp {{ background: {BG}; color: {TEXT}; }}
    [data-testid="stHeader"] {{ background: rgba(8,15,24,0.92); }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0D1B28 0%, #09131D 100%);
        border-right: 1px solid {BORDER};
        min-width: 285px;
        max-width: 285px;
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT}; }}
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
        padding: 1.1rem 1rem 2rem 1rem;
        overflow-y: auto;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        border: 1px solid transparent;
        border-radius: 9px;
        padding: 7px 9px;
        margin: 3px 0;
        transition: background .15s ease, border-color .15s ease;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
        background: #172B3A;
        border-color: #294454;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
        background: #12323B;
        border-color: #247B80;
    }}
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] {{
        margin-bottom: .35rem;
    }}
    .block-container {{
        max-width: 1700px;
        padding: 1.4rem 2rem 3rem 2rem;
    }}
    @media (max-width: 900px) {{
        .block-container {{ padding: 1rem .9rem 2rem .9rem; }}
        [data-testid="stSidebar"] {{ min-width: 260px; max-width: 260px; }}
    }}
    h1,h2,h3,h4 {{ font-family: 'Manrope', sans-serif !important; color: {TEXT} !important; letter-spacing: -0.5px; }}
    p, label, span {{ color: inherit; }}
    div[data-testid="stMetric"] {{
        background: linear-gradient(145deg, {PANEL_2}, {PANEL});
        border: 1px solid {BORDER}; border-radius: 13px; padding: 15px 17px;
    }}
    div[data-testid="stMetricLabel"] {{ color: {MUTED} !important; font-size: 0.78rem; }}
    div[data-testid="stMetricValue"] {{ color: {TEXT} !important; font-family: 'Manrope'; font-weight: 750; }}
    div[data-testid="stMetricDelta"] {{ font-size: 0.72rem; }}
    [data-testid="stTabs"] button {{ color: {MUTED}; font-weight: 600; }}
    [data-testid="stTabs"] button[aria-selected="true"] {{ color: {CYAN}; border-bottom-color: {CYAN}; }}
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {{ background: {PANEL_2}; border-color: {BORDER}; }}
    .brand {{ display:flex; align-items:center; gap:11px; padding: 8px 2px 17px 2px; min-width:0; }}
    .brand-mark {{ flex:0 0 38px; width:38px; height:38px; display:grid; place-items:center; border-radius:11px;
       background:linear-gradient(135deg,{CYAN},{BLUE}); color:#06131D; font-weight:900; font-size:21px; }}
    .brand-copy {{ min-width:0; }}
    .brand-name {{ font-family:'Manrope'; font-size:19px; line-height:1.15; font-weight:800; letter-spacing:1px; white-space:nowrap; }}
    .brand-sub {{ color:{MUTED}; font-size:8px; letter-spacing:1.45px; white-space:nowrap; }}
    .eyebrow {{ color:{CYAN}; text-transform:uppercase; letter-spacing:2.2px; font-size:10px; font-weight:700; }}
    .hero {{ background:linear-gradient(110deg,#142B3A 0%,#10202D 58%,#132A35 100%);
       border:1px solid #294452; border-radius:16px; padding:25px 28px; margin: 4px 0 20px 0;
       min-height:132px; display:flex; flex-direction:column; justify-content:center; overflow-wrap:anywhere; }}
    .hero h1 {{ font-size:30px; margin:5px 0 4px 0; }}
    .hero p {{ color:#AFC0CD; margin:0; font-size:13px; }}
    .section-title {{ font-family:'Manrope'; color:{TEXT}; font-weight:750; font-size:17px; margin: 5px 0 2px; }}
    .section-sub {{ color:{MUTED}; font-size:11px; margin-bottom:10px; }}
    .panel {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:13px; padding:14px 16px; }}
    .insight {{ background:linear-gradient(135deg,#132B35,#14212D); border:1px solid #28515A;
       border-left:3px solid {CYAN}; border-radius:10px; padding:12px 14px; margin:7px 0; color:#DDEAF0; font-size:12px; }}
    .small-muted {{ color:{MUTED}; font-size:11px; }}
    .stButton button {{ border-radius:8px; border:1px solid {BORDER}; }}
    .stDownloadButton button {{ background:{CYAN}; color:#06131D; border:0; font-weight:700; border-radius:8px; }}
    [data-testid="stDataFrame"] {{ border:1px solid {BORDER}; border-radius:10px; overflow:hidden; }}
    [data-testid="stDataFrame"] * {{ font-size:12px; }}
    .stAlert {{ border-radius:10px; }}
    hr {{ border-color:{BORDER}; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Data loading ----------
DATA_PATH = Path(__file__).parent / "hospital_sample.csv"

@st.cache_resource(show_spinner="Loading the dashboard columns efficiently…")
def load_data(path: str, modified_time: float):
    """
    Load only fields used by the dashboard and store text columns as
    categoricals and numeric measures as float32 to reduce RAM use.
    The original CSV is never modified.
    """
    # Read only the header first so optional/missing columns are handled safely.
    header = pd.read_csv(path, nrows=0, encoding="utf-8-sig")
    available = [str(c).strip() for c in header.columns]

    wanted = [
        "Length of Stay",
        "Total Charges",
        "Total Costs",
        "Age Group",
        "Gender",
        "Race",
        "APR Severity of Illness Description",
        "CCSR Diagnosis Code",
        "CCSR Diagnosis Description",
        "Hospital County",
        "Payment Typology 1",
        "Facility Name",
    ]
    selected = [c for c in wanted if c in available]
    if not selected:
        raise ValueError("None of the expected dashboard columns were found in the CSV header.")

    category_columns = {
        c: "category"
        for c in selected
        if c not in ["Length of Stay", "Total Charges", "Total Costs"]
    }
    numeric_columns = {
        c: "float32"
        for c in selected
        if c in ["Length of Stay", "Total Charges", "Total Costs"]
    }
    dtype_map = {**category_columns, **numeric_columns}

    # The C parser and low_memory=True avoid pandas' large full-file inference buffer.
    data = pd.read_csv(
        path,
        usecols=selected,
        dtype=dtype_map,
        encoding="utf-8-sig",
        low_memory=True,
        memory_map=False,
    )
    data.columns = data.columns.astype(str).str.strip()
    return data


if not DATA_PATH.exists():
    st.error("The cleaned dataset file is missing.")
    st.write(f"Expected location: `{DATA_PATH}`")
    st.info("Place `hospital_sample.csv` in the same folder as `app.py`.")
    st.stop()

if DATA_PATH.stat().st_size == 0:
    st.error("`hospital_sample.csv` is empty.")
    st.stop()

try:
    df = load_data(str(DATA_PATH), DATA_PATH.stat().st_mtime)
except Exception as exc:
    st.error("MEDISYNTH could not load the dashboard columns.")
    st.write(f"File size: {DATA_PATH.stat().st_size / (1024 * 1024):,.2f} MB")
    with st.expander("Technical details", expanded=True):
        st.code(str(exc) if str(exc).strip() else repr(exc))
    st.info(
        "This version reads only the fields needed for the dashboard. "
        "If MemoryError persists, close other memory-heavy applications and "
        "we will switch to a disk-backed Parquet/chunked approach."
    )
    st.stop()


# Column helpers - keeps the app robust if optional fields are absent.
def has(col):
    return col in df.columns

def clean_options(frame, col):
    if col not in frame.columns:
        return []
    vals = frame[col].dropna().astype(str).str.strip()
    vals = vals[vals.ne("")]
    return sorted(vals.unique().tolist())

def money(value):
    return "—" if pd.isna(value) else f"${value:,.0f}"

def number(value):
    return "—" if pd.isna(value) else f"{value:,.0f}"

def chart_theme(fig, height=300):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=TEXT, size=11),
        margin=dict(l=12, r=12, t=35, b=12),
        height=height,
        legend=dict(orientation="h", y=-0.22, title=""),
        hoverlabel=dict(bgcolor="#132432", bordercolor=BORDER, font_color=TEXT),
    )
    fig.update_xaxes(gridcolor="#22313E", zerolinecolor="#22313E", linecolor="#304252")
    fig.update_yaxes(gridcolor="#22313E", zerolinecolor="#22313E", linecolor="#304252")
    return fig

# ---------- Sidebar / navigation + global filters ----------
FILTER_COLUMNS = {
    "County": "Hospital County",
    "Age group": "Age Group",
    "Gender": "Gender",
    "Severity": "APR Severity of Illness Description",
    "Payment type": "Payment Typology 1",
}

with st.sidebar:
    st.markdown(
        f"""<div class="brand">
        <div class="brand-mark">✚</div><div class="brand-copy">
        <div class="brand-name">MEDISYNTH</div>
        <div class="brand-sub">HOSPITAL INTELLIGENCE</div></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown('<div class="eyebrow">WORKSPACE</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate",
        ["Command Centre", "Clinical Analytics", "Hospital Network",
         "Financial Intelligence", "Data Explorer"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown('<div class="eyebrow">GLOBAL FILTERS</div>', unsafe_allow_html=True)
    st.caption("Filter every analysis view. Leave a field untouched to include all records.")
    selections = {}
    for label, col in FILTER_COLUMNS.items():
        if has(col):
            options = clean_options(df, col)
            selections[col] = st.multiselect(
                label, options, default=[], placeholder=f"All {label.lower()}",
                key=f"filter_{col}",
            )
    if st.button("↺ Reset all filters", use_container_width=True):
        for col in FILTER_COLUMNS.values():
            st.session_state.pop(f"filter_{col}", None)
        st.rerun()
    st.markdown("---")
    st.markdown('<div class="eyebrow">DATA SOURCE</div>', unsafe_allow_html=True)
    st.markdown("**NY State · SPARCS**")
    st.caption("Hospital Inpatient Discharges · 2021")
    st.markdown(
        f"""
        <div style="background:#132634;border:1px solid #294454;border-radius:11px;
                    padding:12px;margin:12px 0;">
          <div style="font-size:9px;letter-spacing:1.7px;color:{CYAN};font-weight:700;">
            DATA CONNECTION
          </div>
          <div style="font-size:12px;font-weight:700;margin-top:5px;color:{TEXT};">
            ● Dataset loaded
          </div>
          <div style="font-size:10px;color:{MUTED};margin-top:3px;">
            {len(df):,} records · {len(df.columns)} fields
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("↻ Refresh dataset", use_container_width=True):
        load_data.clear()
        st.rerun()

filtered = df
for col, selected in selections.items():
    if selected:
        filtered = filtered[filtered[col].astype(str).isin(selected)]

# ---------- Header ----------
st.markdown(
    """<div class="hero">
      <div class="eyebrow">✦ HEALTHCARE DATA / ANALYTICS PLATFORM</div>
      <h1>Hospital Intelligence</h1>
      <p>Explore inpatient discharge patterns, clinical complexity, hospital utilisation and financial trends across New York State.</p>
    </div>""",
    unsafe_allow_html=True,
)

# ---------- Metrics ----------
total = len(filtered)
avg_los = filtered["Length of Stay"].mean() if has("Length of Stay") else float("nan")
avg_charges = filtered["Total Charges"].mean() if has("Total Charges") else float("nan")
facilities = filtered["Facility Name"].nunique() if has("Facility Name") else 0
total_charges = filtered["Total Charges"].sum() if has("Total Charges") else float("nan")
median_los = filtered["Length of Stay"].median() if has("Length of Stay") else float("nan")
avg_costs = filtered["Total Costs"].mean() if has("Total Costs") else float("nan")

def metric_row():
    cols = st.columns(4)
    cols[0].metric("TOTAL DISCHARGES", number(total))
    cols[1].metric("AVG. LENGTH OF STAY", "—" if pd.isna(avg_los) else f"{avg_los:.2f} days")
    cols[2].metric("AVG. TOTAL CHARGES", money(avg_charges))
    cols[3].metric("HOSPITAL FACILITIES", number(facilities))

# ---------- Dynamic insight helper ----------
def insight_text():
    notes = []
    if has("Age Group") and len(filtered):
        age = filtered["Age Group"].astype("object").fillna("Unknown").astype(str).value_counts()
        if len(age):
            notes.append(f"The largest discharge age group in the current selection is **{age.index[0]}** ({age.iloc[0]:,} records).")
    if has("CCSR Diagnosis Description") and has("Length of Stay"):
        dx = filtered.dropna(subset=["CCSR Diagnosis Description", "Length of Stay"])
        if len(dx):
            top = dx.groupby("CCSR Diagnosis Description")["Length of Stay"].mean().nlargest(1)
            if len(top):
                notes.append(f"The diagnosis category with the highest average stay in this selection is **{top.index[0]}** ({top.iloc[0]:.2f} days).")
    if has("APR Severity of Illness Description") and has("Total Charges"):
        sev = filtered.dropna(subset=["APR Severity of Illness Description", "Total Charges"])
        if len(sev):
            top = sev.groupby("APR Severity of Illness Description")["Total Charges"].mean().nlargest(1)
            if len(top):
                notes.append(f"**{top.index[0]}** has the highest average charges among severity groups in this selection ({money(top.iloc[0])}).")
    return notes

# ---------- Page: Command Centre ----------
if page == "Command Centre":
    st.markdown('<div class="eyebrow">01 / OVERVIEW</div><div class="section-title">Discharge overview</div><div class="section-sub">Live calculations from the selected records — use the filters above to explore.</div>', unsafe_allow_html=True)
    metric_row()

    a, b, c = st.columns([1.05, 1.5, 1])
    with a:
        st.markdown('<div class="section-title">Patient mix</div><div class="section-sub">Discharges by age group</div>', unsafe_allow_html=True)
        if has("Age Group"):
            age = filtered["Age Group"].astype("object").fillna("Unknown").astype(str).value_counts().rename_axis("Age group").reset_index(name="Discharges")
            fig = px.pie(age, names="Age group", values="Discharges", hole=.66, color_discrete_sequence=PALETTE)
            fig.update_traces(textposition="inside", textinfo="percent")
            st.plotly_chart(chart_theme(fig, 285), use_container_width=True)
        else:
            st.info("Age Group field not available.")
    with b:
        st.markdown('<div class="section-title">Diagnostic data trends</div><div class="section-sub">Top diagnosis categories by discharge volume</div>', unsafe_allow_html=True)
        if has("CCSR Diagnosis Description"):
            dx = filtered["CCSR Diagnosis Description"].astype("object").fillna("Unknown").astype(str).value_counts().head(10).sort_values().reset_index()
            dx.columns = ["Diagnosis", "Discharges"]
            fig = px.bar(dx, x="Discharges", y="Diagnosis", orientation="h", color="Discharges",
                         color_continuous_scale=[[0, "#24556A"], [1, CYAN]])
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(chart_theme(fig, 285), use_container_width=True)
        else:
            st.info("Diagnosis description field not available.")
    with c:
        st.markdown('<div class="section-title">Network snapshot</div><div class="section-sub">Selected hospital footprint</div>', unsafe_allow_html=True)
        st.metric("Facilities represented", number(facilities))
        if has("Hospital County"):
            county_count = filtered["Hospital County"].nunique()
            st.metric("Counties represented", number(county_count))
        if has("Total Charges"):
            st.metric("Total charges", money(total_charges))
        if has("Total Costs"):
            st.metric("Average total costs", money(avg_costs))

    st.markdown("---")
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown('<div class="section-title">Length-of-stay distribution</div><div class="section-sub">How long inpatient stays lasted across the selected records</div>', unsafe_allow_html=True)
        if has("Length of Stay"):
            los = filtered["Length of Stay"].dropna()
            fig = px.histogram(los, x="Length of Stay", nbins=45, color_discrete_sequence=[CYAN])
            fig.update_traces(marker_line_color=BG, marker_line_width=.4)
            fig.update_layout(xaxis_title="Length of stay (days)", yaxis_title="Discharges")
            st.plotly_chart(chart_theme(fig, 300), use_container_width=True)
    with right:
        st.markdown('<div class="section-title">Analytical signals</div><div class="section-sub">Automatically calculated observations — not clinical predictions</div>', unsafe_allow_html=True)
        notes = insight_text()
        if notes:
            for note in notes[:3]:
                st.markdown(f'<div class="insight">✦ {note}</div>', unsafe_allow_html=True)
        else:
            st.info("Select a broader dataset or check that the relevant columns are present.")

# ---------- Page: Clinical Analytics ----------
elif page == "Clinical Analytics":
    st.markdown('<div class="eyebrow">02 / CLINICAL PATTERNS</div><div class="section-title">Clinical analytics</div><div class="section-sub">Explore diagnosis mix, length of stay and severity-associated charges.</div>', unsafe_allow_html=True)
    metric_row()
    left, right = st.columns(2)
    with left:
        st.markdown("**Average hospital stay by diagnosis**")
        if has("CCSR Diagnosis Description") and has("Length of Stay"):
            dx = filtered.dropna(subset=["CCSR Diagnosis Description", "Length of Stay"])
            top_dx = dx.groupby("CCSR Diagnosis Description")["Length of Stay"].mean().nlargest(12).sort_values().reset_index()
            top_dx.columns = ["Diagnosis", "Average stay"]
            fig = px.bar(top_dx, x="Average stay", y="Diagnosis", orientation="h", color="Average stay",
                         color_continuous_scale=[[0, "#24556A"], [1, CYAN]], hover_data={"Average stay":":.2f"})
            fig.update_layout(coloraxis_showscale=False, xaxis_title="Average stay (days)")
            st.plotly_chart(chart_theme(fig, 430), use_container_width=True)
        else:
            st.info("Diagnosis description and Length of Stay are required.")
    with right:
        st.markdown("**Total charges by severity**")
        if has("APR Severity of Illness Description") and has("Total Charges"):
            box = filtered.dropna(subset=["APR Severity of Illness Description", "Total Charges"]).copy()
            # Sampling keeps the interactive chart responsive while retaining the distribution shape.
            if len(box) > 30000:
                box = box.sample(30000, random_state=42)
            fig = px.box(box, x="APR Severity of Illness Description", y="Total Charges",
                         color="APR Severity of Illness Description", color_discrete_sequence=PALETTE,
                         points=False)
            fig.update_layout(showlegend=False, xaxis_title="Severity of illness", yaxis_title="Total charges ($)")
            st.plotly_chart(chart_theme(fig, 430), use_container_width=True)
        else:
            st.info("Severity and Total Charges are required.")
    st.markdown("**Length-of-stay distribution**")
    if has("Length of Stay"):
        los = filtered["Length of Stay"].dropna()
        fig = px.histogram(los, x="Length of Stay", nbins=55, color_discrete_sequence=[BLUE])
        fig.update_layout(xaxis_title="Length of stay (days)", yaxis_title="Number of discharges")
        st.plotly_chart(chart_theme(fig, 310), use_container_width=True)

# ---------- Page: Hospital Network ----------
elif page == "Hospital Network":
    st.markdown('<div class="eyebrow">03 / HOSPITAL NETWORK</div><div class="section-title">Hospital network intelligence</div><div class="section-sub">Compare facility activity and geographic variation in length of stay.</div>', unsafe_allow_html=True)
    metric_row()
    if has("Facility Name") and has("Hospital County") and has("Length of Stay"):
        heat = filtered.dropna(subset=["Facility Name", "Hospital County", "Length of Stay"]).copy()
        top_counties = heat["Hospital County"].value_counts().head(12).index
        heat = heat[heat["Hospital County"].isin(top_counties)]
        top_facilities = heat["Facility Name"].value_counts().head(18).index
        heat = heat[heat["Facility Name"].isin(top_facilities)]
        pivot = heat.pivot_table(index="Facility Name", columns="Hospital County",
                                 values="Length of Stay", aggfunc="mean")
        st.markdown("**Average stay by facility and county**")
        if not pivot.empty:
            fig = px.imshow(pivot, aspect="auto", color_continuous_scale="Teal",
                            labels=dict(x="County", y="Hospital facility", color="Avg. days"))
            st.plotly_chart(chart_theme(fig, 540), use_container_width=True)
        else:
            st.info("Not enough facility, county and stay data for this heatmap.")
    else:
        st.info("Facility Name, Hospital County and Length of Stay are needed for the heatmap.")

    left, right = st.columns(2)
    with left:
        st.markdown("**Highest-volume facilities**")
        if has("Facility Name"):
            fac = filtered["Facility Name"].astype("object").fillna("Unknown").astype(str).value_counts().head(12).sort_values().reset_index()
            fac.columns = ["Facility", "Discharges"]
            fig = px.bar(fac, x="Discharges", y="Facility", orientation="h", color_discrete_sequence=[CYAN])
            st.plotly_chart(chart_theme(fig, 390), use_container_width=True)
    with right:
        st.markdown("**Average stay by county**")
        if has("Hospital County") and has("Length of Stay"):
            county = filtered.dropna(subset=["Hospital County", "Length of Stay"]).groupby("Hospital County")["Length of Stay"].mean().nlargest(12).sort_values().reset_index()
            county.columns = ["County", "Average stay"]
            fig = px.bar(county, x="Average stay", y="County", orientation="h", color_discrete_sequence=[VIOLET])
            st.plotly_chart(chart_theme(fig, 390), use_container_width=True)

# ---------- Page: Financial Intelligence ----------
elif page == "Financial Intelligence":
    st.markdown('<div class="eyebrow">04 / FINANCIAL INTELLIGENCE</div><div class="section-title">Financial analytics</div><div class="section-sub">Understand how charges and costs vary across patient and payment groups.</div>', unsafe_allow_html=True)
    metric_row()
    left, right = st.columns(2)
    with left:
        st.markdown("**Average charges by age group and gender**")
        if has("Age Group") and has("Gender") and has("Total Charges"):
            fin = filtered.dropna(subset=["Age Group", "Gender", "Total Charges"])
            grouped = fin.groupby(["Age Group", "Gender"], as_index=False)["Total Charges"].mean()
            fig = px.bar(grouped, x="Age Group", y="Total Charges", color="Gender", barmode="group",
                         color_discrete_sequence=[CYAN, BLUE, VIOLET])
            fig.update_layout(yaxis_title="Average charges ($)")
            st.plotly_chart(chart_theme(fig, 380), use_container_width=True)
        else:
            st.info("Age Group, Gender and Total Charges are required.")
    with right:
        st.markdown("**Discharges by payment type**")
        if has("Payment Typology 1"):
            pay = filtered["Payment Typology 1"].astype("object").fillna("Unknown").astype(str).value_counts().reset_index()
            pay.columns = ["Payment type", "Discharges"]
            fig = px.pie(pay, names="Payment type", values="Discharges", hole=.58,
                         color_discrete_sequence=PALETTE)
            fig.update_traces(textposition="inside", textinfo="percent")
            st.plotly_chart(chart_theme(fig, 380), use_container_width=True)
        else:
            st.info("Payment Typology 1 field not available.")
    left, right = st.columns(2)
    with left:
        st.markdown("**Average charges by severity**")
        if has("APR Severity of Illness Description") and has("Total Charges"):
            sev = filtered.dropna(subset=["APR Severity of Illness Description", "Total Charges"]).groupby("APR Severity of Illness Description", as_index=False)["Total Charges"].mean()
            fig = px.bar(sev, x="APR Severity of Illness Description", y="Total Charges",
                         color="APR Severity of Illness Description", color_discrete_sequence=PALETTE)
            fig.update_layout(showlegend=False, yaxis_title="Average charges ($)")
            st.plotly_chart(chart_theme(fig, 350), use_container_width=True)
    with right:
        st.markdown("**Total costs by age group**")
        if has("Age Group") and has("Total Costs"):
            costs = filtered.dropna(subset=["Age Group", "Total Costs"]).groupby("Age Group", as_index=False)["Total Costs"].sum()
            fig = px.bar(costs, x="Age Group", y="Total Costs", color_discrete_sequence=[LIME])
            fig.update_layout(yaxis_title="Total costs ($)")
            st.plotly_chart(chart_theme(fig, 350), use_container_width=True)

# ---------- Page: Data Explorer ----------
else:
    st.markdown('<div class="eyebrow">05 / DATA LABORATORY</div><div class="section-title">Discharge data explorer</div><div class="section-sub">Search, inspect and export the records matching your current filters.</div>', unsafe_allow_html=True)
    metric_row()
    search = st.text_input("Search records", placeholder="Search facility, diagnosis, county or other visible text…")
    view = filtered
    if search.strip():
        searchable = [c for c in ["Facility Name", "CCSR Diagnosis Description", "Hospital County",
                                  "Age Group", "Gender", "Payment Typology 1"] if has(c)]
        if searchable:
            mask = pd.Series(False, index=view.index)
            for col in searchable:
                mask |= view[col].astype(str).str.contains(search.strip(), case=False, na=False)
            view = view[mask]
    st.caption(f"Showing {min(1000, len(view)):,} of {len(view):,} matching records.")
    st.dataframe(view.head(1000), use_container_width=True, height=480)
    csv = view.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download filtered records (CSV)", csv,
                       file_name="medisynth_filtered_discharges.csv", mime="text/csv")
    st.markdown("---")
    st.markdown("**Data quality snapshot**")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Missing cells", number(int(filtered.isna().sum().sum())))
    q2.metric("Duplicate check", "See EDA")
    q3.metric("Columns", number(len(filtered.columns)))
    q4.metric("Rows after filters", number(len(filtered)))

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    '<div class="small-muted">MEDISYNTH · Hospital Inpatient Discharge Analytics · '
    'New York State SPARCS 2021 · Exploratory analysis only; not clinical advice.</div>',
    unsafe_allow_html=True,
)
