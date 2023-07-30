import requests
from bs4 import BeautifulSoup
import json
from flask import *

app = Flask(__name__)


@app.route('/ticker/', methods=['GET'])
def getData():

	ticker = str(request.args.get('ticker'))  # so query string would be something like /ticker/?ticker=MSFT
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
	url = f"https://finance.yahoo.com/quote/{ticker}"

	r = requests.get(url, headers=headers)

	soup = BeautifulSoup(r.text, 'html.parser')
	try:
		current = soup.select_one(f'fin-streamer[data-symbol="{ticker}"][data-field="regularMarketPrice"]')
		data = {'Price': current['value']}
		json_dump = json.dumps(data)
	except:
		data = {'Price': 'Price not found. Please recheck ticker symbol.'}
		json_dump = json.dumps(data)
	return json_dump


if __name__ == '__main__':
	app.run(port=5856)
