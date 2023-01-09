# Building limits splitter
An API which given building limits and height plateaus splits building limits into corresponding height plateaus

# Requirements to run and test the application locally
1. Running postgres instance, you can create it either locally or create a free instance at https://www.elephantsql.com/
2. Install poetry following https://python-poetry.org/docs/
3. Add `.env` file with `DATABASE_URL`='running postgres url'

# To run the application locally
1. Clone repo.
2. `cd` into repo and run `poetry shell`, this should spawn a new virtual environment
3. Run `poetry install`, this should install all needed packages

4. To start application run `flask run`
4. To run tests run `pytest`
