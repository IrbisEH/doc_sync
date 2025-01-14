import os
from app_py.app.App import App


DIR = os.path.abspath(os.path.dirname(__file__))
app = App(DIR)
app.sync()