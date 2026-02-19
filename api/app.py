from flask import Flask,request,redirect,url_for,render_template,make_response
from datetime import datetime
app = Flask(__name__, template_folder="templates", static_folder="static")

users={}
statements={}
@app.route('/')  #base and first route   #we can only render one file for one route
def welcome():
    return render_template('welcome.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        print(request.form)
        username=request.form['username']
        userpassword=request.form['password']
        if username not in users:
            users[username]={'userpassword':userpassword,'Amount':0}
            if username not in statements:
                statements[username]={'deposit_stm':[],'withdraw_stm':[]}
            return redirect(url_for('login')) 
        else:
            return 'user already existed'   
    return render_template('register.html')


#login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_username=request.form['username']
        login_password=request.form['password']
        if login_username in users:
            if users[login_username]['userpassword']==login_password:
                resp=make_response(redirect(url_for('dashboard')))
                resp.set_cookie('user',login_username)  #generating cookie #cookie name=user and value username
                return resp
            else:
                return 'invalid password'
        else:
            return 'invalid user details'
        
    return render_template('login.html')

#dashboard route
@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        print(username)
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


#route for deposit
@app.route('/deposit',methods=['GET','POST'])
def deposit():
    if request.cookies.get('user'):
        username=request.cookies.get('user')
        if request.method=='POST':
            deposit_amount=int(request.form['amount'])
            if deposit_amount>0:
                if deposit_amount%100==0:
                    if deposit_amount<=50000:
                        users[username]['Amount']=users[username]['Amount']+deposit_amount
                        deposit_time=datetime.now() #current time
                        deposit_data=(deposit_amount,deposit_time)
                        statements[username]['deposit_stm'].append(deposit_data)
                        return redirect(url_for('dashboard'))
                    else:
                        return 'amount exceeded'
                else:
                    return 'amount should be multiples of 100'
            else:
                return 'amount should be greater than 0'

        return render_template('deposit.html')
    else:
        return redirect(url_for('login'))
    
# route for withdraw
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.cookies.get('user'):   # check login
        username = request.cookies.get('user')
        if request.method == 'POST':
            withdraw_amount = int(request.form['amount'])
            if withdraw_amount > 0:
                if withdraw_amount % 100 == 0:
                    if withdraw_amount <= users[username]['Amount']:
                        users[username]['Amount'] -= withdraw_amount
                        withdraw_time = datetime.now()  # current time
                        withdraw_data = (withdraw_amount, withdraw_time)
                        statements[username]['withdraw_stm'].append(withdraw_data)
                        return redirect(url_for('dashboard'))

                    else:
                        return 'Withdraw amount greater than present balance'
                else:
                    return 'Withdraw amount should be multiple of 100'
            else:
                return 'Withdraw amount should be greater than 0'

        return render_template('withdraw.html')

    else:
        return redirect(url_for('login'))

#dummy route just for learning purpose
@app.route('/dummy')
def dummy():
    name='chandrika'
    age=35
    data=[(1,'chandrika',100000),(2,'Vijaya',400000)]
    return render_template('dummy.html',name=name,age=age,data=data)

#route for balance
@app.route('/balance')
def balance():
    if request.cookies.get('user'):
        username = request.cookies.get('user')
        balance_amt = users[username]['Amount']
        return render_template('balance.html', username=username, balance_amt=balance_amt)
    else:
        return redirect(url_for('login'))
    
#route for statements
@app.route('/userstatements',methods=['GET','POST'])
def userstatements():
    if request.cookies.get('user'):
        username = request.cookies.get('user')
        deposit_statements=statements[username]['deposit_stm']
        withdraw_statements=statements[username]['withdraw_stm']
        return render_template('statements.html',deposit_statements=deposit_statements,withdraw_statements=withdraw_statements)
    else:
        return redirect(url_for('login')) 
    # return render_template('statements.html')


@app.route('/logout')
def logout():
    if request.cookies.get('user'):
        resp=make_response(redirect(url_for('login')))
        resp.delete_cookie('user')
        return resp
    else:

       return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()

app = app
