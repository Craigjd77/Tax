import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class PersonalTaxAssistant:
    def __init__(self):
        self.user_data = {
            'name': 'User',
            'age': 47,
            'state': 'Massachusetts',
            'filing_status': 'Single',
            'salary': 129000,
            'bonus_range': (12000, 16000),
            'assets': {
                'real_estate': {'South Boston Condo': 800000},
                'vehicles': ['BMW X3 2019', 'Vanagon 1985 Westfalia'],
                'investments': {
                    'GS_traditional_IRA': 350000,
                    'GS_brokerage': 280000,
                    'GS_cash': 20000,
                    'work_401k': 300000,
                    'Schwab_roth_IRA': 5000,
                    'Schwab_investment': 15000,
                    'Schwab_cash': 2000,
                    'rolled_quarters': 1000,
                    'savings_bonds': 1000,
                    'bitcoin': 5000
                }
            },
            'expenses': {
                'mortgage': 2500,
                'car_insurance': 150,
                'parking': 140,
                'utilities': 250
            },
            'savings': {
                'monthly_transfer': 800
            },
            'retirement_goal': {
                'age': 65,
                'net_worth': 4000000
            }
        }

    def calculate_net_worth(self):
        total = sum(self.user_data['assets']['real_estate'].values())
        total += sum(self.user_data['assets']['investments'].values())
        return total

    def visualize_asset_allocation(self):
        assets = self.user_data['assets']['investments']
        labels = list(assets.keys())
        sizes = list(assets.values())

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Asset Allocation')
        plt.show()

    def tax_optimization_strategies(self):
        strategies = [
            "Maximize 401(k) contributions",
            "Consider backdoor Roth IRA contributions",
            "Harvest tax losses in your brokerage account",
            "Explore tax-efficient investment options",
            "Consider charitable giving strategies",
            "Evaluate the benefits of a Health Savings Account (HSA)"
        ]
        return strategies

    def retirement_projection(self):
        current_age = self.user_data['age']
        retirement_age = self.user_data['retirement_goal']['age']
        years_to_retirement = retirement_age - current_age
        current_net_worth = self.calculate_net_worth()
        target_net_worth = self.user_data['retirement_goal']['net_worth']

        annual_growth_needed = (target_net_worth / current_net_worth) ** (1 / years_to_retirement) - 1

        print(f"Years to retirement: {years_to_retirement}")
        print(f"Current net worth: ${current_net_worth:,.2f}")
        print(f"Target net worth: ${target_net_worth:,.2f}")
        print(f"Required annual growth rate: {annual_growth_needed:.2%}")

    def run(self):
        print("Welcome to your Personal Tax Assistant!")
        while True:
            print("\nWhat would you like to do?")
            print("1. Calculate net worth")
            print("2. Visualize asset allocation")
            print("3. Get tax optimization strategies")
            print("4. View retirement projection")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                net_worth = self.calculate_net_worth()
                print(f"Your current net worth is: ${net_worth:,.2f}")
            elif choice == '2':
                self.visualize_asset_allocation()
            elif choice == '3':
                strategies = self.tax_optimization_strategies()
                print("Tax Optimization Strategies:")
                for i, strategy in enumerate(strategies, 1):
                    print(f"{i}. {strategy}")
            elif choice == '4':
                self.retirement_projection()
            elif choice == '5':
                print("Thank you for using your Personal Tax Assistant. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    assistant = PersonalTaxAssistant()
    assistant.run()