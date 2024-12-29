from flask import Blueprint, jsonify, request
from app import db
from app.models.diagram import DiagramRequest
from app.services.gemini_service import GeminiService
from app.services.diagram_service import DiagramService
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

diagram_bp = Blueprint('diagram', __name__)
gemini_service = GeminiService()
diagram_service = DiagramService()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@diagram_bp.route('/generate', methods=['POST'])
@limiter.limit("20 per minute")
def generate_diagram():
    diagram_request = None
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Create new diagram request
        diagram_request = DiagramRequest(prompt=prompt)
        db.session.add(diagram_request)
        db.session.commit()
        
        # Generate diagram code using Gemini
        try:
            diagram_code = gemini_service.generate_diagram_code(prompt)
        except Exception as e:
            raise Exception(f"Code generation failed: {str(e)}")
        
        # Generate the actual diagram
        try:
            diagram_image = diagram_service.generate_diagram(diagram_code, diagram_request.id)
        except Exception as e:
            raise Exception(f"Diagram rendering failed: {str(e)}")
        
        # Update the diagram request
        diagram_request.diagram_code = diagram_code
        diagram_request.status = 'completed'
        db.session.commit()
        
        return jsonify({
            'id': diagram_request.id,
            'diagram_code': diagram_code,
            'diagram_image': diagram_image
        })
    
    except Exception as e:
        error_message = str(e)
        if diagram_request:
            diagram_request.status = 'failed'
            diagram_request.error_message = error_message
            db.session.commit()
        return jsonify({
            'error': error_message,
            'status': 'failed'
        }), 500

@diagram_bp.route('/history', methods=['GET'])
def get_diagram_history():
    diagrams = DiagramRequest.query.order_by(DiagramRequest.created_at.desc()).all()
    return jsonify([{
        'id': d.id,
        'prompt': d.prompt,
        'status': d.status,
        'created_at': d.created_at.isoformat(),
        'error_message': d.error_message
    } for d in diagrams]) 