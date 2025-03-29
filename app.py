from flask import render_template
from website import create_app

app = create_app()

# Register a global 404 error handler   
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)