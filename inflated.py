from http.client import HTTPResponse
# from msilib.schema import tables
import plaid
from flask import Flask, render_template,request,g,session,redirect,jsonify,Blueprint
import pymysql
import json
import os,binascii
from dotenv import load_dotenv
from werkzeug.wrappers import response
import time
import requests
import numpy as np
from datetime import datetime,date,timedelta
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from sqlalchemy import create_engine
import datetime
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from plaid.exceptions import ApiException
import pandas as pd
load_dotenv()
from datetime import date
mailchimp = MailchimpTransactional.Client(os.getenv('MAILCHIMP_API'))
inflated = Flask(__name__)
inflated.secret_key = binascii.hexlify(os.urandom(20)).decode()
# inflated.config['SERVER_NAME'] = 'localhost:3015'
import numpy as np
import pandas as pd
import re
#############################Basic Set Up##########################
#DB Connect
conn = pymysql.connect(
        host=os.getenv('MySQL_HOST'),
        user=os.getenv('MySQL_USER'), 
        password = os.getenv('MySQL_PASS'),
        db=os.getenv('MySQL_DB'),
        )


configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': '',
        'secret': '',
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# Set User Session
def user(data):
    user={'id':data[0],'name':data[1],'email':data[2],'email':data[3]}
    session['user']=user
 

def admin(self,data):
    admin={'id':data[0],'name':data[1],'email':data[2],'password':data[3]}
    session['admin']=admin

@inflated.route('/test')
def test():
    get_id=session['user']['id']
    cur = conn.cursor()
    sql=f"select category,sum(amount) from transaction WHERE user_id={get_id} group by category ORDER BY category asc"
    conn.ping(reconnect=True)
    cur.execute(sql)
    data=cur.fetchall()
    totalAmountCategory=pd.DataFrame(data, columns=['category','amount'])['amount'].sum()
    # print(totalAmountCategory)
    dt=()
    for i in month:
        sql=f"select category, sum(amount) as 'amount', round((sum(amount)/%s*100),2), %s as 'Month' from transaction where user_id=1 and monthname(transaction_date)=%s and YEAR(transaction_date) = %s GROUP BY category"
        conn.ping(reconnect=True)
        sql=cur.execute(sql,(totalAmountCategory,i,i,currentDate,))
        if sql:
            data=cur.fetchall()
            dt=dt+data
    # print(dt)
    if len(data) >0:
        # print('*******************{}***********************'.format(currentMonth))
        data=pd.DataFrame(dt,columns=['Category','Amount','Total_Percentage','Months'])
        # print(data)
    else:
        pass
    Weighted_Inflation=[]
    for i in range(data['Amount'].count()):
        sql="select (value*{})/100 as wh from cpi where Categories LIKE '%{}%'".format(data["Total_Percentage"][i],data['Category'][i])
        conn.ping(reconnect=True)
        sql=cur.execute(sql)
        dtt=cur.fetchone()
        # print(dtt)
        Weighted_Inflation.append(dtt[0])
    data['Weighted_Inflation']=Weighted_Inflation
    # print(data.loc[data['Months'] == currentMonth])
    
    pivot_table = data.pivot_table(values=["Weighted_Inflation"], index=["Months"], aggfunc=np.sum)
    pivot_table['Months']=pivot_table.index
    pivot_table=pivot_table.set_index(pd.Index(np.arange(1,len(pivot_table)+1)))
    # print(pivot_table)
    # print(data)
    # # data.to_csv('test.csv')
    # return render_template('test.html', tables=data.values.tolist())
    return render_template('test.html')


@inflated.route('/', methods= ['POST', 'GET'])
def index():
    """
    Website Home Page
    """
    if request.method=='POST':
        req=request.form
        first_name=req['first_name']
        last_name=req['last_name']
        email=req['email']
        message=req['message']
        
        cur = conn.cursor()
        sql="insert into contact(fname,lname,email,message) values(%s,%s,%s,%s)"
        conn.ping(reconnect=True)
        sql=cur.execute(sql,(first_name,last_name,email,message))
        conn.commit()
        if(sql):
           return jsonify({'type':'success','message':'Your form has been submitted successfully'})
        else:
            return jsonify({'type':'error','message':'Your form data not submitted successfully'})
    else:
        return render_template('index.html')

@inflated.route('/sign-in', methods= ['POST', 'GET'])
def sign_in():
    '''
    User Sign In Page
    '''
    if 'user' in session:
        return redirect('dashboard')

    if request.method=='POST':
        req=request.form          
        cur = conn.cursor()
        # change status of email veryfication

        # sql='select * from user_registration where email=%s and password=%s and status=%s'
        sql='select * from user_registration where email=%s and password=%s'
        conn.ping(reconnect=True)
        # sql=cur.execute(sql,(req['email'],req['password'],1))
        sql=cur.execute(sql,(req['email'],req['password']))
        if sql:
            user(cur.fetchone())
            return jsonify({'type':'success','message':'Success'})           
        else:
            return jsonify({'type':'error','message':'Your email and password not match'})
    else:
        return render_template('auth/sign-in.html')

@inflated.route('/sign-up', methods= ['POST', 'GET'])
def sign_up():
    if 'user' in session:
        return redirect('dashboard')
    if request.method=='POST':        
        req = request.form
        name = req['name']
        if(name==""):
            return json.dumps({'type':'error','message':"Please enter the full name."})
        email = req['email']
        if(email==""):
            return json.dumps({'type':'error','message':"Please enter the email id."})
        number = req['number']
        if(number==""):
            return json.dumps({'type':'error','message':"Please enter the phone number."})    
        password = req['password']
        confirm_password = req['confirm_password']
        cur = conn.cursor()
        sql='select * from user_registration where email=%s'
        conn.ping(reconnect=True)
        sql=cur.execute(sql,(email))    
        if(password!=confirm_password):
            return json.dumps({'type':'error'})
        if(sql):
            return json.dumps({'type':'error','message':"Email id are already exist."})

        verificationToken=binascii.hexlify(os.urandom(20)).decode()         
        resetToken=binascii.hexlify(os.urandom(20)).decode()         
           
        sql = "insert into user_registration(name,email,mobile,password,resetToken,verificationToken,status) values(%s,%s,%s,%s,%s,%s,%s)"
        conn.ping(reconnect=True)
        sql=cur.execute(sql,(name,email,number,password,resetToken,verificationToken,1))
        conn.commit()       
        if(sql): 
            # return json.dumps({'type':'success','message':"Your registration data has been submitted successfully."})

            # return render_template('auth/sign-in.html') 
           
            # text='''Please <a href='{0}?verificationToken={1}'> Click Here </a> to comform your registration'''.format('https://inflated.devtrust.biz/sign-up',verificationToken)
            text="Thank you for your registration"
            message = {
            "from_email": "info@inflated.me",
            "subject": "Inflated: Thank you for registration",
            "html": text,   
            "to": [
            {
            "email": email,
            "type": "to"
            }
            ]
            }
            mailchimp.messages.send({"message":message})             
            # return json.dumps({'type':'success','message':"A verification mail has been sent to your email address. Please verify!"})
            return json.dumps({'type':'success','message':"Your registration data has been submitted successfully."})
        
        else:
            return json.dumps({'type':'error','message':"Your form data not submitted successfully"})
        
    # sign-up verificationToken     
    if request.args.get('verificationToken'):
        cur = conn.cursor()
        sql='select * from user_registration where verificationToken=%s'
        conn.ping(reconnect=True)
        sql = cur.execute(sql,(request.args.get('verificationToken')))
        if sql:
            status="1"; 
            cur=conn.cursor()    
            sql = "update user_registration set status=%s where verificationToken=%s"
            conn.ping(reconnect=True)
            sql=cur.execute(sql,(status,request.args.get('verificationToken')))
            conn.commit()
            if(sql):
                return redirect('/sign-in')
            else:
                return redirect("/sign-up")
        
    else:
        return render_template('auth/sign-up.html')
    

@inflated.route('/forget_password', methods=['POST','GET'])
def forget_password():
    '''
    User Forgot Page
    '''
    if request.method=='POST':
        req=request.form
        cur = conn.cursor()
        sql='select * from user_registration where email=%s'
        conn.ping(reconnect=True)
        sql = cur.execute(sql,(req['email']))
        if sql:
            token=binascii.hexlify(os.urandom(20)).decode()
            sql = "update user_registration set resetToken=%s where email=%s"
            conn.ping(reconnect=True)
            sql=cur.execute(sql,(token,req['email']))
            conn.commit()
            # text='''Please <a href='{0}?token={1}'> Click Here </a> to reset your password'''.format(request.base_url,token)
            text='''Please <a href='{0}?token={1}'> Click Here </a> to reset your password'''.format(request.base_url,token)
            print("+++++++++++++++++++",text)
            message = {
            "from_email": "info@inflated.me",
            "subject": "Forgot Password",
            "html": text,   
            "to": [
            {
            "email": req['email'],
            "type": "to"
            }
            ]
            }
            mailchimp.messages.send({"message":message})
            return render_template('auth/forget_password.html',message='Reset Password link has been sent to the registered email address.')
        else:
            return render_template('auth/forget_password.html',error='Email address is not exist.')
    
    if request.args.get('token'):
        cur = conn.cursor()
        sql='select * from user_registration where resetToken=%s'
        conn.ping(reconnect=True)
        sql = cur.execute(sql,(request.args.get('token')))
        if sql:
            session['resetToken']=request.args.get('token')
            # return redirect('https://inflated.devtrust.biz/reset-password')
            return redirect('/reset-password')
        else:
            # return redirect('https://inflated.devtrust.biz/forgot-password')
            return redirect('/forgot-password')

        
    return render_template('auth/forget_password.html',message='You will receive an E-mail with instructions to reset your password.')
   
'''''''''''''''''''''''''''''Dashboard'''''''''''''''''''''''''''''''''
@inflated.route('/dashboard', methods= ['POST', 'GET'])
def dashboard():
    '''
    User Dashboard Page
    '''
    if 'user' in session:
        if request.method=='POST':
            req=request.form   
            currentMonthAjax=req['data']
            print(currentMonthAjax)
        get_id = session['user']['id']
        cur = conn.cursor()
        sql=f"select user_id,transaction_date,amount,category,subcategory from transaction WHERE user_id = {get_id}"
        conn.ping(reconnect=True)
        check=cur.execute(sql)
        df=pd.DataFrame(cur.fetchall())
        df.columns=['user_id','transaction_date','amount','category','subcategory']
        df['transaction_date']=pd.to_datetime(df['transaction_date'])
        cat=list(set(df['category']))
        data=pd.DataFrame()
        result='Dec'
        for j in cat:
            try:
                df1=df[(df['user_id']==get_id) & (df['category']==f'{j}')]
                df1=df1[['transaction_date','amount','category']]
                df1['amount']=df1['amount'].astype(float)
                df1=df1.set_index('transaction_date')
                df1=df1.resample("M").sum()
                df1=df1.reset_index()
                df1['CPI']=(df1['amount']/df1['amount'].iloc[0])*100
                df1['Month']=[i.strftime("%B") for i in df1['transaction_date']]
                df1['Year']=[i.strftime("%Y") for i in df1['transaction_date']]
                df1['category']=j
                data=data.append(df1,ignore_index=True)
            except:
                pass

        pi=data.groupby(['category']).resample("Y",on="transaction_date").mean().CPI.pct_change()
        pi=pi.reset_index()
        pi.rename(columns={'CPI':'PI'},inplace=True)
        pi=pi[pi['transaction_date']=='2022-12-31']
        pi=pi.to_dict('r')
        y=data.groupby(['Month','category']).sum()
        y['pi_monthly']=[(i-100) for i in y.CPI]
        y['pi_monthly']=y['pi_monthly']/y['CPI']
        y=y.reset_index()
        y['pi_monthly']= y['pi_monthly'].replace([np.NaN,np.inf,-np.inf],0)
        jan=y[y['Month'].str.contains(r'\bjan',flags=re.IGNORECASE,regex=True)]
        feb=y[y['Month'].str.contains(r'\bfeb',flags=re.IGNORECASE,regex=True)]
        mar=y[y['Month'].str.contains(r'\bmar',flags=re.IGNORECASE,regex=True)]
        apr=y[y['Month'].str.contains(r'\bapr',flags=re.IGNORECASE,regex=True)]
        may=y[y['Month'].str.contains(r'\bmay',flags=re.IGNORECASE,regex=True)]
        jun=y[y['Month'].str.contains(r'\bjun',flags=re.IGNORECASE,regex=True)]
        jul=y[y['Month'].str.contains(r'\bjul',flags=re.IGNORECASE,regex=True)]
        aug=y[y['Month'].str.contains(r'\baug',flags=re.IGNORECASE,regex=True)]
        sep=y[y['Month'].str.contains(r'\bsep',flags=re.IGNORECASE,regex=True)]
        oct=y[y['Month'].str.contains(r'\boct',flags=re.IGNORECASE,regex=True)]
        nov=y[y['Month'].str.contains(r'\bnov',flags=re.IGNORECASE,regex=True)]
        dec=y[y['Month'].str.contains(r'\bdec',flags=re.IGNORECASE,regex=True)]
        jan=jan.to_dict('r')
        feb=feb.to_dict('r')
        mar=mar.to_dict('r')
        apr=apr.to_dict('r')
        may=may.to_dict('r')
        jun=jun.to_dict('r')
        jul=jul.to_dict('r')
        aug=aug.to_dict('r')
        sep=sep.to_dict('r')
        oct=oct.to_dict('r')
        nov=nov.to_dict('r')
        dec=dec.to_dict('r')
        data=data.groupby(["Month"]).mean()
        data=data.reset_index()
        data=data.to_dict('r')
        print(nov)
        return render_template('dashboard/index.html', sidebar='dashboard',data=data,pi=pi,jan=jan,feb=feb,mar=mar,apr=apr,may=may,jun=jun,jul=jul,aug=aug,sep=sep,oct=oct,nov=nov,dec=dec)    
    else:
        return redirect('/sign-in')
@inflated.route('/link-bank-account')
def link_bank_account():
    '''
    Dashboard  Link Bank Account
    '''
    if 'user' not in session:
        return redirect('/')
    url = "https://sandbox.plaid.com/link/token/create"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    res = requests.post(url, data=req, headers=headers)
    token_link=res.json()['link_token']
    return render_template('dashboard/link-bank-account.html',token=token_link,sidebar='link_account')

@inflated.route('/reset-password')
def reset_password():
    '''
    Dashboard  User Profile
    '''
    if 'resetToken' in session:
        return render_template('auth/reset_password.html')
    else:
        return render_template('/')

@inflated.route('/setPassword',methods=['POST','GET'])
def resetPassword():
    if request.method=='POST':
        req=request.form
        password=req['password']
        repassword=req['repassword']
        if(password!=repassword):
            return render_template('auth/reset_password.html', message="Password does not match.")
        else:
            cur=conn.cursor()
            sql = "update user_registration set password=%s where resetToken=%s"
            conn.ping(reconnect=True)
            sql=cur.execute(sql,(password,session['resetToken']))
            conn.commit()
            if(sql):
                cur=conn.cursor()
                sql = "update user_registration set resetToken=%s where resetToken=%s"
                conn.ping(reconnect=True)
                sql=cur.execute(sql,('',session['resetToken']))
                conn.commit()
                session.pop('resetToken',None)
                return redirect('/sign-in')
            else:
                return render_template('auth/reset_password.html', message="Something went wrong!!!")

@inflated.route('/transaction')
def transaction():
    '''
    Dashboard  User Profile
    '''
    if 'user' not in session:
        return redirect('/')
    cur=conn.cursor()
    get_id = session['user']['id']
    # print(get_id)
    trans_query='SELECT * FROM transaction WHERE user_id=%s'
    conn.ping(reconnect=True)    
    trans=cur.execute(trans_query,get_id)
    data = cur.fetchall()
    return render_template('dashboard/transaction.html',sidebar='transaction',transaction=data)



# Admin Panel


@inflated.route("/admin/login", methods= ['POST', 'GET'])
def admin_login():   
    if 'admin' in session:
        return redirect('/admin/login')
    if request.method=='POST':
        req=request.form 
        email=req['email']
        password=req['password']          
        cur = conn.cursor()
        sql='SELECT * FROM admin WHERE email=%s and password=%s'
        conn.ping(reconnect=True)
        sql=cur.execute(sql,(email,password))
        # print(sql)               
        if sql:
            # admin(cur.fetchone())  
            session['admin']=email         
            return jsonify({'type':'success','message':'Success'})          
        else:
            return jsonify({'type':'error','message':'Your  email and password not match'})
    else:
        return render_template("admin/auth/login.html")

@inflated.route("/admin/logout")
def adminlogout():
    session.pop('admin',None)    
    return render_template("admin/auth/login.html")

@inflated.route("/admin/tranasaction")
def user_transaction():
    return render_template("admin/tranasaction.html")

@inflated.route("/admin/lockscreen")
def adminlockscreen():
    return render_template("admin/auth/lockscreen.html")

@inflated.route("/admin/forgot_password")
def adminforgotpassword():
    return render_template("admin/auth/forgot_password.html")

@inflated.route("/admin")
def admin():
    if 'admin' not in session:
        return redirect('/admin/login')
    return redirect('/admin/users')

@inflated.route("/admin/graph")
def admingraph():
    return render_template("admin/graph.html")




@inflated.route('/crud/delete/<string:delete_id>', methods=['POST','GET'])
def cruddelete(delete_id):  
    cur = conn.cursor()
    conn.ping(reconnect=True)
    cur.execute("DELETE FROM user_registration WHERE id = %s" , (delete_id))
    conn.commit()
    if(cur):
        return redirect('/admin/users')
    

@inflated.route('/crud/edit/<string:edit_id>', methods=['POST','GET'])
def crudedit(edit_id):
    cur = conn.cursor()
    conn.ping(reconnect=True)
    cur.execute("SELECT * FROM user_registration WHERE id = %s" , (edit_id))
    data = cur.fetchall()  
    return render_template("admin/crud/edit.html", data = data)


# strat add data in graph


# end add data in graph

@inflated.route('/crud/update', methods=['POST','GET'])
def crudupdate():  
    if request.method=='POST':
        id=request.form['id']
        name=request.form['name']
        email=request.form['email']
        cur = conn.cursor()
        conn.ping(reconnect=True)
        sql=cur.execute("update user_registration SET name = %s, email = %s WHERE id = %s" , (name,email,id))
        conn.ping(reconnect=True)
        if sql:
            return redirect('/admin/users')
        else:
            return redirect('/admin/users')


@inflated.route('/logout')
def logout():
    session.pop('user',None)    
    return render_template('auth/sign-in.html')



@inflated.route('/data')
def data():
    cur = conn.cursor()
    conn.ping(reconnect=True)
    cur.execute("SELECT * FROM user_registration ORDER BY mobile IS NULL")
    data = cur.fetchall()
    return jsonify

if __name__ == "__main__":
    inflated.run(debug=True,port=3015,host='0.0.0.0')
