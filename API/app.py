from __init__ import create_app
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8160)