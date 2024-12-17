import os

from rest import Piro360rest
from models import start_sqlite_db

class Application:
    def __init__(self, env_keys):
        self.env_vars = self.fetch_env_vars(env_keys)

    def fetch_env_vars(self, keys):
        env_vars = {}
        for key in keys:
            env_vars[key] = os.getenv(key)
        return env_vars

    def start(self):
        app_instance = Piro360rest()
        #db_path = self.env_vars.get('./test.db')
        session = create_db_and_tables(engine)
        app_instance.run_app(session)

if __name__ == "__main__":
    env_keys = ["DBPATH", "ENV_VAR2"]
    app = Application(env_keys)
    app.start()

# sweet.