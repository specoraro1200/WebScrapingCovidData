from selenium import webdriver
import os
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'covidproject-313000-f1858a4a2dc7.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
TEXAS = '1YT0JPblznqQcHTcAKCBYaOgb2yIYXIqVlO6-uuWIVOY'

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
def Texas():

    page = requests.get("https://dshs.texas.gov/coronavirus/AdditionalData.aspx")
    soup = BeautifulSoup(page.text, 'html.parser')
    probableCases = soup.find("a", title="Probable Cases over Time by County").get('href')
    confirmedCases = soup.find("a", title="Confirmed Cases over Time by County").get('href')
    confirmedDeaths = soup.find("a", title="Fatalities over Time by County").get('href')
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
    enable_download(driver, downloadPath)
    driver.get("https://dshs.texas.gov/"+probableCases)
    isFileDownloaded(downloadPath,'Texas COVID-19 Probable Cases by County.xlsx')
    driver.get("https://dshs.texas.gov/"+confirmedDeaths)
    isFileDownloaded(downloadPath,"Texas COVID-19 Fatality Count Data by County.xlsx")
    driver.get("https://dshs.texas.gov/"+confirmedCases)
    isFileDownloaded(downloadPath,"Texas COVID-19 Case Count Data by County.xlsx")
    df = pd.read_excel(downloadPath + "/Texas COVID-19 Case Count Data by County.xlsx")
    df = df.fillna("")
    df = df.iloc[1:]
    covidList = df.values.tolist()

    df2 = pd.read_excel(downloadPath +"/Texas COVID-19 Probable Cases by County.xlsx")
    df2 = df2.fillna("")
    df2 = df2.iloc[1:]

    covidList2 = df2.values.tolist()

    df3 = pd.read_excel(downloadPath + "/Texas COVID-19 Fatality Count Data by County.xlsx")
    df3 = df3.fillna("")
    df3 = df3.iloc[1:]

    covidList3 = df3.values.tolist()

    for x in range(len(covidList[1])):
        if x >= 1:
            covidList[0][x] = covidList[0][x].split(' ', 1)[1]
    for x in range(len(covidList2[1])):
        if x >= 1:
            covidList2[0][x] = covidList2[0][x].split(' ', 1)[1]
    for x in range(len(covidList3[1])):
        if x >= 1:
            covidList3[0][x] = covidList3[0][x].split(' ', 1)[1]
    result = sheet.values().update(spreadsheetId=TEXAS, range="ConfirmedCases!A1",
                                   valueInputOption="USER_ENTERED",
                                   body={"values": covidList}).execute()
    result = sheet.values().update(spreadsheetId=TEXAS, range="ProbableCases!A1",
                                   valueInputOption="USER_ENTERED",
                                   body={"values": covidList2}).execute()
    result = sheet.values().update(spreadsheetId=TEXAS, range="ConfirmedDeaths!A1",
                                   valueInputOption="USER_ENTERED",
                                   body={"values": covidList3}).execute()
Texas()