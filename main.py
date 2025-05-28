import sys

import streamlit
from streamlit.web import cli as stcli

streamlit.set_page_config(layout="wide")

sys.argv = ["streamlit", "run", "consulta1.py"]
sys.exit(stcli.main())


