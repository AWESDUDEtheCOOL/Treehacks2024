from flask import Flask, render_template, Response, request, send_file
import time
import os
import json
from transcriber import *
from prompts import *
from sat import *

app = Flask(__name__)

ER_LIST = [None, None, None]
ER_AUDIO_LIST = [None, None, None]


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


@app.route("/sat")
def get_sat():
    # send dispatch message
    with open("static/networkalert.txt", "w") as f:
        f.write("TRUE")

    print("making inference...")
    confidence = make_inference("static/gps2.jpg")
    print(confidence)

    return {"result": confidence}


@app.route("/msg", methods=["POST"])
def get_msg():
    line = request.data.decode("utf-8")
    print(f"[!!!] INCOMING MESSAGE: {line}")

    return "Got message"


@app.route("/ER1", methods=["POST"])
def trigger_ER1():
    print("Setting ER1...")
    ER_AUDIO_LIST[0] = True


@app.route("/ER1")
def get_ER1_status():
    status = ER_AUDIO_LIST[0]
    ER_AUDIO_LIST[0] = None
    return {"status": status}


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

    prompt = SUMMARY_PROMPT(transcription)
    result = pg.Completion.create(model="Neural-Chat-7B", prompt=prompt)
    summary = result["choices"][0]["text"]
    summary = summary.replace("\n", "")
    summary = summary.strip()

    with open("logs/summaries.txt", "a") as f:
        f.write(f"{timestamp};{responder};{summary}\n")
    print("Saved summary to logs.")

    prompt = REQUEST_PROMPT(transcription)
    result = pg.Completion.create(model="Neural-Chat-7B", prompt=prompt)
    needs = result["choices"][0]["text"]
    needs = needs.replace("\n", "")
    needs = needs.strip()
    print(f"Request: {needs}")

    if needs != "NONE":
        with open("logs/requests.txt", "a") as f:
            f.write(f"{timestamp};{responder};{needs}\n")

    prompt = KEYWORD_PROMPT(transcription)
    result = pg.Completion.create(model="Neural-Chat-7B", prompt=prompt)
    keyword = result["choices"][0]["text"]
    keyword = keyword.replace("\n", "")
    keyword = keyword.strip()
    keyword = keyword[:18]
    print(f"Keyword: {keyword}")

    with open("logs/keywords.txt", "a") as f:
        f.write(f"{timestamp};{responder};{keyword}\n")

    return "Got message"


# Route for SSE
@app.route("/stream")
def stream():
    return Response(generate_data(), mimetype="text/event-stream")


@app.route("/timeline")
def get_timeline():
    return send_file("logs/summaries.txt")


@app.route("/keywords")
def get_keywords():
    return send_file("logs/keywords.txt")


@app.route("/requests")
def get_requests():
    return send_file("logs/requests.txt")


if __name__ == "__main__":
    app.run(debug=True)
