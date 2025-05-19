import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Pakistan Renewable Energy Dashboard", layout="wide")

st.title("🇵🇰 Pakistan Renewable Energy Dashboard")
st.markdown("Analyze trends in electricity generation from various energy sources in Pakistan (2000–2022).")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Cleaned_Renewable_Energy.csv")
    return df

df = load_data()

# Sidebar Year Filter
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (2010, 2022))
df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

# Energy Types
energy_types = ['Fossil fuels', 'Hydropower', 'Solar energy', 'Wind energy', 'Bioenergy']

# --- Chart 1: Normalized Line Chart (for equal scale) ---
st.subheader("📈 Normalized Trends Over Time")
df_trend = df.groupby("Year")[energy_types].sum().reset_index()
df_normalized = df_trend.copy()
df_normalized[energy_types] = df_normalized[energy_types].div(df_normalized[energy_types].max()) * 100

fig1 = px.line(
    df_normalized,
    x="Year",
    y=energy_types,
    title="Normalized Generation by Energy Type (100 = max)",
    labels={'value': 'Normalized %', 'variable': 'Energy Type'},
    markers=True
)
fig1.update_layout(template="plotly_white")
st.plotly_chart(fig1, use_container_width=True)

# --- Chart 2: Pie Chart for a Single Year ---
st.subheader("🥧 Energy Share in a Year")
selected_year = st.selectbox("Select Year", sorted(df['Year'].unique(), reverse=True))
df_year = df[df["Year"] == selected_year]
df_pie = df_year[energy_types].sum().reset_index()
df_pie.columns = ['Energy Type', 'Generation']

fig2 = px.pie(
    df_pie,
    names='Energy Type',
    values='Generation',
    title=f"Electricity Generation Share - {selected_year}"
)
fig2.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig2, use_container_width=True)

# --- Chart 3: Stacked Area Chart ---
st.subheader("📊 Stacked Area Chart Over Time")
fig3 = px.area(
    df_trend,
    x='Year',
    y=energy_types,
    title='Electricity Generation by Energy Type (2000–2022)',
    labels={'value': 'Generation (GWh)', 'variable': 'Energy Type'}
)
fig3.update_layout(template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# --- Chart 4: Bar Chart for Selected Year ---
st.subheader("📊 Bar Chart of Generation in Selected Year")
df_bar = df[df["Year"] == selected_year]
total_by_tech = df_bar[energy_types].sum().sort_values(ascending=False)

fig4 = px.bar(
    x=total_by_tech.index,
    y=total_by_tech.values,
    labels={'x': 'Energy Type', 'y': 'Generation (GWh)'},
    title=f"Electricity Generation by Type - {selected_year}"
)
fig4.update_layout(template="plotly_white")
st.plotly_chart(fig4, use_container_width=True)

st.subheader("🧩 Share of Each Energy Source Over Time (%)")
fig5 = px.area( x="Year", y=energy_types,
               title="Relative Contribution of Each Renewable Source",
               groupnorm='percent', stackgroup='one')
st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Developed by **Hamza Javed** | [LinkedIn](https://linkedin.com/)")
