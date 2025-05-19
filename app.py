import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned data
df = pd.read_csv("Cleaned_Renewable_Energy.csv")

# Rename for clarity
df.rename(columns={"Hydropower_(excl._Pumped.Storage)": "Hydropower"}, inplace=True)

# Configure Streamlit page
st.set_page_config(page_title="Pakistan Renewable Energy Dashboard", layout="wide")
st.title("🔋 Pakistan Renewable Energy Dashboard")
st.markdown("Visual insights into the country's renewable energy trends.")

# Sidebar filters
st.sidebar.header("🔧 Filters")
energy_sources = [col for col in df.columns if col != "Year"]
selected_energy = st.sidebar.selectbox("Select Energy Source", energy_sources)
show_moving_avg = st.sidebar.checkbox("Show 3-Year Moving Average")

# --------- Visualization 1: Line Chart ---------
st.subheader(f"📈 {selected_energy} Production Over Time")
fig1 = px.line(df, x="Year", y=selected_energy, markers=True)
st.plotly_chart(fig1, use_container_width=True)

# --------- Visualization 2: Moving Average (optional) ---------
if show_moving_avg:
    df_ma = df.copy()
    df_ma[f"{selected_energy}_MA"] = df_ma[selected_energy].rolling(window=3).mean()
    st.subheader(f"📉 3-Year Moving Average of {selected_energy}")
    fig2 = px.line(df_ma, x="Year", y=f"{selected_energy}_MA", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

# --------- Visualization 3: All Energy Sources Comparison ---------
st.subheader("🌐 Comparison of All Renewable Energy Sources")
fig3 = px.line(df, x="Year", y=energy_sources, title="Trends of Renewable Sources", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# --------- Visualization 4: Latest Year Production Bar Chart ---------
latest_year = df["Year"].max()
latest_data = df[df["Year"] == latest_year].set_index("Year").T
latest_data.reset_index(inplace=True)
latest_data.columns = ["Energy Type", "Production"]

st.subheader(f"📊 Production in {latest_year}")
fig4 = px.bar(latest_data, x="Energy Type", y="Production", color="Energy Type")
st.plotly_chart(fig4, use_container_width=True)

# --------- Visualization 5: Share of Each Source Over Time (Area Chart) ---------
df_total = df.copy()
df_total["Total"] = df_total[energy_sources].sum(axis=1)
df_share = df_total.copy()
for col in energy_sources:
    df_share[col] = df_share[col] / df_share["Total"] * 100

st.subheader("🧩 Share of Each Energy Source Over Time (%)")
fig5 = px.area(df_share, x="Year", y=energy_sources,
               title="Relative Contribution of Each Renewable Source",
               groupnorm='percent', stackgroup='one')
st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Developed by **Hamza Javed** | [LinkedIn](https://linkedin.com/)")
