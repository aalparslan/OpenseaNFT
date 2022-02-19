from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_apscheduler import APScheduler
import retriever

cached_collection_names = []
refresh_in_minutes = 120

cache = Cache()


app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
cache.init_app(app)
scheduler = APScheduler()


# TYPE OF POST REQUEST
    # {
    # "collections":["the-wanderers", "crpytopunks", "boredapeyachtclub"],
    # }
@app.route('/nfts', methods=['GET', 'POST'])
def send_nft_data():

    if(request.method == 'POST'):
        some_json = request.get_json()
        collection_names = some_json['collections']
        result = {}
        for name in collection_names:
            collection_data = pull_nft_data(name)
            result[name] = collection_data
            global cached_collection_names
            cached_collection_names.append(name)
        return jsonify({'result': result})
        

@cache.memoize(timeout=refresh_in_minutes*60) 
def pull_nft_data(collection_name):
    return retriever.get_collection_data(collection_name)


@scheduler.task("interval", id="do_job_1", minutes=(refresh_in_minutes+1), misfire_grace_time=900)
def updateCaches():
    global cached_collection_names
    for name in cached_collection_names:
        pull_nft_data(name)
        print(f'{name} is being updated')
    

def initial_message():
    print('\n\n### Flask is running! ###')
    print('### Make a POST request to http://localhost:5000/nfts as shown in the READ.ME file ###\n\n')

if __name__ == '__main__':
    scheduler.api_enabled = True  # noqa: E800
    scheduler.init_app(app)
    scheduler.start()
    initial_message()
    app.run(debug=True)


