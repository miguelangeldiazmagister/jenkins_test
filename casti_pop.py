import requests
from datetime import datetime
import time
import os,sys
import pandas as pd
import zipfile,coloredlogs,logging
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
path_CURRENT=os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_CURRENT+'/../')
from utilities.data import paths
from utilities.master import totalTime
#=====================================================================
#=====================================================================
#=====================================================================
print("======================================================")
print("[START-TIME]["+str(datetime.now())+"]")
print("[Script]["+os.path.basename(__file__)+"]")
load_dotenv()
start=datetime.now()
session = requests.session()
load_dotenv()
filename='ptti_catalogo'
name_zip=filename+'.zip'
name_xlsx=filename+'.xlsx'
final_path = paths['logs'] + name_xlsx
user = os.getenv('PTTI_USER3')
pasw = os.getenv('PTTI_PASSWORD3')
try:
    burp2_url = "https://ptti.es.telefonica:443/siteminderagent/login.fcc?TYPE=33554433&REALMOID=06-0003e523-0897-1e22-b56e-28f60a240000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-J%2bWkOwjv2OeQBZGNYCBVI9lUfKNhw4CeDCkcltwuN8qZ7WH0yUJ%2bVhrF5Y%2fv6R3E&TARGET=-SM-http%3a%2f%2fptti%2ees%2etelefonica%2f"
    burp2_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://ptti.es.telefonica", "Connection": "close", "Referer": "https://ptti.es.telefonica/siteminderagent/login.fcc?TYPE=33554433&REALMOID=06-0003e523-0897-1e22-b56e-28f60a240000&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-J%2bWkOwjv2OeQBZGNYCBVI9lUfKNhw4CeDCkcltwuN8qZ7WH0yUJ%2bVhrF5Y%2fv6R3E&TARGET=-SM-http%3a%2f%2fptti%2ees%2etelefonica%2f", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1"}
    burp2_data = {"USER": user, "PASSWORD": pasw, "SMENC": "utf-8", "SMLOCALE": "US-EN", "target": "http://ptti.es.telefonica/", "smquerydata": '', "smauthreason": "0", "smagentname": "J+WkOwjv2OeQBZGNYCBVI9lUfKNhw4CeDCkcltwuN8qZ7WH0yUJ+VhrF5Y/v6R3E", "postpreservationdata": ''}
    response2 = session.post(burp2_url, headers=burp2_headers, data=burp2_data,verify=False)
    string_correct = "Aviso_Legal"
    if string_correct in response2.text:
        print("Usuario loggeado")
    else:
        raise Exception("Usuario incorrecto")
    burp0_url = "https://ptti.es.telefonica:443/informeExcelServiciosComerciales.do?accion=informeServiciosComercialesExcel"
    burp0_cookies = {"SMSESSION": "KD5Rs95Hse/NNXj6Ynvs9AohxmuzOkhhFIyWlAwIwqfN5+w8BWxhvETwAkwqlNm4bR5gIaT0i4u+0J46Jg8tf338aH12qtEE6wVIFFTPK+kh+2tg/wFkKC6LIqYwdZgHQxqR5rnZD5GExRzObLSFSTNdmJ0ap47AQfC5cfglJUF5zEc7+sVDEFiMoQN8ZhGH/hKYj/xFYB0VH5TijD+d3qQkFNmj5T3y0vCJ2se4ryG3XsFql+C0RmuhfsYUnJ2SUYR28TfGEoCi0G1Gi5zoeOtkmWWTTvXudy+HFLl9qaE8I8ODD+huJjZ+vduqDYUNX84RHVV4uC9zpNzfiYuAORbxt+GTs4Jm7Qh3cYEsxMwFxP/kmsbusBzed/64HcM8vyFWlqJtifrDPtZX214JySQMQPJzMrpfflyoClVxClceBEebYDGuWlB9+TexBGG3Crw7irqj/V38DZU1joKzRazWVrSpd2DoxOXQcoVUNUD3XkmBduD/FgOfskKJOmfSa4ytjDq0VcmekEWLK7hTLrHKBO9Tpd73XKnFIkOi98eCF/URmI2OLqAYi6pmqpEM6KYhaLG1VjNeIoL3CP3h3UtMJ2a4SXyAPzrv2Z7Lf85jxIURAlrULBNXVVNyAGeX7BliMlR22Be7i9Nvj00iOneCcwQ7S+FnFxBKTjxA45jf0s5D62xOWRLxCG6sRGujWb74UELUwrqMw7j37R1vT0L6jeggjLeFEjJqY4j90bw53VbYJXsobfyWMwtHmJJPqaY5eoKu2wQ0aaix1MOW4jSEBrcXRQiLFVcMlqKszRpNFf+EGVOfZ4ASqws+D9oum61hnA7xHTD1r+i6QxJfe3p4arXrCVmQW/I7OkJuu5yKmbJhHK6sK7lGmGnE+jt4Stq0WvQnPdl4jSqBCZSke1jgWYuVoD8PLOOHM2gLQf8ZwBOV7FBmpDhXinkGyiBYZX4zwrjJNRWLo9InfYye14FrjehkhbwzbOxg+Qh3joOE9YeOgRcdlD8l+aU8QJq6iop996zUo58dLxsi1K7IiPFCOyLcRc35AjODpNJgzuZrG1EHkwVyPEDwICCC9+iiIPaYAlyPtJJCsuJEPbiuUHltHS3c4K1l5taiRO7TK/0xOZcXPBlOaGaEKgmLkHSi4hZ77jq5tDLpxIWNBpRPhiS6wuMq0TIdssxf+X6dsbw8Gib6MGt8Gd7HhfGmUb6XMWcr9u+WFTq/iO93eAney8LOCv30CuLrZclNWdxSoydHbMdyCAOky4p0FdvXX5oQqU99oH3P1OPemocSsBn5EQrNg+B9B7Fa", "JSESSIONID": "B3DC88434582A10EACDCDDA70FC1AC1B"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://ptti.es.telefonica", "Connection": "keep-alive", "Referer": "https://ptti.es.telefonica/mostrarServiciosComerciales.do?navegacion=no&soloActivos=1", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "frame", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1"}
    response0=session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies,verify=False)
    open(final_path, 'wb').write(response0.content)
    print("Fichero generado en " + final_path)
    print("[END-TIME]["+str(datetime.now())+"]")
    print('Total runtime: '+ str(totalTime(start, datetime.now())[0])+ ' minutes '+ str(totalTime(start, datetime.now())[1])+ ' seconds')
    print("======================================================")
except Exception as e:
    print(str(e))
    print("======================================================")