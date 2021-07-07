from flask import Flask
from flask_cors import CORS
from flask import request
from src.bot import getResponse

app = Flask(__name__)
CORS(app)
# logging.getLogger('flask_cors').level = logging.DEBUG

@app.route('/')
def hello_world():
    # logging.getLogger('flask_cors').level = logging.DEBUG
    return {'hi':"yo"}

@app.route('/msg',methods=['POST'])
def get_msg():
    return (getResponse(request.get_json()['msg']))
    pass