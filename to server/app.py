from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    session,
    redirect,
    url_for,
)
import stereo
import os
import shutil
from zipfile import ZipFile


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        shutil.rmtree(f"static/audio")
    except:
        pass
    # if request.method == "POST":
    #     dir = request.form["dir"]
    #     shutil.rmtree(f"static/audio")
    #     return redirect("index")
    return render_template("index.html")


@app.route("/monoizer", methods=["POST"])
def monoizer():

    try:
        os.mkdir(f"static/audio")
    except:
        pass
    shutil.rmtree(f"static/audio")
    os.mkdir(f"static/audio")
    files = request.files.getlist("file")
    for file in files:
        file.save(f"static/audio/" + file.filename)

    stereo.start()

    file_list = os.listdir(f"static/audio")
    with ZipFile(f"static/audio/monoizer.zip", "w") as zip:
        for file_name in file_list:
            zip.write(f"static/audio/" + file_name, arcname=file_name)

    return send_from_directory(f"static/audio", "monoizer.zip", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
