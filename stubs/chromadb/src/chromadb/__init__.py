from chromadb.api import AsyncClientAPI, ClientAPI

def PersistentClient(*a, **kw):
    raise RuntimeError("chromadb is not available in this environment.")

def Client(*a, **kw):
    raise RuntimeError("chromadb is not available in this environment.")

def EphemeralClient(*a, **kw):
    raise RuntimeError("chromadb is not available in this environment.")
