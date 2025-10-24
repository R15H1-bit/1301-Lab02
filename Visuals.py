# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:

if os.path.exists("data.csv"):
    try:
        edrinkcsv = pd.read_csv("data.csv")
        st.success("Loaded CSV file successfully!")
        st.dataframe(edrinkcsv)
    except Exception as error:
        st.error(f"Error loading CSV file: {error}")
else:
    st.warning("CSV file not found.")

if os.path.exists("data.json"):
    try:
        with open("data.json", "r") as edrinks:
            edrinkdata = json.load(edrinks)
        st.success("Loaded JSON successfully!")
    except Exception as error:
        st.error(f"Error loading data.json: {error}")
else:
    st.warning("JSON not found.")


st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH

st.subheader("Graph 1: Rishi's Energy Drink Ratings (Static)")
st.write("This static bar chart my average ratings for a few energy drinks.")

if edrinkdata and "energy_drink_ratings" in edrinkdata:
    ratingsdata = pd.DataFrame(edrinkdata["energy_drink_ratings"])
    st.bar_chart(ratingsdata.set_index("name")["rating"])
else:
    st.warning("No rating data found in JSON.")



# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Energy Drink Consumption Over Time (Dynamic)")
st.write("Use the slider to filter days based on the number of energy drinks consumed.")

if edrinkcsv is not None and not edrinkcsv.empty:
    if "category" in edrinkcsv.columns and "value" in edrinkcsv.columns:


        
        minimumdrinks = int(edrinkcsv["value"].min())
        maximumdrinks = int(edrinkcsv["value"].max())
        st.slider("Select minimum number of energy drinks to display:", min_value = minimumdrinks, max_value=maximumdrinks, value = minimumdrinks, key = 'drinks')

        fileteredDrinks = edrinkcsv[edrinkcsv["value"] >= st.session_state.drinks]

        st.line_chart(fileteredDrinks.set_index("category")["value"]) # NEW

        st.info(f"Showing days where you had at least {st.session_state.drinks} drinks.")
    else:
        st.warning("CSV does not have 'category' and 'value' columns.")
else:
    st.warning("CSV is not available.")



# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Filter Energy Drink Ratings (Dynamic)")
st.write("Use the  widget to filter energy drink brands and view their ratings.")

if edrinkdata and "energy_drink_ratings" in edrinkdata:
    edrinkjson = pd.DataFrame(edrinkdata["energy_drink_ratings"])
    brands = edrinkjson["name"].tolist()

    if "brands" not in st.session_state:
        st.session_state.brands = brands
        
    st.session_state.brands = st.multiselect("Select brands to display", options=brands, default=st.session_state.brands) #NEW

    filteredDrinks2 = edrinkjson[edrinkjson["name"].isin(st.session_state.brands)]
    st.bar_chart(filteredDrinks2.set_index("name")["rating"]) #NEW

else:
    st.warning("JSON data not available.")
