from typing import List, Dict, Any

def calculate_summary(accounts: List[Any], loans: List[Any], credit_cards: List[Any]) -> Dict[str, float]:
    total_balance = sum(account.balance for account in accounts) if accounts else 0.0
    total_debt_loans = sum(loan.remaining_amount for loan in loans) if loans else 0.0
    total_debt_cards = sum(card.used_amount for card in credit_cards) if credit_cards else 0.0
    total_debt = total_debt_loans + total_debt_cards
    net_worth = total_balance - total_debt
    
    return {
        "total_balance": total_balance,
        "total_debt": total_debt,
        "net_worth": net_worth
    }

def calculate_monthly_requirement(loans: List[Any], credit_cards: List[Any]) -> Dict[str, float]:
    loan_emi_total = sum(loan.emi for loan in loans) if loans else 0.0
    credit_min_due_total = sum(card.minimum_due for card in credit_cards) if credit_cards else 0.0
    total_required = loan_emi_total + credit_min_due_total
    
    return {
        "total_required": total_required,
        "loan_emi_total": loan_emi_total,
        "credit_min_due_total": credit_min_due_total
    }

def normalize_debts(loans: List[Any], credit_cards: List[Any]) -> List[Dict[str, Any]]:
    debts = []
    if loans:
        for loan in loans:
            if loan.remaining_amount > 0:
                debts.append({
                    "name": loan.name,
                    "type": "loan",
                    "balance": loan.remaining_amount,
                    "interest": loan.interest_rate,
                    "min_payment": loan.emi
                })
    if credit_cards:
        for card in credit_cards:
            if card.used_amount > 0:
                debts.append({
                    "name": card.name,
                    "type": "credit_card",
                    "balance": card.used_amount,
                    "interest": card.interest_rate,
                    "min_payment": card.minimum_due
                })
    return debts

def generate_strategy(debts: List[Dict[str, Any]], method: str = "avalanche") -> Dict[str, Any]:
    if not debts:
        return {"focus": None, "ordered_debts": []}
        
    if method == "avalanche":
        ordered_debts = sorted(debts, key=lambda x: x["interest"], reverse=True)
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
    
    if credit_cards:
        for card in credit_cards:
            if card.limit > 0:
                utilization = (card.used_amount / card.limit) * 100
                if utilization > 40:
                    alerts.append(f"High credit utilization ({utilization:.1f}%) on {card.name}.")
            if card.interest_rate > 30:
                alerts.append(f"Very high interest rate ({card.interest_rate}%) on {card.name}. Consider balance transfer.")
                
    if loans:
        for loan in loans:
            if loan.interest_rate > 30:
                alerts.append(f"Very high interest rate ({loan.interest_rate}%) on {loan.name}.")
                
    total_debts_count = (len(loans) if loans else 0) + (len(credit_cards) if credit_cards else 0)
    if total_debts_count > 5:
        alerts.append("You have many active debt accounts. Consider consolidating them to simplify payments.")
        
    return alerts

def create_dashboard(accounts: List[Any], loans: List[Any], credit_cards: List[Any]) -> Dict[str, Any]:
    summary = calculate_summary(accounts, loans, credit_cards)
    monthly_req = calculate_monthly_requirement(loans, credit_cards)
    debts = normalize_debts(loans, credit_cards)
    
    # Calculate potential extra payment from loans
    extra_payment = sum(loan.extra_payment for loan in loans if loan.extra_payment) if loans else 0.0
    action_plan = generate_action_plan(debts, extra_payment)
    alerts = generate_alerts(loans, credit_cards)
    
    return {
        "summary": summary,
        "monthly_requirement": monthly_req,
        "strategy": action_plan,
        "alerts": alerts
    }
