import streamlit as st
import requests
import pandas as pd
# Crop suitability reference data
crop_data = {
    "Green Gram": {
        "min_temp": 25,
        "max_temp": 35,
        "min_rain": 600,
        "max_rain": 750,
        "soils": ["Sandy", "Loamy"],
        "water": "Low"
    },

    "Chickpea": {
        "min_temp": 20,
        "max_temp": 30,
        "min_rain": 300,
        "max_rain": 600,
        "soils": ["Sandy", "Loamy", "Clay"],
        "water": "Low"
    },

    "Groundnut": {
        "min_temp": 22,
        "max_temp": 30,
        "min_rain": 500,
        "max_rain": 1000,
        "soils": ["Sandy", "Loamy"],
        "water": "Moderate"
    },

    "Soybean": {
        "min_temp": 20,
        "max_temp": 30,
        "min_rain": 450,
        "max_rain": 700,
        "soils": ["Loamy", "Clay"],
        "water": "Moderate"
    }
}
crop_families = {
    "Rice": "Cereal",
    "Wheat": "Cereal",
    "Maize": "Cereal",
    "Cotton": "Fibre",
    "Sugarcane": "Other",
    "Green Gram": "Legume",
    "Chickpea": "Legume",
    "Groundnut": "Legume",
    "Soybean": "Legume",
    "Other": "Other"
}
# Page configuration
st.set_page_config(
    page_title="AGROGUIDE",
    page_icon="🌱",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #F4F8F1;
}
h1, h2, h3, h4, h5, h6 {
    color: #17452B !important;
    opacity: 1 !important;
}
}
.stButton>button {
    background-color: #287A45;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
}

.stTextInput label,
.stNumberInput label,
.stSelectbox label {
    display: block !important;
    visibility: visible !important;
    color: #245C38 !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌱 AGROGUIDE")

st.subheader("Smart Crop Rotation & Climate Adaptation Platform")

st.info(
    "Explore climate-aware crop choices using NASA Earth observation "
    "data, soil information and farmer priorities."
)

st.markdown("---")
st.info("""
    Welcome to **AGROGUIDE** — a decision-support platform that helps
    farmers explore sustainable crop rotation strategies using NASA
    Earth observations, soil information and crop characteristics.
    """)

st.markdown("---")

# Introduction
st.header("🌾 Tell us about your farm")

st.info(
    "Enter your farm details to explore crop rotation possibilities "
    "that suit your environmental conditions and farming priorities."
)

# Farm details form
with st.form("farm_details"):

    col1, col2 = st.columns(2)

    with col1:
        location = st.text_input(
            "Farm location",
            placeholder="e.g. Kerala, India"
        )
        latitude = st.number_input(
            "Farm Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=10.85
        )

        longitude = st.number_input(
            "Farm Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=76.27
        )

        soil = st.selectbox(
            "Soil type",
            ["Clay", "Sandy", "Loamy", "Silty", "Unknown"]
        )

        current_crop = st.selectbox(
            "Currently cultivated crop",
            ["Rice", "Wheat", "Maize", "Cotton", "Sugarcane", "Other"]
        )
        previous_crop = st.selectbox(
            "Previously cultivated crop",
            [
                "Rice", "Wheat", "Maize", "Cotton",
                "Sugarcane", "Green Gram", "Chickpea",
                "Groundnut", "Soybean", "Other"
            ]
        )

    with col2:
        water = st.selectbox(
            "Water availability",
            ["Abundant", "Moderate", "Limited"]
        )

        priority = st.selectbox(
            "Your farming priority",
            [
                "Improve soil health",
                "Conserve water",
                "Increase crop diversity",
                "Improve long-term sustainability"
            ]
        )

    submitted = st.form_submit_button("Analyse My Farm 🌱")

# Display submitted details
if submitted:
    st.session_state["farm_submitted"] = True

if st.session_state.get("farm_submitted", False):
    if not location.strip():
        st.warning("Please enter your farm location.")

    else:
        st.success("Farm details submitted successfully!")

        st.header("🌾 Your Farm Profile")

        st.info(f"📍 Location: {location}")

        st.info(f"🌱 Soil Type: {soil}")

        st.info(f"🌾 Current Crop: {current_crop}")
        st.info(f"🌱 Previous Crop: {previous_crop}")

        st.info(f"💧 Water Availability: {water}")

        st.info(f"🎯 Farming Priority: {priority}")
        st.info(
            "Your farm profile is ready! "
            "Next, let's analyse NASA environmental data "
            "and explore suitable crop rotation strategies."
        )

        st.caption("AGROGUIDE | Sustainable Farming")
        st.markdown("---")
        st.header("🛰️ NASA Climate Analysis")

        if st.button("Fetch NASA Climate Data"):

            url = "https://power.larc.nasa.gov/api/temporal/climatology/point"

            params = {
                "parameters": "T2M,PRECTOTCORR",
                "community": "AG",
                "longitude": longitude,
                "latitude": latitude,
                "format": "JSON"
            }

            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()
                climate = data["properties"]["parameter"]

                temperature = climate["T2M"]
                rainfall = climate["PRECTOTCORR"]
                # Calculate climate statistics from NASA data

                month_keys = [
                    "JAN", "FEB", "MAR", "APR",
                    "MAY", "JUN", "JUL", "AUG",
                    "SEP", "OCT", "NOV", "DEC"
                ]

                month_days = [31, 28, 31, 30, 31, 30,
                            31, 31, 30, 31, 30, 31]

                monthly_temp = [
                    float(temperature[m])
                    for m in month_keys
                    if temperature[m] is not None
                ]

                avg_temp = sum(monthly_temp) / len(monthly_temp)

                annual_rainfall = sum(
                    float(rainfall[m]) * days
                    for m, days in zip(month_keys, month_days)
                    if rainfall[m] is not None
                )

                st.session_state["avg_temperature"] = avg_temp
                st.session_state["annual_rainfall"] = annual_rainfall
                st.session_state["avg_rainfall"] = sum(
                    float(rainfall[m]) for m in month_keys
                    if rainfall[m] is not None
                ) / 12

                st.session_state["climate_ready"] = True
                st.subheader("🌍 Climate Summary")

                st.info(
                    f"Average Annual Temperature: {avg_temp:.2f} °C"
                )

                st.info(
                    f"Estimated Annual Rainfall: {annual_rainfall:.2f} mm"
                )

                st.success("NASA climate data fetched successfully!")

                months = [
                        "JAN", "FEB", "MAR", "APR",
                        "MAY", "JUN", "JUL", "AUG",
                        "SEP", "OCT", "NOV", "DEC"
                    ]

                temp_chart = pd.Series({
                        m: float(temperature[m]) for m in months
                        if temperature[m] is not None
                    })

                rain_chart = pd.Series({
                        m: float(rainfall[m]) for m in months
                        if rainfall[m] is not None
                    })

                st.subheader("🌡️ Monthly Average Temperature (°C)")
                st.line_chart(temp_chart)

                st.subheader("🌧️ Average Daily Precipitation by Month (mm/day)")
                st.line_chart(rain_chart)
                st.subheader("📋 Monthly Climate Data")

                monthly_climate = pd.DataFrame({
                    "Month": months,
                    "Average Temperature (°C)": [
                        float(temperature[m]) for m in months
                    ],
                    "Average Daily Rainfall (mm/day)": [
                        float(rainfall[m]) for m in months
                    ]
                })

                st.dataframe(monthly_climate)

                st.caption("Source: NASA POWER | Long-term monthly climatology")

            except Exception as e:
                st.error(f"Could not fetch NASA data: {e}")
        st.markdown("---")
        st.header("🌱 Crop Rotation Recommendations")
        st.subheader("📊 Crop Suitability Scores")

        if st.session_state.get("climate_ready", False):

            avg_temp = st.session_state["avg_temperature"]
            annual_rain = st.session_state["annual_rainfall"]

            results_list = []

            for crop, details in crop_data.items():

                # Temperature score
                temp_score = 30 if details["min_temp"] <= avg_temp <= details["max_temp"] else 0

                # Rainfall score
                rain_score = 30 if details["min_rain"] <= annual_rain <= details["max_rain"] else 0

                # Soil score
                if soil == "Unknown":
                    soil_score = 10
                elif soil in details["soils"]:
                    soil_score = 20
                else:
                    soil_score = 0

                # Water score
                water_score = 0

                if water == "Abundant":
                    water_score = 20
                elif water == "Moderate" and details["water"] in ["Low", "Moderate"]:
                    water_score = 20
                elif water == "Limited" and details["water"] == "Low":
                    water_score = 20

                # Calculate base score
                base_score = temp_score + rain_score + soil_score + water_score

                # Crop rotation adjustment
                rotation_adjustment = 0
                rotation_note = "Good crop diversity"

                if crop == previous_crop or crop == current_crop:
                    rotation_adjustment = -20
                    rotation_note = "Repeated crop - rotation discouraged"

                elif crop_families[crop] == crop_families.get(current_crop, "Other"):
                    rotation_adjustment = -10
                    rotation_note = "Same crop family - consider diversification"

                score_after_rotation = max(0, base_score + rotation_adjustment)

                # Farmer priority bonus
                priority_bonus = 0
                priority_note = "General suitability"

                if priority == "Improve soil health" and crop_families[crop] == "Legume":
                    priority_bonus = 10
                    priority_note = "Supports soil fertility"

                elif priority == "Conserve water" and details["water"] == "Low":
                    priority_bonus = 10
                    priority_note = "Lower water requirement"

                elif priority == "Increase crop diversity" and crop != current_crop and crop != previous_crop:
                    priority_bonus = 10
                    priority_note = "Supports crop diversity"

                elif priority == "Improve long-term sustainability" and crop_families[crop] == "Legume":
                    priority_bonus = 10
                    priority_note = "Supports sustainable soil management"

                # Final score
                total_score = min(100, score_after_rotation + priority_bonus)
                results_list.append({
                    "Crop": crop,
                    "Temperature": temp_score,
                    "Rainfall": rain_score,
                    "Soil": soil_score,
                    "Water": water_score,
                    "Total Score": total_score,
                    "Rotation Note": rotation_note,
                    "Priority Note": priority_note,
                    "Rotation Adjustment": rotation_adjustment,
                    "Priority Bonus": priority_bonus
                })

            results = pd.DataFrame(results_list)

            results = results.sort_values(
                by="Total Score",
                ascending=False
            )

            st.dataframe(results)

            best_crop = results.iloc[0]["Crop"]

            st.success(f"🌱 Best scoring crop: {best_crop}")
            st.write("### Why was this crop selected?")

            best_details = crop_data[best_crop]

            st.info(f"🌡️ Suitable temperature: {best_details['min_temp']}–{best_details['max_temp']} °C")
            st.info(f"🌧️ Suitable annual rainfall: {best_details['min_rain']}–{best_details['max_rain']} mm")
            st.info(f"🌱 Suitable soil types: {', '.join(best_details['soils'])}")
            st.info(f"💧 Water requirement: {best_details['water']}")
            st.markdown("---")

            st.subheader("📊 Crop Suitability Comparison")

            chart_data = results.set_index("Crop")[["Total Score"]]

            st.bar_chart(chart_data)
            st.subheader("⚠️ Climate Suitability Alerts")

            for crop, details in crop_data.items():

                if not (details["min_temp"] <= avg_temp <= details["max_temp"]):
                    st.warning(f"{crop}: Temperature is outside the reference range.")

                if not (details["min_rain"] <= annual_rain <= details["max_rain"]):
                    st.warning(f"{crop}: Annual rainfall is outside the reference range.")
        else:
            st.warning("Fetch NASA climate data to calculate crop scores.")
    if st.session_state.get("climate_ready", False):

            st.subheader("🌾 Final Crop Recommendation")

            best_crop = results.iloc[0]["Crop"]

            st.success(f"Recommended next crop: {best_crop}")
            st.caption(
                    "Note: This is an experimental suitability estimate based on "
                    "available climate data, soil information, crop characteristics "
                    "and farmer preferences. Verify recommendations with local "
                    "agricultural experts before making farming decisions."
            )
            st.subheader("🔍 Why is this crop recommended?")

            best_result = results.iloc[0]

            st.info(f"🌡️ Temperature Score: {best_result['Temperature']}/30")

            st.info(f"🌧️ Rainfall Score: {best_result['Rainfall']}/30")

            st.info(f"🌱 Soil Score: {best_result['Soil']}/20")

            st.info(f"💧 Water Score: {best_result['Water']}/20")

            st.info(f"🔄 Rotation: {best_result['Rotation Note']}")

            st.info(f"🎯 Farmer Priority: {best_result['Priority Note']}")

            st.info(
                f"AGROGUIDE selected {best_crop} because it received "
                f"the highest suitability score of "
                f"{results.iloc[0]['Total Score']}/100."
            )

    else:
            st.warning("Please fetch NASA climate data first.")
st.markdown("---")
st.header("ℹ️ About AGROGUIDE")
st.info("AGROGUIDE is a climate-aware crop rotation platform.")

st.info("Data Source: NASA POWER Earth Observation Data.")

st.info("Factors considered:")
st.info("- Temperature and rainfall")
st.info("- Soil type")
st.info("- Water availability")
st.info("- Previous and current crops")
st.info("- Farmer's farming priority")

st.info("Recommendation Method:")
st.info("A weighted suitability scoring system.")
st.caption(
        "AGROGUIDE provides prototype recommendations for decision support. "
        "Farmers should verify crop choices with local agricultural experts."
)
st.success("ABOUT SECTION REACHED!")
st.markdown("---")
st.header("⚙️ How AGROGUIDE Works")

st.info(
    "1. Farm Details: Collects location, soil type, "
    "crop history, water availability and farmer priorities."
)

st.info(
    "2. NASA Climate Data: Retrieves temperature and "
    "precipitation data using NASA POWER API."
)

st.info(
    "3. Suitability Analysis: Compares climate conditions, "
    "soil compatibility, water needs and crop characteristics."
)

st.info(
    "4. Crop Rotation: Applies adjustments based on crop "
    "history and crop families."
)

st.info(
    "5. Final Recommendation: Ranks crops using a weighted "
    "suitability scoring system."
)