from pathlib import Path
import re
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore", category=FutureWarning)
st.set_page_config(page_title="Ames Housing | Team 8", page_icon="⌂", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).resolve().parent

# ----------------------------- Theme ---------------------------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{
 --bg:#050706;--panel:#101512;--panel2:#151c18;--line:rgba(173,201,183,.12);
 --muted:#858f89;--text:#edf3ee;--green:#19d58b;--green2:#0e9c65;
 --orange:#f0783d;--violet:#a28cff;--red:#ee646b;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--text)}
.stApp{background:
 radial-gradient(ellipse at 52% 8%,rgba(28,82,54,.22),transparent 38%),
 radial-gradient(ellipse at 89% 63%,rgba(116,73,35,.12),transparent 29%),
 linear-gradient(145deg,#030504 0%,#080d0a 52%,#040605 100%);color:var(--text)}
[data-testid="stHeader"]{background:rgba(4,7,5,.76);border-bottom:1px solid rgba(190,215,198,.07)}
[data-testid="stToolbar"]{right:1rem}
[data-testid="stSidebar"],section[data-testid="stSidebar"]{
 background:linear-gradient(180deg,#080d0a 0%,#050806 100%);
 border-right:1px solid rgba(190,215,198,.10);
 width:248px!important;min-width:248px!important;max-width:248px!important;
}
[data-testid="stSidebar"] > div:first-child{padding:1.15rem .9rem 1rem;width:248px!important}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:.55rem}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stRadio"] > label{display:none!important}
[data-testid="stSidebar"] [data-testid="stRadio"]{width:100%;margin-top:.35rem}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"]{
 display:flex;flex-direction:column;align-items:stretch;gap:.38rem;width:100%;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label{
 box-sizing:border-box;display:flex;justify-content:flex-start;align-items:center;
 width:100%;min-width:0;height:44px;margin:0;padding:0 .85rem!important;
 border:1px solid transparent;border-radius:11px;background:transparent;
 color:#a6b1a9!important;font-size:.88rem!important;font-weight:500;
 white-space:nowrap;overflow:hidden;transition:background .15s,border-color .15s,color .15s;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{
 margin:0!important;font-size:.88rem!important;line-height:1.2!important;
 white-space:nowrap!important;overflow:hidden;text-overflow:ellipsis;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){
 background:linear-gradient(100deg,rgba(17,117,75,.34),rgba(10,53,34,.26));
 border-color:rgba(38,207,137,.22);color:#eafff3!important;
 box-shadow:inset 3px 0 0 #20cf88;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{
 background:rgba(255,255,255,.045);border-color:rgba(190,215,198,.08);color:#f0f6f1!important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input{accent-color:#20cf88}
[data-testid="stSidebar"] hr{border-color:rgba(190,215,198,.10);margin:.8rem .1rem}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{
 color:#718078;font: .62rem 'DM Mono',monospace;text-align:left;line-height:1.55;
}
.main .block-container{max-width:1580px;padding-top:1.05rem;padding-bottom:2.1rem;padding-left:2rem;padding-right:2rem}
h1,h2,h3{font-family:'Manrope',sans-serif;letter-spacing:-.045em;color:#f0f5f1}
h1{font-size:1.8rem!important;font-weight:700!important}
h2{font-size:1.2rem!important}
h3{font-size:1rem!important}
.hero{padding:.55rem 0 .95rem;text-align:center;position:relative}
.hero-greeting{font:500 .78rem 'DM Sans',sans-serif;color:#e4ebe6;letter-spacing:.01em;margin-bottom:.45rem}
.hero-kicker{font: .61rem 'DM Mono',monospace;color:#47dca0;letter-spacing:.17em;text-transform:uppercase;margin-bottom:.55rem}
.hero-title{font:500 clamp(1.8rem,3.2vw,2.65rem) 'Manrope',sans-serif;letter-spacing:-.065em;color:#cbd3ce;line-height:1.12}
.hero-title strong{font-weight:700;color:#f4f7f4}
.hero-sub{font-size:.78rem;color:#858f89;margin-top:.55rem}
.top-controls{border:1px solid rgba(176,201,184,.11);border-radius:15px;background:rgba(12,18,14,.74);padding:.6rem .8rem;margin:.25rem 0 1.05rem}
.panel-title{font-family:'DM Sans',sans-serif;font-size:.88rem;font-weight:600;color:#e1eae3;margin:0 0 7px}
.panel-sub{color:#7e8982;font: .63rem 'DM Mono',monospace;letter-spacing:.04em;margin-top:-2px;margin-bottom:9px}
.metric-card{background:linear-gradient(145deg,rgba(28,35,30,.82),rgba(12,17,14,.94));border:1px solid rgba(181,207,190,.13);border-radius:17px;padding:14px 15px;min-height:112px;box-shadow:0 12px 30px rgba(0,0,0,.15)}
.metric-card.primary{background:linear-gradient(140deg,rgba(20,75,49,.94),rgba(10,31,20,.96));border-color:rgba(42,207,135,.34)}
.metric-card.green{background:linear-gradient(140deg,rgba(18,49,34,.94),rgba(9,19,13,.96));border-color:rgba(42,207,135,.22)}
.metric-card.purple{background:linear-gradient(140deg,rgba(37,34,49,.91),rgba(14,16,19,.96));border-color:rgba(161,140,255,.2)}
.metric-label{color:#98a49c;font: .62rem 'DM Mono',monospace;letter-spacing:.08em;margin-bottom:7px}
.metric-value{color:#f2f7f3;font-family:'Manrope',sans-serif;font-size:1.36rem;font-weight:750;letter-spacing:-.035em}
.metric-note{color:#78847c;font-size:.66rem;margin-top:4px}
.metric-card.primary .metric-label,.metric-card.primary .metric-value,.metric-card.primary .metric-note{color:#effff5}
.mini-card{background:linear-gradient(150deg,rgba(24,31,26,.86),rgba(9,14,11,.95));border:1px solid rgba(177,204,186,.12);border-radius:17px;padding:13px 14px 8px;min-height:218px}
.gauge-card{background:linear-gradient(165deg,rgba(28,44,34,.94),rgba(10,17,12,.98));border:1px solid rgba(181,207,190,.16);border-radius:19px;padding:16px 14px 14px;min-height:100%;box-shadow:0 15px 35px rgba(0,0,0,.2)}
.gauge-caption{text-align:center;color:#e4ece6;font-size:.78rem;font-weight:600;margin-top:-.2rem}
.gauge-sub{text-align:center;color:#7e8982;font-size:.63rem;margin-top:.25rem}
.insight-row{display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-bottom:1px solid rgba(181,207,190,.10);color:#dce7df;font-size:.78rem}
.insight-dot{width:27px;height:27px;flex:0 0 27px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:rgba(21,125,77,.22);color:#43dda0;font-weight:800}
[data-testid="stDataFrame"]{border:1px solid rgba(181,207,190,.14);border-radius:12px;overflow:hidden}
div[data-testid="stAlert"]{border-radius:12px;background:#101a13;border:1px solid #293b2f}
div[data-testid="stPlotlyChart"]{background:linear-gradient(145deg,rgba(20,27,22,.78),rgba(8,12,9,.84));border:1px solid rgba(181,207,190,.10);border-radius:16px;padding:6px 7px}
div[data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(150deg,rgba(23,31,25,.88),rgba(9,14,11,.96));border:1px solid rgba(181,207,190,.13)!important;border-radius:18px;padding:10px 11px 7px}
div[data-testid="stSelectbox"] label,div[data-testid="stMultiSelect"] label,div[data-testid="stSlider"] label{color:#9aaca1!important;font-size:.72rem}
.stButton>button,.stDownloadButton>button{background:#123e2a;border:1px solid #286344;color:#e5fff0;border-radius:10px}
.stButton>button:hover,.stDownloadButton>button:hover{background:#155238;border-color:#35bd7c;color:white}
[data-testid="stTextInput"] input,[data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:#0d1510;color:#e8eee9;border:1px solid rgba(181,207,190,.16);border-radius:11px}
[data-testid="stExpander"]{border:1px solid rgba(181,207,190,.12);border-radius:14px;background:rgba(10,15,12,.55)}
.stCaption{color:#7f8b83}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

PLOT={"template":"plotly_dark","paper_bgcolor":"rgba(0,0,0,0)","plot_bgcolor":"rgba(0,0,0,0)","font":{"family":"DM Sans","color":"#cbd8cf"},"margin":{"l":12,"r":12,"t":42,"b":12},"colorway":["#00d68f","#4be3a8","#8ccfb0","#f28b35","#d7bd55","#7ba58e"]}

def norm(v): return re.sub(r"[^a-z0-9]", "", str(v).lower())
def find_col(df,*aliases):
    lookup={norm(c):c for c in df.columns}
    for a in aliases:
        if norm(a) in lookup:return lookup[norm(a)]
    return None

def locate(candidates):
    for x in candidates:
        p=ROOT/x
        if p.exists():return p
    names={Path(x).name.lower() for x in candidates}
    for p in ROOT.rglob('*.csv'):
        if p.name.lower() in names:return p
    return None

@st.cache_data(show_spinner=False)
def read_csv(path): return pd.read_csv(path,low_memory=False)
def load(candidates):
    p=locate(candidates)
    if p is None:return None,None
    try:return read_csv(str(p)),p
    except Exception as e:st.warning(f"Could not read {p.name}: {e}");return None,p

def money(x):return "N/A" if pd.isna(x) else f"${x:,.0f}"
def metric(label,value,note='',style=''):
    st.markdown(f'<div class="metric-card {style}"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',unsafe_allow_html=True)
def layout(fig,height=360):
    fig.update_layout(**PLOT,height=height)
    fig.update_xaxes(showgrid=False,zeroline=False,linecolor="#2a394a")
    fig.update_yaxes(gridcolor="#223142",zeroline=False)
    return fig
def section(title):st.markdown(f'<div class="panel-title">{title}</div>',unsafe_allow_html=True)
def numeric(df,col):return pd.to_numeric(df[col],errors='coerce')
def safe_sample(df,n=2500):return df if len(df)<=n else df.sample(n,random_state=42)

# ----------------------------- Data ----------------------------------
clean,clean_path=load(["Week 3/AmesHousing_Uncleaned_Cleaned.csv","Week 5/Cleaned_AmesHousing_Week5.csv","Week 6/Cleaned_AmesHousing_Week6.csv"])
engineered,engineered_path=load(["Week 6/Feature_Engineered_AmesHousing.csv"])
selected,selected_path=load(["Week 7/Selected_Features_AmesHousing.csv"])
pca,pca_path=load(["Week 7/PCA_Transformed_AmesHousing.csv"])
variance,variance_path=load(["Week 7/PCA_Explained_Variance.csv","Week 7/Explained_Variance.csv","Week 7/PCA_ExplainedVariance.csv","Week 7/pca_variance.csv"])
if clean is None:
    st.error("Cleaned Ames Housing data was not found. Keep app.py in the repository root and verify the Week 3 cleaned CSV path.")
    st.stop()
price=find_col(clean,'SalePrice','Sale Price')
neigh=find_col(clean,'Neighborhood')
quality=find_col(clean,'Overall Qual','OverallQual','Overall Quality')
area=find_col(clean,'Gr Liv Area','GrLivArea','Above Ground Living Area')
year_built=find_col(clean,'Year Built','YearBuilt')
year_sold=find_col(clean,'YrSold','Year Sold')
if price is None:st.error('SalePrice column was not found in the cleaned dataset.');st.stop()
clean[price]=pd.to_numeric(clean[price],errors='coerce')
base=clean.dropna(subset=[price]).copy()

# ----------------------------- Sidebar --------------------------------
nav_map = {
    "⌂   Overview": "Overview",
    "▥   Market Analysis": "Market Analysis",
    "⌁   Statistical Insights": "Statistical Insights",
    "◇   Feature Engineering": "Feature Engineering",
    "◌   PCA Analysis": "PCA Analysis",
    "▣   Property Explorer": "Property Explorer",
}
with st.sidebar:
    st.markdown('''
    <div style="display:flex;align-items:center;gap:11px;padding:2px 7px 18px;margin-bottom:10px;border-bottom:1px solid rgba(190,215,198,.10)">
      <div style="width:38px;height:38px;flex:0 0 38px;border-radius:12px;background:linear-gradient(145deg,#25df98,#08744b);color:#06150d;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800">⌂</div>
      <div style="min-width:0">
        <div style="font:700 13px 'Manrope',sans-serif;color:#edf5ef;white-space:nowrap">AMES HOUSING</div>
        <div style="font:9px 'DM Mono',monospace;color:#718078;letter-spacing:.16em;margin-top:3px">TEAM 08 · ANALYTICS</div>
      </div>
    </div>
    <div style="font:9px 'DM Mono',monospace;color:#637169;letter-spacing:.15em;padding:5px 9px 2px">WORKSPACE</div>
    ''', unsafe_allow_html=True)
    selected_page = st.radio(
        'Navigation', list(nav_map.keys()), index=0,
        label_visibility='collapsed',
        help='Navigate between dashboard sections'
    )
    page = nav_map[selected_page]
    st.divider()
    st.markdown('''
    <div style="padding:8px 9px;color:#748078;font:10px 'DM Mono',monospace;line-height:1.8">
      DATASET<br><span style="color:#c4d1c8">AMES HOUSING</span><br>
      <span style="color:#5f6d64">2,930 RECORDS · TEAM 08</span>
    </div>
    ''', unsafe_allow_html=True)

# ----------------------------- Header ---------------------------------
st.markdown('<div class="hero"><div class="hero-greeting">Good morning, Team 8</div><div class="hero-title">Just ask your data <strong>anything.</strong></div><div class="hero-sub">Explore property values, neighbourhoods and the features shaping the Ames housing market.</div></div>', unsafe_allow_html=True)

# Global filters live in a compact top strip instead of crowding the icon rail.
view = base.copy()
with st.expander('⌕  Refine the dataset', expanded=False):
    filter_cols = st.columns([1.35, 1, 1])
    with filter_cols[0]:
        if neigh:
            vals = sorted(view[neigh].dropna().astype(str).unique())
            chosen = st.multiselect('Neighborhoods', vals, default=[], placeholder='All neighborhoods')
            if chosen:
                view = view[view[neigh].astype(str).isin(chosen)]
        else:
            st.caption('Neighborhood field unavailable')
    with filter_cols[1]:
        if quality:
            q = numeric(view, quality).dropna()
            if len(q) and q.min() < q.max():
                qrange = st.slider('Overall quality', int(q.min()), int(q.max()), (int(q.min()), int(q.max())))
                view = view[numeric(view, quality).between(*qrange)]
        else:
            st.caption('Quality field unavailable')
    with filter_cols[2]:
        if year_sold:
            yrs = sorted(numeric(view, year_sold).dropna().astype(int).unique())
            if len(yrs) > 1:
                yrange = st.select_slider('Year sold', options=yrs, value=(yrs[0], yrs[-1]))
                view = view[numeric(view, year_sold).between(*yrange)]
        else:
            st.caption('Year sold field unavailable')

mean_price = view[price].mean() if len(view) else np.nan
median_price = view[price].median() if len(view) else np.nan
avg_area = numeric(view, area).mean() if area else np.nan

# ----------------------------- Overview -------------------------------
if page=='Overview':
    search_col, meta_col = st.columns([2.2, 1])
    with search_col:
        quick_search = st.text_input('Explore records', placeholder='Search neighborhood, feature or property value…', label_visibility='collapsed', key='overview_quick_search')
    with meta_col:
        st.markdown(f'<div style="text-align:right;color:#7f8b83;font:10px DM Mono;padding-top:9px">FILTERED VIEW · {len(view):,} RECORDS</div>', unsafe_allow_html=True)
    overview_view = view
    if quick_search:
        qmask = overview_view.astype(str).apply(lambda col: col.str.contains(re.escape(quick_search), case=False, na=False)).any(axis=1)
        overview_view = overview_view[qmask]
    view = overview_view
    mean_price = view[price].mean() if len(view) else np.nan
    median_price = view[price].median() if len(view) else np.nan
    avg_area = numeric(view, area).mean() if area else np.nan

    # Three compact insight cards and a tall market-position gauge, inspired by the supplied reference.
    left_area, gauge_area = st.columns([3.05, 1.0], gap='medium')
    with left_area:
        card_cols = st.columns(3, gap='small')
        with card_cols[0]:
            with st.container(border=True):
                section('⌁  Market Activity')
                metric('PROPERTIES IN VIEW', f'{len(view):,}', f'{len(base):,} total cleaned records', 'primary')
                if year_sold and len(view):
                    counts = view.assign(_year=numeric(view, year_sold)).dropna(subset=['_year']).groupby('_year').size().reset_index(name='Properties')
                    fig = px.bar(counts, x='_year', y='Properties', color_discrete_sequence=['#ff743c'])
                    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None, margin=dict(l=0,r=0,t=2,b=0))
                    fig.update_xaxes(showticklabels=False); fig.update_yaxes(showticklabels=False)
                    st.plotly_chart(layout(fig, 108), use_container_width=True, config={'displayModeBar':False})
                else:
                    st.caption('Sales activity by year is unavailable.')
        with card_cols[1]:
            with st.container(border=True):
                section('◉  Price Profile')
                metric('MEDIAN SALE PRICE', money(median_price), f'Average {money(mean_price)}', 'green')
                if len(view):
                    fig = px.histogram(view, x=price, nbins=24, color_discrete_sequence=['#d9783f'])
                    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None, margin=dict(l=0,r=0,t=2,b=0), bargap=.08)
                    fig.update_xaxes(showticklabels=False); fig.update_yaxes(showticklabels=False)
                    st.plotly_chart(layout(fig, 108), use_container_width=True, config={'displayModeBar':False})
                else:
                    st.caption('No records match the current filters.')
        with card_cols[2]:
            with st.container(border=True):
                section('♡  Home Quality')
                qmean = numeric(view, quality).mean() if quality else np.nan
                metric('AVERAGE QUALITY', f'{qmean:.1f} / 10' if pd.notna(qmean) else 'N/A', 'Overall material and finish rating', 'purple')
                if quality and len(view):
                    qdist = numeric(view, quality).dropna().round().value_counts().sort_index().rename_axis('Quality').reset_index(name='Properties')
                    fig = px.bar(qdist, x='Quality', y='Properties', color_discrete_sequence=['#d6ac4e'])
                    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None, margin=dict(l=0,r=0,t=2,b=0), bargap=.22)
                    fig.update_xaxes(showticklabels=False); fig.update_yaxes(showticklabels=False)
                    st.plotly_chart(layout(fig, 108), use_container_width=True, config={'displayModeBar':False})
                else:
                    st.caption('Quality scores are unavailable.')

        st.write('')
        lower_left, lower_right = st.columns([1.2, 1], gap='medium')
        with lower_left:
            section('Market Pulse')
            st.markdown('<div class="panel-sub">AVERAGE AND MEDIAN SALE PRICE BY YEAR SOLD</div>', unsafe_allow_html=True)
            if year_sold and len(view):
                temp = view.copy(); temp['_year'] = numeric(temp, year_sold)
                yearly = temp.dropna(subset=['_year']).groupby('_year')[price].agg(['mean','median','count']).reset_index()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=yearly['_year'], y=yearly['mean'], mode='lines+markers', name='Average price', line={'color':'#f0783d','width':2.5}, fill='tozeroy', fillcolor='rgba(240,120,61,.07)'))
                fig.add_trace(go.Scatter(x=yearly['_year'], y=yearly['median'], mode='lines+markers', name='Median price', line={'color':'#18d58b','width':2.5}))
                fig.update_layout(legend={'orientation':'h','y':1.12,'x':0}, hovermode='x unified')
                st.plotly_chart(layout(fig, 280), use_container_width=True, config={'displayModeBar':False})
            else:
                st.info('Year sold data is unavailable for this view.')
        with lower_right:
            section('Price Drivers')
            st.markdown('<div class="panel-sub">FEATURES MOST ASSOCIATED WITH SALE PRICE</div>', unsafe_allow_html=True)
            num = view.select_dtypes(include=np.number)
            if price in num and num.shape[1] > 1:
                corr = num.corr(numeric_only=True)[price].drop(price).dropna()
                corr = corr.reindex(corr.abs().sort_values(ascending=False).index).head(7).sort_values()
                fig = px.bar(x=corr.values, y=corr.index, orientation='h', labels={'x':'Pearson r','y':''}, color=corr.values, color_continuous_scale=['#ce7652','#344c40','#19d58b'], range_color=[-1,1])
                fig.update_layout(coloraxis_showscale=False, margin=dict(l=4,r=10,t=10,b=6))
                st.plotly_chart(layout(fig, 280), use_container_width=True, config={'displayModeBar':False})
            else:
                st.info('Not enough numeric data to calculate correlations.')
    with gauge_area:
        with st.container(border=True):
            section('◌  Market Position')
            st.markdown('<div class="panel-sub">MEDIAN PRICE PERCENTILE</div>', unsafe_allow_html=True)
            if len(view) and pd.notna(median_price):
                percentile = float((base[price] <= median_price).mean() * 100)
            else:
                percentile = 0.0
            gauge = go.Figure(go.Indicator(
                mode='gauge+number', value=percentile,
                number={'suffix':'%','font':{'size':36,'color':'#f2f7f3','family':'Manrope'}},
                gauge={
                    'axis':{'range':[0,100],'tickvals':[0,25,50,75,100],'tickfont':{'color':'#7e8982','size':9},'tickcolor':'#718078'},
                    'bar':{'color':'#18d58b','thickness':.18},
                    'bgcolor':'rgba(0,0,0,0)','borderwidth':0,
                    'steps':[{'range':[0,35],'color':'#202b24'},{'range':[35,70],'color':'#29372e'},{'range':[70,100],'color':'#344438'}],
                    'threshold':{'line':{'color':'#f0783d','width':3},'thickness':.8,'value':50}
                }
            ))
            gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font={'color':'#dce7df'},height=255,margin=dict(l=8,r=8,t=18,b=2))
            st.plotly_chart(gauge, use_container_width=True, config={'displayModeBar':False})
            st.markdown('<div class="gauge-caption">Selected market price position</div>', unsafe_allow_html=True)
            st.markdown('<div class="gauge-sub">Percentile of the selected median<br>against all cleaned records</div>', unsafe_allow_html=True)
            st.divider()
            st.markdown(f'<div style="font: .62rem DM Mono;color:#87948b;line-height:1.9">MEDIAN PRICE<br><span style="font:700 1.25rem Manrope;color:#f1f7f2">{money(median_price)}</span><br><br>AVG. LIVING AREA<br><span style="font:700 1.05rem Manrope;color:#f1f7f2">{f"{avg_area:,.0f} sq.ft" if pd.notna(avg_area) else "N/A"}</span></div>', unsafe_allow_html=True)

    # Contextual insight strip below the main composition.
    insights = []
    if area and len(view) > 2:
        r = view[price].corr(numeric(view, area))
        if pd.notna(r): insights.append(f'Living area correlation: {r:+.2f}')
    if quality and len(view) > 2:
        r = view[price].corr(numeric(view, quality))
        if pd.notna(r): insights.append(f'Overall quality correlation: {r:+.2f}')
    if neigh and len(view):
        by_neigh = view.groupby(neigh)[price].median().dropna()
        if len(by_neigh): insights.append(f'Highest median in view: {by_neigh.idxmax()}')
    if insights:
        st.markdown('<div style="height:7px"></div><div class="panel-sub">QUICK OBSERVATIONS</div>', unsafe_allow_html=True)
        obs_cols = st.columns(len(insights))
        for c, text in zip(obs_cols, insights):
            with c:
                st.markdown(f'<div class="insight-row"><span class="insight-dot">↗</span><span>{text}</span></div>', unsafe_allow_html=True)
    st.caption(f"Source: {clean_path.relative_to(ROOT) if clean_path else 'cleaned CSV'} · {clean.shape[0]:,} rows × {clean.shape[1]:,} columns · Correlation does not imply causation.")

# ----------------------------- Market ---------------------------------
elif page=='Market Analysis':
    st.markdown('### Market patterns')
    st.caption('Compare neighbourhood pricing, property size and quality across the filtered dataset.')
    if neigh and len(view):
        ndf=view.dropna(subset=[neigh]).copy();stats=ndf.groupby(neigh)[price].agg(['median','mean','count']).reset_index().sort_values('median',ascending=False)
        left,right=st.columns([1.2,1])
        with left:
            section('Median Sale Price by Neighborhood')
            fig=px.bar(stats.head(18).sort_values('median'),x='median',y=neigh,orientation='h',color='median',color_continuous_scale=['#1c4775','#40c4e8'],hover_data={'count':True,'mean':':,.0f'})
            fig.update_layout(coloraxis_showscale=False);st.plotly_chart(layout(fig,500),use_container_width=True)
        with right:
            section('Neighborhood Summary')
            display=stats.rename(columns={neigh:'Neighborhood','median':'Median price','mean':'Average price','count':'Properties'})
            st.dataframe(display.style.format({'Median price':'${:,.0f}','Average price':'${:,.0f}','Properties':'{:,.0f}'}),hide_index=True,use_container_width=True,height=500)
        st.markdown('#### Sale Price Distribution by Neighborhood')
        top_names=stats.head(12)[neigh].tolist()
        boxdf=ndf[ndf[neigh].isin(top_names)].copy()
        fig=px.box(boxdf,x=neigh,y=price,color=neigh,points='outliers',labels={neigh:'Neighborhood',price:'Sale price'})
        fig.update_layout(showlegend=False);st.plotly_chart(layout(fig,440),use_container_width=True)
    if area:
        st.markdown('#### Living Area vs Sale Price')
        x,y=st.columns([1,3]);
        with x:plot_mode=st.radio('Plot style',['Density','Scatter'],horizontal=False)
        sdf=view[[area,price]+([quality] if quality else [])].copy();sdf[area]=numeric(sdf,area);sdf=sdf.dropna(subset=[area,price])
        if plot_mode=='Density':
            fig=px.density_heatmap(sdf,x=area,y=price,nbinsx=35,nbinsy=35,color_continuous_scale=['#101b2a','#1267b8','#43c4ee'],labels={area:'Living area (sq.ft)',price:'Sale price'})
        else:
            sdf=safe_sample(sdf);fig=px.scatter(sdf,x=area,y=price,color=quality if quality else None,opacity=.65,labels={area:'Living area (sq.ft)',price:'Sale price'})
        with y:st.plotly_chart(layout(fig,420),use_container_width=True)
    if quality:
        st.markdown('#### Sale Price by Overall Quality')
        qdf=view[[quality,price]].copy();qdf[quality]=numeric(qdf,quality);qdf=qdf.dropna()
        fig=px.violin(qdf,x=quality,y=price,box=True,points=False,color=quality,color_discrete_sequence=['#18C982'],labels={quality:'Overall quality',price:'Sale price'})
        fig.update_layout(coloraxis_showscale=False);st.plotly_chart(layout(fig,390),use_container_width=True)
    if year_built:
        st.markdown('#### Property Age vs Sale Price')
        age=view[[year_built,price]+([quality] if quality else [])].copy();age[year_built]=numeric(age,year_built);age['Property Age']=2026-age[year_built];age=age[(age['Property Age']>=0)&(age['Property Age']<250)].dropna(subset=['Property Age',price]);age=safe_sample(age)
        fig=px.scatter(age,x='Property Age',y=price,color=quality if quality else None,opacity=.6,labels={price:'Sale price',quality:'Overall quality'} if quality else {price:'Sale price'})
        st.plotly_chart(layout(fig,390),use_container_width=True)
    st.caption('Year-based property age is calculated relative to 2026. These are observed associations, not causal effects.')

# ----------------------------- Statistics -----------------------------
elif page=='Statistical Insights':
    st.markdown('### Statistical relationships')
    st.caption('Explore distributions, correlations and statistical outliers in the selected records.')
    numeric_df=view.select_dtypes(include=np.number)
    if price in numeric_df and numeric_df.shape[1]>1:
        corr=numeric_df.corr(numeric_only=True)[price].drop(price).dropna().reindex(numeric_df.corr(numeric_only=True)[price].drop(price).dropna().abs().sort_values(ascending=False).index)
        l,r=st.columns([1,1.2])
        with l:
            section('Strongest Correlations with Sale Price');top=corr.head(18).sort_values()
            fig=px.bar(x=top.values,y=top.index,orientation='h',labels={'x':'Pearson correlation','y':''},color=top.values,color_continuous_scale=['#e57c82','#263b56','#28c997'],range_color=[-1,1]);fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(layout(fig,520),use_container_width=True)
        with r:
            section('Feature Correlation Heatmap');cols=[price]+list(corr.head(12).index);matrix=numeric_df[cols].corr()
            fig=px.imshow(matrix,text_auto='.2f',aspect='auto',color_continuous_scale='RdBu',zmin=-1,zmax=1)
            st.plotly_chart(layout(fig,520),use_container_width=True)
    st.markdown('#### Distribution and outlier analysis')
    candidates=[c for c in [price,area,quality] if c]
    chosen=st.selectbox('Numeric feature',candidates,index=0)
    vals=numeric(view,chosen).dropna();l,r=st.columns(2)
    with l:
        fig=px.histogram(vals,nbins=45,marginal='box',labels={'value':chosen},color_discrete_sequence=['#00d68f']);st.plotly_chart(layout(fig,350),use_container_width=True)
    with r:
        q1,q3=vals.quantile(.25),vals.quantile(.75);iqr=q3-q1;low,high=q1-1.5*iqr,q3+1.5*iqr;out=((vals<low)|(vals>high)).sum()
        metric('VALID VALUES',f'{len(vals):,}','Non-null observations','primary');metric('IQR OUTLIERS',f'{out:,}',f'Outside {low:,.1f} to {high:,.1f}')
    st.markdown('#### Descriptive statistics');st.dataframe(view.describe(include='all').transpose(),use_container_width=True)
    st.caption('Pearson correlation captures linear association. IQR outliers are statistical flags, not necessarily data errors.')

# ----------------------------- Feature Engineering -------------------
elif page=='Feature Engineering':
    st.markdown('### Engineered feature review')
    st.caption('Inspect the feature-engineered dataset and its relationship with sale price.')
    if engineered is None:st.warning('Week 6 feature-engineered CSV was not found. Check its filename and path.')
    else:
        st.caption(f'Source: {engineered_path.relative_to(ROOT)} · {engineered.shape[0]:,} rows × {engineered.shape[1]:,} columns')
        ep=find_col(engineered,'SalePrice','Sale Price')
        a,b,c=st.columns(3)
        with a:metric('ENGINEERED ROWS',f'{engineered.shape[0]:,}','Week 6 records','primary')
        with b:metric('ENGINEERED COLUMNS',f'{engineered.shape[1]:,}','Total features')
        with c:metric('ADDED COLUMNS',f'{max(engineered.shape[1]-clean.shape[1],0):,}','Net column increase','green')
        if ep:
            en=engineered.select_dtypes(include=np.number);ec=en.corr(numeric_only=True)[ep].drop(ep).dropna();ec=ec.reindex(ec.abs().sort_values(ascending=False).index).head(20).sort_values()
            section('Features Most Associated with Sale Price');fig=px.bar(x=ec.values,y=ec.index,orientation='h',labels={'x':'Pearson correlation','y':'Feature'},color=ec.values,color_continuous_scale=['#e57c82','#263b56','#28c997'],range_color=[-1,1]);fig.update_layout(coloraxis_showscale=False);st.plotly_chart(layout(fig,520),use_container_width=True)
            st.caption('Correlation-based exploration only. This is not model feature importance.')
        original=set(clean.columns);new_cols=[c for c in engineered.columns if c not in original]
        st.markdown('#### New engineered columns');st.write(f'{len(new_cols):,} columns not present in the cleaned dataset.')
        st.dataframe(pd.DataFrame({'Engineered feature':new_cols}),hide_index=True,use_container_width=True,height=260)
    if selected is not None:
        st.markdown('#### Week 7 selected feature set');m,n=st.columns(2)
        with m:metric('SELECTED FEATURES',f'{selected.shape[1]:,}','Columns in selected dataset','purple')
        with n:metric('OBSERVATIONS',f'{selected.shape[0]:,}','Rows in selected dataset')
        st.dataframe(pd.DataFrame({'Selected feature':selected.columns}),hide_index=True,use_container_width=True,height=240)
    st.markdown('#### Data quality monitor')
    missing=view.isna().sum();quality_df=pd.DataFrame({'Column':view.columns,'Data type':view.dtypes.astype(str).values,'Missing':missing.values,'Missing %':(missing/ max(len(view),1)*100).round(2).values,'Unique values':view.nunique(dropna=True).values})
    m1,m2,m3=st.columns(3)
    with m1:metric('MISSING CELLS',f'{int(missing.sum()):,}','Across filtered cleaned data','primary')
    with m2:metric('DUPLICATE ROWS',f'{int(view.duplicated().sum()):,}','Exact duplicate records')
    with m3:metric('FEATURES',f'{view.shape[1]:,}',f'{view.select_dtypes(include=np.number).shape[1]} numeric')
    st.dataframe(quality_df.sort_values('Missing',ascending=False),hide_index=True,use_container_width=True,height=330)

# ----------------------------- PCA ------------------------------------
elif page=='PCA Analysis':
    st.markdown('### Principal Component Analysis')
    st.caption('Review the reduced feature space and explained variance from Week 7.')
    if pca is None:st.warning('Week 7 PCA-transformed CSV was not found.')
    else:
        st.caption(f'Source: {pca_path.relative_to(ROOT)} · {pca.shape[0]:,} rows × {pca.shape[1]:,} columns')
        pc_cols=[c for c in pca.columns if re.match(r'(?i)^(pc|principal.?component)[ _-]*\d+$',str(c).strip())]
        pc_cols=sorted(pc_cols,key=lambda c:int(re.search(r'\d+',str(c)).group()) if re.search(r'\d+',str(c)) else 9999)
        a,b,c=st.columns(3)
        with a:metric('OBSERVATIONS',f'{len(pca):,}','Rows in PCA output','primary')
        with b:metric('OUTPUT COLUMNS',f'{pca.shape[1]:,}','Transformed dataset')
        with c:metric('DETECTED COMPONENTS',f'{len(pc_cols):,}' if pc_cols else 'Unknown','Based on PC column labels','purple')
        if len(pc_cols)>=2:
            xcol,ycol=pc_cols[:2];plot=pca[[xcol,ycol]].apply(pd.to_numeric,errors='coerce').dropna();plot=safe_sample(plot,3500)
            st.markdown('#### PC1 vs PC2');fig=px.scatter(plot,x=xcol,y=ycol,opacity=.55,color_discrete_sequence=['#3988ff'],labels={xcol:'Principal Component 1',ycol:'Principal Component 2'})
            st.plotly_chart(layout(fig,450),use_container_width=True)
        if variance is not None:
            st.markdown('#### Explained variance')
            vcol=find_col(variance,'Explained Variance Ratio','Explained Variance','Variance Ratio')
            ccol=find_col(variance,'Component','Principal Component','PC')
            if vcol:
                variance[vcol]=pd.to_numeric(variance[vcol],errors='coerce');variance=variance.dropna(subset=[vcol]).copy()
                variance['_component']=variance[ccol].astype(str) if ccol else [f'PC{i+1}' for i in range(len(variance))]
                variance['_cumulative']=variance[vcol].cumsum()
                fig=go.Figure();fig.add_bar(x=variance['_component'],y=variance[vcol],name='Individual variance',marker_color='#168cff');fig.add_scatter(x=variance['_component'],y=variance['_cumulative'],name='Cumulative variance',yaxis='y2',mode='lines+markers',line={'color':'#8ccfb0','width':3})
                fig.update_layout(yaxis={'title':'Explained variance ratio'},yaxis2={'title':'Cumulative ratio','overlaying':'y','side':'right','range':[0,1]})
                st.plotly_chart(layout(fig,420),use_container_width=True)
                reached=np.argmax(variance['_cumulative'].values>=.95)+1 if (variance['_cumulative']>=.95).any() else None
                if reached:st.success(f"{reached} components reach at least 95% cumulative explained variance.")
            else:st.warning('Variance metadata file was found, but no explained-variance column could be identified.')
        else:st.info('Explained-variance metadata was not found. Add the PCA explained-variance output from Week 7 to display the scree and cumulative variance plots. Transformed component scores alone cannot provide this information.')
        st.markdown('#### PCA output preview');st.dataframe(pca.head(12),use_container_width=True)

# ----------------------------- Property Explorer ---------------------
elif page=='Property Explorer':
    st.markdown('### Explore individual properties')
    st.caption('Search and inspect records from the currently filtered cleaned dataset.')
    search=st.text_input('Search properties',placeholder='Neighborhood, property ID, or any text in the record')
    explore=view.copy()
    if search:
        mask=explore.astype(str).apply(lambda col:col.str.contains(re.escape(search),case=False,na=False)).any(axis=1)
        explore=explore[mask]
    st.write(f'{len(explore):,} matching properties')
    export=explore.to_csv(index=False).encode('utf-8')
    st.download_button('Download filtered properties (CSV)',data=export,file_name='ames_housing_filtered_properties.csv',mime='text/csv')
    st.dataframe(explore,use_container_width=True,height=390)
    if len(explore):
        st.markdown('#### Property details')
        idcol=find_col(explore,'Order','PID','Id','Property ID')
        labels=explore[idcol].astype(str).tolist() if idcol else [f'Row {i+1}' for i in range(len(explore))]
        chosen_label=st.selectbox('Select a property',labels)
        row=explore.iloc[labels.index(chosen_label)]
        preferred=[price,neigh,quality,area,year_built,find_col(explore,'Garage Cars','GarageCars'),find_col(explore,'Total Bsmt SF','TotalBsmtSF'),find_col(explore,'Full Bath','FullBath'),find_col(explore,'Bedroom AbvGr','BedroomAbvGr')]
        cols=[c for c in preferred if c and c in explore.columns]
        if not cols:cols=list(explore.columns[:12])
        detail=pd.DataFrame({'Attribute':cols,'Value':[row[c] for c in cols]})
        st.dataframe(detail,hide_index=True,use_container_width=True)

# ----------------------------- Footer ---------------------------------
st.divider();st.caption('Team 8 · Ames Housing Analysis | Streamlit · Pandas · Plotly')