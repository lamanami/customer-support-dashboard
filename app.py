import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Customer Support Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       APP BACKGROUND
    ===================================================== */

    .stApp {
        background:
            linear-gradient(
                180deg,
                #101827 0%,
                #111827 100%
            );
        color: #f8fafc;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       HIDE DEFAULT STREAMLIT CLUTTER
    ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }


    /* =====================================================
       WIDER SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {
        width: 330px !important;
        min-width: 330px !important;
        max-width: 330px !important;

        background:
            linear-gradient(
                180deg,
                #0b1220 0%,
                #111827 100%
            );

        border-right: 1px solid #263244;
    }

    section[data-testid="stSidebar"] > div {
        width: 330px !important;
        padding: 1.5rem 1.15rem 2rem 1.15rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #cbd5e1 !important;
    }

    section[data-testid="stSidebar"] label {
        font-weight: 650;
    }


    /* =====================================================
       SIDEBAR MULTISELECT
    ===================================================== */

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background: #172033 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"]
    span[data-baseweb="tag"] {
        background: #1e3a5f !important;
        border-radius: 8px !important;
    }


    /* =====================================================
       HEADER CARD
    ===================================================== */

    .dashboard-header {
        background:
            linear-gradient(
                135deg,
                #18263d 0%,
                #223b5f 55%,
                #28577a 100%
            );

        border: 1px solid #334155;
        border-radius: 22px;

        padding: 28px 32px;

        margin-bottom: 26px;

        box-shadow:
            0 12px 30px rgba(0,0,0,0.24);
    }

    .dashboard-title {
        color: #ffffff;
        font-size: 2.15rem;
        font-weight: 850;
        letter-spacing: -0.5px;
    }

    .dashboard-subtitle {
        color: #cbd5e1;
        margin-top: 8px;
        font-size: 0.98rem;
        line-height: 1.55;
    }


    /* =====================================================
       SECTION TITLES
    ===================================================== */

    .section-title {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 8px;
        margin-bottom: 14px;
    }


    /* =====================================================
       KPI CARDS
    ===================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #1e293b,
                #172033
            );

        border: 1px solid #334155;

        border-radius: 18px;

        padding: 20px 22px;

        box-shadow:
            0 8px 22px rgba(0,0,0,0.20);
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.82rem;
        font-weight: 650;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.8rem;
        font-weight: 850;
    }


    /* =====================================================
   PLOTLY CARDS
===================================================== */

div[data-testid="stPlotlyChart"] {
    width: 100% !important;

    background:
        linear-gradient(
            145deg,
            #1b2433,
            #202b3c
        );

    border: 1px solid #334155;

    border-radius: 20px !important;

    overflow: hidden !important;

    padding: 0 !important;

    box-sizing: border-box;

    box-shadow:
        0 8px 24px rgba(0,0,0,0.18);

    margin-bottom: 10px;
}

/* Force the inner Plotly wrapper to respect the same rounded corners */
div[data-testid="stPlotlyChart"] > div {
    width: 100% !important;
    max-width: 100% !important;

    border-radius: 20px !important;
    overflow: hidden !important;
}

/* Plotly graph container */
div[data-testid="stPlotlyChart"] .js-plotly-plot,
div[data-testid="stPlotlyChart"] .plot-container,
div[data-testid="stPlotlyChart"] .svg-container {
    border-radius: 20px !important;
    overflow: hidden !important;
}
    /* =====================================================
       DATAFRAME CARD
    ===================================================== */

    div[data-testid="stDataFrame"] {
        background: #1b2433;
        border: 1px solid #334155;
        border-radius: 18px;
        overflow: hidden;

        box-shadow:
            0 8px 24px rgba(0,0,0,0.18);
    }


    /* =====================================================
       DIVIDERS
    ===================================================== */

    hr {
        border: none;
        border-top: 1px solid #2b3648;
        margin: 1.6rem 0;
    }


    /* =====================================================
       CAPTIONS
    ===================================================== */

    .stCaption {
        color: #94a3b8 !important;
    }


    /* =====================================================
       RESPONSIVE
    ===================================================== */

    @media (max-width: 1000px) {

        section[data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
        }

        section[data-testid="stSidebar"] > div {
            width: 280px !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/customer_support_clean.csv"
    )

    df["Date of Purchase"] = pd.to_datetime(
        df["Date of Purchase"],
        errors="coerce",
    )

    return df


df = load_data()


# =========================================================
# HEADER
# =========================================================

st.html(
    """
    <div class="dashboard-header">

        <div class="dashboard-title">
            Customer Support Performance Dashboard
        </div>

        <div class="dashboard-subtitle">
            Executive view of ticket activity, service channels,
            priority mix and customer satisfaction.
        </div>

    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("Filters")

st.sidebar.caption(
    "Refine the dashboard using the controls below."
)


status_options = sorted(
    df["Ticket Status"]
    .dropna()
    .unique()
)

selected_status = st.sidebar.multiselect(
    "Ticket Status",
    status_options,
    default=status_options,
)


priority_options = sorted(
    df["Ticket Priority"]
    .dropna()
    .unique()
)

selected_priority = st.sidebar.multiselect(
    "Ticket Priority",
    priority_options,
    default=priority_options,
)


channel_options = sorted(
    df["Ticket Channel"]
    .dropna()
    .unique()
)

selected_channel = st.sidebar.multiselect(
    "Ticket Channel",
    channel_options,
    default=channel_options,
)


type_options = sorted(
    df["Ticket Type"]
    .dropna()
    .unique()
)

selected_type = st.sidebar.multiselect(
    "Ticket Type",
    type_options,
    default=type_options,
)


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    df["Ticket Status"].isin(selected_status)
    & df["Ticket Priority"].isin(selected_priority)
    & df["Ticket Channel"].isin(selected_channel)
    & df["Ticket Type"].isin(selected_type)
].copy()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_tickets = len(filtered_df)

closed_tickets = (
    filtered_df["Ticket Status"]
    .eq("Closed")
    .sum()
)

open_tickets = (
    filtered_df["Ticket Status"]
    .eq("Open")
    .sum()
)

pending_tickets = (
    filtered_df["Ticket Status"]
    .eq("Pending Customer Response")
    .sum()
)

resolution_rate = (
    closed_tickets / total_tickets * 100
    if total_tickets > 0
    else 0
)

avg_csat = (
    filtered_df["Customer Satisfaction Rating"]
    .mean()
)


# =========================================================
# KPI SECTION
# =========================================================

st.markdown(
    '<div class="section-title">Executive Overview</div>',
    unsafe_allow_html=True,
)


k1, k2, k3, k4, k5 = st.columns(5)


k1.metric(
    "Total Tickets",
    f"{total_tickets:,}",
)

k2.metric(
    "Closed",
    f"{closed_tickets:,}",
)

k3.metric(
    "Open",
    f"{open_tickets:,}",
)

k4.metric(
    "Resolution Rate",
    f"{resolution_rate:.1f}%",
)

k5.metric(
    "Average CSAT",
    (
        f"{avg_csat:.2f}/5"
        if pd.notna(avg_csat)
        else "N/A"
    ),
)


st.divider()


# =========================================================
# CHART STYLE HELPER
# =========================================================

def style_chart(fig):

    fig.update_layout(
        template="plotly_dark",

        paper_bgcolor="#1b2433",
        plot_bgcolor="#1b2433",

        autosize=True,

        font=dict(
            family="Arial",
            color="#cbd5e1",
            size=12,
        ),

        title=dict(
            font=dict(
                size=17,
                color="#f8fafc",
            ),
            x=0.03,
            xanchor="left",
        ),

        margin=dict(
            l=30,
            r=8,
            t=55,
            b=35,
        ),

        showlegend=False,
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="#475569",
        tickfont=dict(
            color="#cbd5e1"
        ),
        title_font=dict(
            color="#94a3b8"
        ),
        automargin=True,
    )

    fig.update_yaxes(
        gridcolor="#334155",
        zeroline=False,
        linecolor="#475569",
        tickfont=dict(
            color="#cbd5e1"
        ),
        title_font=dict(
            color="#94a3b8"
        ),
        automargin=True,
    )

    return fig


# =========================================================
# TICKET OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">Ticket Overview</div>',
    unsafe_allow_html=True,
)


left, right = st.columns(
    2,
    gap="large",
)


# ---------------------------------------------------------
# STATUS
# ---------------------------------------------------------

with left:

    status_counts = (
        filtered_df["Ticket Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Ticket Status",
        "Ticket Count",
    ]

    fig = px.bar(
        status_counts,
        x="Ticket Status",
        y="Ticket Count",
        title="Ticket Status Distribution",
        text="Ticket Count",
        color_discrete_sequence=[
            "#4f8cff"
        ],
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ---------------------------------------------------------
# PRIORITY
# ---------------------------------------------------------

with right:

    priority_counts = (
        filtered_df["Ticket Priority"]
        .value_counts()
        .reset_index()
    )

    priority_counts.columns = [
        "Ticket Priority",
        "Ticket Count",
    ]

    fig = px.bar(
        priority_counts,
        x="Ticket Priority",
        y="Ticket Count",
        title="Tickets by Priority",
        text="Ticket Count",
        color_discrete_sequence=[
            "#f59e0b"
        ],
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =========================================================
# CHANNEL + TYPE
# =========================================================

left, right = st.columns(
    2,
    gap="large",
)


# ---------------------------------------------------------
# CHANNEL
# ---------------------------------------------------------

with left:

    channel_counts = (
        filtered_df["Ticket Channel"]
        .value_counts()
        .reset_index()
    )

    channel_counts.columns = [
        "Ticket Channel",
        "Ticket Count",
    ]

    fig = px.bar(
        channel_counts,
        x="Ticket Channel",
        y="Ticket Count",
        title="Tickets by Support Channel",
        text="Ticket Count",
        color_discrete_sequence=[
            "#14b8a6"
        ],
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ---------------------------------------------------------
# TYPE
# ---------------------------------------------------------

with right:

    type_counts = (
        filtered_df["Ticket Type"]
        .value_counts()
        .reset_index()
    )

    type_counts.columns = [
        "Ticket Type",
        "Ticket Count",
    ]

    fig = px.bar(
        type_counts,
        x="Ticket Type",
        y="Ticket Count",
        title="Tickets by Type",
        text="Ticket Count",
        color_discrete_sequence=[
            "#8b5cf6"
        ],
    )

    fig.update_xaxes(
        tickangle=-15
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


st.divider()


# =========================================================
# CUSTOMER SATISFACTION
# =========================================================

st.markdown(
    '<div class="section-title">Customer Satisfaction</div>',
    unsafe_allow_html=True,
)


left, right = st.columns(
    2,
    gap="large",
)


# ---------------------------------------------------------
# CSAT DISTRIBUTION
# ---------------------------------------------------------

with left:

    csat_distribution = (
        filtered_df[
            "Customer Satisfaction Rating"
        ]
        .dropna()
        .value_counts()
        .sort_index()
        .reset_index()
    )

    csat_distribution.columns = [
        "CSAT Rating",
        "Ticket Count",
    ]

    fig = px.bar(
        csat_distribution,
        x="CSAT Rating",
        y="Ticket Count",
        title="CSAT Distribution",
        text="Ticket Count",
        color_discrete_sequence=[
            "#22c55e"
        ],
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ---------------------------------------------------------
# CSAT BY CHANNEL
# ---------------------------------------------------------

with right:

    csat_by_channel = (
        filtered_df
        .groupby(
            "Ticket Channel"
        )[
            "Customer Satisfaction Rating"
        ]
        .mean()
        .dropna()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        csat_by_channel,
        x="Ticket Channel",
        y="Customer Satisfaction Rating",
        title="Average CSAT by Channel",
        text_auto=".2f",
        color_discrete_sequence=[
            "#06b6d4"
        ],
    )

    fig.update_layout(
        yaxis_range=[0, 5]
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# =========================================================
# CSAT BY PRIORITY + TYPE
# =========================================================

left, right = st.columns(
    2,
    gap="large",
)


# ---------------------------------------------------------
# CSAT BY PRIORITY
# ---------------------------------------------------------

with left:

    csat_by_priority = (
        filtered_df
        .groupby(
            "Ticket Priority"
        )[
            "Customer Satisfaction Rating"
        ]
        .mean()
        .dropna()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        csat_by_priority,
        x="Ticket Priority",
        y="Customer Satisfaction Rating",
        title="Average CSAT by Priority",
        text_auto=".2f",
        color_discrete_sequence=[
            "#f97316"
        ],
    )

    fig.update_layout(
        yaxis_range=[0, 5]
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


# ---------------------------------------------------------
# CSAT BY TYPE
# ---------------------------------------------------------

with right:

    csat_by_type = (
        filtered_df
        .groupby(
            "Ticket Type"
        )[
            "Customer Satisfaction Rating"
        ]
        .mean()
        .dropna()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    fig = px.bar(
        csat_by_type,
        x="Ticket Type",
        y="Customer Satisfaction Rating",
        title="Average CSAT by Ticket Type",
        text_auto=".2f",
        color_discrete_sequence=[
            "#ec4899"
        ],
    )

    fig.update_layout(
        yaxis_range=[0, 5]
    )

    fig.update_xaxes(
        tickangle=-15
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig = style_chart(fig)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True,
        },
    )


st.divider()


# =========================================================
# TABLE
# =========================================================

st.markdown(
    '<div class="section-title">Ticket Details</div>',
    unsafe_allow_html=True,
)

st.caption(
    f"{len(filtered_df):,} tickets match "
    "the selected filters."
)


display_columns = [
    "Ticket ID",
    "Product Purchased",
    "Ticket Type",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel",
    "Customer Satisfaction Rating",
]


st.dataframe(
    filtered_df[
        display_columns
    ],
    use_container_width=True,
    hide_index=True,
    height=420,
)