from flask import Blueprint, request, jsonify

#import request limiter
from app.extensions import limiter

from app.extensions import db

from app.glpi_api import open_glpi_ticket
from app.models.ticket import Ticket

newticket_bp = Blueprint("newticket", __name__)

@newticket_bp.route("/api/newticket", methods=['POST'])
@limiter.limit("100 per 10 minutes; 400 per hour")
def create_ticket():
    request_data = request.get_json()
    
    #check if body contains all required informations, if not, returns json informing which ones are missing
    required_fields = [
        'ticket_title',
        'requester_username',
        'department',
        'anydesk',
        'computer_name',
        'logged_username'
    ]
    missing_fields = [field for field in required_fields if field not in request_data]
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
        
    
    try:
        requester_ip = request.remote_addr 
        #opens new ticket on GLPI API
        opened_ticket = open_glpi_ticket(
            request_data["ticket_title"], 
            request_data["requester_username"], 
            request_data["department"], 
            request_data["anydesk"], 
            request_data["computer_name"],
            request_data["logged_username"],
            requester_ip
        )
        
        #registers new ticket on database
        new_ticket = Ticket(
            ticket_title=opened_ticket['ticket_title'],
            requester_username=opened_ticket["requester_username"],
            requester_fullname=opened_ticket['requester_fullname'],
            department=opened_ticket['department'],
            anydesk=opened_ticket['anydesk'],
            computer_name=opened_ticket['computer_name'],
            user_glpi_id=opened_ticket['user_glpi_id'],
            ticket_glpi_id=opened_ticket['ticket_glpi_id'],
            requester_ip=requester_ip
        )
        
        db.session.add(new_ticket)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "erro": "Dados inválidos",
            "detalhes": str(e)
        }), 400

    return jsonify(opened_ticket)