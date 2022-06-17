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

PENSYLVANIA = '1Wlt6SfuSo6wwQfeWfARWwo4HXaFx23Uuao-2iSoDTWY'
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


def Pensylvania():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
    enable_download(driver, downloadPath)
    driver.get("https://data.pa.gov/Covid-19/COVID-19-Aggregate-Death-Data-Current-Daily-County/fbgu-sqgp")
    driver.execute_script("document.getElementsByClassName('btn btn-simple btn-sm download')[0].click()")
    driver.execute_script("document.querySelector('#export-flannel > section > ul > li:nth-child(1) > a').click()")
    isFileDownloaded(downloadPath,"COVID-19_Aggregate_Death_Data_Current_Daily_County_Health.csv")
    driver.get("https://data.pa.gov/Covid-19/COVID-19-Aggregate-Cases-Current-Daily-County-Heal/j72v-r42c")
    driver.execute_script("document.getElementsByClassName('btn btn-simple btn-sm download')[0].click()")
    driver.execute_script("document.querySelector('#export-flannel > section > ul > li:nth-child(1) > a').click()")
    isFileDownloaded(downloadPath,"COVID-19_Aggregate_Cases_Current_Daily_County_Health.csv")
    df = pd.read_csv(downloadPath + "/COVID-19_Aggregate_Death_Data_Current_Daily_County_Health.csv")

    df = df.fillna("")
    df["Date of Death"] = pd.to_datetime(df["Date of Death"])
    df = df.sort_values(by="Date of Death")
    df['Date of Death'] = df['Date of Death'].astype(str)
    df = df.drop('Latitude', 1)
    df = df.drop('Georeferenced Latitude & Longitude', 1)
    df = df.drop('Longitude', 1)
    df = df.drop('County FIPS Code', 1)
    df = df.drop('Total Death Rate', 1)
    df = df.drop('7-day Average New Death Rate', 1)
    df = df.drop('New Deaths Rate', 1)
    df = df.drop('7-day Average New Deaths', 1)
    df = df.drop('New Deaths', 1)
    df = df.iloc[:, :-1]

    covidList = df.values.tolist()

    result = sheet.values().update(spreadsheetId=PENSYLVANIA, range="Deaths!A2",
                                   valueInputOption="USER_ENTERED",
                                   body={"values": covidList}).execute()

    df = pd.read_csv(downloadPath + "/COVID-19_Aggregate_Cases_Current_Daily_County_Health.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")
    df['Date'] = df['Date'].astype(str)
    df = df.drop('Latitude', 1)
    df = df.drop('Longitude', 1)
    df = df.drop('County FIPS Code', 1)
    df = df.drop('Georeferenced Lat & Long',1)
    df = df.drop('Cumulative Case Rate', 1)
    df = df.drop('7-Day Average New Case Rate',1)
    df = df.drop('New Case Rate',1)
    df = df.drop('Population (2019)',1)
    df = df.drop('7-day Average New Cases',1)
    df = df.drop('New Cases',1)
    covidList = df.values.tolist()
    print(df)

    result = sheet.values().update(spreadsheetId=PENSYLVANIA, range="Cases!A2",
                                   valueInputOption="USER_ENTERED",
                                   body={"values": covidList}).execute()
Pensylvania()