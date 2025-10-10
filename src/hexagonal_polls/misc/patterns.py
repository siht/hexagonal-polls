# misc/patterns.py

class Singleton(type):
    """Patrón singleton como metaclase
    la clase que implemente este comportamiento ya no podrá instanciar otro objeto
    diferente al primero que se instanció.

    uso:
    class ClaseSigleton(metaclass=singleton):
        ...

    single0 = ClaseSigleton()
    single1 = ClaseSigleton()
    single2 = ClaseSigleton()

    assert single0 is single1
    assert single0 is single2
    """
    def __init__(cls, name, bases, dct):
        cls._instance = None
        type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = type.__call__(cls, *args,**kw)
        return cls._instance


class FlyWeight(type):
    """Patrón flyweight como metaclase
    por cada llamada de creación con los mismos parámetros no se creará un nuevo objeto
    si es que ya existe uno igual.
    uso:
    class ClaseFlyweight(metaclass=FlyWeight):
        ...
    
    
    a = ClaseFlyweight('fly')
    b = ClaseFlyweight('weight')
    c = ClaseFlyweight('fly')

    assert a is not b
    assert a is c

    """
    def __init__(cls, name, bases, dct):
        cls._instances = {}
        type.__init__(cls, name, bases, dct)

    def __call__(cls, key, *args, **kw):
        instance = cls._instances.get(key)
        if instance is None:
            instance = type.__call__(cls, key, *args, **kw)
            cls._instances[key] = instance
        return instance
