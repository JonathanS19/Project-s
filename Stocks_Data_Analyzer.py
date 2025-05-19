#Imports 

import re
import csv
import ast
import pandas as pd
import os
import datetime
import google.generativeai as genai
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException
from groq import Groq
import google.generativeai as genai


# Open and Download Nifty50 list
def download_nifty():
    url = "https://www.5paisa.com/nifty-50-stocks-list"

    folder_path = "NSE DATA"
    os.makedirs(folder_path,exist_ok=True)

    file_name = "Stocks_page.html"
    Store_path = os.path.join(folder_path,file_name)


    driver = webdriver.Chrome()
    driver.get(url)


    count = 0

    while True:
        try:
            try:
                # Close the subscribe button
                sub_btn = WebDriverWait(driver,10).until(
                    EC.element_to_be_clickable((By.ID,'notify-visitors-confirm-popup-btn-negative'))) 
                print("Subscribe popup closed successfully.")
                
                # Close the popup
                close_btn = WebDriverWait(driver, 20).until(
                   EC.element_to_be_clickable((By.ID, "nv_js-leadform-close-button_4336"))
                    )
                close_btn.click()
                print("Popup closed successfully.")

                html = driver.page_source
                with open(Store_path,"w",encoding = "utf-8") as f:
                    f.write(html)
                print("NIfty Top 50 Downloaded and Stored !!")
                break
            
            except:
            # Download the Webpage
                html = driver.page_source
                with open(Store_path,"w",encoding = "utf-8") as f:
                    f.write(html)
                print("NIfty Top 50 Downloaded and Stored !!")
                break

        except(AttributeError,InvalidSessionIdException,TimeoutException):
            if count<2:
                driver.refresh()
            elif count == 2:
                driver.close()
                driver.get(url)
            else:
                driver.close()
                print("Error!!")
            count+=1
        

    driver.close()
    print('\nNifty Downloading Module Executed Successfully\n')

download_nifty()


# Open downloaded webpage and extract the company names alone
with open('NSE DATA\Stocks_page.html','r',encoding="utf-8") as f:
    text = f.read()

soup = BeautifulSoup(text,'lxml')
company_names = []

Nifty_company_names = soup.find_all(id='stock_name')
for company in Nifty_company_names:
    company_names.append(company.text)

# Use Gemini api to obtain their NSE codes
from google import genai

client = genai.Client(api_key="AIzaSyCRyNkjJeC0MQjsHt3JJgEZgyKB7bDtfBk")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=f"Give me the nse codes {company_names} of these companies alone nothing else"
)
company_codes = response.text

print("Model Response recieved !!")


# Converting Large String List into List
company_codes = ast.literal_eval(company_codes)
company_codes
# Occasionaly the model provides results with words that cause error here


# Downloading and storing Stocks Html pages

driver = webdriver.Chrome()
folder_name = "NSE Data"
os.makedirs(folder_name,exist_ok=True)
cnt = i = 0

for company in company_codes:
    url = f"https://finance.yahoo.com/quote/{company}.NS/history/"
    file_name = f"{company}_Data.html"
    html_file_path = os.path.join(folder_name,file_name)
    
    if not os.path.isfile(html_file_path):
        while i < 3:

            try:
                driver.get(url)
                with open(html_file_path,'w',encoding="utf-8") as file:
                    file.write(driver.page_source)
                print(f"{cnt}) {company} Html Stored !!")
                break

            except(AttributeError,InvalidSessionIdException):
                if i < 2:
                    driver.refresh()
                elif i == 2:
                    driver.close()
                    driver.get(url)
                else:
                    driver.close()
                    print("Webpage Error!!")
                print(f"{company} Iteration no :{i}")
                i+=1
    else:
        cnt+=1
        print(f"{cnt}) {company} Html already exists !!")

driver.close()


# Extracting and Storing the Data from html files 
folder_name = "NSE DATA"
csv_folder_name = "Stock's Data"
headers = ["Dates","Open","High","Low","Close","Adj Close","Volume"]
os.makedirs(csv_folder_name,exist_ok=True)

for company in company_codes:
    file_name = f"{company}_Data.html"
    csv_name = f"{company}_Data.csv"

    html_file_path = os.path.join(folder_name,file_name) 
    csv_file_path = os.path.join(csv_folder_name,csv_name) 

    if not os.path.isfile(csv_file_path):
        with open(html_file_path,'r',encoding="utf-8") as file :
            page = file.read()

        with open(csv_file_path,'w',encoding="utf-8") as file:
            writer = csv.writer(file)

            soup = BeautifulSoup(page,'lxml')
            writer.writerow(headers)

            datas = soup.find('tbody').find_all('tr')

            for data in datas:
                csv_list = []
                elements = data.find_all('td')

                for element in elements:
                    csv_list.append(element.text.strip())

                if csv_list:
                    writer.writerow(csv_list)

        print(f"{company} Data Stored !!")
        
    else:
        print(f"{company} Data Already Stored !!")
    
if (len(os.listdir("Stock's Data"))) == 50:
    print("\nNifty 50 Data Stored Completely !!")
else:
    print("Something is missing !!")


# Data to feed the model
folder_name = "Stock's Data"
file_name = "CIPLA_Data.csv"
file_path = os.path.join(folder_name,file_name)

with open(file_path,'r',encoding='utf-8') as file:
    data = file.read()
  
# Using LLM's to Derive Insights 

from google import genai

client = genai.Client(api_key="AIzaSyCRyNkjJeC0MQjsHt3JJgEZgyKB7bDtfBk")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=f"As a professional stock trader give me your opinion on the data, {data}"
)
print(response.text)


# Creating a data updater
from datetime import date

folder_name = "NSE DATA"
file_name = "HDFCBANK_Data.html"
file_path = os.path.join(folder_name,file_name)

with open(file_path,'r',encoding='utf-8') as file:
    page = file.read()

soup = BeautifulSoup(page,'lxml')

datas = soup.find('tbody').find_all('tr')
current_date = re.findall(r'([A-Za-z]+ \d+)',datas[0].find(class_='yf-1jecxey').text)
latest_date = (date.today()).day

print(current_date[0],latest_date)

# Make the List downloader and name gatherer into a function get it to replenish the new values and check what is missing 
from datetime import date
from datetime import datetime

current_date = (date.today()).strftime("%m-%d")
folder_name = "NSE DATA"

for company in company_codes:
    file_name = f"{company}_Data.html"
    file_path = os.path.join(folder_name,file_name)

    with open(file_path,'r',encoding='utf-8') as file:
        page = file.read()

    soup = BeautifulSoup(page,'lxml')
    datas = soup.find('tbody').find_all('tr')
    last_date = re.findall(r'([A-Za-z]+ \d+)',datas[0].find(class_='yf-1jecxey').text)
    last_date = datetime.strptime(last_date[0],"%B %d").strftime("%m-%d")

    if last_date == current_date:
        print(f"{company} updated")
    else:

        print(f"{company} not updated, Current date : {current_date} and Last updated : {last_date}")


    
