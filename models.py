"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Cupcake class."""

    __tablename__ = 'cupcakes'

    # helpful to have a distinct idea per line so that git diff will show the distinct changes
    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    flavor = db.Column(db.Text, 
                       nullable=False)
    size = db.Column(db.Text, 
                     nullable=False)
    rating = db.Column(db.Float, 
                       nullable=False)
    image = db.Column(db.Text,
                      nullable=False,
                      default='https://tinyurl.com/demo-cupcake')

    def delete_msg(self):
        """Return message dict. for deleted cupcake."""

        return {"message": "Deleted"}