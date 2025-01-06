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
sidebar_image_path = os.path.join(os.path.dirname(__file__), 'images', 'menu.jpg')
main_image_path = os.path.join(os.path.dirname(__file__), 'images', 'main.jpg')

# Sidebar with navigation menu and image
st.sidebar.image(sidebar_image_path, use_container_width=True)
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Add Income/Expense", "View Charts", "View Tables", "Recommendations"])

# Main image
st.image(main_image_path, use_container_width=True)

# GitHub repository button
st.sidebar.markdown("[GitHub Repository](https://github.com/your-repo)")

# Home page
if menu == "Home":
    st.title("Welcome to FINANSMART")
    st.write("Use the navigation menu to manage your finances.")

# Add Income/Expense page
elif menu == "Add Income/Expense":
    st.header("Add Income and Expense")

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
            finance.add_income(amount, description, category)
        else:
            finance.add_expense(amount, description, category)
        st.success(f"{type.capitalize()} added successfully")

# View Charts page
elif menu == "View Charts":
    st.header("Charts")
    df_incomes = pd.DataFrame(finance.incomes)
    df_expenses = pd.DataFrame(finance.expenses)

    fig, ax = plt.subplots(3, 1, figsize=(12, 18))

    if not df_incomes.empty:
        sns.barplot(x="description", y="amount", hue="category", data=df_incomes, ax=ax[0], palette="viridis")
        ax[0].set_title("Incomes")
        ax[0].set_xlabel("Description")
        ax[0].set_ylabel("Amount")
    else:
        ax[0].text(0.5, 0.5, 'No income data available', horizontalalignment='center', verticalalignment='center')
        ax[0].set_title("Incomes")

    if not df_expenses.empty:
        sns.barplot(x="description", y="amount", hue="category", data=df_expenses, ax=ax[1], palette="magma")
        ax[1].set_title("Expenses")
        ax[1].set_xlabel("Description")
        ax[1].set_ylabel("Amount")

        # Pie chart for expenses
        df_expenses_grouped = df_expenses.drop(columns=["date"]).groupby("description").sum()
        ax[2].pie(df_expenses_grouped["amount"], labels=df_expenses_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma", len(df_expenses_grouped)))
        ax[2].set_title("Expense Distribution")
    else:
        ax[1].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
        ax[1].set_title("Expenses")
        ax[2].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
        ax[2].set_title("Expense Distribution")

    st.pyplot(fig)

# View Tables page
elif menu == "View Tables":
    st.header("Income and Expense Tables")
    df_incomes = pd.DataFrame(finance.incomes)
    df_expenses = pd.DataFrame(finance.expenses)
    st.subheader("Incomes")
    st.dataframe(df_incomes)
    st.subheader("Expenses")
    st.dataframe(df_expenses)

# Recommendations page
elif menu == "Recommendations":
    st.header("Recommendations")
    recommendations = finance.generate_recommendations()
    for recommendation in recommendations:
        st.write(f"- {recommendation}")