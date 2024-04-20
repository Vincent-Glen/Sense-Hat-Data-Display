from flask import Flask, render_template, jsonify
from sense_emu import SenseHat 

sense = SenseHat()

app = Flask(__name__)

# defines a route to the templates folder , which will then render the specified file in the template folder.
@app.route("/")
def home():
    return render_template("home.html")

# returns temperature and humidity data from the sense hat emulator
@app.route('/data')
def get_data():
    temperature = sense.temperature
    humidity = sense.humidity
    # runs the check warning function
    warning = check_warning(temperature, humidity)
    # If there is a warning on the web application it displayes the same message is displayed on the sense hat emulator
    if warning:
        # Display the warning on the Sense HAT's LED matrix
        sense.show_message(warning, text_colour=[255, 0, 0], scroll_speed=0.05)

    # returns the sense hat emulators data.
    return jsonify({
        'temperature': temperature,
        'humidity': humidity,
        'warning': warning
    })

# checks to see if the temperatture is greater than 40C, or humidity is greater than 90%, then returns warning to the web application.
def check_warning(temperature, humidity):
    if temperature > 40 or humidity > 90:
        return "Warning: High temperature or humidity!"
    else:
        return ""

if __name__ == '__main__':
    app.run(debug=True) 