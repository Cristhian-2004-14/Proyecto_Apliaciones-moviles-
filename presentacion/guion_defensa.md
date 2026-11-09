# Guion de defensa: ConectaCruz

Duración estimada: 4 minutos y 30 segundos.

## Diapositiva 1: Problema (40 s)

Esta actividad analiza qué framework móvil conviene a un negocio local de Santa Cruz. El caso usa ConectaCruz como nombre del enunciado y mantiene el alcance de una churrasquería. El punto de partida es una primera pantalla de catálogo. Pedidos y reservas se consideran posibles necesidades posteriores, no funcionalidades implementadas.

## Diapositiva 2: Alternativas (40 s)

Comparamos Flutter, React Native y desarrollo nativo separado para Android e iOS. Flutter y React Native permiten compartir gran parte del código. El enfoque nativo prioriza herramientas específicas de Android y Apple, pero requiere mantener más de una base de código si se desean ambas plataformas.

## Diapositiva 3: Método (45 s)

Usé una matriz ponderada de cinco criterios: costo, rendimiento, comunidad, compatibilidad y curva de aprendizaje. La escala fue de uno a cinco. Los pesos dan mayor importancia al costo, con 30%, y a la compatibilidad Android e iOS, con 25%, debido al presupuesto limitado planteado. Los puntajes son una evaluación justificada, no benchmarks.

## Diapositiva 4: Resultados (50 s)

Flutter alcanzó 91 puntos de 100, React Native 83 y desarrollo nativo 66. Flutter recibió cinco en costo por su única base de código y cinco en compatibilidad. Nativo recibió cinco en rendimiento previsto y comunidad, pero perdió puntos por el costo de sostener Android e iOS. La operación aplicada fue peso por calificación dividido entre cinco.

## Diapositiva 5: Decisión y límites (55 s)

Propongo Flutter para el MVP. Permite mantener una interfaz consistente y concentrar el trabajo inicial. La decisión no elimina sus desventajas: exige aprender Dart y no reemplaza una verificación de paquetes o de rendimiento en dispositivos reales. Si el equipo ya dominara React, React Native sería una alternativa razonable. Si se necesitaran integraciones de bajo nivel muy específicas, se reconsideraría el desarrollo nativo.

## Diapositiva 6: Demostración (40 s)

La aplicación contiene un MaterialApp, un Scaffold, el título ConectaCruz y el botón exacto Ver negocios. Al pulsarlo, navega a una pantalla de negocios destacados con un catálogo breve de churrasquería. No se implementaron pedidos, reservas, autenticación ni backend, porque exceden el alcance. La ejecución en emulador queda pendiente por el bloqueo documentado del entorno Flutter; la prueba automatizada ya está preparada para validar la navegación cuando se resuelva.
