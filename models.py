"""Models for Cupcake app."""
 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"


class Cupcake(db.Model):
    """Cupcake."""

    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )

    flavor = db.Column(
       db.String(30),
       nullable=False 
    )

    size = db.Column(
        db.String(30),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    image = db.Column(
        db.String(500),
        nullable=False,
        default=DEFAULT_IMAGE_URL
    )
