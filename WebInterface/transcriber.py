from transformers import pipeline

transcriber = pipeline(model="openai/whisper-base")


def transcribe(input_filename, output_filename):
    result = transcriber(input_filename)

    text = result["text"].strip()
    with open(output_filename, "w") as f:
        f.write(text)

    text = text.replace(
        "Note: The given text transcription might not be complete or perfect; please try to convey the primary message as accurately as possible.",
        "",
    )

    return text
