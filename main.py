from flask import Flask, redirect, url_for, render_template, request, jsonify
from gramatica import parse
app = Flask(__name__)

@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]        
        result = parse(inpt)
        return jsonify(output=result)        
    else:
        return render_template('analyze.html', initial="#JOLC Compiladores 2 USAC 2021")

@app.route("/reports", methods=["POST", "GET"])
def reports():
    if request.method == "POST":
        inpt = request.form["valor"]
    else:
        return render_template('reports.html')

@app.route('/output/')
def output(inpt):
    inpt=inpt.replace("aa11a223","/")
    result = parse(inpt)
    return render_template('output.html', input=result)

if __name__ == "__main__":    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)#para que se actualice al detectar cambios