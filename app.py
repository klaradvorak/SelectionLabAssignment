from flask import Flask, render_template, redirect, request
import speedtest
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataDB.db'
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testDate = db.Column(db.DateTime, nullable=False, default=datetime.now())
    testSpeed = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Test %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        down = getDownloadSpeed()
        test1 = Test(testSpeed=down)
        try:
            db.session.add(test1)
            db.session.commit()
            return redirect('/')
        except:
            return "add to sql error"
        return render_template('index.html')

    else:
        tests = Test.query.order_by(Test.testDate).all()
        return render_template('index.html', tests=tests)

@app.route('/delete/<int:id>')
def delete(id):
    testDelete = Test.query.get_or_404(id)

    try:
        db.session.delete(testDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


def getDownloadSpeed():
    st = speedtest.Speedtest()
    downloadSpeed= st.download() / 1000000
    return downloadSpeed

if __name__ == '__main__':
    app.run()
