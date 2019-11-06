from exts import db



class QuoteModel(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable = False)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
