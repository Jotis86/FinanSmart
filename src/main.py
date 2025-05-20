import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from datetime import datetime
import warnings

# Ignorar FutureWarning de pandas
warnings.simplefilter(action='ignore', category=FutureWarning)

class Finance:
    def __init__(self):
        self.incomes = []
        self.expenses = []
        self.goals = []
        self.load_data()
        self.load_goals()

    def add_income(self, amount, description, category, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        self.incomes.append({"amount": amount, "description": description, "category": category, "date": date})
        self.save_data()

    def add_expense(self, amount, description, category, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        self.expenses.append({"amount": amount, "description": description, "category": category, "date": date})
        self.save_data()

    def calculate_balance(self):
        total_incomes = sum(item["amount"] for item in self.incomes)
        total_expenses = sum(item["amount"] for item in self.expenses)
        return total_incomes - total_expenses

    def generate_charts(self):
        df_incomes = pd.DataFrame(self.incomes)
        df_expenses = pd.DataFrame(self.expenses)

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

            # Pie chart for expenses
            df_expenses_grouped = df_expenses.drop(columns=["date"]).groupby("description").sum()
            ax[2].pie(df_expenses_grouped["amount"], labels=df_expenses_grouped.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("magma", len(df_expenses_grouped)))
            ax[2].set_title("Expense Distribution")

            # Line chart for expense evolution (monthly)
            df_expenses['date'] = pd.to_datetime(df_expenses['date'])
            df_expenses['month_year'] = df_expenses['date'].dt.to_period('M').astype(str)
            df_expenses_grouped_monthly = df_expenses.groupby(['month_year', 'category'])['amount'].sum().reset_index()
            sns.lineplot(x='month_year', y='amount', hue='category', data=df_expenses_grouped_monthly, ax=ax[3], palette="magma", marker='o')
            ax[3].set_title("Monthly Expense Evolution")
            ax[3].set_xlabel("Month-Year")
            ax[3].set_ylabel("Amount")
            ax[3].set_xticklabels(df_expenses_grouped_monthly['month_year'], rotation=45)
        else:
            ax[1].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
            ax[1].set_title("Expenses")
            ax[2].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
            ax[2].set_title("Expense Distribution")
            ax[3].text(0.5, 0.5, 'No expense data available', horizontalalignment='center', verticalalignment='center')
            ax[3].set_title("Monthly Expense Evolution")

        plt.tight_layout()
        plt.show()

    def generate_table(self):
        df_incomes = pd.DataFrame(self.incomes)
        df_expenses = pd.DataFrame(self.expenses)
        print("\nIncome Table:")
        print(df_incomes)
        print("\nExpense Table:")
        print(df_expenses)

    def generate_recommendations(self):
        if not self.incomes and not self.expenses:
            return ["No data available to generate recommendations. Please add your income and expenses."]

        balance = self.calculate_balance()
        total_incomes = sum(item["amount"] for item in self.incomes)
        total_expenses = sum(item["amount"] for item in self.expenses)
        recommendations = []

        if balance > 0:
            recommendations.append("Great job! You are saving money.")
            if balance > 1000:
                recommendations.append("Consider investing part of your savings in options like mutual funds, stocks, or real estate.")
            if total_expenses < total_incomes * 0.5:
                recommendations.append("Your expenses are less than 50% of your income. Excellent financial management!")
            else:
                recommendations.append("Although you have a positive balance, try to reduce your expenses to increase your savings.")
        elif balance < 0:
            recommendations.append("Warning, you are spending more than you earn.")
            if abs(balance) > 500:
                recommendations.append("Review your expenses and look for areas where you can cut back. Consider creating a monthly budget.")
            if total_expenses > total_incomes * 0.75:
                recommendations.append("Your expenses are more than 75% of your income. Try to reduce unnecessary expenses.")
            if any(expense["category"] == "Entertainment" for expense in self.expenses):
                recommendations.append("You have spent on entertainment. Consider reducing these expenses if they are high.")
        else:
            recommendations.append("You are balanced, but you could try to save more.")
            recommendations.append("Review your expenses and look for areas where you can cut back to increase your savings.")

        # Specific recommendations by category
        categories = ["Food", "Transportation", "Housing", "Entertainment", "Health", "Education", "Utilities", "Insurance", "Debt", "Savings", "Gifts", "Travel", "Other"]
        category_limits = {
            "Food": 15,
            "Transportation": 10,
            "Housing": 30,
            "Entertainment": 10,
            "Health": 10,
            "Education": 10,
            "Utilities": 10,
            "Insurance": 10,
            "Debt": 10,
            "Savings": 20,
            "Gifts": 5,
            "Travel": 5,
            "Other": 5
        }

        for category in categories:
            total_category = sum(expense["amount"] for expense in self.expenses if expense["category"] == category)
            if total_category > 0 and total_expenses > 0:
                category_percentage = (total_category / total_expenses) * 100
                limit = category_limits.get(category, 10)
                if category_percentage > limit:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on {category}. Consider reducing these expenses if they are high.")

        # Additional recommendations
        if total_incomes > 0 and total_expenses > 0:
            savings_rate = ((total_incomes - total_expenses) / total_incomes) * 100
            if savings_rate < 10:
                recommendations.append("Your savings rate is less than 10%. Try to save at least 10% of your income.")
            elif savings_rate > 20:
                recommendations.append("Great job! Your savings rate is more than 20%. Keep up the good work.")

        if any(expense["category"] == "Debt" for expense in self.expenses):
            total_debt = sum(expense["amount"] for expense in self.expenses if expense["category"] == "Debt")
            debt_percentage = (total_debt / total_expenses) * 100
            if debt_percentage > 20:
                recommendations.append(f"You have spent {debt_percentage:.2f}% on debt payments. Consider strategies to reduce your debt.")

        if any(expense["category"] == "Savings" for expense in self.expenses):
            total_savings = sum(expense["amount"] for expense in self.expenses if expense["category"] == "Savings")
            savings_percentage = (total_savings / total_expenses) * 100
            if savings_percentage < 10:
                recommendations.append(f"You have saved {savings_percentage:.2f}% of your income. Try to increase your savings rate.")

        return recommendations

    def save_data(self):
        with open('finances.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["type", "amount", "description", "category", "date"])
            for income in self.incomes:
                writer.writerow(["income", income["amount"], income["description"], income["category"], income["date"]])
            for expense in self.expenses:
                writer.writerow(["expense", expense["amount"], expense["description"], expense["category"], expense["date"]])

    def load_data(self):
        try:
            with open('finances.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["type"] == "income":
                        self.incomes.append({"amount": float(row["amount"]), "description": row["description"], "category": row["category"], "date": row["date"]})
                    elif row["type"] == "expense":
                        self.expenses.append({"amount": float(row["amount"]), "description": row["description"], "category": row["category"], "date": row["date"]})
        except FileNotFoundError:
            pass

    # Nuevas funciones para metas financieras
    def add_financial_goal(self, name, target_amount, deadline, category=None):
        self.goals.append({
            "name": name,
            "target_amount": target_amount,
            "deadline": deadline,
            "category": category,
            "created_date": datetime.now().strftime("%Y-%m-%d")
        })
        self.save_goals()

    def save_goals(self):
        with open('financial_goals.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "target_amount", "deadline", "category", "created_date"])
            for goal in self.goals:
                writer.writerow([goal["name"], goal["target_amount"], goal["deadline"], 
                                goal["category"], goal["created_date"]])

    def load_goals(self):
        try:
            with open('financial_goals.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.goals = []
                for row in reader:
                    self.goals.append({
                        "name": row["name"],
                        "target_amount": float(row["target_amount"]),
                        "deadline": row["deadline"],
                        "category": row["category"],
                        "created_date": row["created_date"]
                    })
        except FileNotFoundError:
            self.goals = []

    def track_goals_progress(self):
        if not self.goals:
            return "No hay metas financieras establecidas."
        
        results = []
        for goal in self.goals:
            if goal["category"] == "saving":
                # Para metas de ahorro
                current_savings = sum(item["amount"] for item in self.incomes if item["category"] == "Savings")
                progress = (current_savings / goal["target_amount"]) * 100
            elif goal["category"] == "expense_reduction":
                # Para metas de reducción de gastos
                category = goal["name"].split("_")[-1]
                current_expense = sum(item["amount"] for item in self.expenses if item["category"] == category)
                progress = 100 - (current_expense / goal["target_amount"]) * 100
            else:
                # Meta genérica
                progress = 0  # Necesitaríamos más información para calcular el progreso
            
            results.append({
                "name": goal["name"],
                "target": goal["target_amount"],
                "deadline": goal["deadline"],
                "progress": min(100, max(0, progress))
            })
        
        return results

    # Función para generar reporte mensual
    def generate_monthly_report(self):
        if not self.incomes and not self.expenses:
            return "No hay datos para generar un informe mensual."
        
        # Convertir a DataFrame
        df_incomes = pd.DataFrame(self.incomes)
        df_expenses = pd.DataFrame(self.expenses)
        
        # Añadir fechas
        if not df_incomes.empty:
            df_incomes['date'] = pd.to_datetime(df_incomes['date'])
            df_incomes['month'] = df_incomes['date'].dt.strftime('%Y-%m')
        
        if not df_expenses.empty:
            df_expenses['date'] = pd.to_datetime(df_expenses['date'])
            df_expenses['month'] = df_expenses['date'].dt.strftime('%Y-%m')
        
        # Obtener mes actual
        current_month = datetime.now().strftime('%Y-%m')
        
        # Filtrar para el mes actual
        month_incomes = df_incomes[df_incomes['month'] == current_month] if not df_incomes.empty else pd.DataFrame()
        month_expenses = df_expenses[df_expenses['month'] == current_month] if not df_expenses.empty else pd.DataFrame()
        
        # Calcular totales
        total_month_income = month_incomes['amount'].sum() if not month_incomes.empty else 0
        total_month_expense = month_expenses['amount'].sum() if not month_expenses.empty else 0
        month_balance = total_month_income - total_month_expense
        
        # Crear gráfico de donut para gastos del mes
        if not month_expenses.empty:
            plt.figure(figsize=(10, 6))
            category_totals = month_expenses.groupby('category')['amount'].sum()
            plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', 
                    startangle=90, wedgeprops=dict(width=0.5))
            plt.title(f'Distribución de gastos - {current_month}')
            plt.axis('equal')
            plt.tight_layout()
            plt.show()
        
        return {
            "month": current_month,
            "total_income": total_month_income,
            "total_expense": total_month_expense,
            "balance": month_balance,
            "top_expense_category": month_expenses.groupby('category')['amount'].sum().idxmax() if not month_expenses.empty else None,
            "top_income_category": month_incomes.groupby('category')['amount'].sum().idxmax() if not month_incomes.empty else None
        }


def add_transaction(finance, type, categories, descriptions):
    try:
        amount = float(input(f"Introduce la cantidad del {type}: "))
        if amount <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        
        print(f"\nCategorías disponibles para {type}:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        cat_choice = int(input("Selecciona el número de la categoría: ")) - 1
        if cat_choice < 0 or cat_choice >= len(categories):
            print("Categoría no válida.")
            return
        
        category = categories[cat_choice]
        
        print(f"\nDescripciones disponibles para {category}:")
        for i, desc in enumerate(descriptions[category], 1):
            print(f"{i}. {desc}")
        
        desc_choice = int(input("Selecciona el número de la descripción: ")) - 1
        if desc_choice < 0 or desc_choice >= len(descriptions[category]):
            print("Descripción no válida.")
            return
        
        description = descriptions[category][desc_choice]
        
        # Opcional: Elegir fecha
        use_custom_date = input("¿Deseas usar una fecha específica? (s/n): ").lower() == 's'
        
        if use_custom_date:
            date_str = input("Introduce la fecha (YYYY-MM-DD): ")
            try:
                datetime.strptime(date_str, "%Y-%m-%d")  # Validar formato
                if type == "income":
                    finance.add_income(amount, description, category, date_str)
                else:
                    finance.add_expense(amount, description, category, date_str)
            except ValueError:
                print("Formato de fecha incorrecto. Usando fecha actual.")
                if type == "income":
                    finance.add_income(amount, description, category)
                else:
                    finance.add_expense(amount, description, category)
        else:
            if type == "income":
                finance.add_income(amount, description, category)
            else:
                finance.add_expense(amount, description, category)
            
        print(f"{type.capitalize()} añadido correctamente.")
        
    except ValueError as e:
        print(f"Error: {e}")

def display_balance(finance):
    balance = finance.calculate_balance()
    total_income = sum(item["amount"] for item in finance.incomes)
    total_expenses = sum(item["amount"] for item in finance.expenses)
    
    print("\n===== RESUMEN FINANCIERO =====")
    print(f"Ingresos totales: {total_income:.2f}")
    print(f"Gastos totales: {total_expenses:.2f}")
    print(f"Balance: {balance:.2f}")
    
    if balance > 0:
        print("🟢 ¡Enhorabuena! Tienes un balance positivo.")
    elif balance < 0:
        print("🔴 ¡Cuidado! Tienes un balance negativo.")
    else:
        print("🟡 Tu balance es cero. Considera ahorrar más.")

def display_recommendations(finance):
    recommendations = finance.generate_recommendations()
    print("\n===== RECOMENDACIONES PERSONALIZADAS =====")
    for i, recommendation in enumerate(recommendations, 1):
        print(f"{i}. {recommendation}")

def export_data(finance):
    try:
        format_choice = input("Exportar como: (1) CSV, (2) Excel: ")
        filename = input("Nombre del archivo (sin extensión): ")
        
        if format_choice == "1":
            # Exportar como CSV (ya tienes implementado save_data)
            finance.save_data()
            print(f"Datos exportados a finances.csv correctamente")
        
        elif format_choice == "2":
            # Exportar como Excel
            df_incomes = pd.DataFrame(finance.incomes)
            df_expenses = pd.DataFrame(finance.expenses)
            
            with pd.ExcelWriter(f"{filename}.xlsx") as writer:
                df_incomes.to_excel(writer, sheet_name="Ingresos", index=False)
                df_expenses.to_excel(writer, sheet_name="Gastos", index=False)
                
            print(f"Datos exportados a {filename}.xlsx correctamente")
    
    except Exception as e:
        print(f"Error al exportar: {e}")

def add_goal(finance):
    try:
        name = input("Nombre de la meta financiera: ")
        target_amount = float(input("Cantidad objetivo: "))
        deadline = input("Fecha límite (YYYY-MM-DD): ")
        category_type = input("Tipo de meta (ahorro, reducción_gastos, otro): ")
        
        finance.add_financial_goal(name, target_amount, deadline, category_type)
        print("Meta financiera añadida correctamente.")
    except ValueError as e:
        print(f"Error al añadir meta: {e}")

def display_goals(finance):
    goals_progress = finance.track_goals_progress()
    if isinstance(goals_progress, str):
        print(goals_progress)
        return
    
    print("\n===== PROGRESO DE METAS FINANCIERAS =====")
    for i, goal in enumerate(goals_progress, 1):
        print(f"Meta {i}: {goal['name']}")
        print(f"  Objetivo: {goal['target']:.2f}")
        print(f"  Fecha límite: {goal['deadline']}")
        print(f"  Progreso: {goal['progress']:.2f}%")
        
        # Visualización simple de la barra de progreso
        progress_bar = "█" * int(goal['progress'] / 5) + "░" * (20 - int(goal['progress'] / 5))
        print(f"  [{progress_bar}] {goal['progress']:.2f}%")
        print()

def main():
    finance = Finance()
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
    
    while True:
        print("\n===== FINANSMART MENU =====")
        print("1. Añadir ingreso")
        print("2. Añadir gasto")
        print("3. Ver balance")
        print("4. Ver gráficos")
        print("5. Ver recomendaciones")
        print("6. Exportar datos")
        print("7. Añadir meta financiera")
        print("8. Ver progreso de metas")
        print("9. Generar informe mensual")
        print("0. Salir")
        
        option = input("\nSelecciona una opción: ").strip()
        
        if option == "1":
            add_transaction(finance, "income", income_categories, descriptions)
        elif option == "2":
            add_transaction(finance, "expense", expense_categories, descriptions)
        elif option == "3":
            display_balance(finance)
        elif option == "4":
            finance.generate_charts()
            finance.generate_table()
        elif option == "5":
            display_recommendations(finance)
        elif option == "6":
            export_data(finance)
        elif option == "7":
            add_goal(finance)
        elif option == "8":
            display_goals(finance)
        elif option == "9":
            monthly_report = finance.generate_monthly_report()
            if isinstance(monthly_report, str):
                print(monthly_report)
            else:
                print("\n===== INFORME MENSUAL =====")
                print(f"Mes: {monthly_report['month']}")
                print(f"Ingresos totales: {monthly_report['total_income']:.2f}")
                print(f"Gastos totales: {monthly_report['total_expense']:.2f}")
                print(f"Balance: {monthly_report['balance']:.2f}")
                if monthly_report['top_expense_category']:
                    print(f"Categoría de mayor gasto: {monthly_report['top_expense_category']}")
                if monthly_report['top_income_category']:
                    print(f"Categoría de mayor ingreso: {monthly_report['top_income_category']}")
        elif option == "0":
            print("¡Gracias por usar FinanSmart!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()