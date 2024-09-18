import json
import psycopg2
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd

def load_config(filename='config.json'):
    """Load configuration from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def fetch_data_from_google_sheet(spreadsheet_id, sheet_name, credentials_file):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    creds = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=SCOPES)
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    
    values = sheet.get('values', [])
    
    if not values:
        print("No data found.")
        return pd.DataFrame()
    
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def connect_to_postgresql(conn_params):
    try:
        conn = psycopg2.connect(**conn_params)
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def create_or_refresh_materialized_view(conn, df, view_name):
    cursor = conn.cursor()
    
    schema_name, view_name = view_name.split('.', 1)
    materialized_view_name = f'{schema_name}."{view_name}"'
 
    cursor.execute(f"DROP MATERIALIZED VIEW IF EXISTS {materialized_view_name};")
    
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    formatted_data = ', '.join(cursor.mogrify(f"({placeholders})", tuple(row)).decode('utf-8') for row in df.values.tolist())
    
    create_view_query = f"""
    CREATE MATERIALIZED VIEW {materialized_view_name} AS
    SELECT * FROM (
        VALUES {formatted_data}
    ) AS data ({columns});
    """

    try:
        cursor.execute(create_view_query)
        conn.commit()
        print(f"Materialized view '{view_name}' created or refreshed successfully.")
    except Exception as e:
        print(f"Error creating or refreshing materialized view: {e}")
    
    cursor.close()

def main():
    config = load_config()
    
    spreadsheet_id = config['google_sheets']['spreadsheet_id']
    sheet_name = config['google_sheets']['sheet_name']
    creds_file = config['service_account']['credentials_file']
    view_name = config['db_views']['materialized_view_name']
 
    conn_params = config['postgres']

    df = fetch_data_from_google_sheet(spreadsheet_id, sheet_name, creds_file)
    if df.empty:
        print("No data to process.")
        return
    
    conn = connect_to_postgresql(conn_params)
    if not conn:
        return
    
    create_or_refresh_materialized_view(conn, df, view_name)
    conn.close()

if __name__ == "__main__":
    main()
