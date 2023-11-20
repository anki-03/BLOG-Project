from flask import Flask,redirect,url_for,render_template,request,session
import sqlite3,os



app=Flask(__name__)
app.secret_key="abcd"

UPLOAD_FOLDER = "D:\Programs\Fortune Cloude Class\Python\AdvancePython\BlogProject\static\images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    con=sqlite3.connect("blog.db")
    cur=con.cursor()
    data = con.execute('SELECT * FROM Blog').fetchall()
   
    return render_template('index.html', data=data)
    


@app.route("/admin")
def admin():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def login_check():
    if request.method =='POST':
        email=request.form["email"]
        passs=request.form["passs"]

        if (email=="dhanesh@123" and passs=="123"):
            return redirect(url_for("blog_admin"))
        else:
            return redirect(url_for("admin"))


@app.route("/blog_details")
def blog_admin():
   
        con=sqlite3.connect("blog.db")
        cur=con.cursor()
        cur.execute("select * from Blog")
        data=cur.fetchall()
        return render_template("blog_details.html",data=data)



@app.route("/logout")
def logout():
    return redirect(url_for("admin"))

@app.route("/newblog")
def newblog():
    return render_template("Newblog.html")




@app.route("/updateblog")
def updateblog():
        con=sqlite3.connect("blog.db")
        cur=con.cursor()
        cur.execute("select * from Blog")
        data=cur.fetchall()
        return render_template("update.html",data=data)



#POST Buttun
@app.route("/save",methods=["POST","GET"])
def save():
    if request.method=="POST":
        Blog=request.form["Blog"]
        post=request.form["post"]
        Description=request.form["Description"]
        Date=request.form["Date"]
        img=request.files["img"]

        con=sqlite3.connect("blog.db")
        cur=con.cursor()
        img.save(os.path.join(app.config["UPLOAD_FOLDER"],img.filename))
        
        cur.execute("insert into Blog(Blog,post,Description,Date,img) values (?,?,?,?,?)",(Blog,post,Description,Date,img.filename))

        con.commit()
        cur.execute("select * from Blog")
        data=cur.fetchall()

        return render_template("blog_details.html",data=data)
    else:
        return "fail"

@app.route("/delete/<int:id>")
def delete(id):
    
        con=sqlite3.connect("blog.db")
        cur=con.cursor()
        cur.execute("delete from Blog where id=?",[id])
        con.commit()
        return redirect(url_for("updateblog"))



@app.route("/edit/<int:id>")
def edit(id):
    
        con=sqlite3.connect("blog.db")
        cur=con.cursor()
        cur.execute("select * from Blog where id=?",[id])
        data=cur.fetchone()
        return render_template("edit.html",data=data)

@app.route("/change",methods=["POST","GET"])
def change():
    if request.method=="POST":
        id=request.form["id"]
        Blog=request.form["Blog"]
        post=request.form["post"]
        Description=request.form["Description"]
        Date=request.form["Date"]
        img=request.files["img"]
        img.save(os.path.join(app.config["UPLOAD_FOLDER"],img.filename))
       
        con=sqlite3.connect("blog.db")
        cur=con.cursor()

        

        cur.execute("update  Blog set Blog=?,post=?,Description=?,Date=?,img=?  where id=?",(Blog,post,Description,Date,img.filename,id))

        con.commit()
        

        return redirect(url_for("updateblog"))
    else:
        return redirect(url_for("blog_admin"))




@app.route("/contact")
def contact():
    return render_template("contact.html")




if __name__=='__main__':
    app.run(debug=True) #For automatic Update