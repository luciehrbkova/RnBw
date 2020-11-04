from app import app

@app.route("/")

@app.route("/index")
def index():
    
    user = {'name': 'Lucie'}
    return '''
<html>
    <head>
    <title>app </title></head>
    <body>
    <h1>Hello, ''' + user['name']+ '''!</h1>
    </body>

</html>'''