// referencia a codemirror: https://codemirror.net/doc/manual.html
var editorInput = CodeMirror.fromTextArea(document.getElementById("default"),{
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true,
    theme: "dracula"    
});


var editorOutput = CodeMirror.fromTextArea(document.getElementById("output"),{
    lineNumbers: true,
    theme: '3024-night'    
});


function selectTheme() 
{
  var theme = "3024-night" 
  editorInput.setOption("theme", theme);
  location.hash = "#" + theme;
}