import requests
import os

def open_glpi_ticket(ticket_title, requester_username, department, anydesk, computer_name, logged_username, requester_ip):
    
    url_glpi = os.getenv('GLPI_URL')
    glpi_app_token = os.getenv('GLPI_APP_TOKEN')
    
    #starts session on GLPI API and parse Session-Token
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {os.getenv("GLPI_B64_CREDENTIALS")}',
            'App-Token': f'{glpi_app_token}'
        }
        session_token = requests.get(f"{url_glpi}/initSession/", headers=headers).json()['session_token']
    except Exception as e:
        print(e)
    
    #search for full name and ID by username provided in request
    try:
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': f'{session_token}',
            'App-Token': f'{glpi_app_token}'
        }
        params = {
            'criteria[0][field]': 1,
            'criteria[0][searchtype]': 'contains',
            'criteria[0][value]': f'{requester_username}',
            'forcedisplay[0]': 1,
            'forcedisplay[1]': 2,
            'forcedisplay[2]': 9,
            'forcedisplay[3]': 34,
            'forcedisplay[4]': 60
        }
        response_user = requests.get(f"{url_glpi}/search/User/", headers=headers, params=params).json()
        print(response_user)
        #if no user is found with requester_username, try with logged_username
        if response_user['totalcount'] == 0:
            params['criteria[0][value]'] = f'{logged_username}'
            response_user = requests.get(f"{url_glpi}/search/User/", headers=headers, params=params).json()
            
        user_glpi_id = response_user['data'][0]['2']
        user_firstname = response_user['data'][0]['9']
        user_lastname = response_user['data'][0]['34']
    except Exception as e:
        print(e)
    
    #open ticket using requester username
    try:
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': f'{session_token}',
            'App-Token': f'{glpi_app_token}'
        }
        data = {
            'input':{
                'name': f'{ticket_title}',
                'content': f"Setor: {department}\nAnydesk: {anydesk}\nIP: {requester_ip}\nMaquina: {computer_name}\nNome: {user_firstname} {user_lastname}",
                '_users_id_requester': f'{user_glpi_id}',
            }
        }
        response_ticket = requests.post(f"{url_glpi}/Ticket/", headers=headers, json=data).json()
        ticket_glpi_id = response_ticket['id']
    except Exception as e:
        print(e)
        
    #kill session token
    try:
        headers = {
            'Content-Type': 'application/json',
            'Session-Token': f'{session_token}',
            'App-Token': f'{glpi_app_token}'
        }
        requests.get(f"{url_glpi}/killSession/", headers=headers)
    except Exception as e:
        print(e)
    
        
    opened_ticket = {
        'ticket_title': ticket_title,
        'requester_username': params['criteria[0][value]'], #username used to open ticket
        'requester_fullname': f'{user_firstname} {user_lastname}',
        'user_glpi_id': user_glpi_id,
        'department': department,
        'anydesk': anydesk,
        'computer_name': computer_name,
        'requester_ip': requester_ip,
        'ticket_glpi_id': ticket_glpi_id
    }
    return opened_ticket
