
import json
import plotly
import pandas as pd
import gc

from flask import render_template, request, jsonify
import plotly.graph_objs as goo


from joblib import dump, load
from sqlalchemy import create_engine

import nltk
nltk.download(["punkt","stopwords","wordnet"])

#from disapp import app
from utils.utils import tokenize

from flask import Flask

app = Flask(__name__)

# load data
engine = create_engine('sqlite:///DisasterResponse.db')
#df = pd.read_sql_table('DisasterResponse', engine)

#print(df.head())

# load model
#model = load("disaster.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    
    df = pd.read_sql_table('DisasterResponse', engine)
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # create visuals
    graphs = [
        {
            'data': [
                goo.Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
   
    del df
    gc.collect()
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 
    #print(query)
    
    df = pd.read_sql_table('DisasterResponse', engine)
    model = load("disaster.pkl")

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))
    #print(classification_results)

    del df
    del model

    gc.collect()

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )



#app.run(host='localhost', port=3001, debug=True)
