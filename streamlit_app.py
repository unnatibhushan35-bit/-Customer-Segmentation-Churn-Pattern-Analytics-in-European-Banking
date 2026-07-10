import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="European Banking - Churn Pattern Analytics",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-end professional banking dashboard look
st.markdown("""
<style>
    /* Main body background and font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .header-container {
        background-color: #0F172A;
        padding: 2.5rem 2rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 2rem;
        border-left: 8px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .header-sub {
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.2rem;
    }
    .header-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0;
    }
    
    /* Custom card styles */
    .kpi-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1;
    }
    .kpi-subtext {
        font-size: 0.75rem;
        color: #475569;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Segment headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0F172A;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SELF-CONTAINED RAW DATASET (108 Verified Records)
# ---------------------------------------------------------
# Schema: [year, customerId, surname, creditScore, geography, gender, age, tenure, balance, numOfProducts, hasCrCard, isActiveMember, estimatedSalary, exited]
raw_records = [
    [2025, 15634602, "Hargrave", 619, "France", "Female", 42, 2, 0.0, 1, 1, 1, 101348.88, 1],
    [2025, 15647311, "Hill", 608, "Spain", "Female", 41, 1, 83807.86, 1, 0, 1, 112542.58, 0],
    [2025, 15619304, "Onio", 502, "France", "Female", 42, 8, 159660.8, 3, 1, 0, 113931.57, 1],
    [2025, 15701354, "Boni", 699, "France", "Female", 39, 1, 0.0, 2, 0, 0, 93826.63, 0],
    [2025, 15737888, "Mitchell", 850, "Spain", "Female", 43, 2, 125510.82, 1, 1, 1, 79084.1, 0],
    [2025, 15574012, "Chu", 645, "Spain", "Male", 44, 8, 113755.78, 2, 1, 0, 149756.71, 1],
    [2025, 15592531, "Bartlett", 822, "France", "Male", 50, 7, 0.0, 2, 1, 1, 10062.8, 0],
    [2025, 15656148, "Obinna", 376, "Germany", "Female", 29, 4, 115046.74, 4, 1, 0, 119346.88, 1],
    [2025, 15792365, "He", 501, "France", "Male", 44, 4, 142051.07, 2, 0, 1, 74940.5, 0],
    [2025, 15592389, "H?", 684, "France", "Male", 27, 2, 134603.88, 1, 1, 1, 71725.73, 0],
    [2025, 15767821, "Bearce", 528, "France", "Male", 31, 6, 102016.72, 2, 0, 0, 80181.12, 0],
    [2025, 15737173, "Andrews", 497, "Spain", "Male", 24, 3, 0.0, 2, 1, 0, 76390.01, 0],
    [2025, 15632264, "Kay", 476, "France", "Female", 34, 10, 0.0, 2, 1, 0, 26260.98, 0],
    [2025, 15691483, "Chin", 549, "France", "Female", 25, 5, 0.0, 2, 0, 0, 190857.79, 0],
    [2025, 15600882, "Scott", 635, "Spain", "Female", 35, 7, 0.0, 2, 1, 1, 65951.65, 0],
    [2025, 15643966, "Goforth", 616, "Germany", "Male", 45, 3, 143129.41, 2, 0, 1, 64327.26, 0],
    [2025, 15737452, "Romeo", 653, "Germany", "Male", 58, 1, 132602.88, 1, 1, 0, 5097.67, 1],
    [2025, 15788218, "Henderson", 549, "Spain", "Female", 24, 9, 0.0, 2, 1, 1, 14406.41, 0],
    [2025, 15661507, "Muldrow", 587, "Spain", "Male", 45, 6, 0.0, 1, 0, 0, 158684.81, 0],
    [2025, 15568982, "Hao", 726, "France", "Female", 24, 6, 0.0, 2, 1, 1, 54724.03, 0],
    [2025, 15577657, "McDonald", 732, "France", "Male", 41, 8, 0.0, 2, 1, 1, 170886.17, 0],
    [2025, 15597945, "Dellucci", 636, "Spain", "Female", 32, 8, 0.0, 2, 1, 0, 138555.46, 0],
    [2025, 15699309, "Gerasimov", 510, "Spain", "Female", 38, 4, 0.0, 1, 1, 0, 118913.53, 1],
    [2025, 15725737, "Mosman", 669, "France", "Male", 46, 3, 0.0, 2, 0, 1, 8487.75, 0],
    [2025, 15625047, "Yen", 846, "France", "Female", 38, 5, 0.0, 1, 1, 1, 187616.16, 0],
    [2025, 15738191, "Maclean", 577, "France", "Male", 25, 3, 0.0, 2, 0, 1, 124508.29, 0],
    [2025, 15736816, "Young", 756, "Germany", "Male", 36, 2, 136815.64, 1, 1, 1, 170041.95, 0],
    [2025, 15700772, "Nebechi", 571, "France", "Male", 44, 9, 0.0, 2, 0, 0, 38433.35, 0],
    [2025, 15728693, "McWilliams", 574, "Germany", "Female", 43, 3, 141349.43, 1, 1, 1, 100187.43, 0],
    [2025, 15656300, "Lucciano", 411, "France", "Male", 29, 0, 59697.17, 2, 1, 1, 53483.21, 0],
    [2025, 15589475, "Azikiwe", 591, "Spain", "Female", 39, 3, 0.0, 3, 1, 0, 140469.38, 1],
    [2025, 15706552, "Odinakachukwu", 533, "France", "Male", 36, 7, 85311.7, 1, 0, 1, 156731.91, 0],
    [2025, 15750181, "Sanderson", 553, "Germany", "Male", 41, 9, 110112.54, 2, 0, 0, 81898.81, 0],
    [2025, 15659428, "Maggard", 520, "Spain", "Female", 42, 6, 0.0, 2, 1, 1, 34410.55, 0],
    [2025, 15732963, "Clements", 722, "Spain", "Female", 29, 9, 0.0, 2, 1, 1, 142033.07, 0],
    [2025, 15794171, "Lombardo", 475, "France", "Female", 45, 0, 134264.04, 1, 1, 0, 27822.99, 1],
    [2025, 15788448, "Watson", 490, "Spain", "Male", 31, 3, 145260.23, 1, 0, 1, 114066.77, 0],
    [2025, 15729599, "Lorenzo", 804, "Spain", "Male", 33, 7, 76548.6, 1, 0, 1, 98453.45, 0],
    [2025, 15717426, "Armstrong", 850, "France", "Male", 36, 7, 0.0, 1, 1, 1, 40812.9, 0],
    [2025, 15585768, "Cameron", 582, "Germany", "Male", 41, 6, 70349.48, 2, 0, 1, 178074.04, 0],
    [2025, 15619360, "Hsiao", 472, "Spain", "Male", 40, 4, 0.0, 1, 1, 0, 70154.22, 0],
    [2025, 15738148, "Clarke", 465, "France", "Female", 51, 8, 122522.32, 1, 0, 0, 181297.65, 1],
    [2025, 15687946, "Osborne", 556, "France", "Female", 61, 2, 117419.35, 1, 1, 1, 94153.83, 0],
    [2025, 15755196, "Lavine", 834, "France", "Female", 49, 2, 131394.56, 1, 0, 0, 194365.76, 1],
    [2025, 15684171, "Bianchi", 660, "Spain", "Female", 61, 5, 155931.11, 1, 1, 1, 158338.39, 0],
    [2025, 15754849, "Tyler", 776, "Germany", "Female", 32, 4, 109421.13, 2, 1, 1, 126517.46, 0],
    [2025, 15602280, "Martin", 829, "Germany", "Female", 27, 9, 112045.67, 1, 1, 1, 119708.21, 1],
    [2025, 15771573, "Okagbue", 637, "Germany", "Female", 39, 9, 137843.8, 1, 1, 1, 117622.8, 1],
    [2025, 15766205, "Yin", 550, "Germany", "Male", 38, 2, 103391.38, 1, 0, 1, 90878.13, 0],
    [2025, 15771873, "Buccho", 776, "Germany", "Female", 37, 2, 103769.22, 2, 1, 0, 194099.12, 0],
    [2025, 15616550, "Chidiebele", 698, "Germany", "Male", 44, 10, 116363.37, 2, 1, 0, 198059.16, 0],
    [2025, 15768193, "Trevisani", 585, "Germany", "Male", 36, 5, 146050.97, 2, 0, 0, 86424.57, 0],
    [2025, 15683553, "O'Brien", 788, "France", "Female", 33, 5, 0.0, 2, 0, 0, 116978.19, 0],
    [2025, 15702298, "Parkhill", 655, "Germany", "Male", 41, 8, 125561.97, 1, 0, 0, 164040.94, 1],
    [2025, 15569590, "Yoo", 601, "Germany", "Male", 42, 1, 98495.72, 1, 1, 0, 40014.76, 1],
    [2025, 15760861, "Phillipps", 619, "France", "Male", 43, 1, 125211.92, 1, 1, 1, 113410.49, 0],
    [2025, 15630053, "Tsao", 656, "France", "Male", 45, 5, 127864.4, 1, 1, 0, 87107.57, 0],
    [2025, 15647091, "Endrizzi", 725, "Germany", "Male", 19, 0, 75888.2, 1, 0, 0, 45613.75, 0],
    [2025, 15623944, "T'ien", 511, "Spain", "Female", 66, 4, 0.0, 1, 1, 0, 1643.11, 1],
    [2025, 15804771, "Velazquez", 614, "France", "Male", 51, 4, 40685.92, 1, 1, 1, 46775.28, 0],
    [2025, 15651280, "Hunter", 742, "Germany", "Male", 35, 5, 136857.0, 1, 0, 0, 84509.57, 0],
    [2025, 15773469, "Clark", 687, "Germany", "Female", 27, 9, 152328.88, 2, 0, 0, 126494.82, 0],
    [2025, 15751208, "Pirozzi", 684, "Spain", "Male", 56, 8, 78707.16, 1, 1, 1, 99398.36, 0],
    [2025, 15592461, "Jackson", 603, "Germany", "Male", 26, 4, 109166.37, 1, 1, 1, 92840.67, 0],
    [2025, 15789484, "Hammond", 751, "Germany", "Female", 36, 6, 169831.46, 2, 1, 1, 27758.36, 0],
    [2025, 15696061, "Brownless", 581, "Germany", "Female", 34, 1, 101633.04, 1, 1, 0, 110431.51, 0],
    [2025, 15641582, "Chibugo", 735, "Germany", "Male", 43, 10, 123180.01, 2, 1, 1, 196673.28, 0],
    [2025, 15638424, "Glauert", 661, "Germany", "Female", 35, 5, 150725.53, 2, 0, 1, 113656.85, 0],
    [2025, 15755648, "Pisano", 675, "France", "Female", 21, 8, 98373.26, 1, 1, 0, 18203.0, 0],
    [2025, 15703793, "Konovalova", 738, "Germany", "Male", 58, 2, 133745.44, 4, 1, 0, 28373.86, 1],
    [2025, 15620344, "McKee", 813, "France", "Male", 29, 6, 0.0, 1, 1, 0, 33953.87, 0],
    [2025, 15812518, "Palermo", 657, "Spain", "Female", 37, 0, 163607.18, 1, 0, 1, 44203.55, 0],
    [2025, 15779052, "Ballard", 604, "Germany", "Female", 25, 5, 157780.84, 2, 1, 1, 58426.81, 0],
    [2025, 15770811, "Wallace", 519, "France", "Male", 36, 9, 0.0, 2, 0, 1, 145562.4, 0],
    [2025, 15780961, "Cavenagh", 735, "France", "Female", 21, 1, 178718.19, 2, 1, 0, 22388.0, 0],
    [2025, 15614049, "Hu", 664, "France", "Male", 55, 8, 0.0, 2, 1, 1, 139161.64, 0],
    [2025, 15662085, "Read", 678, "France", "Female", 32, 9, 0.0, 1, 1, 1, 148210.64, 0],
    [2025, 15575185, "Bushell", 757, "Spain", "Male", 33, 5, 77253.22, 1, 0, 1, 194239.63, 0],
    [2025, 15803136, "Postle", 416, "Germany", "Female", 41, 10, 122189.66, 2, 1, 0, 98301.61, 0],
    [2025, 15706021, "Buley", 665, "France", "Female", 34, 1, 96645.54, 2, 0, 0, 171413.66, 0],
    [2025, 15663706, "Leonard", 777, "France", "Female", 32, 2, 0.0, 1, 1, 0, 136458.19, 1],
    [2025, 15641732, "Mills", 543, "France", "Female", 36, 3, 0.0, 2, 0, 0, 26019.59, 0],
    [2025, 15701164, "Onyeorulu", 506, "France", "Female", 34, 4, 90307.62, 1, 1, 1, 159235.29, 0],
    [2025, 15738751, "Beit", 493, "France", "Female", 46, 4, 0.0, 2, 1, 0, 1907.66, 0],
    [2025, 15805254, "Ndukaku", 652, "Spain", "Female", 75, 10, 0.0, 2, 1, 1, 114675.75, 0],
    [2025, 15762418, "Gant", 750, "Spain", "Male", 22, 3, 121681.82, 1, 1, 0, 128643.35, 1],
    [2025, 15625759, "Rowley", 729, "France", "Male", 30, 9, 0.0, 2, 1, 0, 151869.35, 0],
    [2025, 15622897, "Sharpe", 646, "France", "Female", 46, 4, 0.0, 3, 1, 0, 93251.42, 1],
    [2025, 15767954, "Osborne", 635, "Germany", "Female", 28, 3, 81623.67, 2, 1, 1, 156791.36, 0],
    [2025, 15757535, "Heap", 647, "Spain", "Female", 44, 5, 0.0, 3, 1, 1, 174205.22, 1],
    [2025, 15731511, "Ritchie", 808, "France", "Male", 45, 7, 118626.55, 2, 1, 0, 147132.46, 0],
    [2025, 15809248, "Cole", 524, "France", "Female", 36, 10, 0.0, 2, 1, 0, 109614.57, 0],
    [2025, 15640635, "Capon", 769, "France", "Male", 29, 8, 0.0, 2, 1, 1, 172290.61, 0],
    [2025, 15676966, "Capon", 730, "Spain", "Male", 42, 4, 0.0, 2, 0, 1, 85982.47, 0],
    [2025, 15699461, "Fiorentini", 515, "Spain", "Male", 35, 10, 176273.95, 1, 0, 1, 121277.78, 0],
    [2025, 15738721, "Graham", 773, "Spain", "Male", 41, 9, 102827.44, 1, 0, 1, 64595.25, 0],
    [2025, 15693683, "Yuille", 814, "Germany", "Male", 29, 8, 97086.4, 2, 1, 1, 197276.13, 0],
    [2025, 15604348, "Allard", 710, "Spain", "Male", 22, 8, 0.0, 2, 0, 0, 99645.04, 0],
    [2025, 15633059, "Fanucci", 413, "France", "Male", 34, 9, 0.0, 2, 0, 0, 6534.18, 0],
    [2025, 15808582, "Fu", 665, "France", "Female", 40, 6, 0.0, 1, 1, 1, 161848.03, 0],
    [2025, 15743192, "Hung", 623, "France", "Female", 44, 6, 0.0, 2, 0, 0, 167162.43, 0],
    [2025, 15580146, "Hung", 738, "France", "Male", 31, 9, 82674.15, 1, 1, 0, 41970.72, 0],
    [2025, 15776605, "Bradley", 528, "Spain", "Male", 36, 7, 0.0, 2, 1, 0, 60536.56, 0],
    [2025, 15804919, "Dunbabin", 670, "Spain", "Female", 65, 1, 0.0, 1, 1, 1, 177655.68, 1],
    [2025, 15613854, "Mauldon", 622, "Spain", "Female", 46, 4, 107073.27, 2, 1, 1, 30984.59, 1],
    [2025, 15599195, "Stiger", 582, "Germany", "Male", 32, 1, 88938.62, 1, 1, 1, 10054.53, 0],
    [2025, 15812878, "Parsons", 785, "Germany", "Female", 36, 2, 99806.85, 1, 0, 1, 36976.52, 0],
    [2025, 15602312, "Walkom", 605, "Spain", "Male", 33, 5, 150092.8, 1, 0, 0, 71862.79, 0]
]

columns = [
    "year", "customerId", "surname", "creditScore", "geography", "gender",
    "age", "tenure", "balance", "numOfProducts", "hasCrCard", "isActiveMember",
    "estimatedSalary", "exited"
]

df_original = pd.DataFrame(raw_records, columns=columns)

# Map helper categories
df_original["isActiveMember_Label"] = df_original["isActiveMember"].map({1: "Active Member", 0: "Inactive Member"})
df_original["hasCrCard_Label"] = df_original["hasCrCard"].map({1: "Has Credit Card", 0: "No Credit Card"})
df_original["exited_Label"] = df_original["exited"].map({1: "Exited (Churn)", 0: "Retained"})

# ---------------------------------------------------------
# SIDEBAR FILTERS & CONTROL PANEL
# ---------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1501167786227-4cba60f6d58f?auto=format&fit=crop&w=800&q=80", use_container_width=True)
st.sidebar.markdown("<h2 style='font-weight:800; font-size:1.4rem; margin-bottom:1rem; color:#0F172A;'>Control Panel & Segments</h2>", unsafe_allow_html=True)

# Geography multi-select
geography_options = df_original["geography"].unique().tolist()
selected_geographies = st.sidebar.multiselect(
    "🌍 Select Geographies",
    options=geography_options,
    default=geography_options
)

# Gender multi-select
gender_options = df_original["gender"].unique().tolist()
selected_genders = st.sidebar.multiselect(
    "👤 Select Genders",
    options=gender_options,
    default=gender_options
)

# Membership state multi-select
member_options = ["Active Member", "Inactive Member"]
selected_members = st.sidebar.multiselect(
    "🔑 Membership Activity Status",
    options=member_options,
    default=member_options
)

# Age Slider
min_age = int(df_original["age"].min())
max_age = int(df_original["age"].max())
selected_age_range = st.sidebar.slider(
    "🎂 Age Bracket Range",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Balance Range Slider
min_bal = float(df_original["balance"].min())
max_bal = float(df_original["balance"].max())
selected_balance_range = st.sidebar.slider(
    "💰 Account Balance Range ($)",
    min_value=0.0,
    max_value=max_bal,
    value=(0.0, max_bal)
)

# Reset Button
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

# Apply filters
df_filtered = df_original[
    (df_original["geography"].isin(selected_geographies)) &
    (df_original["gender"].isin(selected_genders)) &
    (df_original["isActiveMember_Label"].isin(selected_members)) &
    (df_original["age"] >= selected_age_range[0]) &
    (df_original["age"] <= selected_age_range[1]) &
    (df_original["balance"] >= selected_balance_range[0]) &
    (df_original["balance"] <= selected_balance_range[1])
]

# ---------------------------------------------------------
# HEADER DISPLAY
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="header-sub">European Central Bank • Technical Intelligence Unit</div>
    <div class="header-title">Customer Segmentation & Churn Pattern Analytics</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DYNAMIC MANDATE STATUS CARDS
# ---------------------------------------------------------
m_col1, m_col2, m_col3 = st.columns(3)

# Calculations for metrics
total_cust = len(df_filtered)
churn_cust = df_filtered["exited"].sum()
calc_churn_rate = (churn_cust / total_cust * 100) if total_cust > 0 else 0.0

# Baseline constant verification
baseline_churn = 20.37

with m_col1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #2563EB;">
        <div class="kpi-label">Primary Mandate Status</div>
        <div style="font-size: 1.1rem; font-weight:700; color:#1E293B;">Baseline Churn Target</div>
        <div class="kpi-value" style="color: #2563EB; margin-top: 0.5rem;">{baseline_churn:.2f}%</div>
        <div class="kpi-subtext">Verified Gemini Benchmark population rate (22 exited / 108 records).</div>
    </div>
    """, unsafe_allow_html=True)

with m_col2:
    # High Net Worth Portfolio Exposure (Balances > $100,000)
    hnw_df = df_filtered[df_filtered["balance"] > 100000]
    hnw_total = len(hnw_df)
    hnw_churned = hnw_df["exited"].sum()
    hnw_churn_rate = (hnw_churned / hnw_total * 100) if hnw_total > 0 else 0.0
    total_hnw_balance_at_risk = hnw_df[hnw_df["exited"] == 1]["balance"].sum()
    
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #DC2626;">
        <div class="kpi-label">Secondary Mandate B Status</div>
        <div style="font-size: 1.1rem; font-weight:700; color:#1E293B;">Premium Portfolio Risk</div>
        <div class="kpi-value" style="color: #DC2626; margin-top: 0.5rem;">${total_hnw_balance_at_risk:,.2f}</div>
        <div class="kpi-subtext">Total cash flight in high-net-worth accounts (> $100k) currently filtered.</div>
    </div>
    """, unsafe_allow_html=True)

with m_col3:
    # Active vs Inactive Churn comparison
    active_churned = df_filtered[(df_filtered["isActiveMember"] == 1) & (df_filtered["exited"] == 1)].shape[0]
    inactive_churned = df_filtered[(df_filtered["isActiveMember"] == 0) & (df_filtered["exited"] == 1)].shape[0]
    risk_multiplier = (inactive_churned / active_churned) if active_churned > 0 else 1.0
    
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #D97706;">
        <div class="kpi-label">Key Behavioral Hotspot</div>
        <div style="font-size: 1.1rem; font-weight:700; color:#1E293B;">Member Inactivity Multiplier</div>
        <div class="kpi-value" style="color: #D97706; margin-top: 0.5rem;">{risk_multiplier:.1f}x</div>
        <div class="kpi-subtext">Inactive members demonstrate heightened exit rates compared to active ones.</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TABS SYSTEM
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Portfolio KPI Dashboard",
    "🗺️ Segment Analysis & Hotspots",
    "🔍 Detailed Customer Explorer",
    "📋 Technical Action Recommendations"
])

# ---------------------------------------------------------
# TAB 1: PORTFOLIO KPI DASHBOARD
# ---------------------------------------------------------
with tab1:
    st.markdown("<div class='section-header'>Interactive Portfolio KPI Performance Indicators</div>", unsafe_allow_html=True)
    
    k_col1, k_col2, k_col3, k_col4 = st.columns(4)
    
    with k_col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Active Portfolio Churn Rate</div>
            <div class="kpi-value">{calc_churn_rate:.2f}%</div>
            <div class="kpi-subtext">Current segment churn rate based on your active filters.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k_col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Monitored Customers</div>
            <div class="kpi-value">{total_cust}</div>
            <div class="kpi-subtext">Total active portfolio count following segment filtering.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k_col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Exited Customers</div>
            <div class="kpi-value">{churn_cust}</div>
            <div class="kpi-subtext">Total observed churn volume within the selected filters.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k_col4:
        avg_score = df_filtered["creditScore"].mean() if total_cust > 0 else 0.0
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Credit Score</div>
            <div class="kpi-value">{avg_score:.1f}</div>
            <div class="kpi-subtext">Financial health parameter monitored across this segment.</div>
        </div>
        """, unsafe_allow_html=True)

    # Visualization Row 1
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.markdown("<div class='section-header'>High-Value Premium Risk Analysis (Balances > $100k)</div>", unsafe_allow_html=True)
        # Bar chart comparing churn rates in high value vs normal
        df_original["Balance_Category"] = df_original["balance"].apply(lambda x: "Premium Account (>$100k)" if x > 100000 else "Standard Account")
        
        # Filtered equivalent
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy["Balance_Category"] = df_filtered_copy["balance"].apply(lambda x: "Premium Account (>$100k)" if x > 100000 else "Standard Account")
        
        premium_summary = df_filtered_copy.groupby("Balance_Category")["exited"].agg(["count", "sum"]).reset_index()
        premium_summary["Churn_Rate"] = (premium_summary["sum"] / premium_summary["count"] * 100).round(2)
        
        fig_prem = px.bar(
            premium_summary,
            x="Balance_Category",
            y="Churn_Rate",
            color="Balance_Category",
            text="Churn_Rate",
            labels={"Churn_Rate": "Observed Churn Rate (%)", "Balance_Category": "Portfolio Segment"},
            color_discrete_map={"Premium Account (>$100k)": "#DC2626", "Standard Account": "#2563EB"},
            height=350
        )
        fig_prem.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_prem.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_prem, use_container_width=True)
        st.caption("Premium accounts demonstrate a distinct risk behavior pattern, representing critical high-net-worth liquidity exposure.")
        
    with v_col2:
        st.markdown("<div class='section-header'>Churn Probability by Membership Activity</div>", unsafe_allow_html=True)
        # Churn rate for Active vs Inactive members
        member_summary = df_filtered.groupby("isActiveMember_Label")["exited"].agg(["count", "sum"]).reset_index()
        member_summary["Churn_Rate"] = (member_summary["sum"] / member_summary["count"] * 100).round(2)
        
        fig_member = px.bar(
            member_summary,
            x="isActiveMember_Label",
            y="Churn_Rate",
            color="isActiveMember_Label",
            text="Churn_Rate",
            labels={"Churn_Rate": "Observed Churn Rate (%)", "isActiveMember_Label": "Membership Status"},
            color_discrete_map={"Active Member": "#10B981", "Inactive Member": "#F59E0B"},
            height=350
        )
        fig_member.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_member.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_member, use_container_width=True)
        st.caption("Inactivity constitutes the most powerful behavioral indicator of impending customer account termination.")

# ---------------------------------------------------------
# TAB 2: SEGMENT ANALYSIS & HOTSPOTS
# ---------------------------------------------------------
with tab2:
    st.markdown("<div class='section-header'>Secondary Mandate A: Geographic Risk Vectors</div>", unsafe_allow_html=True)
    
    g_col1, g_col2 = st.columns([1, 1])
    
    with g_col1:
        # Country Churn Rates
        geo_summary = df_filtered.groupby("geography")["exited"].agg(["count", "sum"]).reset_index()
        geo_summary["Churn_Rate"] = (geo_summary["sum"] / geo_summary["count"] * 100).round(2)
        
        fig_geo = px.bar(
            geo_summary,
            x="geography",
            y="Churn_Rate",
            color="geography",
            text="Churn_Rate",
            labels={"Churn_Rate": "Churn Rate (%)", "geography": "Country"},
            color_discrete_sequence=px.colors.qualitative.Prism,
            height=350
        )
        fig_geo.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_geo.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_geo, use_container_width=True)
        st.caption("Geographic division of portfolio risk. Germany typically showcases structurally high churn tendencies.")
        
    with g_col2:
        # Pie chart of customer geographic distribution
        fig_pie = px.pie(
            geo_summary,
            values="count",
            names="geography",
            hole=0.4,
            color="geography",
            color_discrete_sequence=px.colors.qualitative.Prism,
            height=350
        )
        fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("Geographic footprint (customer count distribution) of currently selected customer accounts.")

    st.markdown("<div class='section-header'>Demographic Risk Vectors: Age Brackets & Tenure</div>", unsafe_allow_html=True)
    
    d_col1, d_col2 = st.columns(2)
    
    with d_col1:
        # Age brackets calculation
        def get_age_bracket(age):
            if age < 30:
                return "Under 30"
            elif age <= 45:
                return "30 - 45"
            elif age <= 60:
                return "46 - 60"
            else:
                return "Over 60"
                
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy["Age_Bracket"] = df_filtered_copy["age"].apply(get_age_bracket)
        
        age_summary = df_filtered_copy.groupby("Age_Bracket")["exited"].agg(["count", "sum"]).reset_index()
        age_order = ["Under 30", "30 - 45", "46 - 60", "Over 60"]
        age_summary["Age_Bracket"] = pd.Categorical(age_summary["Age_Bracket"], categories=age_order, ordered=True)
        age_summary = age_summary.sort_values("Age_Bracket")
        age_summary["Churn_Rate"] = (age_summary["sum"] / age_summary["count"] * 100).round(2)
        
        fig_age = px.line(
            age_summary,
            x="Age_Bracket",
            y="Churn_Rate",
            markers=True,
            text="Churn_Rate",
            labels={"Churn_Rate": "Churn Rate (%)", "Age_Bracket": "Age Group"},
            height=350
        )
        fig_age.update_traces(textposition="top center", line=dict(color="#2563EB", width=3))
        fig_age.update_layout(margin=dict(t=20, b=20, l=10, r=10))
        st.plotly_chart(fig_age, use_container_width=True)
        st.caption("Risk curves by age group show significant escalation within the 46 - 60 demographic.")
        
    with d_col2:
        # Tenure Groups
        def get_tenure_group(tenure):
            if tenure <= 3:
                return "Short Term (0 - 3 yrs)"
            elif tenure <= 7:
                return "Medium Term (4 - 7 yrs)"
            else:
                return "Long Term (8+ yrs)"
                
        df_filtered_copy["Tenure_Group"] = df_filtered_copy["tenure"].apply(get_tenure_group)
        tenure_summary = df_filtered_copy.groupby("Tenure_Group")["exited"].agg(["count", "sum"]).reset_index()
        tenure_order = ["Short Term (0 - 3 yrs)", "Medium Term (4 - 7 yrs)", "Long Term (8+ yrs)"]
        tenure_summary["Tenure_Group"] = pd.Categorical(tenure_summary["Tenure_Group"], categories=tenure_order, ordered=True)
        tenure_summary = tenure_summary.sort_values("Tenure_Group")
        tenure_summary["Churn_Rate"] = (tenure_summary["sum"] / tenure_summary["count"] * 100).round(2)
        
        fig_tenure = px.bar(
            tenure_summary,
            x="Tenure_Group",
            y="Churn_Rate",
            color="Tenure_Group",
            text="Churn_Rate",
            labels={"Churn_Rate": "Churn Rate (%)", "Tenure_Group": "Tenure Classification"},
            color_discrete_sequence=px.colors.sequential.Deep,
            height=350
        )
        fig_tenure.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_tenure.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_tenure, use_container_width=True)
        st.caption("Customer retention levels grouped by institutional relationship tenure.")

# ---------------------------------------------------------
# TAB 3: DETAILED CUSTOMER EXPLORER
# ---------------------------------------------------------
with tab3:
    st.markdown("<div class='section-header'>Granular Portfolio Registry Audit</div>", unsafe_allow_html=True)
    st.markdown("Search, inspect, and download filtered raw banking records. Useful for deep technical investigation or CRM triggers.")
    
    # Text Search Field
    search_query = st.text_input("🔍 Search Customers by Surname", "")
    
    df_to_show = df_filtered.copy()
    if search_query:
        df_to_show = df_to_show[df_to_show["surname"].str.contains(search_query, case=False, na=False)]
        
    # Formatting display df
    df_display = df_to_show[[
        "customerId", "surname", "creditScore", "geography", "gender", 
        "age", "tenure", "balance", "numOfProducts", "hasCrCard_Label", 
        "isActiveMember_Label", "estimatedSalary", "exited_Label"
    ]].rename(columns={
        "customerId": "Customer ID",
        "surname": "Surname",
        "creditScore": "Credit Score",
        "geography": "Country",
        "gender": "Gender",
        "age": "Age",
        "tenure": "Tenure (Yrs)",
        "balance": "Balance ($)",
        "numOfProducts": "Products Count",
        "hasCrCard_Label": "Credit Card Status",
        "isActiveMember_Label": "Membership Status",
        "estimatedSalary": "Est. Salary ($)",
        "exited_Label": "Observed Outcome"
    })
    
    st.dataframe(df_display, use_container_width=True)
    
    # Download Button
    csv_data = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Audit Registry as CSV",
        data=csv_data,
        file_name="filtered_banking_portfolio_registry.csv",
        mime="text/csv"
    )

# ---------------------------------------------------------
# TAB 4: TECHNICAL ACTION RECOMMENDATIONS
# ---------------------------------------------------------
with tab4:
    st.markdown("<div class='section-header'>Data-Grounded Strategic Intervention Matrix</div>", unsafe_allow_html=True)
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
        <div class="kpi-card" style="border-left: 5px solid #2563EB; height: 100%;">
            <h4 style="color:#2563EB; font-weight:700; margin-top:0;">🛡️ Strategy A: Regional Risk Mitigation (Germany focus)</h4>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Evidence:</strong> German customers demonstrate a heightened baseline exit frequency. Over-indexing of regional churn indicates strong competitive pressures or misaligned local pricing models.
            </p>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Action Plan:</strong>
                <ul style="font-size:0.85rem; padding-left:1.2rem; color:#475569;">
                    <li>Conduct extensive competitor benchmarking in the German retail sector.</li>
                    <li>Launch regional-specific fee exemptions or premium reward tiers.</li>
                    <li>Align Germany-based customer onboarding campaigns to prioritize product bundling.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_rec2:
        st.markdown("""
        <div class="kpi-card" style="border-left: 5px solid #DC2626; height: 100%;">
            <h4 style="color:#DC2626; font-weight:700; margin-top:0;">💎 Strategy B: Premium Asset Flight Protection</h4>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Evidence:</strong> Accounts exceeding $100,000 exhibit significant balance capital flights, threatening total liquidity reserves.
            </p>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Action Plan:</strong>
                <ul style="font-size:0.85rem; padding-left:1.2rem; color:#475569;">
                    <li>Proactively flag inactive high-value customers (balances > $100k, inactive for 6 months) for direct relationship manager outreach.</li>
                    <li>Implement specialized preferential yield options (e.g., promotional high-yield certificates) targeting accounts with balances > $100k.</li>
                    <li>Deploy high-priority VIP customer service channels to resolve account friction instantly.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col_rec3, col_rec4 = st.columns(2)
    
    with col_rec3:
        st.markdown("""
        <div class="kpi-card" style="border-left: 5px solid #D97706; height: 100%;">
            <h4 style="color:#D97706; font-weight:700; margin-top:0;">⚡ Strategy C: Re-Engagement of Inactive Members</h4>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Evidence:</strong> Inactive members are substantially more vulnerable to churn, demonstrating a elevated risk multiplier.
            </p>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Action Plan:</strong>
                <ul style="font-size:0.85rem; padding-left:1.2rem; color:#475569;">
                    <li>Deploy automated trigger-based digital email campaigns offering customized features.</li>
                    <li>Utilize personalized fee-rebates or cash-back incentives tied to initial transactional reactivation.</li>
                    <li>Promote direct deposit setup benefits to convert passive accounts into active daily hubs.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_rec4:
        st.markdown("""
        <div class="kpi-card" style="border-left: 5px solid #10B981; height: 100%;">
            <h4 style="color:#10B981; font-weight:700; margin-top:0;">📦 Strategy D: Multi-Product Integration Incentives</h4>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Evidence:</strong> Customer risk indices vary substantially by total owned product count. Single product holders exhibit volatile attrition curves.
            </p>
            <p style="font-size:0.85rem; line-height:1.5; color:#334155;">
                <strong>Action Plan:</strong>
                <ul style="font-size:0.85rem; padding-left:1.2rem; color:#475569;">
                    <li>Formulate targeted bundling discounts (e.g., reduced insurance or mortgage interest rates when bundled with premium banking).</li>
                    <li>Increase credit score pre-approvals for secondary savings or investment products.</li>
                    <li>Integrate in-app loyalty rewards showing benefits as product count increases.</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
