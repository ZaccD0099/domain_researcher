import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

api_key = '3mM44UdBKK8qxC_Pa88SUFi3ixzAVUwgKsPqF'
api_secret = 'LKUPF4B2Y6kzXXfuGZLmwg'

@app.route('/check_domains', methods=['POST'])
def check_domains():
    data = request.json
    domain_names = data['domain_names']
    available_domains = []

    for domain in domain_names:
        url = f"https://api.ote-godaddy.com/v1/domains/available?domain={domain}"
        headers = {"Authorization": f"sso-key {api_key}:{api_secret}"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data['available']:
                available_domains.append(domain)
        
    return jsonify({"available_domains": available_domains})

if __name__ == "__main__":
    app.run(debug=True)
