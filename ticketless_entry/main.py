from flask import Flask, render_template,request,redirect,url_for,session
import qrcode
import os
from io import BytesIO
import base64
#from flask_mail import Mail, Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import mysql.connector as mysql

app = Flask(__name__)
app.secret_key = 'museum'
   
""" app.config.update(
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 465,
            MAIL_USE_TLS = False,
            MAIL_USE_SSL = True,
            MAIL_USERNAME = 'geethujoseph03@student.sfit.ac.in',
            MAIL_PASSWORD = '165#GeethuJ',
            MAIL_DEFAULT_SENDER = 'geethujoseph03@student.sfit.ac.in'
        )
mail = Mail(app) """

try:
    db = mysql.connect(
        host = "127.0.0.1",
        port = "3307",
        user = "root",
        password =  "",
        database = "bookticket"
    )
    if db.is_connected():
        global cursor 
        cursor = db.cursor()
except mysql.Error as e:
    print(e.msg)
    quit()

'''@app.route()
    def home():
         return render_template('home.html') '''

@app.route('/')
def start():
    return render_template('form.html')

'''
@app.route('/home')
def csmvs():
    return render_template('CSMVS.html')

@app.route('/csmvs')
def csmvs():
    return render_template('CSMVS.html')

@app.route('/cstm')
def cstm():
    return render_template('CSTM.html')

@app.route('/dbdlm')
def dbdlm():
    return render_template('DBDLM.html')
'''


@app.route('/form',methods = ['POST','GET'])
def form():
    return render_template('form.html')

@app.route('/form1',methods = ['POST','GET'])
def form1():
    try:
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            phone = request.form['phone']
            email = request.form['email']
            age = request.form['age']
            gender = request.form['gender']
            timeslot = request.form['timeslot']
            visitd = request.form['visitd']
            notickets = request.form['notickets']
            child = request.form['child']
            adult = request.form['adult']

            query = f"insert into form values(id, '{fname}', '{lname}', '{phone}', '{email}', '{age}', '{gender}', '{timeslot}', '{visitd}', '{notickets}', '{child}', '{adult}')"

            cursor.execute(query)
            db.commit()
            print("Your details have been entered successfully!")
            session['email'] = email
            return redirect(url_for("form_print"))

    except mysql.Error or Exception as e:
        print(e.msg)
        print("Error!")
        return redirect(url_for('form'))

@app.route("/form_print")
def form_print():
    #email = request.args.get('email')
    email = session.get('email',None)
    try:
        query = f"select visitd,timeslot,fname,lname,id,notickets from form where email='{email}'"
        cursor.execute(query)
        rs = cursor.fetchone()
        visitd = rs[0]
        timeslot = rs[1]
        name = rs[2]+' '+rs[3]
        id = rs[4]
        notickets = rs[5]
        #session.pop('email')
        img = qr_gen(visitd,timeslot,name,id,notickets)
        #img1 = img[0]
        #img2 = img[1]
        recipient = f'{email}'
        #message = Message('Museum Ticket',recipients = [recipient])
        #message.html = render_template('form_print.html',visitd = visitd, timeslot = timeslot, name = name,id = id, notickets = notickets, img = base64.b64decode(img1))
        message = MIMEMultipart()
        message['From'] = 'geethujoseph03@student.sfit.ac.in'
        message['To'] = recipient
        message['Subject'] = 'Museum Ticket'
        html = render_template('form_print.html',visitd = visitd, timeslot = timeslot, name = name,id = id, notickets = notickets, img = base64.b64decode(img))
        body = MIMEText(html,'html')

        '''message.attach(MIMEText(html,'html'))

        with open('qr.png', 'rb') as f:
            img = MIMEImage(f.read())
            img.add_header('Content-ID', '<qr>')
            message.attach(img)'''
        


        message.attach(body)
        smtp_server = 'smtp.gmail.com'
        smtp_username = 'geethujoseph03@student.sfit.ac.in'
        smtp_password = '165#GeethuJ'
        smtp_port = 587
        smtp_connnection = smtplib.SMTP(smtp_server,smtp_port)
        smtp_connnection.starttls()
        smtp_connnection.login(smtp_username,smtp_password)
        smtp_connnection.sendmail(message['From'],message['To'],message.as_string())
        smtp_connnection.quit()
        #mail.send(message)
        print('Email Sent!')
        
        return render_template('form_print.html',visitd = visitd, timeslot = timeslot, name = name,id = id, notickets = notickets, img = img)
    except mysql.Error or Exception as e:
        print(e.msg)
        return redirect(url_for('form_print'))

def qr_gen(visitd,timeslot,name,id,notickets):
    text = f'''DATE = {visitd},
           Time-slot = {timeslot},
           Name = {name},
           Ticket number: {id},
           No. of people: {notickets}'''
    qr = qrcode.QRCode(version=1,box_size=4,border=1)
    qr.add_data(text)
    qr.make(fit=True)
    #qr2 = qrcode.QRCode(version=1,box_size=2,border=1)
    #qr2.add_data(text)
    #qr2.make(fit=True)
    qr_img = qr.make_image(fill_color='black',back_color='white')
    qr_img.save('qr.png')
    #qr_img2 = qr2.make_image(fill_color='black',back_color='white')
    #qr_img2.save('qr2.png')
    f = open('qr.png','rb')
    str = f.read()
    #f2 = open('qr2.png','rb')
    #str2 = f2.read()
    img_data = base64.b64encode(str).decode('ascii')
    #img_data2 = base64.b64encode(str2).decode('ascii')
    #list1 = [img_data,img_data2]
    return img_data
    



if __name__ =="__main__":
    app.run()