from flask import *

from models import init_app as init_db
from resources import init_app as init_api


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] = r"DBU(#_*DCfh89hf98-2hV#*(&CV*&VCXB_#!(@&VCBX"

init_db(app)
init_api(app)


@app.route('/')
def index():
	return render_template("index.html")


if __name__	== "__main__":
	app.run(port=5000)
