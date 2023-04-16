import json
import requests
from flask_babel import _
from flask import current_app


def translate(text, source_language, dest_language):
	if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
		return _('Error: the translation service is not configured.')
	
	auth = {
		'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
		'Ocp-Apim-Subscription-Region': 'westeurope'
	}
	
	r = requests.post(
		f'https://api-eur.cognitive.microsofttranslator.com/'
		f'translate?api-version=3.0&from={source_language}&to={dest_language}',
		headers=auth, json=[{'Text': text}]
	)
	
	if r.status_code != 200:
		return _('Error: the translation service ran into an error.')
	return r.json()[0]['translations'][0]['text']
