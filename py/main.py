# web packages
from flask import request, jsonify, abort, json
import flask
from flask_cors import CORS

# time related pacakges
from datetime import datetime
from timezonefinder import TimezoneFinder
from pytz import timezone

#location related packages
from geopy.geocoders import Nominatim

app = flask.Flask(__name__)
CORS(app) 
tf = TimezoneFinder(in_memory=True)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Time API</h1><p>reeeee</p>"


# time_zone   
request_params = ['location']
geolocator = Nominatim(user_agent="genius")

@app.route('/v1/time', methods=['POST'])
def find():
  request.get_data()
  temp = request.json
  if temp:
    print(temp   )
    if not 'location' in temp:
        print('params')
        abort(400, "doesn\'t have parameters")
  else:
    print('not json')
    print( request.data.decode().split('\'')[0])
    abort(400, 'request not JSON')
  time_zone = get_zone(temp['location'])
  task = {
      'time_zone': time_zone,
      'time': datetime.now(timezone(time_zone)).strftime('%H:%M'),
      'date': datetime.now(timezone(time_zone)).strftime('%B %d, %Y'),
      'loc_name': get_location_name(temp['location'])
  }
  rec_data(request)
  response = app.response_class(

        response=task,
        status=201,
        mimetype='application/json'
    )
  return jsonify(task), 201

def get_location_name(loc):
  if not('long' in loc and 'lat' in loc):
        print('gsd')
        raise abort(400, "request does not have the sufficient location data")
  string = str(loc['lat'])+ ", " + str(loc['long']);
  location = geolocator.reverse(string)
  return location.address


def get_zone(loc):
    if not('long' in loc and 'lat' in loc):
        print('gsd')
        raise abort(400, "request does not have the sufficient location data")
    zone = tf.timezone_at(lat=loc['lat'], lng=loc['long'])

    if not (zone == None):
        return zone
    else:
        print('locerro')
        raise abort(400, 'location not found')

def rec_data(request) :
  with open('text.txt', 'a') as text:
    text.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "," + str(request.json['location']['lat']) + "," + str(request.json['location']['long']) + '\n')
    print(text.read)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)