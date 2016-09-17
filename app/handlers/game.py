from app.handlers import BaseHandler


class GameHandler(BaseHandler):

    def get(self):
        self.finish('OK')