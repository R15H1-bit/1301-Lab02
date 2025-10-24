# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    st.subheader("Energy Drinks per Day")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    values = {}

    for day in days:
        values[day] = st.number_input(f"{day}", min_value = 0, step = 1)

    submitted = st.form_submit_button("Save Data")

    if submitted:
        with open('data.csv', 'w', newline='') as edrinkdata:
            writer = csv.writer(edrinkdata)

            if os.path.getsize('data.csv') == 0 or not os.path.exists('data.csv'):
                writer.writerow(["category", "value"])

            for day, value in values.items():
                writer.writerow([day, value])

            st.success("Your weekly energy drink data has been saved!")
            st.write("Here is your data:")
            st.table(pd.DataFrame(list(values.items()), columns=["category", "value"]))



# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

    st.divider()
    
