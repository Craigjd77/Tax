from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

class PersonalTaxAssistant:
    def __init__(self):
        self.user_data = {
            'name': '',
            'age': 0,
            'state': '',
            'filing_status': '',
            'salary': 0,
            'assets': {
                'real_estate': 0,
                'investments': 0,
                'cash': 0
            },
            'retirement_goal': {
                'age': 0,
                'net_worth': 0
            }
        }

    def update_user_data(self, form_data):
        self.user_data['age'] = int(form_data['age'])
        self.user_data['salary'] = int(form_data['salary'])
        self.user_data['retirement_goal']['age'] = int(form_data['retirement_age'])
        self.user_data['retirement_goal']['net_worth'] = int(form_data['target_net_worth'])
        current_net_worth = int(form_data['current_net_worth'])
        return current_net_worth

    def calculate_net_worth(self):
        return sum(self.user_data['assets'].values())

    def retirement_projection(self, current_net_worth):
        current_age = self.user_data['age']
        retirement_age = self.user_data['retirement_goal']['age']
        years_to_retirement = retirement_age - current_age
        target_net_worth = self.user_data['retirement_goal']['net_worth']

        if years_to_retirement > 0:
            annual_growth_needed = (target_net_worth / current_net_worth) ** (1 / years_to_retirement) - 1
            monthly_savings_needed = (target_net_worth - current_net_worth * (1 + annual_growth_needed) ** years_to_retirement) / \
                                     ((1 + annual_growth_needed / 12) ** (years_to_retirement * 12) - 1) / \
                                     (annual_growth_needed / 12)
            monthly_savings_needed = max(0, monthly_savings_needed)
        else:
            annual_growth_needed = 0
            monthly_savings_needed = 0

        return {
            "current_age": current_age,
            "retirement_age": retirement_age,
            "years_to_retirement": years_to_retirement,
            "current_net_worth": current_net_worth,
            "target_net_worth": target_net_worth,
            "annual_growth_needed": annual_growth_needed,
            "monthly_savings_needed": monthly_savings_needed
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    assistant = PersonalTaxAssistant()
    if request.method == 'POST':
        current_net_worth = assistant.update_user_data(request.form)
        retirement_projection = assistant.retirement_projection(current_net_worth)
        tax_strategies = [
            {"description": "Maximize 401(k) contributions", "impact": 90},
            {"description": "Consider backdoor Roth IRA contributions", "impact": 75},
            {"description": "Explore tax-loss harvesting in brokerage account", "impact": 60},
            {"description": "Optimize tax-efficient fund placement", "impact": 50},
            {"description": "Evaluate Roth IRA conversion opportunities", "impact": 70},
            {"description": "Consider tax implications of Bitcoin holdings", "impact": 40},
            {"description": "Explore charitable giving strategies", "impact": 55},
            {"description": "Investigate opportunity zone investments", "impact": 45},
            {"description": "Consider a Health Savings Account (HSA)", "impact": 65},
            {"description": "Review and optimize savings bond strategy", "impact": 30}
        ]
        response_data = {
            'retirement_projection': retirement_projection,
            'tax_strategies': tax_strategies,
            'assets': assistant.user_data['assets']
        }
        return jsonify(response_data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)