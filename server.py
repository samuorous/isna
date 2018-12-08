import os

from flask import Flask, render_template, jsonify, request
from flask import current_app

from isna import IsnaSession

app = Flask(__name__, static_folder="static/dist", template_folder="static")
app.config.from_object('config')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/<resource>/<command>", methods=['GET', 'POST'])
def api(resource, command):
    if resource == 'sentence':
        if command == 'gets':
            return jsonify(current_app.isna.gets())
        if command == 'update':
            return jsonify(current_app.isna.update(request.json['tags']))
    return ''

if __name__ == "__main__":
    HERE = os.path.dirname(os.path.realpath(__file__))
    app.config['DATA_DIR'] = os.path.join(HERE, app.config['DATA_DIR'], app.config['SESSION_DIR'])
    app.isna = IsnaSession(
        data_dir=app.config['DATA_DIR'],
        unknown_tag=app.config['UNKNOWN_TAG']
    )

    with app.app_context():
        app.run()
    app.isna.store()
