from flask import Flask, jsonify, render_template, request, url_for
from werkzeug.utils import redirect
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt

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


@app.route('/api/v1/search/<bounding_box>', methods=['POST'])
def search_query(bounding_box):
    """ Function to Search query
    that receives the coordinate data from insert_data function,
    then search in tweets index.
    :param bounding_box: array contain coordinate,
    example of box data represented: 
        [
        {"lat":32.14422278872305,"lng":35.01068115234375},
        {"lat":31.84373252620705,"lng":35.24139404296874}
        ]
    Return:
        [Response]: [to validate that the function is running correctly.]
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
                            "top_left": [bounding_box[0]['lat'],
                                         bounding_box[0]['lng']],
                            "bottom_right": [bounding_box[1]['lat'],
                                             bounding_box[1]['lng']]
                        }
                    }
                }
            }
        }
    }

    # receive response from search query in tweets index
    result = es.search(index="tweets", body=body)

    # Plot date frequency
    date_tweets = [hit["_source"]['created_at'].split("T")[0] for hit in result['hits']['hits']]

    ax = date_tweets.hist(xrot=45,  
                        bins = (date_tweets.max() -
                                date_tweets.min()).days)
    
    ax.set_ylabel('Tweet count')

    plt.show()
    plt.savefig('./new_plot.png')
    return render_template('index.html', name = 'new_plot', url ='./new_plot.png')

    # return jsonify(result)


@app.route('/api/v1/insert_data', methods=['POST'])
def insert_data():
    """Function to recieve the coordinate data from
    the JS Script.
    Bounding Box is the area defined by two longitudes and
    two latitudes that will include all spatial points.
    Return:
        [Response]: [Send the Bounding box tuple to search_query function.]
    """
    box = request.data
    # send the location to the search function
    return redirect(url_for('search_query', bounding_box=box))


def create_app():
    """Function to return Flask object
    Returns:
        [app]: [Flask object created]
    """
    return app
