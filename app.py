from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key="dhsg"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///orders.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Information(db.Model):

    orderno = db.Column(db.Integer, primary_key = True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable = True)
    lastname = db.Column(db.String(20), nullable = True)
    phoneNumber = db.Column(db.String(12), nullable = True)
    email = db.Column(db.String(120), nullable = True)
    country = db.Column(db.String(25), nullable = True)
    city = db.Column(db.String(25), nullable = True)
    address1 = db.Column(db.String(200), nullable= True)
    address2 = db.Column(db.String(100), nullable= True)
    ZIP = db.Column(db.Integer,nullable=True)
    orientation = db.Column(db.String(10), nullable=True)
    size = db.Column(db.String(10), nullable=True)
    ShippingMethod = db.Column(db.String(15), nullable=True)

    def __repr__(self) -> str:
        return f"{self.orderno}"

@app.route("/index")
@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method=="POST":
        session['orientation'] = request.form['Orientation']
        session['size'] = request.form['size']
        return redirect(url_for("info")) 
    return render_template("create.html")

@app.route("/info", methods=["GET", "POST"])
def info():
    if request.method=="POST":
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['phoneNumber'] = request.form['phoneno']
        session['email']= request.form['email']
        session['country'] = request.form['country']
        session['city'] = request.form['city']
        session['address1'] = request.form['address-1'] 
        session['address2'] = request.form['address-2']
        session['ZIP'] = request.form['zip']
        return redirect(url_for("shipping")) 
    return render_template("info.html",session=session)

@app.route("/shipping", methods=["GET", "POST"])
def shipping():
    if request.method=="POST":
        session['shippingmethod'] = request.form['shipping-method']
        return redirect(url_for("payment")) 
    return render_template("shipping.html",session=session)

@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method=="POST":
        info = Information(firstname=session['firstname'],lastname=session['lastname'],phoneNumber=session['phoneNumber'],email=session['email'],country=session['country'],city=session['city'],address1=session['address1'],address2=session['address2'],ZIP=session['ZIP'],orientation=session['orientation'],size=session['size'],ShippingMethod=session['shippingmethod'])
        db.session.add(info)
        db.session.commit()
        session['orderno'] = info.orderno
        return redirect(url_for("uploadpics")) 
    return render_template("payment.html")

@app.route("/uploadpics", methods=["GET", "POST"])
def uploadpics():
   
    if request.method=="POST":
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(session['orderno'])))
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(session['orderno']))
        print(path)
        file = request.files['MAIN']
        if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(session['orderno']), filename))
           name="MAIN.jpg"
           os.rename(os.path.join(path,filename),os.path.join(path,name))
        files = request.files.getlist('files[]')
        file_names=[]
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_names.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(session['orderno']), filename))

        
        for i, filename in enumerate(os.listdir(path)):
            if filename != "MAIN.jpg":
                name = str(i) + ".jpg"
                os.rename(os.path.join(path,filename),os.path.join(path,name)) 
               
        return redirect(url_for("revieworder")) 

    return render_template("uploadpics.html")

@app.route("/revieworder", methods=["GET", "POST"])
def revieworder():
    return render_template("revieworder.html",session=session)

@app.route("/completeorder", methods=["GET", "POST"])
def completeorder():
    return render_template("completeorder.html")

@app.route("/test")
def test():
    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], str(session['orderno'])))
    return redirect("\create")

@app.route("/giftcard")
def giftcard():
    return render_template("Giftcard.html")

if __name__ == "__main__":
    app.run(debug=True)



# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # If the user does not select a file, the browser submits an
#         # empty file without a filename.
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>