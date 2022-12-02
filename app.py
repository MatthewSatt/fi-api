from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def root():
    final_data = {}
    # ticker = ticker.lower()
    r = requests.get("https://seekingalpha.com/api/v3/symbols/big/fundamentals_metrics?period_type=annual&statement_type=balance-sheet&target_currency=USD")
    data = r.json()
    
    #assets
    current_assets_category = get_current_assets_category(data)
    category_rows = get_category_rows(current_assets_category)
    total_current_assets = get_total_current_assets(category_rows)
    total_current_assets_cells = get_total_current_asset_cells(total_current_assets)
    total_current_assets_value = get_total_current_assets_value(total_current_assets_cells)
    final_data['total_current_asset_value'] = total_current_assets_value

    #total_liabilities
    total_liabilities_category = get_total_liabilities_category(data)
    category_rows = get_total_liabilities_rows(total_liabilities_category)
    total_liabilities = get_total_liabilities_row(category_rows)
    total_liabilities_cells = get_total_liabilities_cells(total_liabilities)
    total_liabilities_value = get_total_liabilities_value(total_liabilities_cells)
    final_data['total_liabilities_value'] = total_liabilities_value

    # common equity
    return final_data


## Asset Functions
def get_current_assets_category(raw_data):
    for category in raw_data:
        if category['title'] == 'Current Assets':
            return category

def get_category_rows(category):
    return category.get('rows', [])

def get_total_current_assets(category_rows):
    for row in category_rows:
        if row['name'] == 'total_current_assets':
            return row

def get_total_current_asset_cells(total_current_assets):
    return total_current_assets.get('cells', [])

def get_total_current_assets_value(total_current_assets_cells):
    for cell in total_current_assets_cells:
        if cell['name'] == 'Last Report':
            return cell['value']


# liabilities
def get_total_liabilities_category(data):
    for category in data:
        if category['title'] == 'Long-Term Liabilities':
            return category

def get_total_liabilities_rows(category):
    return category.get('rows', [])

def get_total_liabilities_row(category_rows):
    for row in category_rows:
        if row['name'] == 'total_liabilities':
            return row

def get_total_liabilities_cells(total_liabilities):
    return total_liabilities.get('cells', [])

def get_total_liabilities_value(liabilities):
    for cell in liabilities:
        if cell['name'] == 'Last Report':
            return cell['value']
