from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    definition = None
    word = ""
    error = None

    if request.method == "POST":
        word = request.form["word"]
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        try:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                definition = {
                    "word": data[0]["word"],
                    "phonetic": data[0].get("phonetic", ""),
                    "partOfSpeech": data[0]["meanings"][0]["partOfSpeech"],
                    "definition": data[0]["meanings"][0]["definitions"][0]["definition"],
                    "example": data[0]["meanings"][0]["definitions"][0].get("example", "")
                }
            else:
                error = f"No definition found for '{word}'"
        except Exception as e:
            error = "Something went wrong. Try again."

    return render_template("index.html", definition=definition, error=error, word=word)

if __name__ == "__main__":
    app.run(debug=True)
