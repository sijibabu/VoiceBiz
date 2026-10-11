import csv
from datetime import date
from datetime import date,timedelta
today = str(date.today())
week_start = str(date.today())
now_month=today[:7]
total_sales=0
paid=0
total_pending=0
monthly_sales=0
monthly_paid=0
monthly_pending=0
weekly_sales=0
weekly_paid=0
weekly_pending=0
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
      print("payments received = ", payments_received)
      print("monthly payments received : ", monthly_payments)
      print("total sales = ", total_sales)
      print("total amount paid = ",paid)
      print("total amount pending = ",total_pending)
      for name, balance in debt.items():
            if round(balance, 2) > 0:
                  print(name, "owes", balance)
print("monthly sales : ",monthly_sales)
print("monthly amount paid : ", monthly_paid)
print("monthly amount pending : ", monthly_pending)