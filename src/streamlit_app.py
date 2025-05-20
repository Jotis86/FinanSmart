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


# Dashboard page
if menu == "Dashboard":
    st.markdown("<h1 class='main-header'>FINANSMART Dashboard</h1>", unsafe_allow_html=True)
    
    # Current date information
    today = datetime.now()
    current_month = today.strftime("%B")
    current_year = today.year
    
    # Calculate summary metrics
    total_income = sum(item["amount"] for item in st.session_state['incomes'])
    total_expense = sum(item["amount"] for item in st.session_state['expenses'])
    balance = total_income - total_expense
    
    # Current month data
    current_month_incomes = [
        income for income in st.session_state['incomes'] 
        if 'date' in income and datetime.strptime(income['date'], '%Y-%m-%d').month == today.month
        and datetime.strptime(income['date'], '%Y-%m-%d').year == today.year
    ]
    
    current_month_expenses = [
        expense for expense in st.session_state['expenses'] 
        if 'date' in expense and datetime.strptime(expense['date'], '%Y-%m-%d').month == today.month
        and datetime.strptime(expense['date'], '%Y-%m-%d').year == today.year
    ]
    
    current_month_income = sum(item["amount"] for item in current_month_incomes)
    current_month_expense = sum(item["amount"] for item in current_month_expenses)
    current_month_balance = current_month_income - current_month_expense
    
    # Display key metrics in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Total Balance</h2>", unsafe_allow_html=True)
        balance_color = "green" if balance >= 0 else "red"
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:{balance_color}'>${balance:.2f}</div><div class='metric-label'>All-time Balance</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Total Income</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:blue'>${total_income:.2f}</div><div class='metric-label'>All-time Income</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='sub-header'>Total Expenses</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:purple'>${total_expense:.2f}</div><div class='metric-label'>All-time Expenses</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Current month metrics
    st.markdown("<h2 class='sub-header' style='margin-top: 30px;'>Current Month Overview</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{current_month} Balance</h3>", unsafe_allow_html=True)
        month_balance_color = "green" if current_month_balance >= 0 else "red"
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:{month_balance_color}'>${current_month_balance:.2f}</div><div class='metric-label'>{current_month} {current_year}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{current_month} Income</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:blue'>${current_month_income:.2f}</div><div class='metric-label'>{current_month} {current_year}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{current_month} Expenses</h3>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-card'><div class='metric-value' style='color:purple'>${current_month_expense:.2f}</div><div class='metric-label'>{current_month} {current_year}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Monthly trends
    st.markdown("<h2 class='sub-header' style='margin-top: 30px;'>Monthly Trends</h2>", unsafe_allow_html=True)
    
    # Calculate monthly data
    monthly_incomes = calculate_monthly_totals(st.session_state['incomes'])
    monthly_expenses = calculate_monthly_totals(st.session_state['expenses'])
    
    # Only render if we have data
    if not monthly_incomes.empty or not monthly_expenses.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot income
        if not monthly_incomes.empty:
            ax.bar(monthly_incomes['month_name'], monthly_incomes['amount'], alpha=0.6, label='Income', color='blue')
        
        # Plot expenses
        if not monthly_expenses.empty:
            ax.bar(monthly_expenses['month_name'], monthly_expenses['amount'], alpha=0.6, label='Expenses', color='red')
        
        ax.set_title('Monthly Income vs Expenses')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.legend()
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
    else:
        st.info("No monthly data available yet. Add income and expenses to see trends.")
    
    # Recent transactions
    st.markdown("<h2 class='sub-header' style='margin-top: 30px;'>Recent Transactions</h2>", unsafe_allow_html=True)
    
    # Combine and sort transactions
    all_transactions = []
    
    for income in st.session_state['incomes']:
        transaction = income.copy()
        transaction['type'] = 'Income'
        all_transactions.append(transaction)
    
    for expense in st.session_state['expenses']:
        transaction = expense.copy()
        transaction['type'] = 'Expense'
        all_transactions.append(transaction)
    
    # Sort by date (most recent first)
    all_transactions.sort(key=lambda x: datetime.strptime(x.get('date', '1900-01-01'), '%Y-%m-%d'), reverse=True)
    
    # Display recent transactions
    if all_transactions:
        # Take only the 5 most recent transactions
        recent_transactions = all_transactions[:5]
        
        # Create a dataframe for display
        df_recent = pd.DataFrame(recent_transactions)
        df_recent = df_recent[['date', 'type', 'category', 'description', 'amount']]
        
        # Style the dataframe
        st.dataframe(df_recent, height=200)
    else:
        st.info("No transactions available yet. Add income and expenses to see recent transactions.")


# Add Income/Expense page
elif menu == "Add Income/Expense":
    st.markdown("<h1 class='main-header'>Add Income and Expense</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Here you can add your income and expenses. Select the type, category, and description, 
    then enter the amount. This will help you keep track of your financial transactions.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Define categories and descriptions
    income_categories = ["Salary", "Bonus", "Investment", "Other"]
    expense_categories = ["Food", "Transportation", "Housing", "Entertainment", "Health", 
                         "Education", "Utilities", "Insurance", "Debt", "Savings", "Gifts", 
                         "Travel", "Other"]
    
    descriptions = {
        "Salary": ["Monthly Salary", "Freelance Work", "Part-time Job", "Consulting"],
        "Bonus": ["Year-end Bonus", "Performance Bonus", "Referral Bonus", "Holiday Bonus"],
        "Investment": ["Stock Dividends", "Real Estate Income", "Interest Income", "Cryptocurrency Gains"],
        "Other": ["Gift", "Lottery", "Inheritance", "Found Money"],
        "Food": ["Groceries", "Dining Out", "Snacks", "Beverages"],
        "Transportation": ["Gas", "Public Transport", "Car Maintenance", "Parking Fees"],
        "Housing": ["Rent", "Mortgage", "Property Taxes", "Home Repairs"],
        "Entertainment": ["Movies", "Concerts", "Streaming Services", "Games"],
        "Health": ["Doctor Visit", "Medication", "Health Insurance", "Gym Membership"],
        "Education": ["Tuition", "Books", "Online Courses", "Workshops"],
        "Utilities": ["Electricity", "Water", "Internet", "Phone"],
        "Insurance": ["Car Insurance", "Home Insurance", "Life Insurance", "Health Insurance"],
        "Debt": ["Credit Card Payment", "Loan Payment", "Mortgage Payment", "Student Loan Payment"],
        "Savings": ["Emergency Fund", "Retirement Fund", "Investment Account", "Savings Account"],
        "Gifts": ["Birthday Gifts", "Holiday Gifts", "Wedding Gifts", "Charity"],
        "Travel": ["Flights", "Hotels", "Car Rental", "Activities"],
        "Other": ["Miscellaneous", "Unexpected Expenses", "Pet Expenses", "Subscriptions"]
    }
    
    # Create a form for adding income or expense
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Transaction Details")
        
        # Select transaction type
        trans_type = st.selectbox("Select type", ["Income", "Expense"])
        
        # Select category based on transaction type
        if trans_type == "Income":
            category = st.selectbox("Select category", income_categories)
        else:
            category = st.selectbox("Select category", expense_categories)
        
        # Select description based on category
        description = st.selectbox("Select description", descriptions[category])
        
        # Enter amount
        amount = st.number_input("Enter amount", min_value=0.01, step=0.01, format="%.2f")
        
        # Select date
        date = st.date_input("Select date", datetime.now())
        date_str = date.strftime("%Y-%m-%d")
        
        # Add button
        if st.button("Add Transaction"):
            if trans_type == "Income":
                # Add income
                new_income = {"amount": amount, "description": description, 
                             "category": category, "date": date_str}
                st.session_state['incomes'].append(new_income)
                save_data(st.session_state['incomes'], incomes_file_path)
                st.success(f"Income of ${amount:.2f} added successfully!")
            else:
                # Add expense
                new_expense = {"amount": amount, "description": description, 
                              "category": category, "date": date_str}
                st.session_state['expenses'].append(new_expense)
                save_data(st.session_state['expenses'], expenses_file_path)
                st.success(f"Expense of ${amount:.2f} added successfully!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Quick Summary")
        
        # Display total income, expenses and balance
        total_income = sum(item["amount"] for item in st.session_state['incomes'])
        total_expense = sum(item["amount"] for item in st.session_state['expenses'])
        balance = total_income - total_expense
        
        st.info(f"Total Income: ${total_income:.2f}")
        st.info(f"Total Expenses: ${total_expense:.2f}")
        
        # Show balance with appropriate color
        if balance >= 0:
            st.success(f"Current Balance: ${balance:.2f}")
        else:
            st.error(f"Current Balance: ${balance:.2f}")
            
        # Show recent transactions
        st.subheader("Last 3 Transactions")
        
        # Combine and sort transactions
        all_transactions = []
        for income in st.session_state['incomes']:
            transaction = income.copy()
            transaction['type'] = 'Income'
            all_transactions.append(transaction)
        
        for expense in st.session_state['expenses']:
            transaction = expense.copy()
            transaction['type'] = 'Expense'
            all_transactions.append(transaction)
        
        # Sort by date (most recent first)
        all_transactions.sort(key=lambda x: datetime.strptime(x.get('date', '1900-01-01'), '%Y-%m-%d'), reverse=True)
        
        # Display recent transactions
        if all_transactions:
            # Take only the 3 most recent transactions
            recent_transactions = all_transactions[:3]
            
            for idx, transaction in enumerate(recent_transactions):
                date = transaction.get('date', 'N/A')
                trans_type = transaction.get('type', 'N/A')
                category = transaction.get('category', 'N/A')
                amount = transaction.get('amount', 0)
                
                type_color = "blue" if trans_type == "Income" else "red"
                st.markdown(f"<p>{date} - <span style='color:{type_color}'>{trans_type}</span> - {category} - ${amount:.2f}</p>", unsafe_allow_html=True)
        else:
            st.write("No transactions yet.")
        
        st.markdown("</div>", unsafe_allow_html=True)