import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from main import Finance

# Inicializar la clase Finance
finance = Finance()

# Título de la aplicación
st.title("FINANSMART")

# Sección para agregar ingresos y gastos
st.header("Agregar Ingresos y Gastos")

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

type = st.selectbox("Selecciona el tipo", ["income", "expense"])
amount = st.number_input("Introduce el monto", min_value=0.0, format="%.2f")

if type == "income":
    category = st.selectbox("Selecciona una categoría", income_categories)
else:
    category = st.selectbox("Selecciona una categoría", expense_categories)

description = st.selectbox("Selecciona una descripción", descriptions[category])

if st.button("Agregar"):
    if type == "income":
        finance.add_income(amount, description, category)
    else:
        finance.add_expense(amount, description, category)
    st.success(f"{type.capitalize()} agregado exitosamente")

# Mostrar balance
balance = finance.calculate_balance()
st.header(f"Tu balance mensual es: {balance}")

# Generar gráficos
st.header("Gráficos")
df_incomes = pd.DataFrame(finance.incomes)
df_expenses = pd.DataFrame(finance.expenses)

fig, ax = plt.subplots(4, 1, figsize=(12, 24))

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

    # Pie chart para los gastos
    df_expenses_grouped = df_expenses.drop(columns=["date"]).groupby("description").sum()
    ax[2].pie(df_expenses_grouped["amount"], labels=df_expenses_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma", len(df_expenses_grouped)))
    ax[2].set_title("Distribución de Gastos")

    # Gráfico de líneas para la evolución de los gastos
    df_expenses['date'] = pd.to_datetime(df_expenses['date'])
    df_expenses['month_year'] = df_expenses['date'].dt.to_period('M').astype(str)
    df_expenses_grouped_monthly = df_expenses.groupby(['month_year', 'category'])['amount'].sum().reset_index()
    sns.lineplot(x='month_year', y='amount', hue='category', data=df_expenses_grouped_monthly, ax=ax[3], palette="magma", marker='o')
    ax[3].set_title("Evolución de los Gastos Mensuales")
    ax[3].set_xlabel("Mes-Año")
    ax[3].set_ylabel("Monto")
    ax[3].set_xticklabels(df_expenses_grouped_monthly['month_year'], rotation=45)
else:
    ax[1].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
    ax[1].set_title("Gastos")
    ax[2].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
    ax[2].set_title("Distribución de Gastos")
    ax[3].text(0.5, 0.5, 'No hay datos de gastos', horizontalalignment='center', verticalalignment='center')
    ax[3].set_title("Evolución de los Gastos Mensuales")

st.pyplot(fig)

# Mostrar tabla de ingresos y gastos
st.header("Tabla de Ingresos y Gastos")
st.subheader("Ingresos")
st.dataframe(df_incomes)
st.subheader("Gastos")
st.dataframe(df_expenses)

# Generar recomendaciones
st.header("Recomendaciones")
recomendaciones = finance.generate_recommendations()
for recomendacion in recomendaciones:
    st.write(f"- {recomendacion}")