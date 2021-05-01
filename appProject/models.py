from appProject import db
from datetime import datetime 

# Feeback Model
class Feedback(db.Model):
    
    __tablename__ = 'feedback'
    
    id                  = db.Column(db.Integer,primary_key=True)
    customerName        = db.Column(db.String(80),nullable=False)
    feedbackInformation = db.Column(db.Text)
    feedbackDate        = db.Column(db.DateTime,default=datetime.utcnow)
    feedbackType        = db.Column(db.String(10)) 
    datasrc_id          = db.Column(db.Integer,db.ForeignKey('dataSource.id'))
    
    
    def __repr__(self):
        return f"Feedback: Id:{self.id} CustomerName:{self.customerName} "\
               f"Date:{self.feedbackDate} Type:{self.feedbackType} FileId:{self.datasrc_id}"
               
# Data Source Model
class DataSource(db.Model):
    
    __tablename__ = 'dataSource'
    
    id               = db.Column(db.Integer,primary_key=True)
    fileName         = db.Column(db.String(45),nullable=False,unique=True)
    dateUploaded     = db.Column(db.DateTime,default=datetime.utcnow)
    fileDescription  = db.Column(db.String(100))
    feedbacks        = db.relationship('Feedback',backref='datasrc',lazy='dynamic')
    
    def __repr__(self):
        return f"DataSource: Id:{self.id} FileName:{self.fileName} DateUploaded:{self.dateUploaded}"