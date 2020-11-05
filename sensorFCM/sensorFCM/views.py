
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
import datetime as dt
import sqlite3
import json
import requests
key="**ServerKey**"
pkey = '**MobileKey**'

dlength=10
limit=150

def door(request):
    return render(request,"graph.html")


def dstack(request):
    init()
    time=dt.datetime.now()
    time = time.strftime('%Y/%m/%d %H:%M')
    if request.method == "POST":
        jsondata = json.loads(request.body)
        data=jsondata['flow']
        print(int(data),limit)
        if int(data)>=limit:
            sendToFCM(key,pkey,"Warnnig!\nlimit is over.",time+"\n"+str(data))

        cur.executemany('INSERT INTO dtable(time_stamp,fdata) VALUES (?,?)',[(time,data)])
        cur.execute('SELECT * FROM dtable')
        table = cur.fetchall()
        for i in range(len(table) - int(dlength)):
            cur.execute('delete from dtable where num in '
                        '(SELECT num FROM dtable LIMIT 1 OFFSET 0);')
        conn.commit()
        conn.close()
    return HttpResponse("Done.")

def dpop(request):
    init()
    cur.execute('SELECT * FROM dtable')
    table=cur.fetchall()
    datalist=[]
    for row in table:
        data={'time':row[1],'fdata':row[2]}
        datalist.append(data)
    conn.commit()
    conn.close()
    return JsonResponse(datalist,safe=False)

def set(request):
    global dlength,limit
    #init()
    if request.method == "POST":
        dlength=request.POST.get('dlength')
        limit=request.POST.get('limit')
        #print(len(table) > int(dlength),len(table),int(dlength))
        print(dlength,limit)
    return redirect('/')

def init():
    global conn,cur
    conn = sqlite3.connect("sqlite.db")
    cur = conn.cursor()
    conn.execute('CREATE TABLE IF NOT EXISTS dtable'
                      '(num INTEGER PRIMARY KEY,'
                     'time_stamp VARCHAR(20), '
                     'fdata INT)')

def sendToFCM(skey,key,head,body):
    url = 'https://fcm.googleapis.com/fcm/send'
    headers = {
        'Authorization': 'key =' + skey,
        'Content-Type': 'application/json;UTF-8',
    }
    data = {
        'to': key,
        "time_to_live": 60,
        "priority": "high",
        "data": {
            "text": {
                "title": head,
                "message": body,
            }
        }
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.content)
