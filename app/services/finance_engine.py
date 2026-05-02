from typing import List, Dict, Any, Optional
from datetime import datetime

def calculate_summary(accounts: List[Any], loans: List[Any], credit_cards: List[Any], cc_loans: List[Any]) -> Dict[str, float]:
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    active_cc_loans = [l for l in cc_loans if getattr(l, 'status', 'active') == 'active']
    
    total_balance = sum(account.balance for account in accounts) if accounts else 0.0
    total_debt_loans = sum(loan.remaining_amount for loan in active_loans) if active_loans else 0.0
    total_debt_cards = sum(card.used_amount for card in credit_cards) if credit_cards else 0.0
    total_debt_cc_loans = sum(l.remaining_amount for l in active_cc_loans) if active_cc_loans else 0.0
    
    total_debt = total_debt_loans + total_debt_cards + total_debt_cc_loans
    net_worth = total_balance - total_debt
    
    return {
        "total_balance": total_balance,
        "total_debt": total_debt,
        "net_worth": net_worth
    }

def calculate_monthly_requirement(loans: List[Any], credit_cards: List[Any], cc_loans: List[Any]) -> Dict[str, float]:
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    active_cc_loans = [l for l in cc_loans if getattr(l, 'status', 'active') == 'active']
    
    loan_emi_total = sum(loan.emi for loan in active_loans) if active_loans else 0.0
    credit_min_due_total = sum(card.minimum_due for card in credit_cards) if credit_cards else 0.0
    credit_card_loan_emi_total = sum(l.emi for l in active_cc_loans) if active_cc_loans else 0.0
    
    # Total required only includes Loans + CC Min Due (which already includes CC EMIs)
    total_required = loan_emi_total + credit_min_due_total
    
    return {
        "total_required": round(total_required, 2),
        "loan_emi_total": round(loan_emi_total, 2),
        "credit_min_due_total": round(credit_min_due_total, 2),
        "credit_card_loan_emi_total": round(credit_card_loan_emi_total, 2)
    }

def normalize_debts(loans: List[Any], credit_cards: List[Any], cc_loans: List[Any]) -> List[Dict[str, Any]]:
    debts = []
    
    # Priority logic: 
    # CC Swipes (Highest) > PayLater/CC Loans (High) > Personal Loans (Normal)
    
    # 1. Credit Cards (Highest Priority)
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
                    "priority": card.interest_rate + 50  # Base bonus for CC swipes
                })
                
    # 2. CC Loans / PayLater (High Priority)
    active_cc_loans = [l for l in cc_loans if getattr(l, 'status', 'active') == 'active']
    if active_cc_loans:
        for l in active_cc_loans:
            if l.remaining_amount > 0:
                debts.append({
                    "id": l.id,
                    "name": l.name,
                    "type": "credit_card_loan",
                    "balance": l.remaining_amount,
                    "interest": l.interest_rate,
                    "min_payment": l.emi,
                    "priority": l.interest_rate + 25 # High priority for EMIs
                })
                
    # 3. Regular Loans (Normal Priority)
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    if active_loans:
        for loan in active_loans:
            if loan.remaining_amount > 0:
                priority_bonus = 0
                if getattr(loan, 'loan_category', 'personal') == 'paylater':
                    priority_bonus = 25
                
                debts.append({
                    "id": loan.id,
                    "name": loan.name,
                    "type": "loan",
                    "balance": loan.remaining_amount,
                    "interest": loan.interest_rate,
                    "min_payment": loan.emi,
                    "priority": loan.interest_rate + priority_bonus
                })
                
    return debts

def generate_action_plan(debts: List[Dict[str, Any]], extra_payment: float = 0.0) -> Dict[str, Any]:
    if not debts:
        return {
            "focus": "No debts to focus on.",
            "reason": "You are debt-free or have no active debts recorded.",
            "steps": ["Enjoy your debt-free life!"]
        }
        
    # Always prioritize highest priority score
    ordered_debts = sorted(debts, key=lambda x: x["priority"], reverse=True)
    focus_debt = ordered_debts[0]
    
    steps = ["Pay all minimum requirements first."]
    if focus_debt['type'] == 'credit_card':
        steps.append(f"Clear the ₹{focus_debt['balance']} balance on {focus_debt['name']} as it has the highest priority/interest.")
    else:
        steps.append(f"Focus on {focus_debt['name']} to reduce the overall debt burden faster.")
        
    if extra_payment > 0:
        steps.append(f"Add extra payment of ₹{extra_payment} to {focus_debt['name']}.")
    
    return {
        "focus": focus_debt['name'],
        "reason": f"Targeting {focus_debt['name']} first based on debt type priority and interest savings.",
        "steps": steps
    }

def generate_alerts(loans: List[Any], credit_cards: List[Any], cc_loans: List[Any]) -> List[str]:
    alerts = []
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    active_cc_loans = [l for l in cc_loans if getattr(l, 'status', 'active') == 'active']
    
    if credit_cards:
        for card in credit_cards:
            # Find loans associated with this card
            card_specific_loans = [l for l in active_cc_loans if l.card_id == card.id]
            total_card_debt = card.used_amount + sum(l.remaining_amount for l in card_specific_loans)
            
            if card.limit > 0:
                utilization = (total_card_debt / card.limit) * 100
                if utilization > 30:
                    alerts.append(f"High credit utilization ({utilization:.1f}%) on {card.name} (includes EMIs).")
            if card.interest_rate > 35:
                alerts.append(f"High interest debt detected on {card.name} ({card.interest_rate}%).")
                
    if active_cc_loans:
        alerts.append(f"Hidden EMI debt detected: You have {len(active_cc_loans)} active credit card EMIs.")
        for l in active_cc_loans:
            if l.interest_rate > 35:
                alerts.append(f"High interest EMI detected: {l.name} ({l.interest_rate}%).")

    return alerts

def calculate_payment_split(debt_type: str, debt: Any, amount: float) -> Dict[str, float]:
    """
    Calculates interest and principal components of a payment.
    """
    interest_rate = debt.interest_rate
    interest_type = getattr(debt, 'interest_type', 'yearly')
    
    if debt_type == "loan":
        balance = debt.remaining_amount
    elif debt_type == "credit_card_loan":
        balance = debt.remaining_amount
    else: # credit_card
        balance = debt.used_amount
        interest_type = "yearly" # Cards are always yearly
        
    if interest_type == "yearly":
        monthly_rate = (interest_rate / 100) / 12
    else: # monthly
        monthly_rate = (interest_rate / 100)
        
    interest_component = balance * monthly_rate
    principal_component = amount - interest_component
    
    # Validation
    if principal_component < 0:
        principal_component = 0.0
    if principal_component > balance:
        principal_component = balance
        
    return {
        "interest": round(interest_component, 2),
        "principal": round(principal_component, 2)
    }

def create_dashboard(accounts: List[Any], loans: List[Any], credit_cards: List[Any], cc_loans: List[Any], payments: List[Any] = None) -> Dict[str, Any]:
    active_loans = [loan for loan in loans if getattr(loan, 'status', 'active') == 'active']
    active_cc_loans = [l for l in cc_loans if getattr(l, 'status', 'active') == 'active']
    
    summary = calculate_summary(accounts, active_loans, credit_cards, active_cc_loans)
    monthly_req = calculate_monthly_requirement(active_loans, credit_cards, active_cc_loans)
    debts = normalize_debts(active_loans, credit_cards, active_cc_loans)
    
    extra_payment = sum(loan.extra_payment for loan in active_loans if getattr(loan, 'extra_payment', 0)) if active_loans else 0.0
    action_plan = generate_action_plan(debts, extra_payment)
    alerts = generate_alerts(active_loans, credit_cards, active_cc_loans)
    
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
