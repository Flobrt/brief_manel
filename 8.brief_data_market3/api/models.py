from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Utilisateur(db.Model):
    __tablename__ = "utilisateurs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

class Produit(db.Model):
    __tablename__ = "produits"
    id = db.Column(db.Integer, primary_key=True)
    brands = db.Column(db.String(255))
    utilisateur_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"))
    product_name = db.Column(db.String(255))
    nutrition_grades = db.Column(db.String(10))
    ecoscore_grade = db.Column(db.String(10))
    lang = db.Column(db.String(10))

    def to_dict(self):
        return {
            "id": self.id,
            "brands": self.brands,
            "utilisateur_id": self.utilisateur_id,
            "product_name": self.product_name,
            "nutrition_grades": self.nutrition_grades,
            "ecoscore_grade": self.ecoscore_grade,
            "lang": self.lang
        }

