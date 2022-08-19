
import json
from flask import Flask, redirect, render_template, request,jsonify,session,url_for
import sqlite3
import hashlib
import os

con = sqlite3.connect('users.db')
cursor = con.cursor()
cursor.execute('create table if not exists Users(username varchar, password varchar, nickname varchar, email varchar)')
cursor.execute('create table if not exists Cred(realuser varchar,website varchar, username varchar, password varchar)')
con.commit()
con.close()


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'harrish07')



@app.route('/')
def log():
    return render_template('home.html')

@app.route('/nlog', methods = ['POST','GET'])
def nlog():
    n = request.form['nt']
    passi = request.form['passt']
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists Users(username varchar, password varchar, nickname varchar, email varchar)')

    cursor.execute("select * from Users where username = '%s'" %n)
    Users = None
    for i in cursor:
        Users = i
        break
    if Users:
        print(Users)
        passit = Users[1]
        hash_func = hashlib.sha1()
        string = passi + "h7"
        encoded_string=string.encode()
        hash_func.update(encoded_string)
        passi=hash_func.hexdigest()
        print(passit)
        con.commit()
        con.close()
        if passi == passit:
            session['cuser'] = n
            return jsonify({'info' : 1})
        else:
            return jsonify({'info' : "passwords dont match"})

    else:
        return jsonify({'info' : "error"})

@app.route('/reg')
def reg():
    return render_template('register.html')

@app.route('/regf', methods = ['POST'])
def regf():
    dn = request.form['dnt'] 
    n = request.form['nt'] 
    e = request.form['et']
    passi = request.form['passt']
    cpass = request.form['cpasst']
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists Users(username varchar, password varchar, nickname varchar, email varchar)')
    cursor.execute("select * from Users where username = '%s'" %n)
    U = None 
    for i in cursor:
        U = i
    if U:
        return jsonify({'info' : "User name taken"}) 
    
    if '.' in n:
        return jsonify({'info' : " '.' is not allowed in username"}) 


    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_"
    digits="0123456789"

    Ca = 0
    Sm = 0
    Sc = 0
    Di = 0
    for i in passi:
        if i in capitalalphabets:
            Ca+=1 
        if i in smallalphabets:
            Sm+=1 
        if i in specialchar:
            Sc+=1 
        if i in digits:
            Di+=1 
    
    if not Ca:
        return jsonify({'info' : 'The password should contain a uppercase letter'})
    
    if not Sm:
        return jsonify({'info' : 'The password should contain a lowercase letter'})

    if not Sc:
        return jsonify({'info' : 'The password should contain a one of the special character ($,@,_)'})

    if not Di:
        return jsonify({'info' : 'The password should contain a digit'})
    
    if len(passi) < 8:
        return jsonify({'info' : "The password should atleast have 8 characters"})

    if passi == cpass:
        hash_func = hashlib.sha1()
        string = passi + "h7"
        encoded_string=string.encode()
        hash_func.update(encoded_string)
        passi=hash_func.hexdigest()
        cursor.execute("insert into Users values (?, ?, ?, ?)", (n,passi,dn,e))
        con.commit()
        con.close()
        return jsonify({'info' : "registered successfully"})
    else:
        return jsonify({'info' : "passwords dont match"})


@app.route('/dash')
def dash():
    d = session['cuser']
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    if d:
        cursor.execute("select * from Users where username = '%s'" %d)
        U = None 
        for i in cursor:
            U = i 
        if U:
            L = []
            L.append(['Username : ',U[0]])
            L.append(['Nick Name', U[2]])
            L.append(['Email',U[3]])

            con = sqlite3.connect('users.db')
            cursor = con.cursor()
            cursor.execute('create table if not exists Cred(realuser varchar,website varchar, username varchar, password varchar)')
            
            cursor.execute("select * from Cred where realuser = '%s'" %d)
            cred = []
            for i in cursor:
                cred.append(i[1:])

            return render_template('dashboard.html',data = L, posts = cred)
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout', methods = ['POST'])
def logout():
    session['cuser'] = None 

    return jsonify({'info' : 1})

@app.route('/givepass', methods = ['POST'])
def givepass():
    s = request.form['st']
    t = s.split('-')
    print(t[0],t[1])
    return jsonify({'info' : 1})


@app.route('/addp', methods = ['POST'])
def addp():
    web = request.form['webt']
    user = request.form['usert']
    passi = request.form['passt']
    print(passi)
    if web.strip() == "" or user.strip() == "" or passi.strip() == "":
        return jsonify({'info' : "all entries are mandatory"})
    web = web.strip()
    user = user.strip()
    passi = passi.strip()
    print(web,passi,user)
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists Cred(realuser varchar,website varchar, username varchar, password varchar)')

    cursor.execute('select * from Cred where website = ? and username = ?', (web,user))
    U = None 
    for i in cursor:
        U = i 
    
    if not U:
        d = session['cuser']
        cursor.execute("insert into Cred values (?, ?, ?, ?)", (d,web,user,passi))
        con.commit()
        con.close()

        return jsonify({'info' : 1}) 

    return jsonify({'info' : "Error or the username of the website already exists"})

@app.route('/check2', methods = ['POST'])
def check2():
    passi = request.form['passt']
    d = request.form['dt']
    t = d.split('-')
    # w = t[0]
    # u = t[1]
    # w = w.split('_')
    # w = (".").join(w)
    # u = u.split('_')
    # u = (".").join(u)
    n = session['cuser']
    # t = [w,u]
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    cursor.execute('create table if not exists Users(username varchar, password varchar, nickname varchar, email varchar)')

    cursor.execute(f'select * from Users where username = "{n}"')
    Users = None
    for i in cursor:
        Users = i
        break
    if Users:
        print(Users)
        passit = Users[1]
        hash_func = hashlib.sha1()
        string = passi + "h7"
        encoded_string=string.encode()
        hash_func.update(encoded_string)
        passi=hash_func.hexdigest()
        print(passit)
        if passi == passit:
            cursor.execute('create table if not exists Cred(realuser varchar, website varchar, username varchar, password varchar)')
            cursor.execute('select * from Cred where website = ? and username = ?', (t[0],t[1]))
            pt = None 
            for i in cursor:
                pt = i
                break 
            if pt:
                print(pt)
                return jsonify({'info' : pt[3]})
            else:
                return jsonify({'info' : 'error'})
        else:
            return jsonify({'info' : "passwords dont match"})

    else:
        return jsonify({'info' : "error"})


@app.route('/delpass', methods = ['POST'])
def delpass():
    try:
        s = request.form['st']
        t = s.split('-')
        con = sqlite3.connect('users.db')
        cursor = con.cursor()
        cursor.execute('create table if not exists Cred(realuser varchar, website varchar, username varchar, password varchar)')

        cursor.execute('delete from Cred where website = ? and username = ?',(t[0],t[1]))
        con.commit()
        con.close()
        return jsonify({'info' : 1})
    
    except:
        return jsonify({'info' : 'error'})


if __name__ == "__main__":
    app.run(debug=True)