from flask import Flask, redirect, url_for, render_template, request, jsonify
from gramatica import parse
from singlenton import global_utils, Error
import json
from json import JSONEncoder
import AST as AST

app = Flask(__name__)

@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        global_utils.iniciar()
        inpt = request.form["inpt"] 
        raiz = parse(inpt) 
        if raiz is not None:
            entornoGlobal  = AST.Entorno(None)
            raiz.ejecutar(entornoGlobal) 
            if len(global_utils._errors)>0:
                return jsonify(output=entornoGlobal.tabla.consola, errores=True)
            else:
                return jsonify(output=entornoGlobal.tabla.consola, errores=False)
        else:        
            salida = []
            salida.append('')
            if len(global_utils._errors)>0:
                return jsonify(output=salida, errores= True)
            else:
                return jsonify(output=salida, errores= False)
    else:
        return render_template('analyze.html', initial="#JOLC Compiladores 2 USAC 2021")

@app.route("/reports", methods=["POST", "GET"])
def reports():
    if request.method == "POST":
        inpt = request.form["valor"]
    else:
        return render_template('reports.html')

@app.route("/errors" , methods=["POST"])
def errors():
    if request.method == "POST":
        errores = []
        for err in global_utils._errors:
            errores.append(json.loads(err.toJSON()))
        #print('Errores')
        #print(errores)
        return jsonify(errors=errores)

@app.route('/output/')
def output(inpt):
    inpt=inpt.replace("aa11a223","/")
    result = parse(inpt)
    return render_template('output.html', input=result)

if __name__ == "__main__":    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)#para que se actualice al detectar cambios