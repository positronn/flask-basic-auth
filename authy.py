from flask_migrate import Migrate

from restauth import create_app
from restauth import db

from restauth.model import User

app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)
