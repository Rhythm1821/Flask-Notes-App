from website import create_app

app = create_app()

if __name__=="__main__":
    app.run(debug=True)

# flask run -h localhost -p 3000 to run in terminal local host