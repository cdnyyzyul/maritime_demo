'''
    Contains the server to run our application.
'''


from app import app

if __name__ == "__main__":
    app.run_server(port="8052", debug=True)

