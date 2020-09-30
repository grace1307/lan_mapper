import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from marshmallow import ValidationError
from app.db import db
from app.marsh import marsh
from app.views import index

load_dotenv()


def start_app():
    app = Flask(__name__, static_url_path='/static')

    app.config["DEBUG"] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    CORS(app)

    app._static_folder = os.path.join(
        os.path.dirname(__file__),
        'public'
    )

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    db.init_app(app)
    marsh.init_app(app)

    app.register_blueprint(index.app)

    return app
