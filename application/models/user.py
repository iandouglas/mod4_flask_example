from application import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    tasks = db.relationship('Task', backref='users', lazy='select')

    def __repr__(self):
        return 'Id: {}, name: {}'.format(self.id, self.name)