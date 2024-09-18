
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
REQUIREMENTS=requirements.txt
EXECUTE_VIEW_SCRIPT=exeview_update_sheet.py
UPDATE_VIEW_SCRIPT=update_materialized_view.py
UPDATE_SHEET_AND_MATERIALIZED_VIEW_SCRIPT=update_sheet_and_mview.py

create-venv:
	python3 -m venv $(VENV_DIR)

install_dependencies:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

setup: create-venv install_dependencies

execute-view-update-sheet:
	$(PYTHON) $(EXECUTE_VIEW_SCRIPT)

update-materialized-view:
	$(PYTHON) $(UPDATE_VIEW_SCRIPT)

update-sheet-and-materialized-view:
	$(PYTHON) $(UPDATE_SHEET_AND_MATERIALIZED_VIEW_SCRIPT)

clean:
	rm -rf $(VENV_DIR)
