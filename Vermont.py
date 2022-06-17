from selenium import webdriver
import os
import time
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = '/Users/salpecoraro/PycharmProjects/covidAutomation2/covidproject-313000-f1858a4a2dc7.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
VERMONT = '16xQi0Cg8jxVyqmdbT5sk4rhH8krydTzvhrRXnJZVTp8'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

VIRGINIA = '18seMOiPIf_-XOKZ-e3Q4acutZM9RN-JrXeU3CU7I6wI'
service = build('sheets','v4', credentials = creds)

sheet = service.spreadsheets()

def setting_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    return chrome_options;

def enable_download(driver,downloadPath):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "/Users/salpecoraro/Downloads"}}
    driver.execute("send_command", params)

def isFileDownloaded(download_dir,filename):
    file_path = download_dir+"/"+filename
    print(file_path)
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.isfile(file_path):
        print("File Downloaded successfully..")

downloadPath = "/Users/salpecoraro/Downloads"


def Vermont():
    pathname = "/Users/salpecoraro/Downloads/"
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
    enable_download(driver, downloadPath)
    driver.get("https://geodata.vermont.gov/datasets/VCGI::vt-covid-19-cases-by-county-time-series/explore")
    time.sleep(2.5)
    driver.execute_script(
        "return document.getElementsByClassName('hub-toolbar-inner hide-overflow')[0].getElementsByTagName('button')[2].click()")
    time.sleep(2.5)
    driver.execute_script(
        "return document.getElementsByClassName('dataset-download-card')[0].querySelector('hub-download-card').shadowRoot.querySelector('calcite-card > div > calcite-button').click()")

    isFileDownloaded(downloadPath, "VT_COVID-19_Cases_by_County_Time_Series.csv")
    df = pd.read_csv(downloadPath + "/VT_COVID-19_Cases_by_County_Time_Series.csv")
    covidList = df.values.tolist()
    print(df)
    for x in covidList:
        x[2] = x[2].split(' ', 1)[0]
        print(x)
    result = sheet.values().update(spreadsheetId=VERMONT, range="Sheet1!A2",
                                   valueInputOption="USER_ENTERED",
                                   body={"values": covidList}).execute()
Vermont()