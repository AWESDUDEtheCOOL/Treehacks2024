from flask import Flask, render_template, Response, request, send_file
import time
import os
import json
from transcriber import *
from prompts import *

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


@app.route("/gps", methods=["POST"])
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


@app.route("/msg", methods=["POST"])
def get_msg():
    line = request.data.decode("utf-8")
    print(f"[!!!] INCOMING MESSAGE: {line}")

    return "Got message"


@app.route("/audio", methods=["POST"])
def get_audio():
    print("[!!!] INCOMING MESSAGE")
    audio_request = request.data.decode("utf-8")
    audio_request = json.loads(audio_request)

    filename = audio_request["audioclip"]
    timestamp = audio_request["timestamp"]
    responder = audio_request["responder"]
    print("Getting transcription...")
    transcription = transcribe("static/" + filename, "logs/demo.txt")

    print("Getting summary...")
    prompt = SUMMARY_PROMPT + transcription + "\n\n" + "### In summary: "
    result = pg.Completion.create(model="Neural-Chat-7B", prompt=prompt)

    summary = result["choices"][0]["text"]
    summary = summary.replace("\n", "")
    print(summary)

    with open("logs/summaries.txt", "a") as f:
        f.write(f"{timestamp};{responder};{summary}\n")

    print("Saved summary to logs.")

    return "Got message"


# Route for SSE
@app.route("/stream")
def stream():
    return Response(generate_data(), mimetype="text/event-stream")


@app.route("/timeline")
def get_timeline():
    return send_file("logs/summaries.txt")


if __name__ == "__main__":
    app.run(debug=True)
