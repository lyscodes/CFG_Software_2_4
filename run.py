from app import create_app
import os
from socket import gethostname

app = create_app()

if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'

    if 'liveconsole' not in gethostname():
        app.run(debug=True, ssl_context=('certs/certificate.pem', 'certs/private.pem'), host='0.0.0.0', port=443)
