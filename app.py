import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="Amazon GTL Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

AMAZON_ORANGE = "#FF9900"
AMAZON_DARK = "#232F3E"
AMAZON_BLUE = "#146EB4"
AMAZON_LIGHT = "#FEBD69"
GREEN = "#067D62"
RED = "#CC0C39"

st.markdown("""
<style>
    .main { background-color: #F8F8F8; }
    .block-container { padding: 1.5rem 2rem; }
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 16px 20px;
        border-left: 4px solid #FF9900;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        min-height: 90px;
    }
    .metric-label {
        font-size: 11px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #232F3E;
        line-height: 1.2;
    }
    .metric-delta-neg { font-size: 11px; color: #CC0C39; margin-top: 3px; }
    .metric-delta-pos { font-size: 11px; color: #067D62; margin-top: 3px; }
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        background-color: #232F3E;
        padding: 10px 16px;
        border-radius: 6px;
        margin: 1.5rem 0 1rem;
        border-left: 5px solid #FF9900;
    }
    .savings-card {
        background: white;
        border-radius: 8px;
        padding: 16px 20px;
        border-top: 4px solid #FF9900;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        height: 100%;
    }
    .savings-title { font-size: 14px; font-weight: 700; color: #232F3E; margin-bottom: 6px; }
    .savings-amount { font-size: 22px; font-weight: 700; color: #067D62; margin-bottom: 8px; }
    .savings-desc { font-size: 12px; color: #666; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('deliveries.csv')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['promised_delivery'] = pd.to_datetime(df['promised_delivery'])
    df['actual_delivery'] = pd.to_datetime(df['actual_delivery'])
    df['is_late'] = (df['status'] == 'Late').astype(int)
    df['cost_per_km'] = df['shipping_cost_eur'] / df['distance_km'].replace(0, 1)
    df['is_weekend'] = df['order_date'].dt.dayofweek >= 5
    return df

df = load_data()

st.sidebar.markdown("""
<div style='text-align:center; padding: 10px 0 20px;'>
    <span style='font-size:28px;'>📦</span>
    <div style='color:white; font-size:16px; font-weight:700; margin-top:6px;'>Amazon GTL</div>
    <div style='color:#FF9900; font-size:12px;'>Germany Operations</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div style='color:#FF9900; font-size:12px; font-weight:700; letter-spacing:0.1em; margin-bottom:8px;'>FILTERS</div>", unsafe_allow_html=True)

selected_warehouse = st.sidebar.multiselect("Warehouse", options=df['warehouse'].unique(), default=df['warehouse'].unique())
selected_carrier = st.sidebar.multiselect("Carrier", options=df['carrier'].unique(), default=df['carrier'].unique())
selected_month = st.sidebar.multiselect("Month", options=['January','February','March','April','May','June'], default=['January','February','March','April','May','June'])

filtered = df[df['warehouse'].isin(selected_warehouse) & df['carrier'].isin(selected_carrier) & df['month'].isin(selected_month)]

st.markdown("""
<div style='background:#232F3E; padding:16px 24px; border-radius:8px; margin-bottom:1.5rem;'>
    <div style='display:flex; align-items:center; gap:12px;'>
        <span style='font-size:32px;'>📦</span>
        <div>
            <div style='color:white; font-size:22px; font-weight:700;'>Amazon Global Transportation & Logistics</div>
            <div style='color:#FF9900; font-size:13px; margin-top:2px;'>Operations KPI Dashboard &nbsp;|&nbsp; Germany Delivery Network &nbsp;|&nbsp; Jan-Jun 2024</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

total_orders = len(filtered)
on_time_rate = (filtered['status'] == 'On-Time').mean() * 100
late_orders = (filtered['status'] == 'Late').sum()
avg_cost = filtered['shipping_cost_eur'].mean()
total_cost = filtered['shipping_cost_eur'].sum()
avg_delay = filtered[filtered['status'] == 'Late']['delay_days'].mean() if late_orders > 0 else 0
gap = on_time_rate - 88.0

# format total cost as K
total_cost_display = f"€{total_cost/1000:.1f}K"

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Orders</div><div class='metric-value'>{total_orders:,}</div></div>""", unsafe_allow_html=True)
with c2:
    delta_class = 'metric-delta-pos' if gap >= 0 else 'metric-delta-neg'
    delta_sign = '+' if gap >= 0 else ''
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>On-Time Rate</div><div class='metric-value'>{on_time_rate:.1f}%</div><div class='{delta_class}'>{delta_sign}{gap:.1f}% vs target</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Late Orders</div><div class='metric-value'>{late_orders:,}</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Avg Ship Cost</div><div class='metric-value'>€{avg_cost:.2f}</div></div>""", unsafe_allow_html=True)
with c5:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Cost</div><div class='metric-value'>{total_cost_display}</div></div>""", unsafe_allow_html=True)
with c6:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Avg Delay</div><div class='metric-value'>{avg_delay:.1f} days</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

AXIS_STYLE = dict(
    title_font=dict(size=13, color='#232F3E', family='Arial'),
    tickfont=dict(size=12, color='#232F3E', family='Arial'),
    gridcolor='#e0e0e0',
    linecolor='#232F3E',
    linewidth=1
)

st.markdown("<div class='section-title'>📊 Carrier Performance</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    carrier_kpi = filtered.groupby('carrier').agg(total=('status','count'), on_time=('status', lambda x: (x=='On-Time').sum())).reset_index()
    carrier_kpi['rate'] = (carrier_kpi['on_time'] / carrier_kpi['total'] * 100).round(1)
    carrier_kpi = carrier_kpi.sort_values('rate', ascending=True)
    colors = [GREEN if r >= 88 else RED for r in carrier_kpi['rate']]
    fig = go.Figure(go.Bar(x=carrier_kpi['rate'], y=carrier_kpi['carrier'], orientation='h', marker_color=colors, text=[f"{r:.1f}%" for r in carrier_kpi['rate']], textposition='outside', textfont=dict(size=13, color='#232F3E')))
    fig.add_vline(x=88, line_dash="dash", line_color=AMAZON_ORANGE, line_width=2, annotation_text="SLA 88%", annotation_font=dict(color=AMAZON_ORANGE, size=12))
    fig.update_layout(title=dict(text="On-Time Rate by Carrier", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="On-Time Rate (%)", range=[70,105], ticksuffix='%'), yaxis=dict(**AXIS_STYLE, title="Carrier"), margin=dict(l=20,r=50,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    late_df = filtered[filtered['status'] == 'Late']
    rca = late_df['delay_reason'].value_counts().reset_index()
    rca.columns = ['Reason', 'Count']
    fig = go.Figure(go.Pie(
        labels=rca['Reason'],
        values=rca['Count'],
        hole=0.4,
        marker=dict(colors=[AMAZON_ORANGE, AMAZON_BLUE, RED, GREEN, '#8B5CF6', '#64748B']),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=12, color='#232F3E'),
        automargin=True
    ))
    fig.update_layout(
        title=dict(text="Delay Root Cause Analysis", font=dict(size=15, color='#232F3E')),
        height=380,
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='section-title'>📈 Trends & Cost Analysis</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    weekly = filtered.groupby('week').agg(total=('status','count'), on_time=('status', lambda x: (x=='On-Time').sum())).reset_index()
    weekly['rate'] = (weekly['on_time'] / weekly['total'] * 100).round(1)
    fig = go.Figure()
    fig.add_hrect(y0=88, y1=102, fillcolor=GREEN, opacity=0.05, line_width=0)
    fig.add_hrect(y0=70, y1=88, fillcolor=RED, opacity=0.05, line_width=0)
    fig.add_trace(go.Scatter(x=weekly['week'], y=weekly['rate'], mode='lines+markers', line=dict(color=AMAZON_ORANGE, width=2.5), marker=dict(size=6, color=AMAZON_ORANGE), fill='tozeroy', fillcolor='rgba(255,153,0,0.08)'))
    fig.add_hline(y=88, line_dash="dash", line_color=AMAZON_DARK, line_width=1.5, annotation_text="SLA Target 88%", annotation_font=dict(color='#232F3E', size=12))
    fig.update_layout(title=dict(text="Weekly On-Time Rate Trend", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="Week Number"), yaxis=dict(**AXIS_STYLE, title="On-Time Rate (%)", range=[70,102], ticksuffix='%'), showlegend=False, margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    cost_carrier = filtered.groupby('carrier').agg(avg_cost=('shipping_cost_eur','mean')).round(2).reset_index()
    cost_carrier = cost_carrier.sort_values('avg_cost', ascending=False)
    fig = go.Figure(go.Bar(x=cost_carrier['carrier'], y=cost_carrier['avg_cost'], marker_color=[AMAZON_ORANGE if i==0 else AMAZON_BLUE for i in range(len(cost_carrier))], text=[f"€{c:.2f}" for c in cost_carrier['avg_cost']], textposition='outside', textfont=dict(size=13, color='#232F3E')))
    fig.update_layout(title=dict(text="Average Shipping Cost by Carrier", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="Carrier"), yaxis=dict(**AXIS_STYLE, title="Average Cost (€)", tickprefix='€'), margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    month_order = ['January','February','March','April','May','June']
    monthly = filtered[filtered['month'].isin(month_order)].groupby('month').agg(orders=('order_id','count'), total_cost=('shipping_cost_eur','sum')).reindex(month_order).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly['month'], y=monthly['total_cost'], name='Total Cost (€)', marker_color=AMAZON_ORANGE, text=[f"€{v:,.0f}" for v in monthly['total_cost']], textposition='outside', textfont=dict(size=11, color='#232F3E')))
    fig.add_trace(go.Scatter(x=monthly['month'], y=monthly['orders'], name='Total Orders', mode='lines+markers', line=dict(color=AMAZON_DARK, width=2), marker=dict(size=7, color=AMAZON_DARK), yaxis='y2'))
    fig.update_layout(title=dict(text="Monthly Cost & Volume", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="Month"), yaxis=dict(**AXIS_STYLE, title="Total Cost (€)", tickprefix='€'), yaxis2=dict(title="Total Orders", overlaying='y', side='right', title_font=dict(size=13, color='#232F3E'), tickfont=dict(size=12, color='#232F3E')), legend=dict(orientation='h', y=1.1, x=0, font=dict(size=11, color='#232F3E')), margin=dict(l=20,r=50,t=60,b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    weekend_kpi = filtered.groupby('is_weekend')['is_late'].agg(['sum','count']).reset_index()
    weekend_kpi.columns = ['is_weekend','late_orders','total_orders']
    weekend_kpi['late_rate'] = (weekend_kpi['late_orders'] / weekend_kpi['total_orders'] * 100).round(1)
    weekend_kpi['label'] = ['Weekday','Weekend']
    fig = go.Figure(go.Bar(x=weekend_kpi['label'], y=weekend_kpi['late_rate'], marker_color=[AMAZON_BLUE, RED], text=[f"{r:.1f}%" for r in weekend_kpi['late_rate']], textposition='outside', textfont=dict(size=14, color='#232F3E'), width=0.4))
    fig.add_hline(y=12, line_dash="dash", line_color=AMAZON_ORANGE, line_width=2, annotation_text="Avg 12%", annotation_font=dict(color=AMAZON_ORANGE, size=12))
    fig.update_layout(title=dict(text="Weekend vs Weekday Delay Rate", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="Day Type"), yaxis=dict(**AXIS_STYLE, title="Late Rate (%)", range=[0,25], ticksuffix='%'), margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='section-title'>🏭 Warehouse & Monthly Delay Performance</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    warehouse_kpi = filtered.groupby('warehouse').agg(total=('status','count'), on_time=('status', lambda x: (x=='On-Time').sum())).reset_index()
    warehouse_kpi['rate'] = (warehouse_kpi['on_time'] / warehouse_kpi['total'] * 100).round(1)
    warehouse_kpi = warehouse_kpi.sort_values('rate', ascending=True)
    colors = [GREEN if r >= 88 else RED for r in warehouse_kpi['rate']]
    fig = go.Figure(go.Bar(x=warehouse_kpi['rate'], y=warehouse_kpi['warehouse'], orientation='h', marker_color=colors, text=[f"{r:.1f}%" for r in warehouse_kpi['rate']], textposition='outside', textfont=dict(size=13, color='#232F3E')))
    fig.add_vline(x=88, line_dash="dash", line_color=AMAZON_ORANGE, line_width=2, annotation_text="SLA 88%", annotation_font=dict(color=AMAZON_ORANGE, size=12))
    fig.update_layout(title=dict(text="On-Time Rate by Warehouse", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="On-Time Rate (%)", range=[70,105], ticksuffix='%'), yaxis=dict(**AXIS_STYLE, title="Warehouse"), margin=dict(l=20,r=50,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    month_order = ['January','February','March','April','May','June']
    monthly_delay = filtered[filtered['month'].isin(month_order)].groupby('month').agg(total=('status','count'), late=('is_late','sum')).reindex(month_order).reset_index()
    monthly_delay['late_rate'] = (monthly_delay['late'] / monthly_delay['total'] * 100).round(1)
    colors = [GREEN if r < 12 else RED for r in monthly_delay['late_rate']]
    fig = go.Figure(go.Bar(x=monthly_delay['month'], y=monthly_delay['late_rate'], marker_color=colors, text=[f"{r:.1f}%" for r in monthly_delay['late_rate']], textposition='outside', textfont=dict(size=13, color='#232F3E')))
    fig.add_hline(y=12, line_dash="dash", line_color=AMAZON_ORANGE, line_width=2, annotation_text="Avg 12%", annotation_font=dict(color=AMAZON_ORANGE, size=12))
    fig.update_layout(title=dict(text="Monthly Delay Rate", font=dict(size=15, color='#232F3E')), height=380, plot_bgcolor='white', paper_bgcolor='white', xaxis=dict(**AXIS_STYLE, title="Month"), yaxis=dict(**AXIS_STYLE, title="Late Rate (%)", range=[0,20], ticksuffix='%'), margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='section-title'>💡 Cost Savings Opportunities</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

saving_1 = (38.24 - 37.29) * len(filtered[filtered['carrier'] == 'UPS'])
wrong_routing = len(filtered[filtered['delay_reason'] == 'Wrong Routing'])
saving_2 = wrong_routing * 37.00 * 0.30
long_routes = filtered[filtered['distance_km'] > 400]
saving_3 = long_routes['shipping_cost_eur'].sum() * 0.12
total_saving = saving_1 + saving_2 + saving_3

with col1:
    st.markdown(f"""<div class='savings-card'><div class='savings-title'>🔄 Switch UPS to DHL</div><div class='savings-amount'>€{saving_1:,.0f} / 6 months</div><div class='savings-desc'>UPS costs €38.24/order vs DHL €37.29. Reassigning {len(filtered[filtered['carrier']=='UPS'])} UPS orders to DHL reduces cost by €0.95 per order.</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='savings-card'><div class='savings-title'>🗺️ Fix Wrong Routing</div><div class='savings-amount'>€{saving_2:,.0f} / 6 months</div><div class='savings-desc'>{wrong_routing} orders delayed due to wrong routing. Automated validation eliminates 30% wasted cost per incident.</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class='savings-card'><div class='savings-title'>📍 Reassign Long Routes</div><div class='savings-amount'>€{saving_3:,.0f} / 6 months</div><div class='savings-desc'>{len(long_routes)} orders over 400km fulfilled from wrong warehouse. Nearest warehouse routing saves 12% per order.</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='background:#232F3E; padding:14px 20px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;'>
    <div style='color:#FF9900; font-size:14px; font-weight:700;'>Total Potential Savings (6 months)</div>
    <div style='color:white; font-size:24px; font-weight:700;'>€{total_saving:,.0f}</div>
    <div style='color:#FEBD69; font-size:13px;'>Annualised: €{total_saving*2:,.0f} / year</div>
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📋 Order Details</div>", unsafe_allow_html=True)
show_late = st.checkbox("Show late orders only", value=False)
display_df = filtered[filtered['status'] == 'Late'] if show_late else filtered
display_df = display_df[['order_id','order_date','warehouse','customer_city','carrier','distance_km','shipping_cost_eur','sla_days','status','delay_days','delay_reason']].copy()
display_df['order_date'] = display_df['order_date'].dt.strftime('%Y-%m-%d')
st.dataframe(display_df.sort_values('order_date', ascending=False).head(100), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Deliveries')
        summary = df.groupby('carrier').agg(Total_Orders=('order_id','count'), On_Time=('status', lambda x: (x=='On-Time').sum()), Avg_Cost=('shipping_cost_eur','mean')).reset_index()
        summary['On_Time_Rate'] = (summary['On_Time']/summary['Total_Orders']*100).round(1)
        summary.to_excel(writer, index=False, sheet_name='Carrier Summary')
    return output.getvalue()

st.download_button(label="📥 Export Full Report to Excel", data=to_excel(filtered), file_name="amazon_gtl_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
st.markdown("<br><div style='text-align:center; color:#999; font-size:12px;'>Built by Ayham Bokli | MSc Information & Operations Management | Supply Chain & Logistics Analytics</div>", unsafe_allow_html=True)
