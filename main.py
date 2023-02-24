from library import *
# for importing the mail
from flask import *
from flask_mail import Mail, Message
import mysql.connector
import random
from flask_recaptcha import * # Import ReCaptcha objects
from flask_bcrypt import Bcrypt
from PIL import *
from PIL import Image, ImageDraw, ImageFont

ob=db()
bcrypt = Bcrypt()

app = Flask(__name__)

app.secret_key="nightwing"

@app.route("/", methods=['POST','GET'])
def login():
    return render_template("login.html")

@app.route("/registration")
def Resistration():
    return render_template("registration.html")

@app.route("/insert",methods=['POST','GET'])
def insert():
    try:
        if(request.method=="POST"):
            name=request.form["xname"]
            age=request.form["xage"]
            email=request.form["xmail"]
            phone=request.form['xphone']
            password=request.form['xpas']
            myfile=request.files['xfile']

            myfilename=(str(random.randint(11111,99999)) + "_" + myfile.filename)
            myfile.save("static/upload/" + myfilename)
            im = Image.open("static/upload/" + myfilename)
            im = im.resize((250,250))
            width, height = im.size

            draw = ImageDraw.Draw(im)
            text = "@TECHFLY"

            font = ImageFont.truetype('arial.ttf', 20)
            textwidth, textheight = draw.textsize(text, font)

            
            margin = 10
            x = width - textwidth - margin
            y = height - textheight - margin


            draw.text((x, y), text, font=font)
            
            im.save("static/upload/"+ myfilename)

            pw_hash = bcrypt.generate_password_hash(password)
            dt={"name":name,"email":email,"phone":phone,"password":pw_hash.decode(),"age":age,"image":myfilename}
            retValue=ob.insertdata("member",dt)

            if(retValue['count']>=1):
                message="You have Succesfully registered Yourself"
            else:
                message="You are not registered"
            return render_template("registration.html",mydata=message)
        else:
            return render_template("404.html")  
            
    except:
        message="Email already exist"
        return render_template("registration.html",mydata=message)


@app.route("/auth", methods=['GET','POST'])
def login_auth():
    # if not recaptcha.verify(): # Use verify() method to see if ReCaptcha is filled out
    #     message = 'Please Verify Human Verification' # Send success message
    #     return render_template("login.html", mydata=message)
    if(request.method=="POST"):
        email=request.form['xmail']
        pas=request.form['xpas']
        retValue= ob.getSingleData("member","email",email)

        if(bcrypt.check_password_hash(retValue['data'][5], pas)==True and email==retValue['data'][3]):
            session['username']=retValue['data'][1]
            session['image']=retValue['data'][6]
            session['email']=retValue['data'][3]
            session['age']=retValue['data'][2]


            session['login']=True
            #for creating cookies
            if("rem" in request.form):
                resp = make_response(render_template("home.html"))
                resp.set_cookie('email', email)
                resp.set_cookie('password',pas)
                return resp
            else:
                return render_template("home.html")
        else:
            message="Email or password is not found"
            return redirect("/")
    else:
        return render_template("404.html")

# for destroying the session
@app.route("/logout")
def logout():
    session.pop("login")
    session.pop("username")
    session.pop("image")
    session.pop("age")

    session.clear()
    # for destroying the cookie
    resp = make_response(render_template("login.html"))
    resp.set_cookie('email','', expires=10)
    resp.set_cookie('password','', expires=10)
    return resp

@app.route("/update",methods=['POST','GET'])
def update():
    return render_template("update.html")

        


    
@app.route("/form")
def form():    
    return render_template("form.html") 

@app.route("/service")
def service():
    return render_template("service.html")

if __name__ == '__main__':
   app.run(debug=True)