from demo import app

@app.route('/')
def Hello():
    return "Welcome to Bookshop!"

if __name__ == '__main__':
    app.run(debug=True)