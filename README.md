# hexagonal polls

Este proyecto es una interpretación de la aplicación de django de polls, pero tratando de hacerla hexagonal, pero aun tiene algunos fallos desde mi perspectiva y no tiene todas las pruebas que debería, sin embargo es un experimento para dominar el concepto de arquitectura hexagonal.
Esto necesita implementaciones porque como tal no funciona, no hay un ejecutable ni un punto de entrada, aunque podría tener uno de pruebas, ya que según el DDD podría tener tantas implementaciones posibles aunque sea sólo sea para probar el flujo.
Este respositorio está planeado para ser usado como submodulo.

## dependencias

- python 3.13>= (si hubiese elegido Optional en lugar de pipes | en typehints tal vez 3.8>=. prueba tu mismo)
- zope.interface (está en el requirements), aunque sólo para definir las interfaces.

## organización

La lógica de negocio está a la mano en la raíz, en misc tenemos adaptadores que deben usarse hacia los framework, además de tener dos patrones de diseño que podrán ser usados cuando se conecten las implementaciones con twisted.python.components.registerAdapter (se plantea usar ZCA de zope, para que esa sea la única dependencia fuerte, pero actualmente sólo se sabe la herramienta de twisted).

## como usar

Este repositorio se debe instalar via pip de esta manera, esto te incluirá el zope.interface en tus dependencias.

```bash
$ pip install git+https://github.com/siht/hexagonal-polls.git@v1.1.0
```

una vez instalado sólo implementa las interfaces

```python
from hexagonal_polls.interfaces import IChoiceRepository
from hexagonal_polls.misc.patterns import FlyWeight

from zope.interface import implementer

@implementer(IChoiceRepository)
class DjangoChoiceRepository(metaclass=Flyweight):
    def __init__(self, service):
        self.service = service

    def get_by_id(self, choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        ...
```

Y ya en este punto te sugiero usar twisted para usar su registro de componentes:

```python
from twisted.python import components

components.registerAdapter(DjangoChoiceRepository, IVoteExecutor, IChoiceRepository)
```

al menos hasta que aprenda a usar el ZCA de zope y te diga que pudiera ser mejor opción.

## ¿qué implementar?

### forzoso implementar

- IChoiceRepository: hexagonal_polls.interfaces.IChoiceRepository

- IQuestionRepository: hexagonal_polls.interfaces.IQuestionRepository

### opcional implementar

- AbstractQuestionCreatorIOFrameworkAdapter

- AbstractChoiceCreatorIOFrameworkAdapter

- AbstractVoteIOFrameworkAdapter

## una vez implementadas las interfaces (y tal vez clases abstractas)

Una vez implementados hay que registrarlos con components.registerAdapter

Una vez implementadas la todas interfaces y las clases abstractas se habilita el funcionamiento de los casos de uso:

- hexagonal_polls.use_cases.CreateQuestion, puedes hacer tu propia implementacion con hexagonal_polls.interfaces.ICreateQuestionExecutor, esto sólo te habilita las lógica de negocio pero siquieres validaciones, puedes implementar hexagonal_polls.misc.adapters.AbstractQuestionCreatorIOFrameworkAdapter, para tu framework, quedando esta como opcional y con ello un registro más en components.registerAdapter.


- hexagonal_polls.use_cases.CreateChoice, puedes hacer tu propia implementacion con hexagonal_polls.interfaces.ICreateChoiceExecutor, esto sólo te habilita las lógica de negocio pero siquieres validaciones, puedes implementar hexagonal_polls.misc.adapters.AbstractChoiceCreatorIOFrameworkAdapter, para tu framework, quedando esta como opcional y con ello un registro más en components.registerAdapter.

- hexagonal_polls.use_cases.Vote, puedes hacer tu propia implementacion con hexagonal_polls.interfaces.IVoteExecutor, esto sólo te habilita las lógica de negocio pero siquieres validaciones, puedes implementar hexagonal_polls.misc.adapters.AbstractVoteIOFrameworkAdapter, para tu framework, quedando esta como opcional y con ello un registro más en components.registerAdapter.

tus registros deberán quedar más o menos así:

```python
components.registerAdapter(TuImplementacionQuestionRepository, ICreateQuestionExecutor, IQuestionRepository)
components.registerAdapter(TuImplementacionChoiceRepository, [ICreateChoiceExecutor, IVoteExecutor], IChoiceRepository)
# los ultimos tres son opcionales para que funcionen las clases abstractas
components.registerAdapter(Vote, IVoteIOFrameworkAdapter, IVoteExecutor)
components.registerAdapter(CreateQuestion, IQuestionCreatorIOFrameworkAdapter, ICreateQuestionExecutor)
components.registerAdapter(CreateChoice, IChoiceCreatorIOFrameworkAdapter, ICreateChoiceExecutor)
```