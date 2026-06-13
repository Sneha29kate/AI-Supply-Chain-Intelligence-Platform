import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from database.save_shipment import save_shipment
from database.fetch_shipments import get_shipments
from forecasting.demand_forecasting import forecast_demand
from weather.weather_api import get_weather
from database.save_weather import save_weather
st.set_page_config(
    page_title="AI Supply Chain Intelligence Platform",
    layout="wide"
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Shipment Delay Prediction",
        "Analytics",
        "Demand Forecasting",
        "Weather Delay Risk",
        "RAG Chatbot"
    ]
)

# ==================================================
# SHIPMENT DELAY PREDICTION
# ==================================================

if page == "Shipment Delay Prediction":

    st.title("📦 Shipment Delay Prediction System")

    model = joblib.load(
        "models/shipment_delay_model.pkl"
    )

    distance = st.number_input(
        "Distance",
        min_value=0.0
    )

    shipping_mode = st.number_input(
        "Shipping Mode (encoded)",
        min_value=0
    )

    warehouse = st.number_input(
        "Warehouse (encoded)",
        min_value=0
    )

    priority = st.number_input(
        "Order Priority (encoded)",
        min_value=0
    )

    feature5 = st.number_input(
        "Feature 5",
        min_value=0.0
    )

    feature6 = st.number_input(
        "Feature 6",
        min_value=0.0
    )

    if st.button("Predict"):

        input_data = np.array([[
            distance,
            shipping_mode,
            warehouse,
            priority,
            feature5,
            feature6
        ]])

        prediction = model.predict(
            input_data
        )[0]

        if prediction == 0:

            st.success(
                "🚚 Shipment will be ON TIME"
            )

            delayed_value = 0

        else:

            st.error(
                "⚠️ Shipment will be DELAYED"
            )

            delayed_value = 1

        save_shipment(
            distance=distance,
            warehouse=str(warehouse),
            shipping_mode=str(shipping_mode),
            priority=str(priority),
            delayed=delayed_value
        )

        st.success(
            "✅ Record saved to PostgreSQL"
        )

        if hasattr(model, "predict_proba"):

            prob = model.predict_proba(
                input_data
            )[0]

            st.write(
                "### Prediction Confidence"
            )

            st.write(
                f"On Time: {prob[0]:.2f}"
            )

            st.write(
                f"Delay: {prob[1]:.2f}"
            )

# ==================================================
# ANALYTICS DASHBOARD
# ==================================================

elif page == "Analytics":

    st.title(
        "📊 Supply Chain Analytics Dashboard"
    )

    df = get_shipments()

    st.subheader(
        "Shipment Records"
    )

    st.dataframe(df)

    total_shipments = len(df)

    delayed_shipments = (
        df["delayed"].sum()
    )

    on_time_shipments = (
        total_shipments -
        delayed_shipments
    )

    delay_rate = (
        delayed_shipments /
        total_shipments * 100
    ) if total_shipments > 0 else 0

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Shipments",
        total_shipments
    )

    c2.metric(
        "Delayed Shipments",
        delayed_shipments
    )

    c3.metric(
        "Delay %",
        round(delay_rate, 2)
    )

    st.subheader(
        "Shipment Status Distribution"
    )

    fig1, ax1 = plt.subplots()

    ax1.pie(
        [
            on_time_shipments,
            delayed_shipments
        ],
        labels=[
            "On Time",
            "Delayed"
        ],
        autopct="%1.1f%%"
    )

    st.pyplot(fig1)

    st.subheader(
        "Warehouse Distribution"
    )

    warehouse_counts = (
        df["warehouse"]
        .value_counts()
    )

    fig2, ax2 = plt.subplots()

    warehouse_counts.plot(
        kind="bar",
        ax=ax2
    )

    st.pyplot(fig2)

# ==================================================
# DEMAND FORECASTING
# ==================================================

elif page == "Demand Forecasting":

    st.title(
        "📈 Demand Forecasting"
    )

    months, predictions = (
        forecast_demand()
    )

    forecast_df = pd.DataFrame({
        "Future Month": months,
        "Predicted Demand": predictions
    })

    st.subheader(
        "Forecasted Demand"
    )

    st.dataframe(
        forecast_df
    )

    fig3, ax3 = plt.subplots()

    ax3.plot(
        months,
        predictions,
        marker="o"
    )

    ax3.set_title(
        "Demand Forecast"
    )

    ax3.set_xlabel(
        "Month"
    )

    ax3.set_ylabel(
        "Predicted Demand"
    )

    st.pyplot(fig3)

# ==================================================
# ==================================================
# WEATHER DELAY RISK
# ==================================================

elif page == "Weather Delay Risk":

    st.title(
        "🌦 Weather Delay Risk"
    )

    city = st.text_input(
        "Enter City Name",
        "Mumbai"
    )

    if st.button(
        "Check Weather Risk"
    ):

        data = get_weather(
            city
        )

        if data.get("cod") == 200:

            temp = (
                data["main"]["temp"]
            )

            humidity = (
                data["main"]["humidity"]
            )

            weather_desc = (
                data["weather"][0]["description"]
            )

            st.subheader(
                "Current Weather"
            )

            st.write(
                f"Temperature: {temp} °C"
            )

            st.write(
                f"Humidity: {humidity}%"
            )

            st.write(
                f"Condition: {weather_desc}"
            )

            if humidity > 80:

                risk = (
                    "🔴 HIGH RISK"
                )

            elif humidity > 60:

                risk = (
                    "🟡 MEDIUM RISK"
                )

            else:

                risk = (
                    "🟢 LOW RISK"
                )

            st.subheader(
                "Shipment Delay Risk"
            )

            st.success(
                risk
            )

            save_weather(
                city,
                temp,
                humidity,
                weather_desc,
                risk
            )

            st.success(
                "✅ Weather record saved"
            )

        else:

            st.error(
                "City not found"
            )
# ==================================================
# RAG CHATBOT
# ==================================================

elif page == "RAG Chatbot":

    from rag.rag_engine import (
        load_knowledge,
        get_answer
    )

    from rag.gemini_rag import (
        ask_gemini
    )

    st.title(
        "🧠 Supply Chain AI Assistant"
    )

    docs = load_knowledge(
        "rag/knowledge_base.txt"
    )

    query = st.text_input(
        "Ask a supply chain question:"
    )

    if query:

        context = get_answer(
            query,
            docs
        )

        response = ask_gemini(
            query,
            context
        )

        st.success(
            response
        )