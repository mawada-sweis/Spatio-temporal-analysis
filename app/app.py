from flask import Flask, jsonify, render_template, request, url_for
from werkzeug.utils import redirect
from elasticsearch import Elasticsearch

# create elastic search object
es = Elasticsearch()

# create an object of the flask class
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Function to display the form of coordinate data

    Return:
        [Response]: [html file contain form data]
    """
    return render_template('index.html')


@app.route('/api/v1/search/<bounding_box>')
def search_query(bounding_box):
    """ Function to Search query
    that receives the coordinate data from insert_data function,
    then search in tweets index.
    :param bounding_box: tuple contain coordinate, they were represented as follows:
        [0] longitude min
        [1] longitude max
        [2] latitude min
        [3] latitude max
    Return:
        [str]: [to validate that the function is running correctly.]
    """
    # set the body of query using geo bounding box filtering
    body = {
        "query": {
            "bool": {
                "must": {
                    "match_all": {}
                },
                "filter": {
                    "geo_bounding_box": {
                        "location": {
                            "top_right": [bounding_box[2], bounding_box[0]],
                            "bottom_left": [bounding_box[3], bounding_box[1]]
                        }
                    }
                }
            }
        }
    }

    # receive response from search query in tweets index
    result = es.search(index="tweets", body=body)
    return jsonify(result)


@app.route('/api/v1/insert_data', methods=['POST'])
def insert_data():
    """Function to recieve the coordinate data from
    the HTML form, then Combine them in one tuple to
    make it easier to use.
    Bounding Box is the area defined by two longitudes and
    two latitudes that will include all spatial points.
    Return:
        [Response]: [Send the Bounding box tuple to search_query function.]
    """
    # Get the data from the form
    lat_min = request.form['lat_min']
    lat_max = request.form['lat_max']
    lon_min = request.form['lon_min']
    lon_max = request.form['lon_max']

    # Create Bounding box tuple
    box = (lon_min, lon_max, lat_min, lat_max)
    # send the location to the search function
    return redirect(url_for('search_query', bounding_box=box))


def create_app():
    """Function to return Flask object
    Returns:
        [app]: [Flask object created]
    """
    return app
