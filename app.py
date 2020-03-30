"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
# from flask_wtf import FlaskForm
# from forms import AddPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


# Opportunity to move this function into the Cupcake model to make it an instance method
def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy object to a dictionary"""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }

@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Get data about all cupcakes in JSON
    {'cupcakes': [{id, flavor, size, rating, image}...]}."""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:id>')
def list_single_cupcake(id):
    """Get data about a single cupcakes in JSON
    {'cupcake': {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    """Add a new cupcake to the database using post request JSON sent.
    Respond with JSON {cupcake: {id, flavor, size, rating, image}}"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    # how does it know which falsey value to default to? it reads it left to right
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, 
                          size=size, 
                          rating=rating, 
                          image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)
    # how do we remove possibility of duplication
    # add constraints of UNIQUE but do it across multiple columns (see stackoverflow)
    # can add these constraints in __args__(?)
