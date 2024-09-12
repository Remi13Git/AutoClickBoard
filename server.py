from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Activer CORS

# Définir les valeurs par défaut pour les variables
delayStart = 0
pauseClicks = 0.1
pauseKeyPress = 0.1
pauseLoops = 0
numberLoops = 5
showCursor = True
cursorSpeed = 1.5
cursorStyle = "easeOutQuad"
cursorRandomize = False
reverseScroll = 1

# Variables pour suivre l'état d'enregistrement et de la boucle
is_recording = False
is_rotating = False



@app.route('/')
def index():
    # Lire la valeur actuelle de showCursor dans le fichier de configuration JSON
    with open('config.json', 'r') as file:
        current_params = json.load(file)
    current_show_cursor = current_params.get('showCursor', False)

    # Rendre le modèle avec les valeurs actuelles des variables
    return render_template('index.html', 
                           delayStart=delayStart,
                           pauseClicks=pauseClicks,
                           pauseKeyPress=pauseKeyPress,
                           pauseLoops=pauseLoops,
                           numberLoops=numberLoops,
                           showCursor=current_show_cursor,
                           cursorSpeed=cursorSpeed,
                           cursorStyle=cursorStyle,
                           cursorRandomize=cursorRandomize,
                           reverseScroll=reverseScroll)



@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    # Mettre à jour les paramètres dans le fichier de configuration JSON
    params = {
        'delayStart': float(request.form.get('delayBeforeStart', 0)) if request.form.get('delayBeforeStart') else 0,
        'pauseClicks': float(request.form.get('pauseClicks', 0.1)) if request.form.get('pauseClicks') else 0.1,
        'pauseKeyPress': float(request.form.get('pauseKeyPress', 0.1)) if request.form.get('pauseKeyPress') else 0.1,
        'pauseLoops': float(request.form.get('pauseLoops', 0)) if request.form.get('pauseLoops') else 0,
        'numberLoops': int(request.form.get('totalLoops', 1)) if request.form.get('totalLoops') else 1,
        'showCursor': json.loads(request.form.get('showCursor', 'false').lower()),
        'cursorSpeed': float(request.form.get('cursorSpeed', 1.5)) if request.form.get('cursorSpeed') else 1.5,
        'cursorStyle': request.form.get('cursorStyle'),
        'cursorRandomize': request.form.get('cursorRandomize') == 'true',
        'reverseScroll': int(request.form.get('reverseScroll', 1))
    }

    with open('config.json', 'w') as file:
        json.dump(params, file)

    return "Parameters updated successfully!"


@app.route('/home')
def home():
    return "Server is running!"

@app.route('/start_loop')
def start_loop():
    subprocess.run(['python3', 'loop.py'])
    return 'Loop started'


@app.route('/start_record')
def start_record():
    subprocess.run(['python3', 'record.py'])
    return 'Record started'

@app.route('/get_record_status')
def get_record_status():
    return jsonify({'is_recording': is_recording})

@app.route('/stop_record')
def stop_record():
    global is_recording
    is_recording = False
    # Ajoutez le code pour arrêter l'enregistrement ici
    return 'Recording stopped'

@app.route('/get_loop_status')
def get_loop_status():
    return jsonify({'is_rotating': is_rotating})

@app.route('/stop_loop')
def stop_loop():
    global is_rotating
    is_rotating = False
    # Ajoutez le code pour arrêter la boucle ici
    return 'Loop stopped'

if __name__ == '__main__':
    app.run()
