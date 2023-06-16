from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    organizations = db.relationship('Organization', secondary='user_organization', backref='users')

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __repr__(self):
        return f'<Organization {self.name}>'

user_organization = db.Table('user_organization',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                              db.Column('organization_id', db.Integer, db.ForeignKey('organization.id'))
                              )
