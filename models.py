


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(64), index=True, unique=True)

    ...

    date_created = db.Column(db.DateTime, default=dt.now())

    def __repr__(self):
        return '<Company {}>'.format(self.companyName)
