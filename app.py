from flask import Flask, render_template, request, url_for, redirect
import pymongo
from bson.objectid import ObjectId
import degrees
import datetime

# Tell Flask where the templates and static files are
app = Flask(__name__, template_folder='templates', static_folder='statics/', static_url_path='')
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')

# Use 'pymongo' to handle the MongoDB database
client = pymongo.MongoClient(
    "mongodb+srv://mrghastien:1aTmN4MsJfu7YVT0@dorset-database.lpewcuh.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
todos = db.todos


# Returns the number of seconds between the given date and the Unix epoch (Jan. 1 1970, 12 am)
def get_timestamp(date):
    return int(datetime.datetime.fromisoformat(date).timestamp())


# Function to get the tasks with the specified query,
# And marking them overdue or missed if necessary.
def getTasks(query):
    result = todos.find(query)
    now = datetime.datetime.now()
    tasks = []
    for q in result:
        if 'deadline' in q and q['deadline'] < now.timestamp():
            q['overdue'] = True
        if 'schedule' in q and q['schedule'] < now.timestamp():
            q['missed'] = True
        tasks.append(q)
    return tasks


# Route for displaying all the tasks
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        print(request.form)
        # Fill a dictionary with all the task's fields
        obj = {'content': request.form['content'], 'done': False}
        degree = request.form['degree'],
        obj['degree'] = degree[0]
        if 'deadline' in request.form:
            obj['deadline'] = get_timestamp(request.form['deadline-date'])
        if 'schedule' in request.form:
            obj['schedule'] = get_timestamp(request.form['schedule-date'])
        # and adding and entry to the database
        todos.insert_one(obj)
        # And redirecting to the same route but with the 'get' method.
        return redirect(url_for('index'))

    # Get all tasks
    all_todos = getTasks({})
    return render_template('index.html', todos=all_todos, degrees=degrees.degrees, parseDegree=degrees.parse)


@app.get('/agenda/')
def agenda():
    # Only query tasks that have deadlines in 3 days or less,
    # And tasks scheduled for today (up to 11:59 pm)
    now = datetime.datetime.now()
    searchThreshold = datetime.datetime.now() + datetime.timedelta(days=3)
    today = now.date()
    scheduleThreshold = datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time(0))

    deadlines = getTasks({'deadline': {'$lte': searchThreshold.timestamp()}, 'done': False})
    schedules = getTasks({'schedule': {'$lte': scheduleThreshold.timestamp()}, 'done': False})
    return render_template('agenda.html', deadlines=deadlines, schedules=schedules, parseDegree=degrees.parse)


@app.get('/tasks/<id>/')
def detail(id):
    task = getTasks({'_id': ObjectId(id)})[0]
    return render_template('detail.html', task=task, parseDegree=degrees.parse)


@app.post('/tasks/<id>/mark-done/')
def mark_done(id):
    # Toggle the status of the task
    task = getTasks({'_id': ObjectId(id)})[0]
    done = task['done']
    todos.update_one({'_id': ObjectId(id)}, {'$set': {'done': not done}})
    return redirect(url_for('detail', id=id))


@app.post('/tasks/<id>/delete/')
def delete(id):
    # Simply tell MongoDB to delete an entry
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
