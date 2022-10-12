from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(20))

    #backref to medications - attribute for free

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Medication(db.Model):
    """A medication."""

    __tablename__ = "medications"

    med_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    med_name = db.Column(db.String(30), nullable=False, unique=False)
    med_dosage = db.Column(db.Float, nullable=False, unique=False) #med dosage in milligrams
    med_quantity = db.Column(db.Integer, nullable=False, unique=False) #how many pills
    med_frequency = db.Column(db.Integer, nullable=False, unique=False) #how many times per day

    user = db.relationship("User", backref="medications")    

    def __repr__(self):
        return f"<Medication med_id={self.med_id} med_name={self.med_name} med_dosage={self.med_dosage} med_quantity={self.med_quantity} med_frequency={self.med_frequency}>"

    
def connect_to_db(flask_app, db_uri="postgresql:///medications", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    db.create_all()