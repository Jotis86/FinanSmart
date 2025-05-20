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


# View Charts page
elif menu == "View Charts":
    st.markdown("<h1 class='main-header'>Financial Charts</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Visualize your financial data with various charts. These visualizations will help you 
    understand your income and expense patterns better.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for different chart types
    chart_tabs = st.tabs(["Income & Expense Overview", "Category Breakdown", "Time Trends", "Custom Analysis"])
    
    # Get the data
    df_incomes = pd.DataFrame(st.session_state['incomes'])
    df_expenses = pd.DataFrame(st.session_state['expenses'])
    
    # Add date conversion if dataframes aren't empty
    if not df_incomes.empty and 'date' in df_incomes.columns:
        df_incomes['date'] = pd.to_datetime(df_incomes['date'])
    
    if not df_expenses.empty and 'date' in df_expenses.columns:
        df_expenses['date'] = pd.to_datetime(df_expenses['date'])
    
    # Tab 1: Income & Expense Overview
    with chart_tabs[0]:
        st.subheader("Income vs. Expense Overview")
        
        # Create figure with 2 subplots
        if not df_incomes.empty or not df_expenses.empty:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Income vs Expense Bar Chart
            total_income = df_incomes['amount'].sum() if not df_incomes.empty else 0
            total_expense = df_expenses['amount'].sum() if not df_expenses.empty else 0
            
            ax1.bar(['Income', 'Expense'], [total_income, total_expense], color=['green', 'red'])
            ax1.set_title('Total Income vs Expense')
            ax1.set_ylabel('Amount ($)')
            
            # Add value labels on the bars
            for i, v in enumerate([total_income, total_expense]):
                ax1.text(i, v + 5, f"${v:.2f}", ha='center')
            
            # Income vs Expense Pie Chart
            balance = total_income - total_expense
            savings_rate = (balance / total_income * 100) if total_income > 0 else 0
            
            ax2.pie([total_income, total_expense], 
                   labels=['Income', 'Expense'], 
                   autopct='%1.1f%%',
                   colors=['green', 'red'],
                   startangle=90)
            ax2.set_title(f'Income vs Expense (Savings Rate: {savings_rate:.1f}%)')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Additional stats
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Income", f"${total_income:.2f}")
            
            with col2:
                st.metric("Total Expenses", f"${total_expense:.2f}")
            
            with col3:
                st.metric("Balance", f"${balance:.2f}", delta=f"{savings_rate:.1f}% of income" if total_income > 0 else "N/A")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No data available to generate charts. Please add your income and expenses.")
    
    # Tab 2: Category Breakdown
    with chart_tabs[1]:
        st.subheader("Category Breakdown")
        
        # Select income or expense for category analysis
        category_type = st.radio("Select data to analyze", ["Income", "Expense"])
        
        if category_type == "Income" and not df_incomes.empty:
            df = df_incomes
            color_palette = "viridis"
        elif category_type == "Expense" and not df_expenses.empty:
            df = df_expenses
            color_palette = "magma"
        else:
            st.info(f"No {category_type.lower()} data available to generate charts.")
            df = pd.DataFrame()
        
        if not df.empty:
            # Create figure with 2 subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            
            # Category Bar Chart
            category_totals = df.groupby('category')['amount'].sum().reset_index()
            
            # Sort by amount for better visualization
            category_totals = category_totals.sort_values('amount', ascending=False)
            
            sns.barplot(x='category', y='amount', data=category_totals, palette=color_palette, ax=ax1)
            ax1.set_title(f'{category_type} by Category')
            ax1.set_xlabel('Category')
            ax1.set_ylabel('Amount ($)')
            ax1.tick_params(axis='x', rotation=45)
            
            # Add value labels
            for i, v in enumerate(category_totals['amount']):
                ax1.text(i, v + 5, f"${v:.0f}", ha='center')
            
            # Category Pie Chart
            ax2.pie(category_totals['amount'], 
                   labels=category_totals['category'], 
                   autopct='%1.1f%%',
                   colors=sns.color_palette(color_palette, len(category_totals)),
                   startangle=90)
            ax2.set_title(f'{category_type} Distribution by Category')
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Display category breakdown as a table
            st.subheader(f"{category_type} Breakdown by Category")
            
            # Calculate percentages
            total = category_totals['amount'].sum()
            category_totals['percentage'] = category_totals['amount'] / total * 100
            category_totals = category_totals.sort_values('amount', ascending=False)
            
            # Format table
            category_totals['amount'] = category_totals['amount'].apply(lambda x: f"${x:.2f}")
            category_totals['percentage'] = category_totals['percentage'].apply(lambda x: f"{x:.1f}%")
            
            st.table(category_totals)
        
    # Tab 3: Time Trends
    with chart_tabs[2]:
        st.subheader("Time Trends Analysis")
        
        # Filter options
        time_period = st.selectbox("Select time period", ["Monthly", "Weekly", "Daily"])
        
        # Get time series data
        if not df_incomes.empty and 'date' in df_incomes.columns:
            if time_period == "Monthly":
                df_incomes['period'] = df_incomes['date'].dt.strftime('%Y-%m')
            elif time_period == "Weekly":
                df_incomes['period'] = df_incomes['date'].dt.strftime('%Y-%W')
            else:  # Daily
                df_incomes['period'] = df_incomes['date'].dt.strftime('%Y-%m-%d')
                
            incomes_by_period = df_incomes.groupby('period')['amount'].sum()
        else:
            incomes_by_period = pd.Series(dtype=float)
        
        if not df_expenses.empty and 'date' in df_expenses.columns:
            if time_period == "Monthly":
                df_expenses['period'] = df_expenses['date'].dt.strftime('%Y-%m')
            elif time_period == "Weekly":
                df_expenses['period'] = df_expenses['date'].dt.strftime('%Y-%W')
            else:  # Daily
                df_expenses['period'] = df_expenses['date'].dt.strftime('%Y-%m-%d')
                
            expenses_by_period = df_expenses.groupby('period')['amount'].sum()
        else:
            expenses_by_period = pd.Series(dtype=float)
        
        # Create time series chart
        if not incomes_by_period.empty or not expenses_by_period.empty:
            # Get all periods for consistent x-axis
            all_periods = sorted(set(list(incomes_by_period.index) + list(expenses_by_period.index)))
            
            # Create a DataFrame with all periods
            df_time = pd.DataFrame(index=all_periods)
            df_time['income'] = incomes_by_period
            df_time['expense'] = expenses_by_period
            
            # Fill NaN with 0
            df_time.fillna(0, inplace=True)
            
            # Calculate balance
            df_time['balance'] = df_time['income'] - df_time['expense']
            
            # Plot time series
            fig, ax = plt.subplots(figsize=(12, 6))
            
            ax.plot(df_time.index, df_time['income'], marker='o', linestyle='-', color='green', label='Income')
            ax.plot(df_time.index, df_time['expense'], marker='o', linestyle='-', color='red', label='Expense')
            ax.plot(df_time.index, df_time['balance'], marker='o', linestyle='-', color='blue', label='Balance')
            
            ax.set_title(f'{time_period} Financial Trend')
            ax.set_xlabel('Period')
            ax.set_ylabel('Amount ($)')
            ax.legend()
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)
            
            # Show the data as a table
            st.subheader(f"{time_period} Financial Data")
            
            # Format the table
            display_df = df_time.copy()
            display_df['income'] = display_df['income'].apply(lambda x: f"${x:.2f}")
            display_df['expense'] = display_df['expense'].apply(lambda x: f"${x:.2f}")
            display_df['balance'] = display_df['balance'].apply(lambda x: f"${x:.2f}")
            
            st.table(display_df)
        else:
            st.info("Not enough time series data to generate charts. Please add dated income and expenses.")
    
    # Tab 4: Custom Analysis
    with chart_tabs[3]:
        st.subheader("Custom Financial Analysis")
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("""
        Here you can perform a more detailed analysis of your financial data by selecting specific criteria.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Select data type
        data_type = st.radio("Select data to analyze", ["Income", "Expense", "Both"])
        
        if data_type == "Income" and not df_incomes.empty:
            df_analysis = df_incomes.copy()
            analysis_possible = True
        elif data_type == "Expense" and not df_expenses.empty:
            df_analysis = df_expenses.copy()
            analysis_possible = True
        elif data_type == "Both" and (not df_incomes.empty or not df_expenses.empty):
            # Combine income and expense data
            if not df_incomes.empty:
                df_incomes_copy = df_incomes.copy()
                df_incomes_copy['type'] = 'Income'
            else:
                df_incomes_copy = pd.DataFrame()
            
            if not df_expenses.empty:
                df_expenses_copy = df_expenses.copy()
                df_expenses_copy['type'] = 'Expense'
            else:
                df_expenses_copy = pd.DataFrame()
            
            # Combine the data
            if not df_incomes_copy.empty and not df_expenses_copy.empty:
                df_analysis = pd.concat([df_incomes_copy, df_expenses_copy])
            elif not df_incomes_copy.empty:
                df_analysis = df_incomes_copy
            else:
                df_analysis = df_expenses_copy
                
            analysis_possible = True
        else:
            st.info(f"No data available for the selected type. Please add your income and expenses.")
            analysis_possible = False
        
        if analysis_possible:
            # Date range filter
            if 'date' in df_analysis.columns:
                min_date = df_analysis['date'].min().date()
                max_date = df_analysis['date'].max().date()
                
                date_range = st.date_input(
                    "Select date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    df_analysis = df_analysis[
                        (df_analysis['date'].dt.date >= start_date) &
                        (df_analysis['date'].dt.date <= end_date)
                    ]
            
            # Select categories to include
            if 'category' in df_analysis.columns:
                all_categories = df_analysis['category'].unique().tolist()
                selected_categories = st.multiselect(
                    "Select categories to include",
                    options=all_categories,
                    default=all_categories
                )
                
                if selected_categories:
                    df_analysis = df_analysis[df_analysis['category'].isin(selected_categories)]
            
            # Generate custom chart
            if not df_analysis.empty:
                chart_type = st.selectbox(
                    "Select chart type",
                    options=["Bar Chart", "Pie Chart", "Line Chart", "Histogram"]
                )
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                if chart_type == "Bar Chart":
                    # Group data
                    if 'category' in df_analysis.columns:
                        group_by = st.selectbox("Group by", ["category", "description"])
                        df_grouped = df_analysis.groupby(group_by)['amount'].sum().reset_index()
                        
                        # Sort by amount for better visualization
                        df_grouped = df_grouped.sort_values('amount', ascending=False)
                        
                        # Plot bar chart
                        sns.barplot(x=group_by, y='amount', data=df_grouped, palette='viridis', ax=ax)
                        ax.set_title(f'{data_type} by {group_by.capitalize()}')
                        ax.set_xlabel(group_by.capitalize())
                        ax.set_ylabel('Amount ($)')
                        ax.tick_params(axis='x', rotation=45)
                        
                        # Add value labels
                        for i, v in enumerate(df_grouped['amount']):
                            ax.text(i, v + 5, f"${v:.0f}", ha='center')
                    else:
                        st.info("Not enough categorical data for a bar chart.")
                
                elif chart_type == "Pie Chart":
                    # Group data
                    if 'category' in df_analysis.columns:
                        group_by = st.selectbox("Group by", ["category", "description"])
                        df_grouped = df_analysis.groupby(group_by)['amount'].sum()
                        
                        # Plot pie chart
                        ax.pie(df_grouped, 
                              labels=df_grouped.index, 
                              autopct='%1.1f%%',
                              colors=sns.color_palette('viridis', len(df_grouped)),
                              startangle=90)
                        ax.set_title(f'{data_type} Distribution by {group_by.capitalize()}')
                    else:
                        st.info("Not enough categorical data for a pie chart.")
                
                elif chart_type == "Line Chart":
                    # Check if we have date data
                    if 'date' in df_analysis.columns:
                        # Group by time period
                        time_period = st.selectbox("Time period", ["Daily", "Weekly", "Monthly"])
                        
                        if time_period == "Daily":
                            df_analysis['period'] = df_analysis['date'].dt.strftime('%Y-%m-%d')
                        elif time_period == "Weekly":
                            df_analysis['period'] = df_analysis['date'].dt.strftime('%Y-%W')
                        else:  # Monthly
                            df_analysis['period'] = df_analysis['date'].dt.strftime('%Y-%m')
                        
                        # Group by period
                        if data_type == "Both" and 'type' in df_analysis.columns:
                            # Group by period and type
                            df_grouped = df_analysis.groupby(['period', 'type'])['amount'].sum().reset_index()
                            
                            # Get periods sorted
                            periods = sorted(df_grouped['period'].unique())
                            
                            # Plot lines by type
                            for t in df_grouped['type'].unique():
                                df_type = df_grouped[df_grouped['type'] == t]
                                ax.plot(df_type['period'], df_type['amount'], 
                                       marker='o', linestyle='-', 
                                       label=t)
                        else:
                            # Group by period only
                            df_grouped = df_analysis.groupby('period')['amount'].sum()
                            ax.plot(df_grouped.index, df_grouped.values, 
                                   marker='o', linestyle='-')
                        
                        ax.set_title(f'{time_period} {data_type} Trend')
                        ax.set_xlabel('Period')
                        ax.set_ylabel('Amount ($)')
                        ax.legend()
                        
                        # Rotate x-axis labels for better readability
                        plt.xticks(rotation=45)
                    else:
                        st.info("No date data available for a line chart.")
                
                elif chart_type == "Histogram":
                    # Plot histogram of amounts
                    sns.histplot(df_analysis['amount'], bins=20, kde=True, ax=ax)
                    ax.set_title(f'{data_type} Amount Distribution')
                    ax.set_xlabel('Amount ($)')
                    ax.set_ylabel('Frequency')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Show the data
                st.subheader("Filtered Data")
                st.dataframe(df_analysis)
            else:
                st.info("No data available for the selected filters.")


# View Tables page
elif menu == "View Tables":
    st.markdown("<h1 class='main-header'>Financial Data Tables</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    This section shows detailed tables of your income and expenses. You can filter, sort, 
    and manage your financial data here.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for different data tables
    table_tabs = st.tabs(["Income", "Expenses", "Data Management"])
    
    # Tab 1: Income Data
    with table_tabs[0]:
        st.subheader("Income Data")
        
        if st.session_state['incomes']:
            # Convert to DataFrame
            df_incomes = pd.DataFrame(st.session_state['incomes'])
            
            # Add filters
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Filters")
            
            # Date filter
            if 'date' in df_incomes.columns:
                df_incomes['date'] = pd.to_datetime(df_incomes['date'])
                min_date = df_incomes['date'].min().date()
                max_date = df_incomes['date'].max().date()
                
                date_range = st.date_input(
                    "Filter by date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="income_date_filter"
                )
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    mask = ((df_incomes['date'].dt.date >= start_date) & 
                           (df_incomes['date'].dt.date <= end_date))
                    df_incomes_filtered = df_incomes.loc[mask]
                else:
                    df_incomes_filtered = df_incomes
            else:
                df_incomes_filtered = df_incomes
            
            # Category filter
            if 'category' in df_incomes.columns:
                categories = ['All'] + sorted(df_incomes['category'].unique().tolist())
                selected_category = st.selectbox("Filter by category", categories, key="income_category_filter")
                
                if selected_category != 'All':
                    df_incomes_filtered = df_incomes_filtered[df_incomes_filtered['category'] == selected_category]
            
            # Amount filter
            col1, col2 = st.columns(2)
            with col1:
                min_amount = st.number_input("Minimum amount", value=0.0, step=10.0, key="income_min_amount")
            with col2:
                if 'amount' in df_incomes.columns:
                    max_income = float(df_incomes['amount'].max())
                else:
                    max_income = 1000.0
                max_amount = st.number_input("Maximum amount", value=max_income, step=10.0, key="income_max_amount")
            
            if 'amount' in df_incomes_filtered.columns:
                df_incomes_filtered = df_incomes_filtered[
                    (df_incomes_filtered['amount'] >= min_amount) & 
                    (df_incomes_filtered['amount'] <= max_amount)
                ]
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Show data
            st.subheader("Income Records")
            
            if not df_incomes_filtered.empty:
                # Sort data
                sort_options = df_incomes_filtered.columns.tolist()
                selected_sort = st.selectbox("Sort by", sort_options, index=sort_options.index('date') if 'date' in sort_options else 0)
                sort_order = st.radio("Sort order", ["Descending", "Ascending"], horizontal=True)
                
                # Apply sorting
                ascending = sort_order == "Ascending"
                df_incomes_filtered = df_incomes_filtered.sort_values(by=selected_sort, ascending=ascending)
                
                # Display the table
                st.dataframe(df_incomes_filtered, use_container_width=True)
                
                # Show summary statistics
                st.subheader("Income Summary")
                total_income = df_incomes_filtered['amount'].sum()
                avg_income = df_incomes_filtered['amount'].mean()
                count = len(df_incomes_filtered)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Income", f"${total_income:.2f}")
                col2.metric("Average Income", f"${avg_income:.2f}")
                col3.metric("Number of Entries", count)
                
                # Download data as CSV
                csv = df_incomes_filtered.to_csv(index=False)
                st.download_button(
                    label="Download Filtered Income Data as CSV",
                    data=csv,
                    file_name="filtered_income_data.csv",
                    mime="text/csv"
                )
            else:
                st.info("No income data available for the selected filters.")
        else:
            st.info("No income data available. Please add your income in the 'Add Income/Expense' section.")
    
    # Tab 2: Expense Data
    with table_tabs[1]:
        st.subheader("Expense Data")
        
        if st.session_state['expenses']:
            # Convert to DataFrame
            df_expenses = pd.DataFrame(st.session_state['expenses'])
            
            # Add filters
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Filters")
            
            # Date filter
            if 'date' in df_expenses.columns:
                df_expenses['date'] = pd.to_datetime(df_expenses['date'])
                min_date = df_expenses['date'].min().date()
                max_date = df_expenses['date'].max().date()
                
                date_range = st.date_input(
                    "Filter by date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="expense_date_filter"
                )
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    mask = ((df_expenses['date'].dt.date >= start_date) & 
                           (df_expenses['date'].dt.date <= end_date))
                    df_expenses_filtered = df_expenses.loc[mask]
                else:
                    df_expenses_filtered = df_expenses
            else:
                df_expenses_filtered = df_expenses
            
            # Category filter
            if 'category' in df_expenses.columns:
                categories = ['All'] + sorted(df_expenses['category'].unique().tolist())
                selected_category = st.selectbox("Filter by category", categories, key="expense_category_filter")
                
                if selected_category != 'All':
                    df_expenses_filtered = df_expenses_filtered[df_expenses_filtered['category'] == selected_category]
            
            # Amount filter
            col1, col2 = st.columns(2)
            with col1:
                min_amount = st.number_input("Minimum amount", value=0.0, step=10.0, key="expense_min_amount")
            with col2:
                if 'amount' in df_expenses.columns:
                    max_expense = float(df_expenses['amount'].max())
                else:
                    max_expense = 1000.0
                max_amount = st.number_input("Maximum amount", value=max_expense, step=10.0, key="expense_max_amount")
            
            if 'amount' in df_expenses_filtered.columns:
                df_expenses_filtered = df_expenses_filtered[
                    (df_expenses_filtered['amount'] >= min_amount) & 
                    (df_expenses_filtered['amount'] <= max_amount)
                ]
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Show data
            st.subheader("Expense Records")
            
            if not df_expenses_filtered.empty:
                # Sort data
                sort_options = df_expenses_filtered.columns.tolist()
                selected_sort = st.selectbox("Sort by", sort_options, index=sort_options.index('date') if 'date' in sort_options else 0)
                sort_order = st.radio("Sort order", ["Descending", "Ascending"], horizontal=True, key="expense_sort_order")
                
                # Apply sorting
                ascending = sort_order == "Ascending"
                df_expenses_filtered = df_expenses_filtered.sort_values(by=selected_sort, ascending=ascending)
                
                # Display the table
                st.dataframe(df_expenses_filtered, use_container_width=True)
                
                # Show summary statistics
                st.subheader("Expense Summary")
                total_expense = df_expenses_filtered['amount'].sum()
                avg_expense = df_expenses_filtered['amount'].mean()
                count = len(df_expenses_filtered)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Expenses", f"${total_expense:.2f}")
                col2.metric("Average Expense", f"${avg_expense:.2f}")
                col3.metric("Number of Entries", count)
                
                # Download data as CSV
                csv = df_expenses_filtered.to_csv(index=False)
                st.download_button(
                    label="Download Filtered Expense Data as CSV",
                    data=csv,
                    file_name="filtered_expense_data.csv",
                    mime="text/csv"
                )
            else:
                st.info("No expense data available for the selected filters.")
        else:
            st.info("No expense data available. Please add your expenses in the 'Add Income/Expense' section.")
    
    # Tab 3: Data Management
    with table_tabs[2]:
        st.subheader("Data Management")
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.warning("Be careful when deleting data. This action cannot be undone.")
        
        # Data management options
        management_option = st.radio(
            "Select an action",
            ["Delete individual entries", "Reset all data"]
        )
        
        if management_option == "Delete individual entries":
            # Select data type to delete
            data_type = st.radio("Select data type", ["Income", "Expense"], horizontal=True)
            
            if data_type == "Income":
                if st.session_state['incomes']:
                    # Display income data with indices
                    df_incomes = pd.DataFrame(st.session_state['incomes'])
                    
                    # Add index column
                    df_incomes_with_idx = df_incomes.copy()
                    df_incomes_with_idx.insert(0, 'ID', range(len(df_incomes_with_idx)))
                    
                    st.dataframe(df_incomes_with_idx, use_container_width=True)
                    
                    # Select ID to delete
                    id_to_delete = st.number_input(
                        "Enter the ID of the income entry to delete",
                        min_value=0,
                        max_value=len(df_incomes_with_idx)-1 if len(df_incomes_with_idx) > 0 else 0,
                        step=1
                    )
                    
                    if st.button("Delete Income Entry"):
                        if 0 <= id_to_delete < len(st.session_state['incomes']):
                            # Delete the entry
                            del st.session_state['incomes'][id_to_delete]
                            save_data(st.session_state['incomes'], incomes_file_path)
                            st.success(f"Income entry with ID {id_to_delete} deleted successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Invalid ID. Please enter a valid ID.")
                else:
                    st.info("No income data available to delete.")
            else:  # Expense
                if st.session_state['expenses']:
                    # Display expense data with indices
                    df_expenses = pd.DataFrame(st.session_state['expenses'])
                    
                    # Add index column
                    df_expenses_with_idx = df_expenses.copy()
                    df_expenses_with_idx.insert(0, 'ID', range(len(df_expenses_with_idx)))
                    
                    st.dataframe(df_expenses_with_idx, use_container_width=True)
                    
                    # Select ID to delete
                    id_to_delete = st.number_input(
                        "Enter the ID of the expense entry to delete",
                        min_value=0,
                        max_value=len(df_expenses_with_idx)-1 if len(df_expenses_with_idx) > 0 else 0,
                        step=1
                    )
                    
                    if st.button("Delete Expense Entry"):
                        if 0 <= id_to_delete < len(st.session_state['expenses']):
                            # Delete the entry
                            del st.session_state['expenses'][id_to_delete]
                            save_data(st.session_state['expenses'], expenses_file_path)
                            st.success(f"Expense entry with ID {id_to_delete} deleted successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Invalid ID. Please enter a valid ID.")
                else:
                    st.info("No expense data available to delete.")
        
        elif management_option == "Reset all data":
            # Reset all data confirmation
            st.error("This will delete ALL of your financial data. This action cannot be undone.")
            
            # Require typing "DELETE" to confirm
            confirm_text = st.text_input("Type 'DELETE' to confirm")
            
            if st.button("Reset All Data"):
                if confirm_text == "DELETE":
                    # Reset all data
                    st.session_state['incomes'] = []
                    st.session_state['expenses'] = []
                    st.session_state['goals'] = []
                    
                    # Save empty data
                    save_data(st.session_state['incomes'], incomes_file_path)
                    save_data(st.session_state['expenses'], expenses_file_path)
                    save_data(st.session_state['goals'], goals_file_path)
                    
                    st.success("All data has been reset successfully!")
                    st.experimental_rerun()
                else:
                    st.warning("Please type 'DELETE' to confirm data reset.")
        
        st.markdown("</div>", unsafe_allow_html=True)