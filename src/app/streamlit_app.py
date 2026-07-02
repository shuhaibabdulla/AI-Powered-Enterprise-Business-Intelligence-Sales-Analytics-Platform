# ================================================
# RETAILX CORP — STREAMLIT DASHBOARD APP
# Run with: streamlit run src/app/streamlit_app.py
# ================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="RetailX Corp Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    base = 'outputs/exports/'
    fact        = pd.read_csv(base + 'fact_table.csv')
    customers   = pd.read_csv(base + 'customer_kpis.csv')
    categories  = pd.read_csv(base + 'category_kpis.csv')
    monthly     = pd.read_csv(base + 'monthly_revenue.csv')
    forecast    = pd.read_csv(base + 'sales_forecast.csv')
    seller_kpis = pd.read_csv(base + 'seller_kpis.csv')
    return fact, customers, categories, monthly, forecast, seller_kpis

fact, customers, categories, monthly, forecast, seller_kpis = load_data()

# ---- SIDEBAR ----
st.sidebar.image(
    "https://img.icons8.com/color/96/shop.png",
    width=80
)
st.sidebar.title("RetailX Corp")
st.sidebar.markdown("**AI-Powered BI Platform**")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Navigate",
    ["Executive Dashboard",
     "Sales Analysis",
     "Customer Analytics",
     "Product Performance",
     "Seller Performance",
     "Revenue Forecast"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("📅 Data: 2016 - 2018")
st.sidebar.markdown("📦 Orders: 99,441")
st.sidebar.markdown("🌍 Market: Brazil")

# ================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ================================================
if page == "Executive Dashboard":

    st.title("📊 RetailX Corp — Executive Dashboard")
    st.markdown("**Real-time business performance overview**")
    st.markdown("---")

    # KPI Cards Row 1
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = fact['total_revenue'].sum()
    total_orders  = fact['order_id'].nunique()
    aov           = fact.groupby('order_id')['total_revenue'].sum().mean()
    total_cust    = fact['customer_unique_id'].nunique()

    col1.metric("💰 Total Revenue",    f"R$ {total_revenue/1e6:.2f}M")
    col2.metric("📦 Total Orders",     f"{total_orders:,}")
    col3.metric("🛒 Avg Order Value",  f"R$ {aov:.2f}")
    col4.metric("👥 Total Customers",  f"{total_cust:,}")

    st.markdown("---")

    # KPI Cards Row 2
    col5, col6, col7, col8 = st.columns(4)

    delivered     = fact[fact['delivery_days'] > 0]
    avg_delivery  = delivered['delivery_days'].mean()
    late_rate     = fact['is_late_delivery'].mean() * 100
    repeat_rate   = (customers['total_orders'] > 1).mean() * 100
    avg_review    = pd.read_csv('data/processed/reviews_clean.csv')['review_score'].mean()

    col5.metric("🚚 Avg Delivery Days",    f"{avg_delivery:.1f} days")
    col6.metric("⏰ Late Delivery Rate",   f"{late_rate:.1f}%")
    col7.metric("🔁 Repeat Purchase Rate", f"{repeat_rate:.1f}%")
    col8.metric("⭐ Avg Review Score",     f"{avg_review:.2f}/5.00")

    st.markdown("---")

    # Monthly Revenue Chart
    st.subheader("📈 Monthly Revenue Trend")
    monthly_sorted = monthly.sort_values(['order_year', 'order_month'])
    monthly_sorted['period'] = (
        monthly_sorted['order_year'].astype(str) + '-' +
        monthly_sorted['order_month'].astype(str).str.zfill(2)
    )

    fig = px.line(
        monthly_sorted,
        x='period',
        y='total_revenue',
        title='Monthly Revenue (2016-2018)',
        labels={'period': 'Month', 'total_revenue': 'Revenue (R$)'},
        color_discrete_sequence=['#2563EB']
    )
    fig.update_traces(line_width=2.5)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ================================================
# PAGE 2: SALES ANALYSIS
# ================================================
elif page == "Sales Analysis":

    st.title("📈 Sales Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)

    # Revenue by State
    with col1:
        st.subheader("Revenue by State")
        state_rev = (
            fact.groupby('customer_state')['total_revenue']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig = px.bar(
            state_rev,
            x='total_revenue',
            y='customer_state',
            orientation='h',
            color='total_revenue',
            color_continuous_scale='Blues',
            labels={'total_revenue': 'Revenue (R$)', 'customer_state': 'State'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Revenue by Category
    with col2:
        st.subheader("Top Categories by Revenue")
        cat_rev = categories.head(10)
        fig = px.bar(
            cat_rev,
            x='total_revenue',
            y='product_category_name_english',
            orientation='h',
            color='total_revenue',
            color_continuous_scale='Blues',
            labels={
                'total_revenue': 'Revenue (R$)',
                'product_category_name_english': 'Category'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ================================================
# PAGE 3: CUSTOMER ANALYTICS
# ================================================
elif page == "Customer Analytics":

    st.title("👥 Customer Analytics")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers",     f"{len(customers):,}")
    col2.metric("Avg CLV",             f"R$ {customers['total_spent'].mean():,.2f}")
    col3.metric("Repeat Buyers",       f"{(customers['total_orders']>1).sum():,}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Segments by Spend")
        customers['segment'] = pd.cut(
            customers['total_spent'],
            bins=[0, 100, 300, 600, 1000, float('inf')],
            labels=['Bronze','Silver','Gold','Platinum','Diamond']
        )
        seg = customers['segment'].value_counts().reset_index()
        seg.columns = ['segment', 'count']
        fig = px.bar(
            seg,
            x='count',
            y='segment',
            orientation='h',
            color='segment',
            color_discrete_map={
                'Bronze':  '#cd7f32',
                'Silver':  '#a8a9ad',
                'Gold':    '#ffd700',
                'Platinum':'#8b9eb7',
                'Diamond': '#2563EB'
            }
        )
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Orders per Customer")
        order_dist = (
            customers['total_orders']
            .value_counts()
            .sort_index()
            .head(8)
            .reset_index()
        )
        order_dist.columns = ['orders', 'customers']
        fig = px.bar(
            order_dist,
            x='orders',
            y='customers',
            color_discrete_sequence=['#2563EB'],
            labels={'orders': 'Number of Orders', 'customers': 'Customers'}
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ================================================
# PAGE 4: PRODUCT PERFORMANCE
# ================================================
elif page == "Product Performance":

    st.title("📦 Product Performance")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Categories")
        fig = px.bar(
            categories.head(10),
            x='total_revenue',
            y='product_category_name_english',
            orientation='h',
            color_discrete_sequence=['#2563EB'],
            labels={
                'total_revenue': 'Revenue (R$)',
                'product_category_name_english': 'Category'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Bottom 10 Categories")
        fig = px.bar(
            categories.tail(10),
            x='total_revenue',
            y='product_category_name_english',
            orientation='h',
            color_discrete_sequence=['#ef4444'],
            labels={
                'total_revenue': 'Revenue (R$)',
                'product_category_name_english': 'Category'
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ================================================
# PAGE 5: SELLER PERFORMANCE
# ================================================
elif page == "Seller Performance":

    st.title("🏪 Seller Performance")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sellers",      f"{len(seller_kpis):,}")
    col2.metric("Avg Revenue/Seller", f"R$ {seller_kpis['total_revenue'].mean():,.2f}")
    col3.metric("Avg Late Rate",      f"{seller_kpis['late_rate'].mean():.1f}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Sellers by Revenue")
        top_sellers = seller_kpis.nlargest(10, 'total_revenue').copy()
        top_sellers['label'] = top_sellers['seller_id'].str[:10] + '...'
        fig = px.bar(
            top_sellers,
            x='total_revenue',
            y='label',
            orientation='h',
            color_discrete_sequence=['#2563EB'],
            labels={'total_revenue': 'Revenue (R$)', 'label': 'Seller'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Worst Sellers by Late Delivery")
        worst = (
            seller_kpis[seller_kpis['total_deliveries'] >= 10]
            .nlargest(10, 'late_rate')
            .copy()
        )
        worst['label'] = worst['seller_id'].str[:10] + '...'
        fig = px.bar(
            worst,
            x='late_rate',
            y='label',
            orientation='h',
            color_discrete_sequence=['#ef4444'],
            labels={'late_rate': 'Late Rate (%)', 'label': 'Seller'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ================================================
# PAGE 6: REVENUE FORECAST
# ================================================
elif page == "Revenue Forecast":

    st.title("🔮 Revenue Forecast")
    st.markdown("---")

    st.subheader("3-Month Revenue Forecast")

    # Historical
    monthly_sorted = monthly.sort_values(['order_year', 'order_month'])
    monthly_sorted['period'] = (
        monthly_sorted['order_year'].astype(str) + '-' +
        monthly_sorted['order_month'].astype(str).str.zfill(2)
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly_sorted['period'],
        y=monthly_sorted['total_revenue'],
        mode='lines+markers',
        name='Historical Revenue',
        line=dict(color='#2563EB', width=2.5)
    ))

    fig.add_trace(go.Scatter(
        x=forecast['month'],
        y=forecast['predicted_revenue'],
        mode='lines+markers',
        name='Forecasted Revenue',
        line=dict(color='#f97316', width=2.5, dash='dash'),
        marker=dict(symbol='diamond', size=10)
    ))

    fig.update_layout(
        height=450,
        xaxis_title='Month',
        yaxis_title='Revenue (R$)',
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Forecast Numbers")
    st.dataframe(
        forecast.rename(columns={
            'month': 'Month',
            'predicted_revenue': 'Predicted Revenue (R$)'
        }).style.format({'Predicted Revenue (R$)': 'R$ {:,.2f}'}),
        use_container_width=True
    )