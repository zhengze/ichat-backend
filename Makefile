run:
	python manage.py run

pylint:
	pylint ./chat

autopep8:
	autopep8 --in-place --aggressive --aggressive -r ./chat 
