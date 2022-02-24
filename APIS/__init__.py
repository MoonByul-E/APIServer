from flask import Flask, render_template
import json

from .MapleStory import StarForce
from .MapleStory import RoyalStyle
from .MapleStory import MasterPiece
from .MapleStory import Beauty
from .MapleStory import GoldApple
from .MapleStory import WispsWonderBerry
from .MapleStory import LunaCrystal
from .MapleStory import Cube
from .MapleStory import TheSeed

from .LostArk import Avatar
from .LostArk import Character

app = Flask(__name__)

@app.route("/")
def function_Index():
    return render_template("index.html")

@app.route("/MapleStory")
def function_MapleStory_Index():
    return render_template("index_MapleStory.html")

@app.route("/LostArk")
def function_LostArk_Index():
    return render_template("index_LostArk.html")

@app.route("/.well-known/pki-validation/168E706C1C7CE806EEC83AE208BF10DA.txt")
def function_SSL():
    return "70A93419204DE6349F1058C74D11557CA35A4C215E7DF2AB430E1186487FD034\ncomodoca.com\n372f7723d95da70"

@app.errorhandler(404)
def function_Error(error):
    return json.dumps({"Result": "Error", "Error_Result": "Not Found"})


app.register_blueprint(StarForce.StarForce)
app.register_blueprint(RoyalStyle.RoyalStyle)
app.register_blueprint(MasterPiece.MasterPiece)
app.register_blueprint(Beauty.Beauty)
app.register_blueprint(GoldApple.GoldApple)
app.register_blueprint(WispsWonderBerry.WispsWonderBerry)
app.register_blueprint(LunaCrystal.LunaCrystal)
app.register_blueprint(Cube.Cube)
app.register_blueprint(TheSeed.TheSeed)

app.register_blueprint(Avatar.Avatar)
app.register_blueprint(Character.Character)