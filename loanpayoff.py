import pandas as pd
import numpy as np

def analyze_loan_payoff_strategy(loans):
    """
    Analyzes different loan payoff strategies and provides recommendations.
    
    Parameters:
    loans (list of dict): List of loan dictionaries with keys:
        - 'name': Loan identifier
        - 'principal': Current principal balance
        - 'rate': Annual interest rate (as percentage)
        - 'min_payment': Minimum monthly payment
    
    Returns:
    dict: Contains different prioritization strategies and analysis
    """
    df = pd.DataFrame(loans)
    
    # Calculate monthly interest accrual
    df['monthly_interest'] = (df['principal'] * (df['rate']/100) / 12).round(2)
    
    # Calculate interest-to-principal ratio
    df['interest_principal_ratio'] = (df['rate'] / 100) / df['principal']
    
    # Calculate various prioritization scores
    df['avalanche_score'] = df['rate']  # Pure interest rate prioritization
    df['snowball_score'] = -df['principal']  # Pure principal prioritization
    df['balanced_score'] = df['rate'] * np.log(df['principal'])  # Balanced approach
    
    # Generate recommendations
    strategies = {
        'avalanche_method': df.sort_values('avalanche_score', ascending=False),
        'snowball_method': df.sort_values('snowball_score', ascending=False),
        'balanced_method': df.sort_values('balanced_score', ascending=False)
    }
    
    # Calculate potential interest savings
    total_debt = df['principal'].sum()
    total_monthly_interest = df['monthly_interest'].sum()
    
    analysis = {
        'strategies': strategies,
        'summary': {
            'total_debt': total_debt,
            'total_monthly_interest': total_monthly_interest,
            'highest_interest_loan': df.loc[df['rate'].idxmax(), 'name'],
            'smallest_balance_loan': df.loc[df['principal'].idxmin(), 'name'],
            'most_expensive_loan': df.loc[df['monthly_interest'].idxmax(), 'name']
        }
    }
    
    return analysis

# Your current loans
current_loans = [
    {'name': 'AE', 'principal': 0, 'rate': 6.80, 'min_payment': 0},
    {'name': 'AA', 'principal': 790.58, 'rate': 5.60, 'min_payment': 8.62},
    {'name': 'AB', 'principal': 790.54, 'rate': 5.60, 'min_payment': 8.62},
    {'name': 'AI', 'principal': 4500.00, 'rate': 5.05, 'min_payment': 47.84},
    {'name': 'AJ', 'principal': 6396.97, 'rate': 5.05, 'min_payment': 69.61},
    {'name': 'AK', 'principal': 5500.00, 'rate': 4.53, 'min_payment': 57.08},
    {'name': 'AL', 'principal': 7121.42, 'rate': 4.53, 'min_payment': 75.55},
    {'name': 'AC', 'principal': 960.00, 'rate': 4.50, 'min_payment': 9.95},
    {'name': 'AF', 'principal': 3500.00, 'rate': 4.45, 'min_payment': 36.19},
    {'name': 'AG', 'principal': 6620.73, 'rate': 4.45, 'min_payment': 69.83},
    {'name': 'AH', 'principal': 1000.00, 'rate': 4.45, 'min_payment': 10.34},
    {'name': 'AM', 'principal': 5500.00, 'rate': 2.75, 'min_payment': 52.48},
    {'name': 'AN', 'principal': 7000.00, 'rate': 2.75, 'min_payment': 67.70},
    {'name': 'State-1', 'principal': 4420, 'rate': 7.99, 'min_payment': 78.07},
    {'name': 'State-2', 'principal': 3601, 'rate': 6.30, 'min_payment': 38.21}
]

result = analyze_loan_payoff_strategy(current_loans)

print("\nLOAN SUMMARY:")
print(f"Total Debt: ${result['summary']['total_debt']:,.2f}")
print(f"Total Monthly Interest: ${result['summary']['total_monthly_interest']:,.2f}")
print(f"Highest Interest Loan: {result['summary']['highest_interest_loan']}")
print(f"Smallest Balance Loan: {result['summary']['smallest_balance_loan']}")
print(f"Most Expensive Loan: {result['summary']['most_expensive_loan']}")

# Print recommendations in order for each strategy
for strategy, df in result['strategies'].items():
    print(f"\n{strategy.upper()} Priority Order:")
    for idx, row in df.iterrows():
        print(f"{row['name']}: ${row['principal']:,.2f} at {row['rate']}% (Monthly Payment: ${row['min_payment']:.2f})")
