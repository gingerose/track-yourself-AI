# app.py
from flask import Flask
from config import Config
from extensions import db
from controllers.schedule_controller import schedule_bp
from controllers.recommendation_controller import recommendation_bp
from controllers.decomposition_controller import decomposition_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(schedule_bp, url_prefix='/api')
app.register_blueprint(recommendation_bp, url_prefix='/api')
app.register_blueprint(decomposition_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
