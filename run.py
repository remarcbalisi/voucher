

import os
import configparser

from techfarmlink.factory import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("project.ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    ENVIRONMENT = config['GLOBAL']['ENVIRONMENT']
    app.config['MONGO_URI'] = config[ENVIRONMENT]['DB_URI']
    app.config['SECRET_KEY'] = config[ENVIRONMENT]['SECRET_KEY']

    app.run()
