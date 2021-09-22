from flask import Flask, redirect, url_for, render_template, request, jsonify
from gramatica import parse
from singlenton import global_utils, Error
import json
from json import JSONEncoder
import AST as AST
import os

EntornoGlobal = None

app = Flask(__name__)

@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    global EntornoGlobal
    if request.method == "POST":  
        AST.consola = []      
        global_utils.iniciar()
        inpt = request.form["inpt"] 
        raiz = parse(inpt) 
        if raiz is not None:
            entornoGlobal  = AST.Entorno(None)
            EntornoGlobal = entornoGlobal
            raiz.ejecutar(entornoGlobal) 
            if len(global_utils._errors)>0:
                return jsonify(output=AST.consola, errores=True)
            else:
                return jsonify(output=AST.consola, errores=False)
        else:        
            salida = []
            salida.append('')
            if len(global_utils._errors)>0:
                return jsonify(output=salida, errores= True)
            else:
                return jsonify(output=salida, errores= False)
    else:
        path= os.getcwd() +"/test/main.jolc"
        archivo = open(path, 'r')
        codigo = archivo.read()
        return render_template('analyze.html', initial=codigo)

@app.route("/reports", methods=["POST", "GET"])
def reports():
    if request.method == "POST":
        inpt = request.form["valor"]
    else:
        return render_template('reports.html')

@app.route("/errors" , methods=["POST"])
def errors():
    global EntornoGlobal
    if request.method == "POST":
        errores = []
        for err in global_utils._errors:
            errores.append(json.loads(err.toJSON()))
        #print('Errores')
        #print(errores)
        simbolos = []
        indice = 0
        for simb in EntornoGlobal.tabla.tabla: 
            var = EntornoGlobal.tabla.tabla.get(simb)           
            simbolos.append({"index": indice, "nombre": var.id, "tipo": var.tipo.getNombre(), "rol" : var.getRol(), "ambito": "Global", "linea": var.linea, "columna": var.columna  })
            indice += 1
        return jsonify(errors=errores,tabla = simbolos)

@app.route('/output/')
def output(inpt):
    inpt=inpt.replace("aa11a223","/")
    result = parse(inpt)
    return render_template('output.html', input=result)

if __name__ == "__main__":    
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)#para que se actualice al detectar cambios