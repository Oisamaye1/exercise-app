from flask import Flask, render_template

app = Flask(__name__)


database = {
    "number": 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/increment')
def increment():
    database['number'] += 1
    return render_template('index.html', number = database['number'])

@app.route('/decrement')
def decrement():
    database['number'] -= 1
    return render_template('index.html', number = database['number'])

# if __name__ == '__main__':
#     app.run()
