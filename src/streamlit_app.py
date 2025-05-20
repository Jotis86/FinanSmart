import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import calendar
import numpy as np
from main import Finance
import os
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="FINANSMART - Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #5E35B1;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the Finance class
finance = Finance()

# Define paths for images
sidebar_image_path = os.path.join(os.path.dirname(__file__), 'menu.jpg')
main_image_path = os.path.join(os.path.dirname(__file__), 'main.jpg')

# File paths for storing data
incomes_file_path = os.path.join(os.path.dirname(__file__), 'incomes.csv')
expenses_file_path = os.path.join(os.path.dirname(__file__), 'expenses.csv')
goals_file_path = os.path.join(os.path.dirname(__file__), 'goals.csv')

# Function to load data from CSV
def load_data(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            return pd.read_csv(file_path).to_dict('records')
        except pd.errors.EmptyDataError:
            return []
    return []

# Function to save data to CSV
def save_data(data, file_path):
    pd.DataFrame(data).to_csv(file_path, index=False)

# Function to export data to Excel
def to_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(st.session_state['incomes']).to_excel(writer, sheet_name='Incomes', index=False)
        pd.DataFrame(st.session_state['expenses']).to_excel(writer, sheet_name='Expenses', index=False)
    return output.getvalue()

# Function to calculate monthly totals
def calculate_monthly_totals(data):
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    if 'date' not in df.columns:
        df['date'] = datetime.now().strftime("%Y-%m-%d")
    
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    
    monthly_totals = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    monthly_totals['month_name'] = monthly_totals['month'].apply(lambda x: calendar.month_name[x])
    return monthly_totals

# Load data into session state
if 'incomes' not in st.session_state:
    st.session_state['incomes'] = load_data(incomes_file_path)

if 'expenses' not in st.session_state:
    st.session_state['expenses'] = load_data(expenses_file_path)
    
if 'goals' not in st.session_state:
    st.session_state['goals'] = load_data(goals_file_path)

# Initialize dark mode in session state if not present
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

# Apply dark mode if enabled
if st.session_state['dark_mode']:
    st.markdown("""
    <style>
        .reportview-container {
            background-color: #1E1E1E;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #2D2D2D;
        }
        .card {
            background-color: #2D2D2D;
            color: white;
        }
        .metric-card {
            background-color: #3D3D3D;
            color: white;
        }
        .metric-label {
            color: #BBB;
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with navigation menu and image
st.sidebar.image(sidebar_image_path, use_container_width=True)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", [
    "Dashboard", 
    "Add Income/Expense", 
    "View Charts", 
    "View Tables", 
    "Financial Goals",
    "Recommendations", 
    "Export Data",
    "Settings",
    "Acknowledgements"
])

# Dark mode toggle in sidebar
dark_mode = st.sidebar.checkbox("Dark Mode", value=st.session_state['dark_mode'])
if dark_mode != st.session_state['dark_mode']:
    st.session_state['dark_mode'] = dark_mode
    st.experimental_rerun()

# Main image (only on Dashboard)
if menu == "Dashboard":
    st.image(main_image_path, use_container_width=True)

# GitHub repository button
st.sidebar.markdown("""
<a href="https://github.com/Jotis86/FinanSmart" target="_blank">
    <button style="background-color: #000000; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
        GitHub Repository
    </button>
</a>
""", unsafe_allow_html=True)

# Add space between buttons
st.sidebar.write("")

# LinkedIn profile button
st.sidebar.markdown("""
<a href="https://www.linkedin.com/in/juan-duran-bon" target="_blank">
    <button style="background-color: #0077B5; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
        LinkedIn Profile
    </button>
</a>
""", unsafe_allow_html=True)

# Add space between buttons
st.sidebar.write("")

# Website button
st.sidebar.markdown("""
<a href="https://jotis86.github.io/Website/" target="_blank">
    <button style="background-color: #8A2BE2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">
        Juan Duran Website
    </button>
</a>
""", unsafe_allow_html=True)