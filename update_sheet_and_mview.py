import psycopg2
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import json
from update_materialized_view import fetch_data_from_google_sheet, create_or_refresh_materialized_view, connect_to_postgresql

def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def fetch_query_results(query, conn_params):
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        formatted_rows = []
        for row in rows:
            formatted_row = []
            for item in row:
                if isinstance(item, datetime):
                    formatted_row.append(item.strftime('%Y-%m-%d %H:%M:%S'))
                elif isinstance(item, (dict, list, set)):
                    formatted_row.append(str(item))
                else:
                    formatted_row.append(str(item))
            formatted_rows.append(formatted_row)
        cursor.close()
        conn.close()
        return [colnames] + formatted_rows
        
    except Exception as e:
        print(f"Error running query: {e}")
        return []

def create_sheet(service, spreadsheet_id, sheet_title):
    requests = [{
        "addSheet": {
            "properties": {
                "title": sheet_title
            }
        }
    }]
    body = {
        "requests": requests
    }
    response = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()
    print(f"Sheet '{sheet_title}' created.")
    return response

def update_google_sheet(spreadsheet_id, values, creds_file):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=creds)
    
    sheet_title = datetime.now().strftime('%d-%m-%Y|%H:%M')
    create_sheet(service, spreadsheet_id, sheet_title)
    range_name = f"{sheet_title}!A1"
    
    body = {
        'values': values
    }

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} cells updated in sheet '{sheet_title}'.")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")
    return sheet_title 

def main():
    config = load_config()

    conn_params = config['postgres']
    
    spreadsheet_id = config['google_sheets']['spreadsheet_id']
    creds_file = config['service_account']['credentials_file']
    view_name = config['db_views']['view_name']
    materialized_view_name = config['db_views']['materialized_view_name']
    query = f'SELECT * FROM {view_name};'

    query_results = fetch_query_results(query, conn_params)
    
    # print("Query Results:", query_results)
    
    sheet_name = update_google_sheet(spreadsheet_id, query_results, creds_file)
    df = fetch_data_from_google_sheet(spreadsheet_id, sheet_name, creds_file)
    if df.empty:
        print("No data to process.")
        return
    conn = connect_to_postgresql(conn_params)

    if not conn:
        return

    create_or_refresh_materialized_view(conn, df, materialized_view_name)

    conn.close()


if __name__ == "__main__":
    main()
