PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

api:
	uvicorn app.api:app --reload --port 8000

ui:
	streamlit run app/ui.py

test:
	pytest -q

index-demo:
	$(PYTHON) scripts/index_folder.py data/uploads
