from gunicorn.app.base import BaseApplication

from app.config import app_config
from app.application import Application


def get_app():
    return Application(app_config)


class GunicornApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or dict()
        super().__init__()

    def load(self):
        return self.application

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)


if __name__ == '__main__':
    print('Starting...')
    app = get_app()
    gunicorn_app = GunicornApplication(app, options=app.config.get('gunicorn', {}))
    gunicorn_app.run()
