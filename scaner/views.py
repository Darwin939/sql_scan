from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Website,Vulnerability, Log
from .utils.extract_urls import extract_urls
from .utils.sql_vuln_scanner import scan_sql_injection
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import sys
import os





def index(request):
    template = loader.get_template('scaner/index.html')
    cookie = request.COOKIES.get('last_site') 
    if cookie == None:
        vulns = None
    else:
        vulns = Vulnerability.objects.filter(site__url = cookie)
    last_log = Log.objects.order_by('-id')[0]
    context = {
        'vulns': vulns,
        'log' : last_log
    }

    return HttpResponse(template.render(context, request))

@csrf_exempt
def make_analysis(request):
    if request.method == "POST":
        try:
            site_url = request.POST["site_url"]
            w = Website(url = site_url)
            w.save()
            all_urls = extract_urls(site_url)
            all_urls.add(site_url)
            result = []
            for i in all_urls:
                res = scan_sql_injection(i)
                if res != None:
                    result.append(res)
            for i in result:
                if i[1] == "form":
                    t = "SQL Injection vulnerability / FORM vulnerability "
                    v = Vulnerability(url = i[0],type = t,site = w)
                    v.save()
                else:
                    t = "SQL Injection vulnerability / URL vulnerability "
                    v = Vulnerability(url = i[0],type = t,site = w)
                    v.save()
            with open("./log.log","r") as data:
                s = data.read()
            l = Log(text = s)
            l.save()
            os.remove("./log.log")
            return redirect('index')
            
        except:
            with open("./log.log","r") as data:
                s = data.read()
            l = Log(text = s)
            l.save()
            os.remove("./log.log")
           
            return redirect('index')