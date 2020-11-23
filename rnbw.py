from app import app, db
#creates a shell context that adds the database instance and models to the shell session
from app.models import User, Board, Card, Task

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Board': Board, 'Card': Card, 'Task': Task}

