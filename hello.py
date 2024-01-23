from flask import Flask

# Flask-App erstellen
app = Flask(__name__)

# Route für die Wurzel-URL ("/")
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Überprüfen, ob das Skript direkt ausgeführt wird
if __name__ == '__main__':
    # Die Anwendung wird auf dem lokalen Entwicklungsserver gestartet
    app.run(debug=True)
