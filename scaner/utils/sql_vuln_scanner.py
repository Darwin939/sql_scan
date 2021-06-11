import requests
import re # uncomment this for DVWA
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import re
from contextlib import redirect_stdout

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

login_payload = {
    "username": "admin",
    "password": "password",
    "Login": "Login",
}

try:
    # change URL to the login page of your DVWA login URL
    login_url = "http://127.0.0.1/DVWA/login.php"

    # login
    r = s.get(login_url)
    token = re.search("user_token'\s*value='(.*?)'", r.text).group(1)
    login_payload['user_token'] = token
    s.post(login_url, data=login_payload)
except:
    print("Cannot acces to the DVWA")
    pass

def write(text):
    with open('./log.log', 'a+') as f:
        with redirect_stdout(f):
            print(text)

def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML `form`
    """
    details = {}
    # get the form action (target url)
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None

    method = form.attrs.get("method", "get").lower()

    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def is_vulnerable(response):
    """A simple boolean function that determines whether a page 
    is SQL Injection vulnerable from its `response`"""
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
        #MariDB
        "SQL syntax",
    }
    
    for error in errors:

        if error in response.content.decode().lower():
            return True

    return False


def scan_sql_injection(url):
    
    # test on URL
    for c in "\"'":
  
        new_url = f"{url}{c}"
        with open('./log.log', 'a+') as f:
            with redirect_stdout(f):
                print("[!] Trying", new_url)
        print("[!] Trying", new_url)

        res = s.get(new_url)
        if is_vulnerable(res):
            with open('./log.log', 'a+') as f:
                with redirect_stdout(f):
                    print("[+] SQL Injection vulnerability detected, link:", new_url)
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            return (url,"url")

    # test on HTML forms
    forms = get_all_forms(url)
    with open('./log.log', 'a+') as f:
        with redirect_stdout(f):
            print(f"[+] Detected {len(forms)} forms on {url}.")
    print(f"[+] Detected {len(forms)} forms on {url}.")
    
    for form in forms:
        form_details = get_form_details(form)
 
        for c in "\"'":

            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["value"] or input_tag["type"] == "hidden":

                    try:
                        data[input_tag["name"]] = input_tag["value"] + c
                    except:
                        pass
                elif input_tag["type"] != "submit":

                    data[input_tag["name"]] = f"test{c}"

            url = urljoin(url, form_details["action"])
            
            if form_details["method"] == "post":
                res = s.post(url, data=data)
            elif form_details["method"] == "get":
                
                res = s.get(url, params=data)

            if is_vulnerable(res):
                with open('./log.log', 'a+') as f:
                    with redirect_stdout(f):
                        print("[+] SQL Injection vulnerability detected, link:", url)
                        print("[+] Form:")
                        print(form_details)
                print("[+] SQL Injection vulnerability detected, link:", url)
                print("[+] Form:")
                pprint(form_details)
                return (url,"form")   

