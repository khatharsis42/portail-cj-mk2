from src.main import app

if __name__ == "__main__":
    app.config.from_pyfile("config.py")
    app.run(host=app.config["LISTEN_ADDR"], port=app.config["LISTEN_PORT"])

