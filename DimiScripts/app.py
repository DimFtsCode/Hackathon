from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Περνάμε τις συντεταγμένες και τις πληροφορίες στη σελίδα
    return render_template('map.html', lat=37.9838, lng=23.7275, location_name="Αθήνα")

if __name__ == '__main__':
    app.run(debug=True)
