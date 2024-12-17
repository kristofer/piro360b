import os

from rest import Piro360rest


class Application:
    def __init__(self, env_keys):
        self.env_vars = self.fetch_env_vars(env_keys)

    def fetch_env_vars(self, keys):
        env_vars = {}
        for key in keys:
            env_vars[key] = os.getenv(key)
        return env_vars

    def main(self):
        app_instance = Piro360rest()
        app_instance.run_app()

if __name__ == "__main__":
    env_keys = ["ENV_VAR1", "ENV_VAR2"]
    app = Application(env_keys)
    app.main()

# sweet.