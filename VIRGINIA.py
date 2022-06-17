import pandas as pd
from datetime import date
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Put your credential path here
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Distinct url id of spreadsheet
VIRGINIA = '1KCOjTShCfzu3TV0PSUIn-1r6tuadFHfiv5QFb-hUr6U'
service = build('sheets','v4', credentials = creds)

sheet = service.spreadsheets()

# def setting_chrome_options():
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument('--no-sandbox')
#     return chrome_options;

# def enable_download(driver,downloadPath):
#     driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
#     params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "/Users/salpecoraro/Downloads"}}
#     driver.execute("send_command", params)

# def isFileDownloaded(download_dir,filename):
#     file_path = download_dir+"/"+filename
#     print(file_path)
#     while not os.path.exists(file_path):
#         time.sleep(1)
#     if os.path.isfile(file_path):
#         print("File Downloaded successfully..")

# Download path for where your downloaded VA source will be
downloadPath = "/Users/salpecoraro/Downloads"

def Virginia():
    # page = requests.get("https://www.vdh.virginia.gov/coronavirus/",verify = False)
    # soup = BeautifulSoup(page.text, 'html.parser')
    # titles = soup.find("a",text="VDH-COVID-19-PublicUseDataset-Cases").get('href')
    # driver = webdriver.Chrome('/usr/local/bin/chromedriver', options=setting_chrome_options())
    # enable_download(driver,downloadPath)
    # driver.get(titles)
    # driver.execute_script("return document.getElementsByClassName('btn btn-simple btn-sm download')[0].click()")
    # driver.execute_script("return document.getElementsByClassName('featured-download-links')[0].getElementsByClassName('download-link')[0].getElementsByTagName('a')[0].click()")
    # isFileDownloaded(downloadPath,"VDH-COVID-19-PublicUseDataset-Cases.csv")
    df = pd.read_csv(downloadPath + "/VDH-COVID-19-PublicUseDataset-Cases.csv")
    #os.remove(downloadPath+"/VDH-COVID-19-PublicUseDataset-Cases.csv")
    today = date.today()
    today = str(today)
    covidList = df.values.tolist()
    for x in covidList:
        if x[2] == "Charlotte" or x[2] == "Fairfax" or x[2] == "Frederick":
            x[2] += "."
        x.append(today)
    #result = sheet.values().update(spreadsheetId=VIRGINIA, range="Sheet1!A2",
    #                              valueInputOption="USER_ENTERED",
    #                               body={"values": covidList}).execute()

Virginia()