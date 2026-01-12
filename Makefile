.DEFAULT_GOAL := help

run: ## Run the application
	poetry run gunicorn app.main:app -c gunicorn.conf.py
