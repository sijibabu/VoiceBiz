import os
from datetime import date, datetime
import speech_recognition as sr
import csv
from difflib import get_close_matches
r = sr.Recognizer()

def listen_once():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("speak now.....")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def saved_names():
    names = set()
    if not os.path.exists("sales.csv"):
        return []
    with open("sales.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            names.add(row["customer"].lower().strip())
    return list(names)
    
def get_name():
    heard = listen_once()
    names=saved_names()
    if heard != "":
        print("Heard:", heard)
        answer = input("Correct? (y/n): ").lower().strip()

        if answer == "y" and heard.lower().strip() in names:
            name = heard
        else:
            matches = get_close_matches(heard.lower().strip(), names, n=1, cutoff=0.5)
            if matches:
                print("Did you mean", matches[0], "?")
                answer2 = input("(y/n): ").lower().strip()
                if answer2 == "y":
                    name = matches[0]
                else:
                    name = input("type the name: ")
            else:
                name = input("type the name: ")
    else:
        print("Could not hear. Please type.")
        name = input("type the name: ")
    name = name.lower().strip()
    return name
def parse_item(text):
    words=text.lower().split()
    units=["kilo", "kg", "litre", "liter", "rupees", "rupee", "rs", "gram", "packet"]
    spoken = {"half": 0.5, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    name_words = []
    numbers = []

    for word in words:
        if word in units:
            continue
        if word in spoken:
            numbers.append(spoken[word])
        else:
            try:
                numbers.append(float(word))
            except ValueError:
                name_words.append(word)

    if len(numbers) != 2 or len(name_words) == 0:
        return None
    return " ".join(name_words), numbers[0], numbers[1]
def get_item():
    heard = listen_once()

    if heard != "":
        print("Heard:", heard)
        result = parse_item(heard)
        if result is not None:
            item, quantity, price = result
            print(item + ", quantity", quantity, ", price", price)
            answer = input("Correct? (y/n): ").lower().strip()
            if answer == "y":
                return item, quantity, price
        else:
            print("Could not understand it.")
    else:
        print("Could not hear.")

    item = input("type the item: ").lower().strip()
    quantity = float(input("type the quantity: "))
    price = float(input("type the price: "))
    return item, quantity, price

print("ASWATHY STORES")
while True:
    name = input("enter the customer name (or stop or pay or v ): ")
    if name == "stop":
        break
    if name=="pay":
       pay_name = input("customer name: or v")
       if pay_name == "v":
           pay_name = get_name()
       pay_name = pay_name.lower().strip()
       pay_amount = float(input("amount paid: "))
       with open("sales.csv", "a") as f:
            f.write(f"{date.today()},{pay_name},0,0,{pay_amount},{-pay_amount}\n")
       print("Payment received from", pay_name)
       continue 
    if name == "v":
        name = get_name()
    items = []
    bill_total = 0
    while True:
        item = input("enter the item (or done or v): ")
        if item == "done":
            break
        if item == "v":
            item, quantity, price = get_item()
        else:
            quantity = float(input("enter the quantity: "))
            price = float(input("enter the price: "))
        total = quantity * price
        items.append([item, quantity, price, total])
        bill_total = bill_total + total
    if len(items) == 0:
        continue
    print("bill total : ", bill_total)
    status = input("paid or credit or partially paid (p/c/pp): ")
    if status == "p":
        balance = 0
        paid = bill_total
        print("paid")
    elif status == "pp":
        paid = float(input("enter the amount paid:"))
        balance = bill_total - paid
        print("balance = ", balance)
    elif status == "c":
        paid = 0
        balance = bill_total
        print("yet to pay")
        print("balance = ", balance)
    else:
        print("invalid choice")
    if status in ("p", "pp", "c"):
        if not os.path.exists("sales.csv"):
            with open("sales.csv", "w") as f:
                f.write("date,customer,items,total,paid,balance\n")
        with open("sales.csv", "a") as f:
            f.write(f"{date.today()},{name},{len(items)},{bill_total},{paid},{balance}\n")
    #billingg
        bill_text=""
        bill_text+="-"*30+"\n"
        bill_text+="ASWATHY STORES\n"
        bill_text+=f"Date: {date.today()}\n"
        bill_text+=f"customer: {name}\n"
        bill_text+="-"*30+"\n"
        for item_name, qty, price, line in items:
            bill_text+=f"{item_name} {qty} x {price} = {line}\n"
        bill_text+="-"*30+"\n"
        bill_text+=f"TOTAL:{ bill_total}\n"
        bill_text+=f"Paid: {paid}\n"
        bill_text+=f"Balance:{balance}\n"
        bill_text+="-"*30+"\n"
        print(bill_text)
        print("Thank you, visit again!")
        os.makedirs("bills", exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        with open(f"bills/bill_{stamp}.txt", "w") as bf:
            bf.write(bill_text)