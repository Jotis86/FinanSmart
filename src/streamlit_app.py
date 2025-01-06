import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from main import Finance
import os

# Initialize the Finance class
finance = Finance()

# Define paths for images
sidebar_image_path = os.path.join(os.path.dirname(__file__), 'menu.jpg')
main_image_path = os.path.join(os.path.dirname(__file__), 'main.jpg')

# File paths for storing data
incomes_file_path = os.path.join(os.path.dirname(__file__), 'incomes.csv')
expenses_file_path = os.path.join(os.path.dirname(__file__), 'expenses.csv')


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

# Load data into session state
if 'incomes' not in st.session_state:
    st.session_state['incomes'] = load_data(incomes_file_path)

if 'expenses' not in st.session_state:
    st.session_state['expenses'] = load_data(expenses_file_path)

# Sidebar with navigation menu and image
st.sidebar.image(sidebar_image_path, use_container_width=True)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Add Income/Expense", "View Charts", "View Tables", "Recommendations", "Acknowledgements"])

# Main image
st.image(main_image_path, use_container_width=True)

# GitHub repository button
st.sidebar.markdown("""
<a href="https://github.com/Jotis86/FinanSmart" target="_blank">
    <button style="background-color: #000000; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        GitHub Repository
    </button>
</a>
""", unsafe_allow_html=True)

# Add space between GitHub button and LinkedIn button
st.sidebar.write("")
st.sidebar.write("")

# LinkedIn profile button
st.sidebar.markdown("""
<a href="https://www.linkedin.com/in/juan-duran-bon" target="_blank">
    <button style="background-color: #0077B5; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        LinkedIn Profile
    </button>
</a>
""", unsafe_allow_html=True)

# Add space between GitHub button and LinkedIn button
st.sidebar.write("")
st.sidebar.write("")

# Website Jotis button
st.sidebar.markdown("""
<a href="https://jotis86.github.io/Website/" target="_blank">
    <button style="background-color: #8A2BE2; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Juan Duran Website
    </button>
</a>
""", unsafe_allow_html=True)


# Home page
if menu == "Home":
    st.title("Welcome to FINANSMART")
    st.write("""
    **FINANSMART** is a comprehensive financial management application designed to help you track your income and expenses, visualize your financial data, and receive personalized recommendations to improve your financial health.

    ### Features:
    - **Add Income and Expenses** 💰: Easily add your income and expenses with predefined categories and descriptions.
    - **View Charts** 📊: Visualize your financial data with bar charts and pie charts to understand your income and expense distribution.
    - **View Tables** 📋: See detailed tables of your income and expenses for better analysis.
    - **Recommendations** 💡: Get personalized recommendations based on your financial data to help you save more and spend wisely.
    - **User-Friendly Interface** 🖥️: Navigate through the application with ease using the intuitive interface.
    - **Data Security** 🔒: Your financial data is securely stored and managed.

    ### How to Use:
    1. **Navigate** 🧭: Use the navigation menu on the left to switch between different sections of the application.
    2. **Add Data** ✍️: Go to the "Add Income/Expense" section to input your financial data.
    3. **Visualize Data** 👁️: Visit the "View Charts" section to see visual representations of your financial data.
    4. **Analyze Data** 🔍: Check the "View Tables" section for detailed tables of your income and expenses.
    5. **Get Recommendations** 📈: Head to the "Recommendations" section to receive personalized financial advice.

    ### Benefits:
    - **Track Your Finances** 📒: Keep a detailed record of your income and expenses.
    - **Understand Your Spending** 💸: Visualize where your money is going with easy-to-understand charts.
    - **Improve Financial Health** 🏦: Receive actionable recommendations to improve your savings and reduce unnecessary expenses.
    - **Make Informed Decisions** 🧠: Use the insights from the data to make better financial decisions.

    Start managing your finances smarter with **FINANSMART**! 🚀
    """)

# Add Income/Expense page
elif menu == "Add Income/Expense":
    st.header("Add Income and Expense 💰")
    st.write("""
    In this section, you can add your income and expenses. Select the type, category, and description, then enter the amount. This will help you keep track of your financial transactions.
    """)

    income_categories = ["Salary", "Bonus", "Investment", "Other"]
    expense_categories = ["Food", "Transportation", "Housing", "Entertainment", "Health", "Education", "Utilities", "Insurance", "Debt", "Savings", "Gifts", "Travel", "Other"]
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

    type = st.selectbox("Select type", ["income", "expense"])
    amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")

    if type == "income":
        category = st.selectbox("Select category", income_categories)
    else:
        category = st.selectbox("Select category", expense_categories)

    description = st.selectbox("Select description", descriptions[category])

    if st.button("Add"):
        if type == "income":
            st.session_state['incomes'].append({'amount': amount, 'description': description, 'category': category})
            save_data(st.session_state['incomes'], incomes_file_path)
        else:
            st.session_state['expenses'].append({'amount': amount, 'description': description, 'category': category})
            save_data(st.session_state['expenses'], expenses_file_path)
        st.success(f"{type.capitalize()} added successfully")

# View Charts page
elif menu == "View Charts":
    st.header("Charts 📊")
    st.write("""
    In this section, you can visualize your financial data with bar charts and pie charts. This will help you understand your income and expense distribution.
    """)

    df_incomes = pd.DataFrame(st.session_state['incomes'])
    df_expenses = pd.DataFrame(st.session_state['expenses'])

    fig, ax = plt.subplots(4, 1, figsize=(12, 24))

    if not df_incomes.empty:
        sns.barplot(x="description", y="amount", hue="category", data=df_incomes, ax=ax[0], palette="viridis")
        ax[0].set_title("Incomes")
        ax[0].set_xlabel("Description")
        ax[0].set_ylabel("Amount")

        # Pie chart for incomes
        df_incomes_grouped = df_incomes.groupby("description").sum()
        ax[1].pie(df_incomes_grouped["amount"], labels=df_incomes_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis", len(df_incomes_grouped)))
        ax[1].set_title("Income Distribution")
    else:
        ax[0].text(0.5, 0.5, 'No income data available', horizontalalignment='center', verticalalignment='center')
        ax[0].set_title("Incomes")
        ax[1].text(0.5, 0.5, 'No income data available', horizontalalignment='center', verticalalignment='center')
        ax[1].set_title("Income Distribution")

    if not df_expenses.empty:
        sns.barplot(x="description", y="amount", hue="category", data=df_expenses, ax=ax[2], palette="magma")
        ax[2].set_title("Expenses")
        ax[2].set_xlabel("Description")
        ax[2].set_ylabel("Amount")

        # Pie chart for expenses
        df_expenses_grouped = df_expenses.groupby("description").sum()
        ax[3].pie(df_expenses_grouped["amount"], labels=df_expenses_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma", len(df_expenses_grouped)))
        ax[3].set_title("Expense Distribution")
    else:
        ax[2].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
        ax[2].set_title("Expenses")
        ax[3].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
        ax[3].set_title("Expense Distribution")

    st.pyplot(fig)

# View Tables page
elif menu == "View Tables":
    st.header("Income and Expense Tables 📋")
    st.write("""
    In this section, you can see detailed tables of your income and expenses. This will help you analyze your financial data more effectively.
    """)

    # Botón para resetear los datos
    if st.button("Reset All Data"):
        st.session_state['incomes'] = []
        st.session_state['expenses'] = []
        save_data(st.session_state['incomes'], incomes_file_path)
        save_data(st.session_state['expenses'], expenses_file_path)
        

    # Seleccionar y borrar ingreso
    st.subheader("Delete Income")
    if st.session_state['incomes']:
        income_index = st.number_input("Enter the index of the income to delete", min_value=0, max_value=len(st.session_state['incomes'])-1, step=1)
        if st.button("Delete Income"):
            if 0 <= income_index < len(st.session_state['incomes']):
                st.session_state['incomes'].pop(income_index)
                save_data(st.session_state['incomes'], incomes_file_path)
                st.success("Income deleted successfully")
                
    else:
        st.write("No incomes to delete.")

    # Seleccionar y borrar gasto
    st.subheader("Delete Expense")
    if st.session_state['expenses']:
        expense_index = st.number_input("Enter the index of the expense to delete", min_value=0, max_value=len(st.session_state['expenses'])-1, step=1)
        if st.button("Delete Expense"):
            if 0 <= expense_index < len(st.session_state['expenses']):
                st.session_state['expenses'].pop(expense_index)
                save_data(st.session_state['expenses'], expenses_file_path)
                st.success("Expense deleted successfully")
                
    else:
        st.write("No expenses to delete.")

    # Crear DataFrames después de las operaciones de eliminación
    df_incomes = pd.DataFrame(st.session_state['incomes'])
    df_expenses = pd.DataFrame(st.session_state['expenses'])

    st.subheader("Incomes")
    st.dataframe(df_incomes)
    st.subheader("Expenses")
    st.dataframe(df_expenses)

    # Función para convertir DataFrame a CSV
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    # Botón para descargar CSV de ingresos
    st.download_button(
        label="Download Incomes as CSV",
        data=convert_df_to_csv(df_incomes),
        file_name='incomes.csv',
        mime='text/csv'
    )

    # Botón para descargar CSV de gastos
    st.download_button(
        label="Download Expenses as CSV",
        data=convert_df_to_csv(df_expenses),
        file_name='expenses.csv',
        mime='text/csv'
    )

# Recommendations page
elif menu == "Recommendations":
    st.header("Recommendations 💡")
    st.write("""
    In this section, you can get personalized recommendations based on your financial data to help you save more and spend wisely.
    """)

    # Load data from CSV files
    incomes = load_data(incomes_file_path)
    expenses = load_data(expenses_file_path)

    if st.button("Get Recommendations"):
        if not incomes and not expenses:
            st.write("No data available to generate recommendations. Please add your income and expenses.")
        else:
            finance = Finance()
            finance.incomes = incomes
            finance.expenses = expenses
            recommendations = finance.generate_recommendations()
            for recommendation in recommendations:
                st.write(f"- {recommendation}")

# Acknowledgements page
elif menu == "Acknowledgements":
    st.header("Acknowledgements 🙏")
    st.write("""
    We would like to thank the following individuals and organizations for their contributions and support:
    
    - **Streamlit**: For providing an amazing framework to build interactive web applications.
    - **Pandas**: For making data manipulation and analysis easy and efficient.
    - **Seaborn**: For creating beautiful and informative visualizations.
    - **Matplotlib**: For being the backbone of data visualization in Python.
    - **GitHub**: For hosting our code and enabling collaboration.
    - **Our Users**: For their valuable feedback and support.

    Thank you for using **FINANSMART**! We hope it helps you manage your finances better.
    """)

    # Add space between text and image
    st.write("")
    st.write("")
    st.write("")    

    # Add an image to the acknowledgements section and center it
    acknowledgements_image_path = os.path.join(os.path.dirname(__file__), 'Jotis.png')
    st.image(acknowledgements_image_path, width=200)

    # Add text below the image
    st.markdown("""
        <div style="text-align: left; margin-top: 20px;">
            <h3>Coding, Gaming, and Leveling Up</h3>
        </div>
    """, unsafe_allow_html=True)