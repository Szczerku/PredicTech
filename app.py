from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route("/")
def home():
    labels1 = [i + 1 for i in range(50)]
    values1 = [random.randint(1, 20) for _ in range(50)]

    labels2 = [i + 1 for i in range(50)]
    values2 = [random.randint(1, 20) for _ in range(50)]

    labels3 = [i + 1 for i in range(50)]
    values3 = [random.randint(1, 20) for _ in range(50)]

    return render_template('home.html', labels1=labels1, values1=values1, labels2=labels2, values2=values2, labels3=labels3, values3=values3)
