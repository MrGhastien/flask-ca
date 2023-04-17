from flask import Flask, render_template, request, url_for, redirect
import pymongo
from bson.objectid import ObjectId
import degrees

app = Flask(__name__, template_folder='templates', static_folder='statics/', static_url_path='')
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')

client = pymongo.MongoClient(
    "mongodb+srv://mrghastien:1aTmN4MsJfu7YVT0@dorset-database.lpewcuh.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        print(request.form)
        obj = {'content': request.form['content']}
        degree = request.form['degree'],
        obj['degree'] = degree[0]
        if 'deadline' in request.form:
            obj['deadline'] = request.form['deadline-date']
        if 'schedule' in request.form:
            obj['schedule'] = request.form['schedule-date']
        todos.insert_one(obj)
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos, degrees=degrees.degrees, parseDegree=degrees.parse)


@app.get('/tasks/<id>/')
def detail(id):
    task = todos.find({'_id': ObjectId(id)}).next()
    print(task)
    return render_template('detail.html', task=task, parseDegree=degrees.parse)


@app.post('/tasks/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
