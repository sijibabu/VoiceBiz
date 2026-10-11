import os
from datetime import datetime
from datetime import date
from summary_data import get_summary
from flask import Flask, render_template,request,redirect,url_for
app = Flask(__name__)

@app.route("/")
def summary():
    data = get_summary()
    if data is None:
        return "No sales yet"
    return render_template("summary.html", data=data)
@app.route("/pay", methods=["GET", "POST"])
def pay():
    error=None
    if request.method == "POST":
        name = request.form["customer"].lower().strip()
        amount = float(request.form["amount"])
        data = get_summary()
        owing = data["owing"] if data else {}

        if amount <= 0:
            error = "Amount must be more than 0"
        elif name not in owing:
            error = "No debt found for that name"
        elif amount > owing[name]:
            error = "Amount is more than the debt"
        else:
            with open("sales.csv", "a") as f:
                f.write(f"{date.today()},{name},0,0,{amount},{-amount}\n")
            return redirect(url_for("summary")) 
    return render_template("pay.html",error=error)
@app.route("/bill", methods=["GET", "POST"])
def bill():
    error = None
    if request.method == "POST":
        customer = request.form["customer"].lower().strip()
        items = request.form.getlist("item")
        quantities = request.form.getlist("quantity")
        prices = request.form.getlist("price")
        status = request.form["status"]
        paid_text = request.form["paid_amount"]

        bill_items = []
        bill_total = 0
        for item, qty, price in zip(items, quantities, prices):
            item = item.strip()
            if item == "" or qty == "" or price == "":
                continue
            qty = float(qty)
            price = float(price)
            line = qty * price
            bill_items.append([item, qty, price, line])
            bill_total = bill_total + line

        if len(bill_items) == 0:
            error = "Enter at least one item with quantity and price"
        else:
            if status == "p":
                paid = bill_total
            elif status == "c":
                paid = 0
            else:
                paid = float(paid_text) if paid_text != "" else 0
            balance = bill_total - paid

            if status == "pp" and (paid <= 0 or paid > bill_total):
                error = "For partial payment, enter an amount above 0 and not more than the total"
            else:
                if not os.path.exists("sales.csv"):
                    with open("sales.csv", "w") as f:
                        f.write("date,customer,items,total,paid,balance\n")
                with open("sales.csv", "a") as f:
                    f.write(f"{date.today()},{customer},{len(bill_items)},{bill_total},{paid},{balance}\n")
                    bill_text=""
                    bill_text+="-"*30+"\n"
                    bill_text+="ASWATHY STORES\n"
                    bill_text+=f"Date: {date.today()}\n"
                    bill_text+=f"customer: {customer}\n"
                    bill_text+="-"*30+"\n"
                    for item_name, qty, price, line in bill_items:
                        bill_text+=f"{item_name} {qty} x {price} = {line}\n"
                    bill_text+="-"*30+"\n"
                    bill_text+=f"TOTAL:{ bill_total}\n"
                    bill_text+=f"Paid: {paid}\n"
                    bill_text+=f"Balance:{balance}\n"
                    bill_text+="-"*30+"\n"
                    bill_text+="Thank you, visit again!\n"
                    os.makedirs("bills", exist_ok=True)
                    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    with open(f"bills/bill_{stamp}.txt", "w") as bf:
                        bf.write(bill_text)
                    return render_template("bill_result.html", customer=customer,
                    bill_items=bill_items,
                    bill_total=bill_total,
                    paid=paid,
                    balance=balance,
                    today=str(date.today()),)

    return render_template("bill.html", error=error)

if __name__ == "__main__":
    app.run(debug=True)