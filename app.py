from flask import Flask, render_template_string
import requests
import xml.etree.ElementTree as ET
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tally_request import (
    stock_summary_xml,
    stock_voucher_xml,
    account_voucher_view_xml,
    balance_sheet_xml,
    group_table_xml,
    bills_payable_xml,
    bills_receivable_xml
)
import webbrowser
import threading
import re
import html
import csv
from io import StringIO
from bs4 import BeautifulSoup
import sys
import os
import time

app = Flask(__name__)

TALLY_URL = "http://localhost:9000"
GOOGLE_SHEET_NAME = "Tally Data"



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def clean_xml(xml_data):
    # Removes invalid XML character references like &#4;, &#1;, etc.
    return re.sub(r'&#\d+;', '', xml_data)

# ---------- FETCH TALLY REPORTS ----------
def fetch_tally_stock_summary():
    try:
        response = requests.post(TALLY_URL, data=stock_summary_xml, headers={"Content-Type": "text/xml"})
        if response.status_code == 200:
            return response.text
        else:
            return ""
    except Exception as e:
        return ""

def fetch_tally_stock_voucher():
    response = requests.post(TALLY_URL, data=stock_voucher_xml, headers={"Content-Type": "text/xml"})
    return response.text

def fetch_accounting_vouchers():
    response = requests.post(TALLY_URL, data=account_voucher_view_xml, headers={"Content-Type": "text/xml"})
    return response.text
    
def fetch_tally_balance_sheet():
    response = requests.post(TALLY_URL, data=balance_sheet_xml, headers={"Content-Type": "text/xml"})
    return response.text

def fetch_tally_group_table():
    try:
        response = requests.post(TALLY_URL, data=group_table_xml, headers={"Content-Type": "text/xml"})
        if response.status_code == 200:
            return response.text
        else:
            return ""
    except Exception as e:
        return ""

def fetch_tally_bills_payable():
    try:
        response = requests.post(TALLY_URL, data=bills_payable_xml, headers={"Content-Type": "text/xml"})
        if response.status_code == 200:
            return response.text
        else:
            return ""
    except Exception as e:
        return ""

def fetch_tally_bills_receivable():
    try:
        response = requests.post(TALLY_URL, data=bills_receivable_xml, headers={"Content-Type": "text/xml"})
        if response.status_code == 200:
            return response.text
        else:
            return ""
    except Exception as e:
        return ""

# ---------- PARSE STOCK SUMMARY ----------
def parse_stock_summary(xml_data):
    try:
        cleaned_data = clean_xml(xml_data)
        lines = [line.strip() for line in cleaned_data.split('\n') if line.strip()]
        
        items = []
        print("\nParsing Stock Summary Data:")
        print("-" * 50)
        
        def parse_indian_number(value):
            try:
                # Remove any negative signs and store it
                is_negative = value.startswith('(-)')
                value = value.replace('(-)', '')
                
                # Remove commas and convert to float
                value = value.replace(',', '')
                result = float(value)
                
                # Apply negative sign if needed
                return -result if is_negative else result
            except Exception:
                return 0.0
        
        for line in lines:
            try:
                reader = csv.reader(StringIO(line))
                fields = next(reader)
                
                if len(fields) >= 10:  # New format has 10 fields
                    name = fields[0].strip('"')
                    parent = fields[1].strip('"')
                    opening_qty = parse_indian_number(fields[2].strip()) if len(fields) > 2 else 0
                    opening_value = parse_indian_number(fields[3].strip()) if len(fields) > 3 else 0
                    inwards_qty = parse_indian_number(fields[4].strip()) if len(fields) > 4 else 0
                    inwards_value = parse_indian_number(fields[5].strip()) if len(fields) > 5 else 0
                    outwards_qty = parse_indian_number(fields[6].strip()) if len(fields) > 6 else 0
                    outwards_value = parse_indian_number(fields[7].strip()) if len(fields) > 7 else 0
                    closing_qty = parse_indian_number(fields[8].strip()) if len(fields) > 8 else 0
                    closing_value = parse_indian_number(fields[9].strip()) if len(fields) > 9 else 0
                    
                    # Calculate rates
                    opening_rate = opening_value / opening_qty if opening_qty != 0 else 0
                    inwards_rate = inwards_value / inwards_qty if inwards_qty != 0 else 0
                    outwards_rate = outwards_value / outwards_qty if outwards_qty != 0 else 0
                    closing_rate = closing_value / closing_qty if closing_qty != 0 else 0
                    
                    item_data = [
                        name, 
                        str(opening_qty), str(opening_rate), str(opening_value),
                        str(inwards_qty), str(inwards_rate), str(inwards_value),
                        str(outwards_qty), str(outwards_rate), str(outwards_value),
                        str(closing_qty), str(closing_rate), str(closing_value)
                    ]
                    
                    items.append(item_data)
                    
                    # Print item details
                    print(f"\nItem: {name}")
                    print(f"Parent: {parent}")
                    print(f"Opening: {opening_qty:.2f} units @ {opening_rate:.2f} = {opening_value:.2f}")
                    print(f"Inwards: {inwards_qty:.2f} units @ {inwards_rate:.2f} = {inwards_value:.2f}")
                    print(f"Outwards: {outwards_qty:.2f} units @ {outwards_rate:.2f} = {outwards_value:.2f}")
                    print(f"Closing: {closing_qty:.2f} units @ {closing_rate:.2f} = {closing_value:.2f}")
                    print("-" * 30)
                    
            except Exception as e:
                print(f"Error parsing line: {str(e)}")
                continue
        
        print(f"\nTotal items parsed: {len(items)}")
        return items
            
    except Exception as e:
        print(f"Error in parse_stock_summary: {str(e)}")
        return []

# ---------- PARSE STOCK VOUCHER ----------
def parse_stock_voucher(xml_data):
    root = ET.fromstring(clean_xml(xml_data))
    vouchers = []

    for voucher in root.findall(".//VOUCHER"):
        date = voucher.findtext("DATE", default="").strip()
        vtype = voucher.findtext("VOUCHERTYPE", default="").strip()
        number = voucher.findtext("VOUCHERNUMBER", default="").strip()
        party = voucher.findtext("PARTYNAME", default="").strip()
        category = voucher.findtext("VOUCHERCATEGORY", default="").strip()
        narration = voucher.findtext("Narration", default="").strip()

        # Each VOUCHER may contain multiple INVENTORY_ALLOCATION tags
        for inv in voucher.findall("INVENTORY_ALLOCATION"):
            item = inv.findtext("STOCKITEM", default="").strip()
            qty = inv.findtext("QUANTITY", default="").strip()
            amt = inv.findtext("AMOUNT", default="").strip()
            godown = inv.findtext("GODOWN", default="").strip()

            vouchers.append([
                date, vtype, number, party, category, narration,
                item, qty, amt, godown
            ])
    return vouchers

def parse_accounting_vouchers(xml_data):
    root = ET.fromstring(clean_xml(xml_data))
    vouchers = []

    for voucher in root.findall(".//VOUCHER"):
        date = voucher.findtext("DATE", default="").strip()
        vtype = voucher.findtext("VOUCHERTYPE", default="").strip()
        number = voucher.findtext("VOUCHERNUMBER", default="").strip()
        party = voucher.findtext("PARTYNAME", default="").strip()
        category = voucher.findtext("VOUCHERCATEGORY", default="").strip()
        narration = voucher.findtext("Narration", default="").strip()

        # Nested ACCOUNTING_ALLOCATION entries
        for alloc in voucher.findall("ACCOUNTING_ALLOCATION"):
            ledger = alloc.findtext("LEDGER", default="").strip()
            amount = alloc.findtext("AMOUNT", default="").strip()

            vouchers.append([
                date, vtype, number, party, category, narration, ledger, amount
            ])
    return vouchers

def parse_balance_sheet(xml_data):
    root = ET.fromstring(xml_data)
    bs_names = root.findall(".//BSNAME/DSPACCNAME/DSPDISPNAME")
    bs_amounts = root.findall(".//BSAMT/BSMAINAMT")

    items = []
    for name_elem, amount_elem in zip(bs_names, bs_amounts):
        name = name_elem.text.strip() if name_elem is not None and name_elem.text else "N/A"
        amount = amount_elem.text.strip() if amount_elem is not None and amount_elem.text else "0"
        items.append([name, amount])

    return items

def parse_group_table(data):
    try:
        if not data:
            return []
            
        lines = [line.strip() for line in data.split('\n') if line.strip()]
        groups = []
        
        for line in lines:
            try:
                reader = csv.reader(StringIO(line))
                fields = next(reader)
                
                if len(fields) == 8:
                    group = {
                        'guid': fields[0].strip('"'),
                        'name': fields[1].strip('"'),
                        'parent': fields[2].strip('"'),
                        'primary_group': fields[3].strip('"'),
                        'is_revenue': fields[4].strip('"'),
                        'is_deemed_positive': fields[5].strip('"'),
                        'affects_gross_profit': fields[6].strip('"'),
                        'sort_position': fields[7].strip('"')
                    }
                    groups.append(group)
            except Exception:
                continue
        
        return groups
    except Exception:
        return []

def parse_bills_payable(xml_data):
    try:
        if not xml_data:
            return []
            
        cleaned_data = clean_xml(xml_data)
        root = ET.fromstring(cleaned_data)
        bills = []
        
        bill_fixed_entries = root.findall(".//BILLFIXED")
        
        for i in range(len(bill_fixed_entries)):
            try:
                bill_fixed = bill_fixed_entries[i]
                date = bill_fixed.findtext("BILLDATE", default="").strip()
                ref = bill_fixed.findtext("BILLREF", default="").strip()
                party = bill_fixed.findtext("BILLPARTY", default="").strip()
                
                amount = root.findall(".//BILLCL")[i].text.strip() if i < len(root.findall(".//BILLCL")) else "0"
                due_date = root.findall(".//BILLDUE")[i].text.strip() if i < len(root.findall(".//BILLDUE")) else ""
                overdue = root.findall(".//BILLOVERDUE")[i].text.strip() if i < len(root.findall(".//BILLOVERDUE")) else "0"
                
                bill_data = [ref, date, due_date, amount, party, overdue]
                bills.append(bill_data)
                
            except Exception:
                continue
        
        return bills
        
    except Exception:
        return []

def parse_bills_receivable(xml_data):
    try:
        if not xml_data:
            return []
            
        cleaned_data = clean_xml(xml_data)
        root = ET.fromstring(cleaned_data)
        bills = []
        
        bill_fixed_entries = root.findall(".//BILLFIXED")
        
        for i in range(len(bill_fixed_entries)):
            try:
                bill_fixed = bill_fixed_entries[i]
                date = bill_fixed.findtext("BILLDATE", default="").strip()
                ref = bill_fixed.findtext("BILLREF", default="").strip()
                party = bill_fixed.findtext("BILLPARTY", default="").strip()
                
                amount = root.findall(".//BILLCL")[i].text.strip() if i < len(root.findall(".//BILLCL")) else "0"
                due_date = root.findall(".//BILLDUE")[i].text.strip() if i < len(root.findall(".//BILLDUE")) else ""
                overdue = root.findall(".//BILLOVERDUE")[i].text.strip() if i < len(root.findall(".//BILLOVERDUE")) else "0"
                
                bill_data = [ref, date, due_date, amount, party, overdue]
                bills.append(bill_data)
                
            except Exception:
                continue
        
        return bills
        
    except Exception:
        return []

# ---------- WRITE TO GOOGLE SHEET ----------
def write_to_google_sheet(stock_data, voucher_data, accounting_data, balance_data, group_data, bills_data, bills_receivable_data):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(resource_path("service_account.json"), scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open(GOOGLE_SHEET_NAME)

        def write_sheet(sheet_name, headers, data):
            try:
                try:
                    sheet = spreadsheet.worksheet(sheet_name)
                except gspread.exceptions.WorksheetNotFound:
                    sheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")
                
                sheet.clear()
                data_to_write = [headers] + data
                sheet.update("A1", data_to_write)
                
            except Exception as e:
                raise

        write_sheet("Stock Summary", [
            "Item Name",
            "Opening Qty", "Opening Rate", "Opening Value",
            "Inwards Qty", "Inwards Rate", "Inwards Value",
            "Outwards Qty", "Outwards Rate", "Outwards Value",
            "Closing Qty", "Closing Rate", "Closing Value"
        ], stock_data)
        
        write_sheet("Balance Sheet", ["Account", "Amount"], balance_data)
        write_sheet(
            "Stock Vouchers",
            ["Date", "Voucher Type", "Voucher Number", "Party Name", "Voucher Category", "Narration",
             "Stock Item", "Quantity", "Amount", "Godown"],
            voucher_data
        )
        write_sheet("Accounting Vouchers", 
            ["Date", "Voucher Type", "Voucher Number", "Party Name", "Voucher Category", "Narration", "Ledger", "Amount"],
            accounting_data
        )
        
        if bills_data:
            write_sheet("Bills Payable",
                ["Bill Reference", "Bill Date", "Due Date", "Amount", "Party", "Days Overdue"],
                bills_data
            )
            
        if bills_receivable_data:
            write_sheet("Bills Receivable",
                ["Bill Reference", "Bill Date", "Due Date", "Amount", "Party", "Days Overdue"],
                bills_receivable_data
            )
        
        if group_data:
            group_list = []
            for g in group_data:
                row = [
                    g['guid'],
                    g['name'],
                    g['parent'],
                    g['primary_group'],
                    g['is_revenue'],
                    g['is_deemed_positive'],
                    g['affects_gross_profit'],
                    g['sort_position']
                ]
                group_list.append(row)
            
            write_sheet("Group Table",
                ["Guid", "Name", "Parent", "Primary Group", "Is Revenue", "Is Deemed Positive",
                 "Affects Gross Profit", "Sort Position"],
                group_list
            )
        
    except Exception as e:
        raise

# ---------- ROUTES ----------
@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tally Data Sync</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }
            .button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }
            .status {
                margin-top: 20px;
                padding: 10px;
                border-radius: 4px;
            }
            .success {
                background-color: #dff0d8;
                color: #3c763d;
            }
            .error {
                background-color: #f2dede;
                color: #a94442;
            }
        </style>
    </head>
    <body>
        <h1>Tally Data Sync</h1>
        <p>Click the button below to manually sync data from Tally to Google Sheets.</p>
        <a href="/sync-all" class="button">Sync Now</a>
        <div id="status"></div>
        <script>
            document.querySelector('.button').addEventListener('click', function(e) {
                e.preventDefault();
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = 'Syncing...';
                statusDiv.className = 'status';
                
                fetch('/sync-all')
                    .then(response => response.text())
                    .then(data => {
                        statusDiv.innerHTML = data;
                        statusDiv.className = 'status ' + (data.includes('successfully') ? 'success' : 'error');
                    })
                    .catch(error => {
                        statusDiv.innerHTML = 'Error: ' + error;
                        statusDiv.className = 'status error';
                    });
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/sync-all')
def sync_all_reports():
    try:
        xml_stock = fetch_tally_stock_summary()
        xml_voucher = fetch_tally_stock_voucher()
        xml_accounting = fetch_accounting_vouchers()
        xml_balance = fetch_tally_balance_sheet()
        xml_group = fetch_tally_group_table()
        xml_bills = fetch_tally_bills_payable()
        xml_bills_receivable = fetch_tally_bills_receivable()

        stock_data = parse_stock_summary(xml_stock)
        voucher_data = parse_stock_voucher(xml_voucher)
        accounting_data = parse_accounting_vouchers(xml_accounting)
        balance_data = parse_balance_sheet(xml_balance)
        group_data = parse_group_table(xml_group)
        bills_data = parse_bills_payable(xml_bills)
        bills_receivable_data = parse_bills_receivable(xml_bills_receivable)

        if not any([stock_data, voucher_data, accounting_data, balance_data, group_data, bills_data, bills_receivable_data]):
            return "No data found. Check Tally configuration."

        write_to_google_sheet(stock_data, voucher_data, accounting_data, balance_data, group_data, bills_data, bills_receivable_data)
        return "Data synced successfully!"
    except Exception as e:
        return f"Error during sync: {str(e)}"

def periodic_sync():
    """Background thread function to sync data every 2 hours"""
    while True:
        try:
            sync_all_reports()
            time.sleep(2 * 60 * 60)  # Sleep for 2 hours
        except Exception:
            time.sleep(60)  # If error occurs, wait 1 minute before retrying

# ---------- OPEN BROWSER ON START ----------
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

# ---------- MAIN ----------
if __name__ == '__main__':
    # Start periodic sync in background
    sync_thread = threading.Thread(target=periodic_sync, daemon=True)
    sync_thread.start()
    
    # Open browser after 1 second, non-blocking
    threading.Timer(1, open_browser).start()
    
    # Run Flask server with debug=False for production/executable
    app.run(debug=False)
