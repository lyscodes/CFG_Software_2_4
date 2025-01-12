from app import create_app, db
from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database
import os
from sqlalchemy import create_engine
from app.db_init import initialize_dummy_data
from socket import gethostname

app = create_app()

if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'

    with app.app_context():
        load_dotenv()
        engine = create_engine(os.getenv('CONNECTION_STRING'))
        if not database_exists(engine.url):
            create_database(engine.url)

        db.create_all()
        initialize_dummy_data()

    if 'liveconsole' not in gethostname():
        app.run(debug=True, ssl_context=('certs/certificate.pem', 'certs/private.pem'), host='0.0.0.0', port=443)
