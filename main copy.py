from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField 
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField ,SubmitField,IntegerField
from wtforms.validators import InputRequired 
from werkzeug.security import generate_password_hash 
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect




app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'secretkey'
Bootstrap5(app)


app.app_context().push()

class Books(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    author = db.Column(db.String(20), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # def __repr__(self):
    #     return f"Id:{self.id},Name : {self.name}, Author: {self.author}"
    
class MyForm(FlaskForm): 
    name = StringField('Name', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    rating = DecimalField('Rating', validators=[InputRequired()]) 
    submit = SubmitField('Submit') 
    


@app.route('/')
def home():
    all_books = Books.query.all()

    return render_template('index.html',books=all_books)

@app.route('/table')
def table():
  
    return render_template('table.html')


@app.route("/add/<int:id>", methods=['GET', 'POST'])
def add(id=0):
    form = MyForm() 
    if id==0:
        if request.method=='POST':
            if form.validate_on_submit(): 
                name = form.name.data 
                author = form.author.data 
                rating = form.rating.data 
                p = Books(name=name, author=author, rating=rating)
                db.session.add(p)
                db.session.commit()
                return redirect('/')
        return render_template('add.html',form=form,id=id)
    else:
        book_data = Books.query.filter_by(id=id).first()
        if request.method=='GET':
            
            print('Get')
            return render_template('add.html',form=form,update_data=book_data,id=id)
            
        else:
            print('POST')
            if form.validate_on_submit(): 
                name = form.name.data 
                author = form.author.data 
                rating = form.rating.data 
                p = Books(name=name, author=author, rating=rating)
                db.session.add(p)
                db.session.commit()
                return redirect('/')
        return render_template('add.html',form=form,id=id)    



@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and 
    # redirects to home page
    data = Books.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

