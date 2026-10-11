import csv
from datetime import date
from datetime import date,timedelta
import os

def get_summary():
    if not os.path.exists("sales.csv"):
        return None

    today = str(date.today())
    weekly_start = str(date.today())
    now_month=today[:7]

    total_sales=0
    paid=0
    total_pending=0
    monthly_sales=0
    monthly_paid=0
    monthly_pending=0
    payments_received = 0
    monthly_payments = 0
    debt={}
    with open("sales.csv") as f:
        reader = csv.DictReader(f)          
        for row in reader:
            if row["date"] == today:
                if float(row["total"]) > 0:
                    total_sales = total_sales + float(row["total"])
                    paid = paid + float(row["paid"])
                    total_pending = total_pending + float(row["balance"])
                else:
                    payments_received = payments_received + float(row["paid"])
        
            if row["date"][:7]==now_month:
                if float(row["total"]) > 0:
                    monthly_sales=monthly_sales+float(row["total"])
                    monthly_paid=monthly_paid+float(row["paid"])
                    monthly_pending=monthly_pending+float(row["balance"])
                else:
                    monthly_payments = monthly_payments + float(row["paid"])

            name = row["customer"]
            debt[name] = debt.get(name, 0) + float(row["balance"])

    owing = {}
    for name, balance in debt.items():
        if round(balance, 2) > 0:
            owing[name] = balance

    return {
        "today_sales": total_sales,
        "today_paid": paid,
        "today_pending": total_pending,
        "today_payments": payments_received,
        "month_sales": monthly_sales,
        "month_paid": monthly_paid,
        "month_pending": monthly_pending,
        "month_payments": monthly_payments,
        "owing": owing,
    }

