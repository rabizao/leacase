from app import create_app, db
from app.models import Album, Client, Order

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Album': Album, 'Client': Client, 'Order': Order}


if __name__ == "__main__":
    app.run(debug=True)
