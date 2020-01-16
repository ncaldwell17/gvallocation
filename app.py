from src import app, db
from src.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == "__main__":
    app.run()
