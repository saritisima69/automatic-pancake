from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import requests
from gtts import gTTS
from playsound import playsound


UPLOAD_FOLDER = 'images'

if os.environ.get('DOCKER', '') == "yes":
    UPLOAD_FOLDER = '/usr/src/app/images'
else:
    UPLOAD_FOLDER = 'images'

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#url = 'http://app2/images'  <= las dos apps en contenedores
url = 'http://localhost:5050/images'

@app.route("/")
def home():
    return render_template('home.html')
    
@app.route('/uploader', methods = ['POST', ])
def upload_file():
    NO_VALID_IMAGE = "No se ha proporcionado una imagen valida :-("
    if request.method == 'POST' and request.files:
        f = request.files['image']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        files = {'fichero': (f.filename, open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)), 'rb'))}
        resp = requests.post(url=url, files = files)
        
        text = resp.json()['info']
        #text = NO_VALID_IMAGE 

        if not os.environ.get('DOCKER', '') == "yes":
           myobj = gTTS(text=text, lang="es", slow=False)
           myobj.save(app.config['UPLOAD_FOLDER'] + "/speech.mp3")
           playsound(app.config['UPLOAD_FOLDER'] + "/speech.mp3")      
        
        return render_template('results.html', text=text)
    return render_template('home.html')
    
if __name__ == '__main__':
    app.run(debug = True)
    