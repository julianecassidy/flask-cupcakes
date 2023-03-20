"""Flask app for Cupcakes"""

from flask import Flask, redirect, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
# import requests

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get('/api/cupcakes')
def get_all_cupcakes():
    """Returns JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.order_by('id').all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.get('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake_info(cupcake_id):
    """Returns JSON {cupcake: {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.post('/api/cupcakes')
def add_new_cupcake():
    """Add cupcake to DB and return JSON
    ex. {cupcake: {id, flavor, size, rating, image}}"""

    new_cupcake = Cupcake(
        flavor = request.json['flavor'],
        size = request.json['size'],
        rating = request.json['rating'],
        image = request.json['image'] or None
    )

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)