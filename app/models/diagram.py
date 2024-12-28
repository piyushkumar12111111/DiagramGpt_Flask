from app import db
from datetime import datetime

class DiagramRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    diagram_code = db.Column(db.Text)
    diagram_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')
    error_message = db.Column(db.Text) 