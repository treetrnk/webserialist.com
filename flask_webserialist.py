from app import create_app, db
from app.models import User, Fiction, Rating, Vote, Tag, Genre

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
            'db': db, 
            'User': User, 
            'Fiction': Fiction, 
            'Rating': Rating, 
            'Vote': Vote, 
            'Tag': Tag, 
            'Genre': Genre,
        }