from project import create_app

# Call the application factory function to construct a Flask application
# instance using the development configuration (flask_test.cfg)

app = create_app('flask.cfg')
app.run(debug=False, host='0.0.0.0', port=5000)