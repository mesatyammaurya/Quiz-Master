from flask import Flask
from models import db
from controllers.routes import init_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'Satyam_Maurya'


db.init_app(app)

init_routes(app)

with app.app_context():
    db.create_all()

# python -c 'import secrets; print(secrets.token_hex())'  # for secret key
    
if __name__ == "__main__":
    app.run()
