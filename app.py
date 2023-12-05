import requests
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Fetch environment variables
api_key = os.environ.get('GoDaddy_Api_Key', None)
api_secret = os.environ.get('GoDaddy_Secret', None)

@app.route('/check_domains', methods=['POST'])
def check_domains():
    data = request.json
    domain_names = data['domain_names']
    available_domains_info = []

    for domain in domain_names:
        url = f"https://api.godaddy.com/v1/domains/available?domain={domain}"
        headers = {"Authorization": f"sso-key {api_key}:{api_secret}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            domain_data = response.json()
            if domain_data['available']:
                purchase_url = f'https://www.godaddy.com/domainsearch/find?domainToCheck={domain}'
                formatted_price = domain_data['price'] / 1000000  # Adjust the price format
                
                available_domains_info.append({
                "domain": domain,
                "price": formatted_price,
                "currency": domain_data['currency'],
                "purchase_url": purchase_url
                })
        
    return jsonify({"available_domains": available_domains_info})

if __name__ == "__main__":
    app.run(debug=True)

