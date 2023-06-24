from flask import Flask,request,redirect,url_for,render_template
from flask_mail import Mail, Message
import os, random, string
#from datetime import date
import time
import pandas as pd

from firebase import firebase
conn = firebase.FirebaseApplication("https://arduinodata-83659.firebaseio.com/")

app = Flask(__name__, static_url_path='/static')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'manoharreddy1818@gmail.com'
app.config['MAIL_PASSWORD'] = '**********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#result = conn.get("/27-10-2019/18:23:12/", None)


@app.route('/')
def fun():
    return render_template('landingPage.html')

@app.route("/sec")
def fun44():
    return redirect(url_for('all'))

@app.route("/login")
def fun444():
    return render_template("login.html")

@app.route('/aboutus')
def fun626():
    return render_template('aboutus.html')

@app.route('/contactus')
def fun726():
    return render_template('contactus.html')

@app.route('/subscrib')
def fun826():
    return render_template('subscribe.html')


@app.route("/mail")
def index():
    msg = Message('IOT Alert', sender = 'manoharreddy1818@gmail.com', recipients = ['kaustubdutt@gmail.com'])
    x = "35"
    msg.body = "Dear Customer, \n   Your Temperature is exceed than optimal.\n  It's value is  %s .Please Take necesary precautions to avoid further damage" % x
    mail.send(msg)
    return "Successfully send"

@app.route("/monitoring")
def fun56():
    x = conn.get('/', None)
    dates = list(x.keys())
    select=dates[-1]
    #select='6-11-2019'
    date = dict(conn.get(f'{select}', None))
    #date = conn.get("/"+z, None)
    times = list((date.keys()))
    pre=times[-1]
    result=conn.get("/"+select+"/"+pre,None)
    d = {}
    for i in result.keys():
        for j in result[i]:
            # print(i, end=" : ")
            # print(result[i][j])
            d[i] = result[i][j]

    # msg = Message('IOT Alert', sender='manoharreddy1818@gmail.com', recipients=['kittu18061997@gmail.com'])
    x = d["Temperature"]
    y = d["Humidity"]
    z = d["SoilMoist"]
    if(25<=x<34 and 60<=y<85 and 20<=z<50):
        pass
    else:
        msg = Message('IOT Alert', sender='manoharreddy1818@gmail.com', recipients=['kittu18061997@gmail.com'])
        msg.body = "Dear Customer,\n\nYour environmental conditions are exceed than optimal at time {0}.\n\nTemperture = {1}    Normal Range(25,34) \nHumidity = {2}        Normal Range(60,85) \nSoil Moisture = {3}   Normal Range(20,50).\n\nPlease Take necesary precautions to avoid further damage to your Crop\n\nThanks and Regards,\nManohar Reddy".format(pre,x,y,z)
        mail.send(msg)
    return d


@app.route("/getData",methods = ['POST', 'GET'])
def fun1():
    if request.method == 'POST':
        d = request.form['date']
        t = request.form['time']

    result = conn.get("/"+d+"/"+t, None)
    d={}
    for i in result.keys():
        for j in result[i]:
            #print(i, end=" : ")
            #print(result[i][j])
            d[i]=result[i][j]


    #msg = Message('IOT Alert', sender='manoharreddy1818@gmail.com', recipients=['kittu18061997@gmail.com'])
    x=d["Temperature"]
    y=d["Humidity"]
    z=d["SoilMoist"]
    #if(25<=x<34 and 60<=y<85 and 20<=z<50):
     #   pass
    #else:
     #   msg = Message('IOT Alert', sender='manoharreddy1818@gmail.com', recipients=['kittu18061997@gmail.com'])
     #   msg.body = "Dear Customer,\n\nYour environmental conditions are exceed than optimal.\n\nTemperture = {0}    Normal Range(25,34) \nHumidity = {1}        Normal Range(60,85) \nSoil Moisture = {2}   Normal Range(20,50).\n\nPlease Take necesary precautions to avoid further damage to your Crop\n\nThanks and Regards,\nManohar Reddy".format(x,y,z)
     #   mail.send(msg)
    return render_template('secondpage.html',result=d)


@app.route("/demo")
def fun55():
    result = conn.get("/",None)
    h={}
    for i in result.keys():
        h[i]=i
    return render_template('thirdpage.html',result=h)

@app.route("/getone",methods = ['POST', 'GET'])
def fun111():
    if request.method == 'POST':
        d = request.form['date']

    result = conn.get("/"+d, None)
    f = {}
    for i in result.keys():
        f[i] = result[i]

    #x = d["Temperature"]
    #y = d["Humidity"]
    #z = d["SoilMoist"]
    return render_template('thirdpage.html', result=f)
    #return f


@app.route("/subscribe",methods=['POST','GET'])
def all1():
    if request.method=="POST":
        t1=request.form["temp"]
        t3=request.form["hum"]
        t2=request.form["soilmoist"]
        t1 = int(t1)
        t2 = int(t2)
        t3 = int(t3)
        x = pd.read_csv('out.csv')
        X = x.iloc[:, :3]
        y = x.iloc[:, 3]
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = le.fit_transform(y)

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

        from sklearn.tree import DecisionTreeClassifier
        trc = DecisionTreeClassifier(criterion='entropy', random_state=0)
        trc.fit(X_train, y_train)

        y_pred = trc.predict([[t1, t2, t3]])
        print(type(t1))
        print(y_pred[0])
        if (y_pred[0] == 1):
            z="Favourable for growth"
        else:
            z="Difficult to Sustain"
        return render_template('subscribe.html',value=1,z=z)
    else:
        return render_template('subscribe.html',value=0)



@app.route("/new",methods=['POST','GET'])
def all():
    x = conn.get('/', None)
    dates = list(x.keys())
    if request.method=="POST":
        select=request.form['select']
        #print(select)
        d = []
        f = []
        p = []
        t = []
        tm=[]
        hum=[]
        sm=[]
        date = dict(conn.get(f'{select}', None))
        times = list((date.keys()))
        #print(times)
        for i in times:
            time = date[i]
            print(time)
            di = (list(time['Temperature'].keys()))
            di=di[0]
            #print(di)
            tm.append(time['Temperature'][di])
            di = (list(time['Humidity'].keys()))
            di=di[0]
            hum.append(time['Humidity'][di])
            di = (list(time['SoilMoist'].keys()))
            di=di[0]
            sm.append(time['SoilMoist'][di])
            #print(sm)
        #return di
        return render_template('hhnew.html',value=1,length=[i for i in range(len(times))],dates=dates,select=select,times=times,tm=tm,hum=hum,sm=sm)
    else:
        return render_template('hhnew.html',value=0,dates=dates)


if __name__ == "__main__":
    app.run(debug=True)
