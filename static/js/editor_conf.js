// referencia a codemirror: https://codemirror.net/doc/manual.html
var editorInput = CodeMirror.fromTextArea(document.getElementById("default"),{
    theme: "dracula",
    mode:  "javascript",
    value: "function myScript(){return 100;}\n",
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true

});


var editorOutput = CodeMirror.fromTextArea(document.getElementById("output"),{
    theme: '3024-night',
    mode:  "javascript",
    value: "function myScript(){return 100;}\n",
    lineNumbers: true,
    styleActiveLine: true,
    matchBrackets: true  
});


function selectTheme() 
{
  var theme = "3024-night" 
  editorInput.setOption("theme", theme);
  location.hash = "#" + theme;
}