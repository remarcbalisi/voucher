

import os
import configparser

from techfarmlink.factory import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("mongo.ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['PROD']['DB_URI']

    app.run()
