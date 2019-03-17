import os
from woolies.flaskapp import create_app

app = create_app()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', '5000'))
    app.run(host=host, port=port, threaded=True)