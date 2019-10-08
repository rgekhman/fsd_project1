# class Venue:
#     __tablename__ = 'Venue'

#     def __init__(self, dbModel):
#         self._db = dbModel    
    
#     if _db is not None:
#         id = _db.Column(_db.Integer, primary_key=True)
#         name = _db.Column(_db.String)
#         genres = _db.Column(_db.String)
#         address = _db.Column(_db.String(120))
#         city = _db.Column(_db.String(120))
#         state = _db.Column(_db.String(120))
#         phone = _db.Column(_db.String(120))
#         image_link = _db.Column(_db.String(500))
#         facebook_link = _db.Column(_db.String(120))
#         seeking_talent = _db.Column(_db.Boolean)
#         seeking_description = _db.Column(_db.String(500))
#         website = _db.Column(_db.String)