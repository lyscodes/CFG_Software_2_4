from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # where to add in database migrate?
    app.run(ssl_context=('certs/certificate.pem', 'certs/private.pem'), host='0.0.0.0', port=443)
