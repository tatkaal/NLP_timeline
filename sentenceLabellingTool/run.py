from labellertool import app
# from labellertool.routes import app as application

if __name__ == "__main__":
    # run the app
    # application.run(debug=True)
    app.run(host = '0.0.0.0', port = 8005,debug=True)
    # app.run(host = '127.0.0.1', port = 8005,debug=True)
