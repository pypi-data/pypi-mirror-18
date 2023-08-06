
class BmdBatch(object):

    def __init__(self):
        self.sessions = []

    def append(self, session):
        self.sessions.append(session)

    def extend(self, *sessions):
        self.sessions.extend(sessions)

    def to_csv(self):
        pass

    def to_df(self):
        pass

    def to_png(self):
        pass
