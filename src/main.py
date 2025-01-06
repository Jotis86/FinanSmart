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
        self.load_data()

    def add_income(self, amount, description, category):
        self.incomes.append({"amount": amount, "description": description, "category": category, "date": datetime.now().strftime("%Y-%m-%d")})
        self.save_data()

    def add_expense(self, amount, description, category):
        self.expenses.append({"amount": amount, "description": description, "category": category, "date": datetime.now().strftime("%Y-%m-%d")})
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
            if any(expense["category"] == "entertainment" for expense in self.expenses):
                recommendations.append("You have spent on entertainment. Consider reducing these expenses if they are high.")
        else:
            recommendations.append("You are balanced, but you could try to save more.")
            recommendations.append("Review your expenses and look for areas where you can cut back to increase your savings.")

        # Specific recommendations by category
        categories = ["food", "transportation", "housing", "entertainment", "health", "education"]
        for category in categories:
            total_category = sum(expense["amount"] for expense in self.expenses if expense["category"] == category)
            if total_category > 0:
                category_percentage = (total_category / total_expenses) * 100
                if category == "food" and category_percentage > 15:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on food. Consider planning your meals and making more efficient purchases to reduce these expenses.")
                elif category == "transportation" and category_percentage > 10:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on transportation. Consider more economical options or carpooling to reduce these expenses.")
                elif category == "housing" and category_percentage > 30:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on housing. Make sure this expense is within your means and look for more economical options if possible.")
                elif category == "entertainment" and category_percentage > 10:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on entertainment. Consider reducing these expenses if they are high.")
                elif category == "health" and category_percentage > 10:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on health. Make sure these expenses are necessary and look for more economical options if possible.")
                elif category == "education" and category_percentage > 10:
                    recommendations.append(f"You have spent {category_percentage:.2f}% on education. Make sure these expenses are necessary and look for more economical options if possible.")

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
        type = input("Do you want to add an income or an expense? (income/expense): ").strip().lower()
        if type not in ["income", "expense"]:
            print("Invalid type. Please try again.")
            continue

        try:
            amount = float(input(f"Enter the amount of the {type}: "))
            if amount <= 0:
                raise ValueError("The amount must be positive.")
            
            if type == "income":
                category = input(f"Select a category for the {type} ({', '.join(income_categories)}): ").strip()
                if category not in income_categories:
                    print("Invalid category. Please try again.")
                    continue
            else:
                category = input(f"Select a category for the {type} ({', '.join(expense_categories)}): ").strip()
                if category not in expense_categories:
                    print("Invalid category. Please try again.")
                    continue

            description = input(f"Select a description for the {type} ({', '.join(descriptions[category])}): ").strip()
            if description not in descriptions[category]:
                print("Invalid description. Please try again.")
                continue

        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")
            continue

        if type == "income":
            finance.add_income(amount, description, category)
        else:
            finance.add_expense(amount, description, category)

        continue_input = input("Do you want to add another income or expense? (yes/no): ").strip().lower()
        if continue_input != "yes":
            break

    balance = finance.calculate_balance()
    print(f"\nYour monthly balance is: {balance}")

    finance.generate_charts()
    finance.generate_table()
    recommendations = finance.generate_recommendations()
    print("\nRecommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")

if __name__ == "__main__":
    main()