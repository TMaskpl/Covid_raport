import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import base64
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import ssl
import os
import sys
from pathlib import Path

mails = ['mail1', 'mail2']

cd = datetime.today().strftime('%Y-%m-%d')

def polska_covid():
    global cd
    resp = requests.get('https://news.google.com/covid19/map?hl=pl&mid=%2Fm%2F05qhw&gl=PL&ceid=PL%3Apl').content

    jsoup = BeautifulSoup(resp, 'html.parser')
    div = jsoup.find('tbody', attrs={'class':'ppcUXd'})
    div2 = jsoup.find('tr', attrs={'class':'sgXwHf wdLSAe ROuVee'})

    print('Polska ' + cd)
    dict = []
    for g in div2.find_all('td', {'class':'l3HOY'}):
        n = g.get_text()
        dict.append(n.replace('\xa0', ''))
    print(f'Łączna liczba zarażonych: {dict[0]}, Nowych przypadków: {dict[1]}, Przypadki na 1 mln osób: {dict[3]}, Zgony: {dict[4]} ')

def all_covid():
    global cd
    global dict
    resp = requests.get('https://news.google.com/covid19/map?hl=pl&gl=PL&ceid=PL%3Apl').content

    jsoup = BeautifulSoup(resp, 'html.parser')
    div = jsoup.find('tbody', attrs={'class':'dppcUXd'})
    div2 = jsoup.find_all('tr', attrs={'class':'sgXwHf wdLSAe YvL7re'})
    print(cd)

    dict = list()
    row = list()
    for g in div2:
        k = re.sub(r'[\xa0]', '', g.get_text(' '))
        row = k.split(' ')
        row0 = row[0]
        row1 = row[1]
        row2 = row[2]
        if not row0.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])) and not row1.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])) and row2.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])):
            print(f'{row[0]} {row[1]}, : Łącznie: {row[2]}, Nowych przypadków: {row[3]}, Zgony: {row[5]} ')
        if not row0.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])) and row1.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])):
            print(f'{row[0]} : Łącznie: {row[1]}, Nowych przypadków: {row[2]}, Zgony: {row[4]} ')
        if not row0.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])) and not row1.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])) and not row2.startswith(tuple(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])):
            print(f'{row[0]} {row[1]} {row[2]}, : Łącznie: {row[3]}, Nowych przypadków: {row[4]}, Zgony: {row[6]} ')

if os.path.isfile("covid_raport.txt"):
    os.remove("covid_raport.txt")

original_stdout = sys.stdout

with open("covid_raport.txt", "a") as f:
    sys.stdout = f
    all_covid()
    sys.stdout = original_stdout
f.close()

def send_mail(toaddr):
    global DATA
    global cd
    LOG = open('covid_raport.txt')
    DATA = LOG.read()

    fromaddr = 'biuro@tmask.pl'

    message = # Hasło do poczty z której wysyłamy raport

    import smtplib
    from email.message import EmailMessage
    try:
        msg = EmailMessage()
        msg['From'] = fromaddr
        msg['Subject'] = 'Covid Raport World – %s' % cd
        msg['To'] = toaddr
        msg.set_content(DATA)

        s = smtplib.SMTP('ssl0.ovh.net', 587)
        s.login(fromaddr, message)
        s.send_message(msg)
        s.quit()
        print(f'Mail wysłany do: {toaddr}')
    except:
        print("Błąd wysyłania :( ")

for mail in mails:
    send_mail(mail)
