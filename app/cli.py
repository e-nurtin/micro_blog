from app import app
import os
import click


@app.cli.group()
def translate():
	"""Translations and localization commands configuration"""
	pass


# This function adds new command to cmd on this venv - e.g. flask translate ...


@translate.command()
def update():
	"""Update all languages"""
	if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
		raise RuntimeError('extract command failed')
	if os.system('pybabel update -i messages.pot -d app/translations'):
		raise RuntimeError('update command failed')
	os.remove('messages.pot')


@translate.command()
def compile():
	"""Compile all languages"""
	if os.system('pybabel compile -d app/translations'):
		raise RuntimeError('compile command failed')


@translate.command()
@click.argument('lang')
def init(lang):
	"""Initialize a new language"""
	if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
		raise RuntimeError('extract command failed')
	if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
		raise RuntimeError('init command failed')
	os.remove('messages.pot')