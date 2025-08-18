import sys
sys.dont_write_bytecode = True

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from datetime import datetime

from main import get_solution

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    # auto clear uploads
    for path in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, path))

    return render_template("index.html")

@app.route("/solution")
def solution():
    url = request.args.get("image")

    puzzle, steps = get_solution(os.path.join(UPLOAD_FOLDER, url))

    puzzle = '[\n%s\n]' % '\n'.join(f'  {stack}' for stack in puzzle)
    steps = '\n'.join([f'Step {step}: Bolt {src + 1} &#8594; Bolt {dst + 1}' for step, (src, dst) in enumerate(steps, 1)]) if steps else "No solution found!"

    return render_template("solution.html", image=url, puzzle=puzzle, steps=steps)

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/upload", methods=["POST"])
def upload():
    img = request.files["image"]

    filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{img.filename}'
    img.save(os.path.join(UPLOAD_FOLDER, filename))

    return redirect(url_for("solution", image=filename))

if __name__ == "__main__":
    app.run(debug=True)