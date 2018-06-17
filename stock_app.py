from flask import Flask, render_template, request
import requests
from pandas import DataFrame
import json
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np


app = Flask(__name__)

app.vars = {}


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('stockindex.html')
  else:
    return 'request.method was not a GET!'
   # app.vars['name'] = request.form['stock_jo']


def create_figure(feature_name):
        # obtain the Data
    # Set the stock we are interested in, AAPL is Apple stock code
  stock = app.vars['name']
  # Your code
  api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api_url)

  # Probably want to check that requests.Response is 200 - OK here
  # to make sure we got the content successfully.

  # requests.Response has a function to return json file as python dict
  aapl_stock = raw_data.json()
  # We can then look at the keys to see what we have access to
  aapl_stock.keys()
  # column_names Seems to be describing the individual data points
  aapl_stock['column_names']
  # A big list of data, lets just look at the first ten points...
  data = (aapl_stock['data'][0:10])

  # convert to pandas dataframe
  df = DataFrame(data, columns=['Date', 'open', 'high', 'low', 'close', 'volume', 'ex-dividend', 'split-ratio', 'adj_open', 'adj_high', 'adj_low', 'adj_close', 'adj_volumne'])

  p = figure(title='Stock', x_axis_label='Date', x_axis_type="datetime", y_axis_label='Closing Price ($)')

  Dates = np.array(df['Date'], dtype=np.datetime64)
  p.line(Dates, df['close'], line_width=2)
  return p


@app.route('/indexplotter')
def indexplotter():
  # Create the plot
  plot = create_figure()

  # Embed plot into HTML via Flask Render
  script, div = components(plot)
  return render_template("plot.html", script=script, div=div)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
  app.run(port=5060, debug=True)
