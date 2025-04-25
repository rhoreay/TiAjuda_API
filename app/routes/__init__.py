from app.routes.newticket import newticket_bp

def register_routes(app):
    app.register_blueprint(newticket_bp)