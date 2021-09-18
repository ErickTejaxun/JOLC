import json
from json import JSONEncoder
from datetime import date


# Errors 
_error_counter = 0
_file_ = ''




class Error():
    def __init__(self, id, type, desc, line, column):
        global _error_counter
        global _file
        self.index = _error_counter
        self.id = id
        self.type = type
        self.desc = desc
        self.line = line
        self.column = column
        self.file = _file_
        _error_counter = _error_counter + 1 

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)        

class SinglentonMeta(type):
    _instances = {}    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singlenton(metaclass=SinglentonMeta):
    _errors = []
    fecha = date.today()

    def iniciar(self):
        global  _error_counter
        global  _file_
        _error_counter = 0
        _file_ = ''
        self._errors = []

    def registryError(self, id, desc, line, column):
        self._errors.append(Error(id, type, desc, line, column))

    def registryLexicalError(self, id, desc, line, column):
        self._errors.append(Error(id, 'Léxico', desc, line, column))
    
    def registrySyntaxError(self,id, desc, line, column):
        self._errors.append(Error(id, 'Sintáctico', desc, line, column))

    def registrySemanticError(self,id, desc, line, column):
        self._errors.append(Error(id, 'Semántico', desc, line, column))


class ErrorEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class SinglentonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__    

global_utils = Singlenton()