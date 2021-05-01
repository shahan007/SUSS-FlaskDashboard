from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db      = SQLAlchemy(app)
migrate = Migrate(app,db)

# Gets me all the routes created & models
from appProject import routes , models