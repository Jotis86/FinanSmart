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
                            st.rerun()
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

# Financial Goals page
elif menu == "Financial Goals":
    st.markdown("<h1 class='main-header'>Financial Goals</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Set and track your financial goals here. Setting specific goals can help you stay motivated
    and focused on your financial journey.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for different goal actions
    goals_tabs = st.tabs(["My Goals", "Add New Goal", "Goal Progress"])
    
    # Tab 1: View Goals
    with goals_tabs[0]:
        st.subheader("My Financial Goals")
        
        if st.session_state['goals']:
            # Convert to DataFrame for display
            df_goals = pd.DataFrame(st.session_state['goals'])
            
            # Calculate progress for each goal
            for i, goal in enumerate(st.session_state['goals']):
                if goal.get('category') == 'saving':
                    # For saving goals, calculate based on income with Savings category
                    current_savings = sum(
                        item["amount"] for item in st.session_state['incomes'] 
                        if item.get("category") == "Savings"
                    )
                    progress = min(100, max(0, (current_savings / goal.get('target_amount', 1)) * 100))
                elif goal.get('category') == 'expense_reduction':
                    # For expense reduction goals, calculate how close we are to the target
                    category = goal.get('subcategory', '')
                    current_expense = sum(
                        item["amount"] for item in st.session_state['expenses'] 
                        if item.get("category") == category
                    )
                    progress = min(100, max(0, 100 - (current_expense / goal.get('target_amount', 1)) * 100))
                else:
                    # Generic goals - just use stored progress if available
                    progress = goal.get('progress', 0)
                
                # Update progress in the session state
                st.session_state['goals'][i]['progress'] = progress
            
            # Save updated goals
            save_data(st.session_state['goals'], goals_file_path)
            
            # Display goals as cards
            for i, goal in enumerate(st.session_state['goals']):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader(goal.get('name', 'Unnamed Goal'))
                    
                    # Show goal details
                    st.write(f"**Target:** ${goal.get('target_amount', 0):.2f}")
                    st.write(f"**Deadline:** {goal.get('deadline', 'No deadline')}")
                    st.write(f"**Category:** {goal.get('category', 'General')}")
                    
                    # Calculate days remaining
                    try:
                        deadline_date = datetime.strptime(goal.get('deadline', '2099-12-31'), "%Y-%m-%d")
                        days_remaining = (deadline_date - datetime.now()).days
                        
                        if days_remaining > 0:
                            st.write(f"**Days remaining:** {days_remaining}")
                        else:
                            st.write("**Status:** Goal deadline has passed")
                    except:
                        st.write("**Deadline format:** Invalid")
                    
                    # Show progress bar
                    progress = goal.get('progress', 0)
                    st.progress(progress / 100)
                    st.write(f"**Progress:** {progress:.1f}%")
                    
                    # Delete button
                    if st.button(f"Delete Goal {i+1}"):
                        st.session_state['goals'].pop(i)
                        save_data(st.session_state['goals'], goals_file_path)
                        st.success(f"Goal '{goal.get('name')}' deleted successfully!")
                        st.rerun()  # Use st.rerun() instead of experimental_rerun
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    # Visualize progress with a small chart
                    fig, ax = plt.subplots(figsize=(3, 3))
                    
                    # Create a simple gauge chart
                    progress = goal.get('progress', 0)
                    colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
                    color_idx = min(int(progress / 20), 4)
                    
                    ax.pie([progress, 100-progress], 
                          colors=[colors[color_idx], '#f0f0f0'],
                          startangle=90, 
                          counterclock=False)
                    
                    # Add a circle in the center to make it look like a gauge
                    circle = plt.Circle((0, 0), 0.7, fc='white')
                    ax.add_artist(circle)
                    
                    # Add text in center
                    ax.text(0, 0, f"{progress:.1f}%", 
                           ha='center', va='center', 
                           fontsize=12, fontweight='bold')
                    
                    ax.set_title(f"Goal Progress")
                    ax.axis('equal')
                    st.pyplot(fig)
        else:
            st.info("You don't have any financial goals yet. Create one in the 'Add New Goal' tab.")
    
    # Tab 2: Add New Goal
    with goals_tabs[1]:
        st.subheader("Create a New Financial Goal")
        
        with st.form("new_goal_form"):
            # Basic goal information
            goal_name = st.text_input("Goal Name")
            goal_amount = st.number_input("Target Amount ($)", min_value=1.0, step=100.0)
            goal_deadline = st.date_input("Deadline", min_value=datetime.now().date())
            
            # Goal category
            goal_category = st.selectbox(
                "Goal Category",
                ["saving", "expense_reduction", "debt_payoff", "income_increase", "other"]
            )
            
            # Additional fields based on category
            if goal_category == "expense_reduction":
                # For expense reduction, select which expense category to reduce
                expense_categories = ["Food", "Transportation", "Housing", "Entertainment", "Health", 
                                     "Education", "Utilities", "Insurance", "Debt", "Travel", "Other"]
                subcategory = st.selectbox("Expense Category to Reduce", expense_categories)
            else:
                subcategory = ""
            
            # Notes
            goal_notes = st.text_area("Notes (optional)")
            
            # Submit button
            submitted = st.form_submit_button("Create Goal")
            
            if submitted:
                if goal_name and goal_amount > 0:
                    # Create new goal
                    new_goal = {
                        "name": goal_name,
                        "target_amount": goal_amount,
                        "deadline": goal_deadline.strftime("%Y-%m-%d"),
                        "category": goal_category,
                        "subcategory": subcategory,
                        "notes": goal_notes,
                        "created_date": datetime.now().strftime("%Y-%m-%d"),
                        "progress": 0
                    }
                    
                    # Add to session state and save
                    st.session_state['goals'].append(new_goal)
                    save_data(st.session_state['goals'], goals_file_path)
                    
                    st.success(f"Goal '{goal_name}' created successfully!")
                else:
                    st.error("Please provide a name and a valid target amount for your goal.")
    
    # Tab 3: Goal Progress
    with goals_tabs[2]:
        st.subheader("Goal Progress Tracking")
        
        if st.session_state['goals']:
            # Allow user to select a goal to update manually
            goal_names = [goal.get('name', f"Goal {i+1}") for i, goal in enumerate(st.session_state['goals'])]
            selected_goal_idx = st.selectbox("Select a goal to update", range(len(goal_names)), format_func=lambda x: goal_names[x])
            
            selected_goal = st.session_state['goals'][selected_goal_idx]
            
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader(selected_goal.get('name', 'Unnamed Goal'))
            
            # Show current progress
            current_progress = selected_goal.get('progress', 0)
            st.write(f"Current progress: {current_progress:.1f}%")
            
            # Allow manual progress update
            new_progress = st.slider(
                "Update progress", 
                min_value=0.0, 
                max_value=100.0, 
                value=float(current_progress),
                step=1.0
            )
            
            # Add notes about the progress update
            progress_notes = st.text_area("Progress notes (optional)")
            
            if st.button("Update Progress"):
                # Update the goal's progress
                st.session_state['goals'][selected_goal_idx]['progress'] = new_progress
                
                # Add notes if provided
                if progress_notes:
                    if 'progress_history' not in st.session_state['goals'][selected_goal_idx]:
                        st.session_state['goals'][selected_goal_idx]['progress_history'] = []
                    
                    st.session_state['goals'][selected_goal_idx]['progress_history'].append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "progress": new_progress,
                        "notes": progress_notes
                    })
                
                # Save updated goals
                save_data(st.session_state['goals'], goals_file_path)
                
                st.success(f"Progress for '{selected_goal.get('name')}' updated successfully!")
            
            # Show progress history if available
            if 'progress_history' in selected_goal and selected_goal['progress_history']:
                st.subheader("Progress History")
                
                history = selected_goal['progress_history']
                
                # Create a DataFrame for display
                df_history = pd.DataFrame(history)
                st.dataframe(df_history, use_container_width=True)
                
                # Visualize progress over time if there are multiple entries
                if len(history) > 1:
                    fig, ax = plt.subplots(figsize=(10, 5))
                    
                    # Convert dates to datetime for proper sorting
                    df_history['date'] = pd.to_datetime(df_history['date'])
                    df_history = df_history.sort_values('date')
                    
                    ax.plot(df_history['date'], df_history['progress'], marker='o', linestyle='-')
                    ax.set_title('Goal Progress Over Time')
                    ax.set_xlabel('Date')
                    ax.set_ylabel('Progress (%)')
                    ax.grid(True, linestyle='--', alpha=0.7)
                    
                    # Rotate x-axis labels for better readability
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    
                    st.pyplot(fig)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("You don't have any financial goals yet. Create one in the 'Add New Goal' tab.")

# Recommendations page
elif menu == "Recommendations":
    st.markdown("<h1 class='main-header'>Financial Recommendations</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Get personalized financial recommendations based on your income and expense data. 
    These insights can help you improve your financial health and make better financial decisions.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Load data into finance class for analysis
    finance.incomes = st.session_state['incomes']
    finance.expenses = st.session_state['expenses']
    
    if st.button("Generate Recommendations"):
        # Check if there's data available
        if not finance.incomes and not finance.expenses:
            st.warning("No financial data available to generate recommendations. Please add your income and expenses first.")
        else:
            # Get recommendations
            recommendations = finance.generate_recommendations()
            
            if recommendations:
                # Create some analytics for display
                total_income = sum(item["amount"] for item in finance.incomes)
                total_expense = sum(item["amount"] for item in finance.expenses)
                balance = total_income - total_expense
                
                # Financial health score (simple calculation)
                if total_income > 0:
                    savings_rate = max(0, balance) / total_income * 100
                    debt_payments = sum(item["amount"] for item in finance.expenses if item.get("category") == "Debt")
                    debt_ratio = (debt_payments / total_income * 100) if total_income > 0 else 0
                    
                    # Score based on savings rate and debt ratio
                    # Higher savings rate is good, lower debt ratio is good
                    financial_health = min(100, max(0, 50 + (savings_rate/2) - (debt_ratio/10)))
                else:
                    financial_health = 0
                
                # Display financial health score
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Your Financial Health Score")
                
                # Determine score color and status
                if financial_health >= 80:
                    score_color = "green"
                    status = "Excellent"
                elif financial_health >= 60:
                    score_color = "blue"
                    status = "Good"
                elif financial_health >= 40:
                    score_color = "orange"
                    status = "Fair"
                else:
                    score_color = "red"
                    status = "Needs Improvement"
                
                # Display score as a gauge chart
                fig, ax = plt.subplots(figsize=(6, 3))
                
                # Create gauge chart using a partial pie chart
                gauge_colors = ['red', 'orange', 'yellow', 'lightgreen', 'green']
                background = ax.pie([1], 
                                   radius=1, 
                                   colors=['lightgrey'], 
                                   startangle=90, 
                                   counterclock=False, 
                                   wedgeprops=dict(width=0.2, edgecolor='white'))[0]
                
                # Add colored progress arc
                progress_arc = ax.pie([financial_health, 100-financial_health], 
                                     radius=1, 
                                     colors=[score_color, 'white'], 
                                     startangle=90, 
                                     counterclock=False, 
                                     wedgeprops=dict(width=0.2, edgecolor='white'))[0]
                
                # Add a circle in the center to make it look like a gauge
                center_circle = plt.Circle((0, 0), 0.7, fc='white')
                ax.add_artist(center_circle)
                
                # Add score text in center
                ax.text(0, 0, f"{financial_health:.0f}", 
                       ha='center', va='center', 
                       fontsize=24, fontweight='bold', color=score_color)
                
                ax.text(0, -0.2, status, 
                       ha='center', va='center', 
                       fontsize=12, color=score_color)
                
                ax.set_aspect('equal')
                ax.axis('off')
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.pyplot(fig)
                
                with col2:
                    st.write(f"**Status:** {status}")
                    
                    if total_income > 0:
                        st.write(f"**Savings Rate:** {savings_rate:.1f}% of income")
                        
                    if debt_payments > 0:
                        st.write(f"**Debt-to-Income Ratio:** {debt_ratio:.1f}%")
                    
                    st.write("""
                    Your financial health score is calculated based on several factors including your savings rate,
                    debt-to-income ratio, and overall balance between income and expenses.
                    """)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Display recommendations
                st.markdown("<h2 class='sub-header'>Personalized Recommendations</h2>", unsafe_allow_html=True)
                
                for i, recommendation in enumerate(recommendations):
                    st.markdown(
                        f"<div class='card' style='margin-bottom: 10px;'><b>{i+1}.</b> {recommendation}</div>", 
                        unsafe_allow_html=True
                    )
                
                # Additional insights
                if total_expense > 0:
                    st.markdown("<h2 class='sub-header'>Spending Insights</h2>", unsafe_allow_html=True)
                    
                    # Convert to DataFrame for analysis
                    df_expenses = pd.DataFrame(finance.expenses)
                    
                    if not df_expenses.empty and 'category' in df_expenses.columns:
                        # Analyze by category
                        category_totals = df_expenses.groupby('category')['amount'].sum().reset_index()
                        category_totals['percentage'] = category_totals['amount'] / total_expense * 100
                        top_categories = category_totals.sort_values('amount', ascending=False).head(3)
                        
                        # Display top spending categories
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.subheader("Top Spending Categories")
                        
                        fig, ax = plt.subplots(figsize=(8, 5))
                        
                        # Create horizontal bar chart of top categories
                        bars = ax.barh(
                            top_categories['category'], 
                            top_categories['percentage'], 
                            color=sns.color_palette("viridis", len(top_categories))
                        )
                        
                        # Add percentage labels
                        for i, bar in enumerate(bars):
                            width = bar.get_width()
                            ax.text(
                                width + 1, 
                                bar.get_y() + bar.get_height()/2, 
                                f"{width:.1f}%", 
                                ha='left', 
                                va='center'
                            )
                        
                        ax.set_xlabel('Percentage of Total Expenses')
                        ax.set_title('Where Your Money Goes')
                        ax.set_xlim(0, 100)
                        
                        st.pyplot(fig)
                        
                        # Add spending advice based on top categories
                        for _, row in top_categories.iterrows():
                            category = row['category']
                            percentage = row['percentage']
                            
                            if category == "Food" and percentage > 20:
                                st.write("🍔 **Food Spending:** Consider meal planning and cooking at home more often to reduce food expenses.")
                            elif category == "Housing" and percentage > 40:
                                st.write("🏠 **Housing Costs:** Your housing costs are high relative to your expenses. Consider if there are ways to reduce this major expense.")
                            elif category == "Entertainment" and percentage > 15:
                                st.write("🎭 **Entertainment:** Look for free or low-cost entertainment options to reduce spending in this area.")
                            elif category == "Transportation" and percentage > 15:
                                st.write("🚗 **Transportation:** Consider carpooling, public transit, or other alternatives to reduce transportation costs.")
                            elif category == "Shopping" and percentage > 10:
                                st.write("🛍️ **Shopping:** Try implementing a 24-hour rule before making non-essential purchases to reduce impulse buying.")
                            else:
                                st.write(f"💰 **{category}:** This is one of your top spending categories at {percentage:.1f}% of expenses.")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Unable to generate recommendations with the current data.")
    else:
        st.info("Click the button above to generate personalized financial recommendations.")



# Export Data page
elif menu == "Export Data":
    st.markdown("<h1 class='main-header'>Export Your Financial Data</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Export your financial data in different formats for backup or external analysis. 
    This allows you to keep a secure copy of your data or use it in other applications.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Options for what to export
    st.subheader("Select Data to Export")
    export_incomes = st.checkbox("Income Data", value=True)
    export_expenses = st.checkbox("Expense Data", value=True)
    export_goals = st.checkbox("Financial Goals", value=True)
    
    # Format options
    export_format = st.radio("Export Format", ["CSV", "Excel"], horizontal=True)
    
    # Prepare data for export
    if st.button("Generate Export Files"):
        has_data = False
        
        if export_incomes and st.session_state['incomes']:
            df_incomes = pd.DataFrame(st.session_state['incomes'])
            has_data = True
        else:
            df_incomes = pd.DataFrame()
        
        if export_expenses and st.session_state['expenses']:
            df_expenses = pd.DataFrame(st.session_state['expenses'])
            has_data = True
        else:
            df_expenses = pd.DataFrame()
        
        if export_goals and st.session_state['goals']:
            df_goals = pd.DataFrame(st.session_state['goals'])
            has_data = True
        else:
            df_goals = pd.DataFrame()
        
        if has_data:
            if export_format == "Excel":
                # Export to Excel
                excel_file = to_excel({
                    'Incomes': df_incomes if export_incomes else pd.DataFrame(),
                    'Expenses': df_expenses if export_expenses else pd.DataFrame(),
                    'Goals': df_goals if export_goals else pd.DataFrame()
                })
                
                filename = f"finansmart_data_{datetime.now().strftime('%Y%m%d')}.xlsx"
                
                st.download_button(
                    label="Download Excel File",
                    data=excel_file,
                    file_name=filename,
                    mime="application/vnd.ms-excel"
                )
            else:
                # Export as individual CSV files
                st.subheader("Download CSV Files")
                
                if export_incomes and not df_incomes.empty:
                    csv_incomes = df_incomes.to_csv(index=False)
                    st.download_button(
                        label="Download Income Data CSV",
                        data=csv_incomes,
                        file_name=f"finansmart_incomes_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                if export_expenses and not df_expenses.empty:
                    csv_expenses = df_expenses.to_csv(index=False)
                    st.download_button(
                        label="Download Expense Data CSV",
                        data=csv_expenses,
                        file_name=f"finansmart_expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                if export_goals and not df_goals.empty:
                    csv_goals = df_goals.to_csv(index=False)
                    st.download_button(
                        label="Download Goals CSV",
                        data=csv_goals,
                        file_name=f"finansmart_goals_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
        else:
            st.warning("No data selected for export or data is empty.")
    
    # Data Import section
    st.markdown("<h2 class='sub-header' style='margin-top: 30px;'>Import Data</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Import previously exported data or data from other sources. 
    Note: This will replace your current data for the selected categories.
    """)
    
    import_type = st.radio("What data would you like to import?", ["Incomes", "Expenses", "Goals"])
    uploaded_file = st.file_uploader(f"Upload {import_type} CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read the uploaded CSV
            imported_df = pd.read_csv(uploaded_file)
            
            # Show preview of imported data
            st.subheader("Data Preview")
            st.dataframe(imported_df.head())
            
            # Confirm import
            if st.button(f"Import {import_type} Data"):
                # Convert to list of dictionaries
                imported_data = imported_df.to_dict('records')
                
                # Update session state based on import type
                if import_type == "Incomes":
                    st.session_state['incomes'] = imported_data
                    save_data(st.session_state['incomes'], incomes_file_path)
                elif import_type == "Expenses":
                    st.session_state['expenses'] = imported_data
                    save_data(st.session_state['expenses'], expenses_file_path)
                else:  # Goals
                    st.session_state['goals'] = imported_data
                    save_data(st.session_state['goals'], goals_file_path)
                
                st.success(f"{import_type} data imported successfully!")
                st.rerun()
                
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Settings page
elif menu == "Settings":
    st.markdown("<h1 class='main-header'>Application Settings</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("""
    Customize your FINANSMART experience by adjusting various settings.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create settings tabs
    settings_tabs = st.tabs(["Appearance", "Categories", "Notifications", "About"])
    
    # Appearance Settings
    with settings_tabs[0]:
        st.subheader("Appearance Settings")
        
        # Dark mode toggle
        dark_mode = st.checkbox("Dark Mode", value=st.session_state['dark_mode'])
        if dark_mode != st.session_state['dark_mode']:
            st.session_state['dark_mode'] = dark_mode
            st.rerun()
        
        # Currency format
        st.subheader("Currency Format")
        currency_symbol = st.selectbox(
            "Currency Symbol",
            ["$", "€", "£", "¥", "₹", "₽", "₩", "C$", "A$", "Other"],
            index=0
        )
        
        if currency_symbol == "Other":
            custom_symbol = st.text_input("Enter custom currency symbol")
            if custom_symbol:
                currency_symbol = custom_symbol
        
        st.session_state['currency_symbol'] = currency_symbol
        
        # Date format
        st.subheader("Date Format")
        date_format = st.selectbox(
            "Date Format",
            ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY", "Month DD, YYYY"],
            index=0
        )
        
        st.session_state['date_format'] = date_format
        
        # Chart colors
        st.subheader("Chart Color Scheme")
        color_scheme = st.selectbox(
            "Default Color Scheme for Charts",
            ["viridis", "plasma", "inferno", "magma", "cividis", "blues", "greens", "reds", "purples", "oranges"],
            index=0
        )
        
        st.session_state['color_scheme'] = color_scheme
        
        # Preview the color scheme
        fig, ax = plt.subplots(figsize=(8, 2))
        colors = sns.color_palette(color_scheme, 10)
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{color_scheme.capitalize()} Color Scheme")
        st.pyplot(fig)
    
    # Categories Settings
    with settings_tabs[1]:
        st.subheader("Customize Categories")
        
        # Income categories
        st.subheader("Income Categories")
        default_income_categories = ["Salary", "Bonus", "Investment", "Other"]
        
        if "custom_income_categories" not in st.session_state:
            st.session_state['custom_income_categories'] = default_income_categories.copy()
        
        # Show current categories and allow editing
        st.write("Current Income Categories:")
        categories_text = st.text_area(
            "Edit Income Categories (one per line)",
            value="\n".join(st.session_state['custom_income_categories']),
            height=150
        )
        
        # Save button for income categories
        if st.button("Save Income Categories"):
            new_categories = [cat.strip() for cat in categories_text.split("\n") if cat.strip()]
            if new_categories:
                st.session_state['custom_income_categories'] = new_categories
                st.success("Income categories updated successfully!")
            else:
                st.error("Please provide at least one category.")
        
        # Reset to default button
        if st.button("Reset Income Categories to Default"):
            st.session_state['custom_income_categories'] = default_income_categories.copy()
            st.success("Income categories reset to defaults!")
            st.rerun()
        
        # Expense categories
        st.subheader("Expense Categories")
        default_expense_categories = [
            "Food", "Transportation", "Housing", "Entertainment", "Health", 
            "Education", "Utilities", "Insurance", "Debt", "Savings", "Gifts", 
            "Travel", "Other"
        ]
        
        if "custom_expense_categories" not in st.session_state:
            st.session_state['custom_expense_categories'] = default_expense_categories.copy()
        
        # Show current categories and allow editing
        st.write("Current Expense Categories:")
        expense_categories_text = st.text_area(
            "Edit Expense Categories (one per line)",
            value="\n".join(st.session_state['custom_expense_categories']),
            height=200
        )
        
        # Save button for expense categories
        if st.button("Save Expense Categories"):
            new_categories = [cat.strip() for cat in expense_categories_text.split("\n") if cat.strip()]
            if new_categories:
                st.session_state['custom_expense_categories'] = new_categories
                st.success("Expense categories updated successfully!")
            else:
                st.error("Please provide at least one category.")
        
        # Reset to default button
        if st.button("Reset Expense Categories to Default"):
            st.session_state['custom_expense_categories'] = default_expense_categories.copy()
            st.success("Expense categories reset to defaults!")
            st.rerun()
    
    # Notifications Settings
    with settings_tabs[2]:
        st.subheader("Notification Settings")
        
        st.info("Notification settings are currently in development. This feature will be available in a future update.")
        
        # Placeholder for future notification settings
        st.checkbox("Enable email notifications", value=False, disabled=True)
        st.checkbox("Send monthly summary reports", value=False, disabled=True)
        st.checkbox("Alert when expenses exceed budget", value=False, disabled=True)
        st.checkbox("Remind about upcoming bill payments", value=False, disabled=True)
        
        st.text_input("Email address for notifications", disabled=True)
    
    # About Settings
    with settings_tabs[3]:
        st.subheader("About FINANSMART")
        
        st.markdown("""
        **FINANSMART** is a comprehensive financial management application designed to help you track your income and expenses, 
        visualize your financial data, and receive personalized recommendations to improve your financial health.
        
        **Version:** 1.0.0
        
        **Created by:** Juan Duran
        
        **GitHub Repository:** [github.com/Jotis86/FinanSmart](https://github.com/Jotis86/FinanSmart)
        
        **License:** MIT License
        """)
        
        st.subheader("System Information")
        
        # Display basic system info
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Python Version:** 3.x")
            st.write(f"**Streamlit Version:** {st.__version__}")
            st.write(f"**Pandas Version:** {pd.__version__}")
        
        with col2:
            st.write(f"**Matplotlib Version:** {plt.matplotlib.__version__}")
            st.write(f"**Seaborn Version:** {sns.__version__}")
            st.write(f"**NumPy Version:** {np.__version__}")