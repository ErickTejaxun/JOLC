// referencia a codemirror: https://codemirror.net/doc/manual.html
var editorInput = CodeMirror.fromTextArea(document.getElementById("inpt"),{
    theme: "eclipse",
    mode:  "julia",    
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true

});

var editorOutput = CodeMirror.fromTextArea(document.getElementById("output"),{
    theme: '3024-night',
    mode:  "shell",    
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true  
});


CodeMirror.on(editorInput, "cursorActivity", (instance, obj)=>{        
    var posicion = document.getElementById("posicion");
    var cursor = instance.doc.getCursor();
    posicion.innerHTML = "Posición:  Línea:"+cursor.line + "  Columna:"+ cursor.ch;
});