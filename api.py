# from colorama import Cursor
from distutils.util import execute
from colorama import Cursor
from flask import *
import mysql.connector
from datetime import datetime, timedelta

app=Flask(__name__)

app.secret_key='user' 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Shukurmern@786",
  database="project2"
)


mycursor = mydb.cursor(buffered=True)



@app.route('/index',methods=['POST','GET'])
def home0():
    return render_template('index.html')



@app.route('/reg',methods=['POST','GET'])
def home2():
    return render_template('reg.html')


@app.route('/regf',methods=['POST','GET'])
def home4():
    r=dict(request.form)
    print(r)
    global mydb
    global mycursor
    s="insert into customers(c_name,c_email,c_mobile,c_password,c_gender)  values(%s,%s,%s,%s,%s) "
    l=[r['u'],r['e'],r['m'],r['p'],r['g']]
    mycursor.execute(s,l)
    mydb.commit()
    return render_template('login.html')


@app.route('/login',methods=['POST','GET'])
def home3():
    return render_template('login.html')


@app.route('/loginf',methods=['POST','GET'])
def home5():
    r=dict(request.form)
    print(r)
    if len(r)<2:
        return render_template('login.html',u="Please Enter All Fields")
    s="select * from customers where c_name=%s and c_password=%s"
    l=[r['u'],r['p']]
    mycursor.execute(s,l)
    l1=list(mycursor)
    if len(l1)<1:
        return render_template('login.html',u="Invalid Login")
    session['city']=""
    mycursor.execute("select c_id from customers where c_name=%s",[r['u']])
    session['username']=list(mycursor)[0][0]
    return redirect(url_for('movies'))
    

@app.route('/alogin',methods=['POST','GET'])
def adlogin():
    return render_template('alogin.html')


@app.route('/aloginf',methods=['POST','GET'])
def adloginf():
        r=dict(request.form)
        if r['u']=='Irfan' and r['p']=='@123':
            session['msg']=""
            return render_template('admin.html',u="")
        else:
            
                global mycursor
                s="select * from t_owner where o_name=%s and o_pass=%s"
                print(r)
                mycursor.execute(s,[r['u'],r['p']])
                l=list(mycursor)
                if len(l)==0:
                    return render_template('alogin.html',u="Invalid login")

                mycursor.execute("select o_id from t_owner where o_name=%s",[r['u']])
                p=list(mycursor)[0][0]
                mycursor.execute("select t_id from theater where o_id=%s",[p])
    
                session['tid']=list(mycursor)[0][0]
                print(session['tid'])
                session['admin']=r['u']
                session['show']=""
                return render_template('toadmin.html',u=r['u'])



@app.route('/addtheater',methods=['POST','GET'])
def addtheater():
    s="select * from city "
    global mydb
    global mycursor
    mycursor.execute(s)
    l=list(mycursor)
    print(l)
    s="select o_name from t_owner"
    mycursor.execute(s)
    l1=list(mycursor) 
    print(l1) 
    if len(session['msg'])>2:
             msg="Successfully Added"
    else:
        msg=""
    return render_template('addtheater.html',u=l,u1=l1,msg=msg)

@app.route('/temp/<m_id>',methods=['POST','GET'])
def temp(m_id):
    print(m_id)
    r=dict(request.form)
    print(r)
    return ""

@app.route('/addtheaterf',methods=['POST','GET'])
def addtheaterf():
    r=request.form
    print(r)
    s=f"select city_id from city where pincode={r['p']}"
    global mydb
    global mycursor
    mycursor.execute(s)
    p1=list(mycursor)[0][0]
    print(p1)
    s="select o_id from t_owner where o_name=%s"
    mycursor.execute(s,[r['o']])
    p2=list(mycursor)[0][0]
    print(p2)
    l=[r['n'],p2,r['y'],p1]
    s="insert into theater(t_name,o_id,e_year,c_id) values(%s,%s,%s,%s)"
    mycursor.execute(s,l)
    mydb.commit()
    mycursor.execute("select t_id from theater order by t_id desc limit 1")
    p3=list(mycursor)[0][0]
    print(p3)
    ts=int(r['ts'])
    for i in range(1,ts+1):
        s=f"insert into seats(t_id,se_id) values({p3},{i})"
        mycursor.execute(s)
        mydb.commit()
    session['msg']='successfully added'
    return redirect(url_for('addtheater'))


@app.route('/addmovie',methods=['POST','GET'])
def addmovie():   
    return render_template('addmovie.html',u= "")

@app.route('/addmovief',methods=['POST','GET'])
def addmovierf():    
        r=dict(request.form)
        print(r)
        global mydb
        global mycursor
        s="insert into movies(m_name,m_desc,m_genre,m_year,m_length) values(%s,%s,%s,%s,%s)"
        l=[r['m'],r['d'],r['g'],r['y'],r['l']]
        mycursor.execute(s,l)
        mydb.commit()
        return render_template('addmovie.html',u='Successfully Added')
            
@app.route('/toaddmovie',methods=['POST','GET'])
def toaddmovie():   
    return render_template('toaddmovie.html',u= "")

@app.route('/addmovief',methods=['POST','GET'])
def toaddmovierf():    
        r=dict(request.form)
        print(r)
        global mydb
        global mycursor
        s="insert into movies(m_name,m_desc,m_genre,m_year,m_length) values(%s,%s,%s,%s,%s)"
        l=[r['m'],r['d'],r['g'],r['y'],r['l']]
        mycursor.execute(s,l)
        mydb.commit()
        return render_template('toaddmovie.html',u='Successfully Added')
        
@app.route('/addcity',methods=['POST','GET'])
def addcity(): 
    return render_template('city.html',u= "")

@app.route('/addcityf',methods=['POST','GET'])
def addcityf(): 
    r=dict(request.form)
    global mydb
    global mycursor

    s="insert into city(c_name,pincode) values(%s,%s)"
    l=[r['c'],r['p']]
    try:
        mycursor.execute(s,l)
        mydb.commit()
        return render_template('city.html',u1='Successfully Added')
    except:
        return render_template('city.html',u='Already Exists')



@app.route('/addowner',methods=['POST','GET'])
def addowner(): 
   return render_template('addowner.html',u="")

@app.route('/addownerf',methods=['POST','GET'])
def addownerf(): 
    r=dict(request.form)
    print(r)
    l=[r['n'],r['b'],r['e'],r['m'],r['g'],r['id'],r['idnum'],r['p']]
    s="insert into t_owner(o_name,o_dob,email,o_mobile,gender,id_type,id_num,o_pass) values(%s,%s,%s,%s,%s,%s,%s,%s)"
    global mycursor
    global mydb
    try :
        mycursor.execute(s,l)
        mydb.commit()
        return render_template("addowner.html",u="successffuly Added")
    except:
        return render_template("addowner.html",u="check details")

@app.route('/toaddshow',methods=['POST','GET'])
def addshow():
    s="select m_name,m_year,m_id from movies"
    global mycursor
    mycursor.execute(s)
    l=list(mycursor)
    if len(session['show'])>10:
        msg=session['show']
        session['show']=""
        return render_template('toaddshow.html',u=msg,u1=l)
    return render_template('toaddshow.html',u1=l)

@app.route('/toaddshowf',methods=['POST','GET'])
def addshowf(): 
        r=dict(request.form)
        print(r['d'])
        now = datetime.now()
        print(now)
        pr = now.strftime('%Y-%m-%d')
        pd = datetime.strptime(pr,'%Y-%m-%d')
        sd=datetime.strptime(r['d'], '%Y-%m-%d')
        print(pd,sd,end='\n')
        print(sd >= pd )
        if sd >= pd :
                s_t=datetime.strptime(r['s']+':00', '%H:%M:%S')
                e_t=datetime.strptime(r['e']+':00', '%H:%M:%S')
                global mydb
                global mycursor
                try:
                        mycursor.execute("select s_end from shows where t_id=%s and s_date=%s order by s_end desc limit 1",[session['tid'],r['d']])
                        de=list(mycursor)[0][0]
                        print(de)
                        de=datetime.strptime(str(de), '%H:%M:%S')
                        print(s_t < de)
                        if s_t < de:
                            session['show']="time overlapse with previous show time"
                            return redirect(url_for('addshow'))

                        s="insert into shows(t_id,m_id,s_date,s_start,s_end)  values(%s,%s,%s,%s,%s)"
                        mycursor.execute(s,[session['tid'],r['m'],r['d'],s_t,e_t])
                        session['show']="Successfully Added"
                        return redirect(url_for('addshow'))
                except:
                        
                        s="insert into shows(t_id,m_id,s_date,s_start,s_end)  values(%s,%s,%s,%s,%s)"
                        mycursor.execute(s,[session['tid'],r['m'],r['d'],s_t,e_t])
                        session['show']="Successfully Added"
                        mydb.commit()
                        return redirect(url_for('addshow'))

        session['show']="Date Need to more then or equal to today date"
        return redirect(url_for('addshow'))

        
        
@app.route('/movies',methods=['POST','GET'])
def movies():
    s="select * from city "
    global mydb
    global mycursor
    mycursor.execute(s)
    l1=list(mycursor)
    s="select distinct m.*  from movies m join shows s on s.m_id=m.m_id"
    mycursor.execute(s)
    l2=list(mycursor)
    return render_template('movies.html',u="Add city to search",u1=l1,u2=l2)


@app.route('/citymovie',methods=['POST','GET'])
def citymovies():
    r=dict(request.form)
    session['city']=r['city']
    # s="select *  from movies m join shows s on s.m_id=m.m_id join theater t on  t.t_id=s.t_id join city c on c.city_id=t.c_id where c.pincode=%s;
    s="select distinct m.* from movies m where m.m_id in ( select m_id from shows s where t_id in (select t_id from theater t join city on city.city_id=t.c_id where city.pincode=%s) ) "
    global mycursor
    mycursor.execute(s,[r['city']])
    l2=list(mycursor)
    if len(l2)<1:
        msg="You don't have any shows in your area"
    else:
        msg=""
    s="select * from city"
    mycursor.execute(s)
    l1=list(mycursor)
    return render_template('movies.html',u="Add city to search",u1=l1,u2=l2,msg=msg)


@app.route('/theater/<m_id>',methods=['POST','GET'])
def theater(m_id):
    print(m_id)
    c=session['city']
    global mycursor
    if len(c)>0:
        s="select distinct t.*,c.* from shows s join theater t on s.t_id=s.t_id join city c on c.city_id=t.c_id where c.pincode=%s and s.m_id=%s and s.s_date > now()"
        # now = datetime.now()
        # pd= now.strftime('%Y-%m-%d %H:%M:%S')
        mycursor.execute(s,[c,m_id])
        l1=list(mycursor)
        print(l1)
        s="select * from city"
        mycursor.execute(s)
        l2=list(mycursor)
        timings=[]
        for i in l1:
                s="select s_date,s_start from shows where t_id=%s and m_id=%s "
                mycursor.execute(s,[i[0],m_id])
                n=tuple(mycursor)
                if len(n)<1:
                      n=("","")
                timings.append(n)
        print(timings)
        return render_template('theater.html',u1=l2,u2=l1,timings=timings)
        
        
    s="select distinct t.*,c.* from shows s join theater t on s.t_id=s.t_id join city c on c.city_id=t.c_id where s.m_id=%s and s.s_date > now()"
    mycursor.execute(s,[m_id])
    l1=list(mycursor)
    s="select * from city"
    mycursor.execute(s)
    l2=list(mycursor)
    timings=[]
    for i in l1:
        s="select s_date,s_start from shows where t_id=%s and m_id=%s"
        mycursor.execute(s,[i[0],m_id])
        n=tuple(mycursor)
        if len(n)<1:
            n=("","")
        timings.append(n)
    print(timings)
    return render_template('theater.html',u1=l2,u2=l1,timings=timings)
    
@app.route('/selectseat/<tid>',methods=['POST','GET'])
def selectseat(tid): 
    r=str(dict(request.form)['datetime']).split(',')
    print(r)
    global mycursor
    try:
        s="select s_id from shows where s_date=%s and t_id=%s and s_start=%s"
        mycursor.execute(s,[r[0],tid,r[1]])
        sid=list(mycursor)[0][0]
        print(sid)
        session['sid']=sid
        mycursor.execute("select se_id from seats where t_id=%s",[tid])
        l=list(mycursor)
        print(l)
        str1="<div class='row1'>"
        c=0
        for i in l:
                print(i[0])
                s=f'<input type="checkbox" name="{i[0]}" value="{i[0]}">'
                str1=str1+s
                c=c+1
                if c==10:
                    c=0
                    str1=str1+"</div><div class='row1'>"
        str1=str1+"</div>"
        return render_template('selectseats.html',seats=str1)
    except:
        return "render_template('movies.html')"
    
@app.route('/bookings',methods=['POST','GET'])
def boookings(): 
        r=list(dict(request.form).values())
        print(r)
        global mycursor
    # try:
        mycursor.execute("insert into bookings(s_id,c_id) values(%s,%s)",[session['sid'],session['username']])
        mycursor.execute("select b_id from bookings order by b_id desc limit 1")
        bid=list(mycursor)[0][0]
        print(bid)
        print(session['sid'])
        for i in r:
                mycursor.execute("insert into booking_seats(b_id,s_id,se_id,price) values(%s,%s,%s,%s)",[bid,session['sid'],i,100])
        mydb.commit()
        return "<h1>successfully Booked</h1>"
    # except:
    #     return "failure"

@app.route('/mybookings',methods=['POST','GET'])
def mybookings(): 
      s='select b.b_id,bs.se_id,s.s_date,s.s_start,t.t_name,s.s_status from bookings b join booking_seats bs on bs.b_id=b.b_id join shows s on s.s_id=bs.s_id join theater t on t.t_id=s.t_id where b.c_id=%s '
      global mycursor
      mycursor.execute(s,[session['username']])
      l=list(mycursor)
      if len(l)<1:
          return render_template('mybookings.html',u="You didn't Started Your Bookings upto now")
      return render_template('mybookings.html',l=l)

@app.route('/cancelshows',methods=['POST','GET'])
def cancelshows():
    s="select m.m_id,m.m_name,s.s_date,s.s_start,s.s_end,m.m_length,s.s_id from shows s join movies m on m.m_id=s.m_id where t_id=%s and s.s_status='1'"
    global mycursor
    mycursor.execute(s,[session['tid']])
    l=list(mycursor)
    return render_template('cancelshows.html',l=l)

@app.route('/cancelshowsf/<sid>',methods=['POST','GET'])
def cancelshowsf(sid):
    print(sid)
    global mycursor
    mycursor.execute("update shows set s_status='0' where s_id=%s",[sid])
    mycursor.execute("update booking_seats set bs_status='0' where s_id=%s",[sid])
    mydb.commit()
    return redirect(url_for('cancelshows'))

@app.route('/showscancelled',methods=['POST','GET'])
def showscancelled():
    s="select m.m_id,m.m_name,s.s_date,s.s_start,s.s_end,m.m_length,s.s_id from shows s join movies m on m.m_id=s.m_id where t_id=%s and s.s_status=%s"
    global mycursor
    mycursor.execute(s,[session['tid'],'0'])
    l=list(mycursor)
    return render_template('cancelshows.html',l1=l)

app.run(debug=True)