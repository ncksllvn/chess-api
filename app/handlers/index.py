from app.handlers import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.finish('OK')