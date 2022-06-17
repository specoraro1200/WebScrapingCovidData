import pandas as pd
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

import pandas as pd

##gives authorization to access georgia visual data spreadsheet
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
OKLAHOMA = '1bOfsKTWoBXUGiaCBmhp9ZnDmOMbd2IKF2xJQDvfh7Y0'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets','v4', credentials = creds)
sheet = service.spreadsheets()

oklahoma_df = pd.read_csv('/Users/salpecoraro/Downloads/Georgia Visual Data (Updated Daily) - Sheet1.csv')

oklahoma_filled = oklahoma_df.fillna("")

oklahoma_filled = oklahoma_filled.values.tolist()
print(len(oklahoma_filled))
##converts values in georgia visual data spreadsheet into a dataframe
source_sheet_instance = source_sheet.get_worksheet(0)
source_data = pd.DataFrame(source_sheet_instance.get_all_records())

##gives authorization to access Update Georgia spreadsheet
target_sheet = client.open("Update Georgia")
target_instance = target_sheet.get_worksheet(1)

##updates the Georgia Data tab on the Update Georgia spreadsheet with the contents of that dataframe
target_instance.update([source_data.columns.values.tolist()]+source_data.values.tolist(), value_input_option = "USER_ENTERED")
