from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///block.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.id


@app.route('/')
@app.route('/home')
def projects():
    return render_template('projects.html')


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'server error'
    else:
        return render_template('create_article.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/posts')
def posts():
    art = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', art=art)


@app.route('/posts/<int:id>')
def posts_d(id):
    arti = Article.query.get(id)
    return render_template('posts_d.html', arti=arti)


@app.route('/posts/<int:id>/del')
def post_del(id):
    arti = Article.query.get_or_404(id)

    try:
        db.session.delete(arti)
        db.session.commit()
        return redirect('/posts')
    except:
        return "An error occurred during deletion, please try again."


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    arti = Article.query.get(id)
    if request.method == 'POST':
        arti.title = request.form['title']
        arti.intro = request.form['intro']
        arti.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'An error occurred during the update, restart the server'
    else:
        return render_template('post_update.html', arti=arti)


@app.route('/chartjs-example')
def homepage():

    labels = [
        '2002',
        '2004',
        '2006',
        '2008',
        '2010',
        '2012',
        '2014',
        '2016',
        '2018',
        '2020',
        '2022',
        '2024'
    ]
    data = [1.5, 7, 5, 3, 6, 6, 2, 7, 9, 12, 14, 16]
    return render_template(
        template_name_or_list='chartjs-example.html',
        data=data,
        labels=labels,
    )

@app.route('/pie')
def pie():
    labels = [
        'JAN', 'FEB', 'MAR', 'APR',
        'MAY', 'JUN', 'JUL', 'AUG',
        'SEP', 'OCT', 'NOV', 'DEC'
    ]

    values = [
        967.67, 1190.89, 1079.75, 1349.19,
        1328.91, 2504.28, 1873.83, 4764.87,
        2349.29, 3458.30, 1907, 1297
    ]

    colors = [
        "rgba(200,200,200,0.2)", "rgba(205,205,205,0.2)", "rgba(210,210,210,0.2)", "rgba(215,215,215,0.2)",
        "rgba(220,220,220,0.2)", "rgba(225,225,225,0.2)", "rgba(230,230,230,0.2)", "rgba(235,235,235,0.2)",
        "rgba(240,240,240,0.2)", "rgba(245,245,245,0.2)", "rgba(250,250,250,0.2)", "rgba(255,255,255,0.2)"]

    pie_labels = labels
    pie_values = values
    return render_template('pie.html', title='The popularity of the flask framework', max=17000, set=zip(values, labels, colors))





if __name__ == '__main__':
    app.run(debug=True)
