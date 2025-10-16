from flask import Flask
from flask_restx import Api, Resource, fields
from models import db, Utilisateur, Produit
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app, version="1.0", title="API Produits", description="API Flask + MariaDB avec Swagger UI")

# =========================
# Models Swagger
# =========================
utilisateur_model = api.model("Utilisateur", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True),
    "email": fields.String(required=True)
})

produit_model = api.model("Produit", {
    "id": fields.Integer(readonly=True),
    "brands": fields.String,
    "utilisateur_id": fields.Integer(required=True),
    "product_name": fields.String,
    "nutrition_grades": fields.String,
    "ecoscore_grade": fields.String,
    "lang": fields.String
})

# =========================
# Namespace utilisateurs
# =========================
ns_utilisateurs = api.namespace("utilisateurs", description="Opérations sur les utilisateurs")

@ns_utilisateurs.route("/")
class UtilisateurList(Resource):
    @ns_utilisateurs.marshal_list_with(utilisateur_model)
    def get(self):
        return Utilisateur.query.all()

    @ns_utilisateurs.expect(utilisateur_model, validate=True)
    @ns_utilisateurs.marshal_with(utilisateur_model, code=201)
    def post(self):
        data = api.payload
        if Utilisateur.query.filter_by(email=data["email"]).first():
            api.abort(400, "Email déjà utilisé")
        u = Utilisateur(name=data["name"], email=data["email"])
        db.session.add(u)
        db.session.commit()
        return u, 201

@ns_utilisateurs.route("/<int:id>")
@ns_utilisateurs.param("id", "ID de l'utilisateur")
class UtilisateurDetail(Resource):
    @ns_utilisateurs.marshal_with(utilisateur_model)
    def get(self, id):
        u = Utilisateur.query.get_or_404(id)
        return u

    def delete(self, id):
        u = Utilisateur.query.get_or_404(id)
        db.session.delete(u)
        db.session.commit()
        return {"message": "Utilisateur supprimé"}, 200

# =========================
# Namespace produits
# =========================
ns_produits = api.namespace("produits", description="Opérations sur les produits")

@ns_produits.route("/")
class ProduitList(Resource):
    @ns_produits.marshal_list_with(produit_model)
    def get(self):
        return Produit.query.all()

    @ns_produits.expect(produit_model, validate=True)
    @ns_produits.marshal_with(produit_model, code=201)
    def post(self):
        data = api.payload
        # Vérifier que l'utilisateur existe
        u = Utilisateur.query.get(data["utilisateur_id"])
        if not u:
            api.abort(404, "Utilisateur inexistant")
        p = Produit(
            brands=data.get("brands"),
            utilisateur_id=data["utilisateur_id"],
            product_name=data.get("product_name"),
            nutrition_grades=data.get("nutrition_grades"),
            ecoscore_grade=data.get("ecoscore_grade"),
            lang=data.get("lang")
        )
        db.session.add(p)
        db.session.commit()
        return p, 201

@ns_produits.route("/<int:id>")
@ns_produits.param("id", "ID du produit")
class ProduitDetail(Resource):
    @ns_produits.marshal_with(produit_model)
    def get(self, id):
        p = Produit.query.get_or_404(id)
        return p

    def delete(self, id):
        p = Produit.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return {"message": "Produit supprimé"}, 200

# =========================
# Lancement
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
