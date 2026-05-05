from flask import Flask, render_template, request, redirect, url_for, send_file
from scraper import scrape, prepare_for_download


app = Flask(__name__)
last_results = []
query = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global last_results
    global query
    if request.method == "POST":
        query = request.form.get("query")
        last_results = scrape(query)
        return render_template("index.html", results=last_results, query=query)

    return render_template("index.html", results=[], query="")
        #Takhle hloupe, results=last_results, je to kvuli Flask, protoze potrebuje vedet jak se ty promenne jmenuji v HTML

@app.route("/save", methods=["POST"])
def save():
    global last_results
    file_stream = prepare_for_download(last_results)
    if file_stream:
        filename = "Vysledky pro " + str(query) + ".json"
        return send_file(file_stream,
            mimetype="application/json",
            as_attachment=True,
            download_name=filename
        )
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)