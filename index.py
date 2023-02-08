from dash import Dash
from Layout import AppLayout
from AppCallback import AppCallback
from dash_google_oauth.google_auth import GoogleAuth
from dotenv import load_dotenv


load_dotenv()
styles = ["https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"]
app = Dash(name = __name__, external_stylesheets=styles)
# auth = GoogleAuth(app)
app.title = "Dashboard"
server = app.server


layout = AppLayout()
app.layout = layout.getAppLayout(app)
AppCallback._register_callbacks(app)


if __name__ == "__main__":
    app.run_server(host='localhost',  port=5000, debug=False)