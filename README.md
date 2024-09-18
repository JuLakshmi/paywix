This code syncs data between PostgreSQL and Google Sheets, allowing for automatic updates and management of materialized views within a PostgreSQL database. 

## Prerequisites

1. **Python**: Ensure you have Python 3.x installed.
2. **PostgreSQL**: Install PostgreSQL and have it running.
3. **Google Sheets API**: Set up Google Sheets API access with proper credentials.

## Setup

1. Install required dependencies:
    ```bash
    make setup
    ```

2. Place your `credentials.json` file for Google Sheets API in the project root directory (or specify its location in the config).

## Configuration

The configuration is stored in `config.json`. Below is a description of the configuration fields.

### `config.json`

```json
{
    "postgres": {
        "host": "localhost",
        "database": "prod21aug",
        "user": "postgres",
        "password": ""
    },
    "google_sheets": {
        "spreadsheet_id": "1C5sNC1B0VlUsopYMFDJfc0o833a2Ow0D3PGT_pu5_J4",
        "sheet_name": "06-09-2024|21:23"
    },
    "service_account": {
        "credentials_file": "credentials.json"
    },
    "db_views": {
        "materialized_view_name": "analytics.homework_details_materialized_view",
        "view_name": "analytics.homework_details_view"
    }
}
```

#### Sections:

1. **`postgres`: PostgreSQL Connection Details**
   - **`host`**: The hostname where PostgreSQL is running.
   - **`database`**: The name of the database to connect to.
   - **`user`**: PostgreSQL username.
   - **`password`**: Password for authentication.

2. **`google_sheets`: Google Sheets Configuration**
   - **`spreadsheet_id`**: The ID of the Google Sheet you want to update.
   - **`sheet_name`**: The specific sheet within the spreadsheet to update.
   > **Note**: Change these values to match the correct Spreadsheet ID and sheet name.

3. **`service_account`: Google Service Account Credentials**
   - **`credentials_file`**: Path to your `credentials.json` file for authenticating the Google Sheets API.
   > **Note**: Ensure that this file is placed in the project root or provide the full path to the file.

4. **`db_views`: PostgreSQL View and Materialized View Details**
   - **`materialized_view_name`**: The name of the materialized view in your PostgreSQL database.
   - **`view_name`**: The name of the standard view in your database.
   > **Note**: Ensure that the names correspond to the actual view names in your PostgreSQL database, including the schema name (e.g., `analytics.homework_details_materialized_view`).

## Makefile Commands

- **`update-materialized-view`**:  
  This command updates the materialized view in the PostgreSQL database.
    ```bash
    make update-materialized-view
    ```

- **`execute-view-update-sheet`**:  
  This command runs the given view from config file and updates the Google Sheet with the corresponding data.
    ```bash
    make execute-view-update-sheet
    ```

- **`update-sheet-and-materialized-view`**:  
  This command updates the Google Sheet first, by using that sheet name refreshes the materialized view in PostgreSQL.
    ```bash
    make update-sheet-and-materialized-view
    ```

## Usage

1. Ensure PostgreSQL is running and accessible.
2. Update the configuration in `config.json` with the correct details.
3. Use the provided Makefile commands to run the desired operations.

## Notes

- Ensure that the Google service account has access to the specified Google Sheet.
- Make sure that the PostgreSQL user has the necessary permissions to create and update views.
