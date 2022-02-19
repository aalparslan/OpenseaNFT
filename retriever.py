import requests

api_key = ""
headers = {
    "Accept": "application/json",
    "X-API-KEY": api_key
}

def get_collection_data(name:str):
    # fetch assets in collection 50 at a time
    offset = 0
    data = {'assets': []}
    while True:
        params = {
            'collection': name,
            'order_by': 'pk',
            'order_direction': 'asc',
            'offset': offset,
            'limit': 50
        }

        r = requests.get('https://api.opensea.io/api/v1/assets', params=params, headers=headers)
        response_json = r.json()
        
        for asset in response_json['assets']:
            temp = {'id': asset['token_id'],'collection_name': params['collection'], 'url': asset['permalink'],
            'last_sale_price': asset['last_sale']['total_price'] if asset['last_sale'] else '',
            'current_listing_price':asset['sell_orders'][0]['current_price'] if asset['sell_orders'] else ''}
            data['assets'].append(temp)
        
        if len(response_json['assets']) < 50:
            break
        
        offset += 50

        print(params['collection'], ' looping: ', offset)
        # uncomment if you want to add a delay in case you get throttled
        #time.sleep(1)
    return data



