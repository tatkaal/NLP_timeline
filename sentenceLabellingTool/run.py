from labellertool import app
# from labellertool.routes import app as application

if __name__ == "__main__":
    # run the app
    # application.run(debug=True)
    app.run(host = '0.0.0.0', port = 5005,debug=True)
