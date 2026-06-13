import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Supply Chain Analytics Dashboard")

data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Delayed Shipments": [12, 18, 9, 15, 10, 7]
}

df = pd.DataFrame(data)

st.subheader("Shipment Delay Trend")

st.dataframe(df)

fig, ax = plt.subplots()

ax.plot(df["Month"], df["Delayed Shipments"])

st.pyplot(fig)