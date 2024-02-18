from flask import Flask, render_template, Response, request
import time

app = Flask(__name__)

ER_LIST = [None, None, None]


def generate_data():
    while True:
        for i in range(len(ER_LIST)):
            if ER_LIST[i]:
                data = ER_LIST[i]
                ER_LIST[i] = None
                yield "data: {}\n\n".format(data)

        time.sleep(0.1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def get_data():
    line = request.data.decode("utf-8")  # Decode byte string to Unicode
    print("Received from client: {}".format(line))
    if line.startswith("ER1"):
        ER_LIST[0] = line
    if line.startswith("ER2"):
        ER_LIST[1] = line
    if line.startswith("ER3"):
        ER_LIST[2] = line

    return "Data received successfully!"


# Route for SSE
@app.route("/stream")
def stream():
    return Response(generate_data(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)
