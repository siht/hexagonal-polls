# hexagonal polls

Este proyecto es una interpretación de la aplicación de django de polls, pero tratando de hacerla hexagonal, pero aun tiene algunos fallos desde mi perspectiva y no tiene todas las pruebas que debería, sin embargo es un experimento para dominar el concepto de arquitectura hexagonal.
Esto necesita implementaciones porque como tal no funciona, no hay un ejecutable ni un punto de entrada, aunque podría tener uno de pruebas, ya que según el DDD podría tener tantas implementaciones posibles aunque sea sólo sea para probar el flujo.
Este respositorio está planeado para ser usado como submodulo.

## dependencias
- python 3.13>= (si hubiese elegido Optional en lugar de pipes | en typehints tal vez 3.8>=. prueba tu mismo)
- zope.interface (está en el requirements), aunque sólo para definir las interfaces.

## organización
La lógica de negocio está a la mano en la raíz, en misc tenemos adaptadores que deben usarse hacia los framework, además de tener dos patrones de diseño que podrán ser usados cuando se conecten las implementaciones con twisted.python.components.registerAdapter (se plantea usar ZCA de zope, para que esa sea la única dependencia fuerte, pero actualmente sólo se sabe la herramienta de twisted).