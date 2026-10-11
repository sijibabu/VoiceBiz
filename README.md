# VoiceBiz

A voice-enabled billing and credit-tracking tool for small vendors, built with Python, Flask, HTML/CSS and JavaScript.

Small shops often track sales and customer credit in notebooks. VoiceBiz lets a vendor speak an item, check it, save the bill, and see who still owes money.

## Features
- Voice item entry in the browser (Chrome/Edge). The spoken item, quantity and price fill a form row for the vendor to check before saving.
- Bills with several items, saved as one record, shown as a receipt page, and stored as a text file.
- Paid, credit and partial payments.
- Debt list showing who owes how much.
- Payment page that refuses unknown names and amounts above the debt.
- Daily and monthly summary of sales, money received and credit given.
- Original command-line version (bill.py, summary.py, voice.py) with voice input for customer names, items and payments, including matching a heard name to saved customers.

## How to run
1. Install Python 3.
2. Install the packages: py -m pip install -r requirements.txt
3. Start the app: py app.py
4. Open http://127.0.0.1:5000 in Chrome or Edge.
5. To try the summary page with sample data, copy sales_sample.csv to sales.csv.

Voice input needs Chrome or Edge, a microphone, and an internet connection.

## Screenshots
(add: summary page, bill form, receipt)

## Demo video
(add link)

## Limitations
- Data is stored in a CSV file, which is fine for a demo but not for real business records.
- No login, so anyone who opens the site sees all the data.
- Voice works in English only, and short or unusual item names can be misheard, so every voice entry must be checked before saving.
- Customer names and payments are typed in the web version. Voice for those is in the command-line version only.
- Refreshing the receipt page saves the bill again.

## Future work
- Profit and loss, which needs buying prices for each item.
- Weekly summary.
- Voice for customer names and payments in the browser.
- Malayalam and mixed-language voice.
- A real database, login, and online hosting.