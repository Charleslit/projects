from flask import Flask , render_template ,flash, redirect ,url_for
from forms import RegistrationForm,LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '5161d89653efc3056cc624fd3aac9243'


posts =[
      {'author':'jane doue',
      'date':'23/4/5',
      'title':'jany',
      'content':'first post'
},
{
      'author':'james',
      'date':'7/67/234',
      'title':'vikings',
      'content':'first post'

}

]

@app.route("/")

@app.route("/Home")
def Home():
      return render_template('Home.html', posts=posts)

@app.route('/About')
def about():
      return render_template('About.html', title='About')

@app.route('/Register',methods=['GET', 'POST'])
def register():
      form = RegistrationForm()
      if form.validate_on_submit():
           flash(f'account created for{form.username.data}!','success' )
           return redirect(url_for('Home'))
      return render_template('register.html', title='Register', form=form )
@app.route('/login')
def login():
      form = LoginForm()
      return render_template('login.html', title='Login', form= form )

      
if __name__ == '__main__':
 app.run(debug=True)