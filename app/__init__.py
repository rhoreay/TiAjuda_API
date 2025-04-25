from flask import Flask
from flask_ipfilter import IPFilter, Whitelist
import ipaddress

#importing database instance, request limiter, ip whitelist and routes
from app.extensions import db, SQLALCHEMY_CONNECTION_STRING, limiter, ip_whitelist
from app.routes import register_routes
from app.models import * 


def create_app():
    app = Flask(__name__)
    
    # database config
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_CONNECTION_STRING
    
    # initialize database
    db.init_app(app)
    
    #initialize request limiter
    limiter.init_app(app)
    
    #apply ip filters (AI generated)
    if ip_whitelist:
        ip_filter = IPFilter(app, ruleset=Whitelist())
        valid_ips = []
        for ip in ip_whitelist:
            try:
                # Try to parse as IP network first (for ranges like 10.111.2.0/24)
                try:
                    network = ipaddress.ip_network(ip)
                    ip_filter.ruleset.permit(str(network))
                    valid_ips.append(str(network))
                except ValueError:
                    # If not a network, try as single IP address
                    ipaddress.ip_address(ip)
                    ip_filter.ruleset.permit(ip)
                    valid_ips.append(ip)
            except ValueError:
                print(f"Warning: Invalid IP or network range ignored in whitelist: {ip}")
        
        if not valid_ips:
            print("Warning: No valid IPs or network ranges configured in whitelist. All requests will be allowed.")
    else:
        print("Warning: No IPs configured in whitelist. All requests will be allowed.")

    #register all routes
    register_routes(app)
    
    return app