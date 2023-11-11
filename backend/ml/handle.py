from .cascade_retriever import CascadeRetriever



def ask(request: str):
    model = CascadeRetriever.get_or_create()
    return model.process(request)