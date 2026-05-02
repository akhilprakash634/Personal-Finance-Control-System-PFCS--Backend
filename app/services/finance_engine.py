from typing import List, Dict, Any, Optional
from datetime import datetime

def calculate_summary(accounts: List[Any], loans: List[Any], credit_cards: List[Any]) -> Dict[str, float]:
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    total_balance = sum(account.balance for account in accounts) if accounts else 0.0
    total_debt_loans = sum(loan.remaining_amount for loan in active_loans) if active_loans else 0.0
    total_debt_cards = sum(card.used_amount for card in credit_cards) if credit_cards else 0.0
    total_debt = total_debt_loans + total_debt_cards
    net_worth = total_balance - total_debt
    
    return {
        "total_balance": total_balance,
        "total_debt": total_debt,
        "net_worth": net_worth
    }

def calculate_monthly_requirement(loans: List[Any], credit_cards: List[Any]) -> Dict[str, float]:
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    loan_emi_total = sum(loan.emi for loan in active_loans) if active_loans else 0.0
    credit_min_due_total = sum(card.minimum_due for card in credit_cards) if credit_cards else 0.0
    total_required = loan_emi_total + credit_min_due_total
    
    return {
        "total_required": total_required,
        "loan_emi_total": loan_emi_total,
        "credit_min_due_total": credit_min_due_total
    }

def normalize_debts(loans: List[Any], credit_cards: List[Any]) -> List[Dict[str, Any]]:
    debts = []
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    if active_loans:
        for loan in active_loans:
            if loan.remaining_amount > 0:
                priority_bonus = 0
                if getattr(loan, 'loan_category', 'personal') == 'paylater':
                    priority_bonus = 10
                
                debts.append({
                    "id": loan.id,
                    "name": loan.name,
                    "type": "loan",
                    "balance": loan.remaining_amount,
                    "interest": loan.interest_rate,
                    "min_payment": loan.emi,
                    "priority": loan.interest_rate + priority_bonus
                })
    if credit_cards:
        for card in credit_cards:
            if card.used_amount > 0:
                debts.append({
                    "id": card.id,
                    "name": card.name,
                    "type": "credit_card",
                    "balance": card.used_amount,
                    "interest": card.interest_rate,
                    "min_payment": card.minimum_due,
                    "priority": card.interest_rate
                })
    return debts

def generate_strategy(debts: List[Dict[str, Any]], method: str = "avalanche") -> Dict[str, Any]:
    if not debts:
        return {"focus": None, "ordered_debts": []}
        
    if method == "avalanche":
        ordered_debts = sorted(debts, key=lambda x: x["priority"], reverse=True)
    elif method == "snowball":
        ordered_debts = sorted(debts, key=lambda x: x["balance"], reverse=False)
    else:
        ordered_debts = debts

    focus_debt = ordered_debts[0] if ordered_debts else None
    
    return {
        "focus": focus_debt,
        "ordered_debts": ordered_debts
    }

def generate_action_plan(debts: List[Dict[str, Any]], extra_payment: float = 0.0) -> Dict[str, Any]:
    strategy = generate_strategy(debts, method="avalanche")
    focus_debt = strategy["focus"]
    ordered_debts = strategy["ordered_debts"]
    
    if not focus_debt:
        return {
            "focus": "No debts to focus on.",
            "reason": "You are debt-free or have no active debts recorded.",
            "steps": ["Enjoy your debt-free life!"]
        }
    
    steps = ["Pay minimum on all debts."]
    if extra_payment > 0:
        steps.append(f"Add extra payment of ₹{extra_payment} to {focus_debt['name']}.")
    else:
        steps.append(f"Focus any additional funds you get towards {focus_debt['name']}.")
    steps.append("Once the focus debt is cleared, move its total payment to the next debt.")
    
    return {
        "focus": focus_debt['name'],
        "reason": f"Targeting {focus_debt['name']} first saves the most money on interest (Avalanche method).",
        "steps": steps
    }

def estimate_payoff(debt: Dict[str, Any], extra_payment: float) -> float:
    total_payment = debt["min_payment"] + extra_payment
    if total_payment <= 0:
        return -1 # Never pays off
    return debt["balance"] / total_payment

def generate_alerts(loans: List[Any], credit_cards: List[Any]) -> List[str]:
    alerts = []
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    
    if credit_cards:
        for card in credit_cards:
            if card.limit > 0:
                utilization = (card.used_amount / card.limit) * 100
                if utilization > 40:
                    alerts.append(f"High credit utilization ({utilization:.1f}%) on {card.name}.")
            if card.interest_rate > 30:
                alerts.append(f"Very high interest rate ({card.interest_rate}%) on {card.name}. Consider balance transfer.")
                
    if active_loans:
        for loan in active_loans:
            if loan.interest_rate > 30:
                alerts.append(f"Very high interest rate ({loan.interest_rate}%) on {loan.name}.")
                
    total_debts_count = (len(active_loans) if active_loans else 0) + (len(credit_cards) if credit_cards else 0)
    if total_debts_count > 5:
        alerts.append("You have many active debt accounts. Consider consolidating them to simplify payments.")
        
    return alerts

def calculate_payment_split(debt_type: str, debt: Any, amount: float) -> Dict[str, float]:
    """
    Calculates interest and principal components of a payment.
    """
    if debt_type == "loan":
        interest_rate = debt.interest_rate
        interest_type = getattr(debt, 'interest_type', 'yearly')
        balance = debt.remaining_amount
        
        if interest_type == "yearly":
            monthly_rate = (interest_rate / 100) / 12
        else:
            monthly_rate = (interest_rate / 100)
            
        interest_component = balance * monthly_rate
    else: # credit_card
        interest_rate = debt.interest_rate
        balance = debt.used_amount
        # Credit cards are almost always yearly interest
        monthly_rate = (interest_rate / 100) / 12
        interest_component = balance * monthly_rate
        
    principal_component = amount - interest_component
    
    # Ensure principal doesn't exceed amount or make balance negative
    if principal_component < 0:
        principal_component = 0.0
        
    if principal_component > balance:
        principal_component = balance
        
    return {
        "interest": round(interest_component, 2),
        "principal": round(principal_component, 2)
    }

def create_dashboard(accounts: List[Any], loans: List[Any], credit_cards: List[Any], payments: List[Any] = None) -> Dict[str, Any]:
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    summary = calculate_summary(accounts, active_loans, credit_cards)
    monthly_req = calculate_monthly_requirement(active_loans, credit_cards)
    debts = normalize_debts(active_loans, credit_cards)
    
    # Calculate potential extra payment from loans
    extra_payment = sum(loan.extra_payment for loan in active_loans if getattr(loan, 'extra_payment', 0)) if active_loans else 0.0
    action_plan = generate_action_plan(debts, extra_payment)
    alerts = generate_alerts(active_loans, credit_cards)
    
    # This Month Stats
    now = datetime.now()
    this_month_payments = []
    if payments:
        this_month_payments = [p for p in payments if p.date.month == now.month and p.date.year == now.year]
        
    total_paid_this_month = sum(p.amount for p in this_month_payments)
    total_interest_this_month = sum(p.interest_component for p in this_month_payments)
    total_principal_this_month = sum(p.principal_component for p in this_month_payments)
    
    insights = []
    if total_interest_this_month > total_principal_this_month and total_paid_this_month > 0:
        insights.append("Warning: You're mostly paying interest this month. Consider increasing payments to reduce principal faster.")
    elif total_paid_this_month > 0:
        insights.append(f"Good job! ₹{total_principal_this_month:.2f} of your payments went towards reducing your actual debt.")

    return {
        "summary": summary,
        "monthly_requirement": monthly_req,
        "strategy": action_plan,
        "alerts": alerts,
        "this_month": {
            "total_paid": round(total_paid_this_month, 2),
            "interest_paid": round(total_interest_this_month, 2),
            "principal_reduced": round(total_principal_this_month, 2),
            "insights": insights
        }
    }
