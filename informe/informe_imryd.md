# Elección de un framework móvil para un negocio local de Santa Cruz

**Asignatura:** Aplicaciones Móviles I  
**Caso:** ConectaCruz y una churrasquería local  
**Fecha de consulta:** 8 de noviembre de 2026

## Introducción

Pequeños negocios de Santa Cruz suelen presentar su oferta y atender consultas por WhatsApp y redes sociales. En este caso académico, ConectaCruz requiere una primera aplicación que pueda mostrar un catálogo y que, en una fase posterior, admita pedidos y reservas. La información del caso no demuestra que exista hoy una operación con pagos, pedidos o reservas digitales. Esas funciones se tratan como necesidades de alcance futuro, no como hechos observados.

El problema consiste en elegir una tecnología que permita construir una aplicación para Android e iOS con un presupuesto limitado y una sola base de código cuando sea razonable. El objetivo fue comparar Flutter, React Native y desarrollo nativo separado para Android e iOS mediante una matriz ponderada. La evaluación no constituye un benchmark empírico ni una medición de rendimiento en dispositivos reales.

## Métodos

Se compararon tres alternativas: Flutter, React Native y desarrollo nativo Android/iOS. Se evaluaron cinco criterios: costo inicial y de mantenimiento, rendimiento, comunidad y ecosistema, compatibilidad Android/iOS y curva de aprendizaje. La escala fue de 1 a 5, donde 1 representa una condición menos favorable para este caso y 5 una condición más favorable. Los pesos suman 100% y responden al supuesto de presupuesto limitado y necesidad de atender ambas plataformas.

Flutter permite compilar desde una sola base de código para Android e iOS, entre otras plataformas (Flutter, s. f.-a). Su documentación explica que Dart usa compilación JIT durante el desarrollo y AOT para código nativo eficiente en producción (Flutter, s. f.-a). React Native permite reutilizar código, pero conserva puntos específicos por plataforma cuando son necesarios (Meta, s. f.-a); su guía actual recomienda usar un framework como Expo para nuevos proyectos (Corti, 2024). El enfoque nativo utiliza herramientas oficiales de cada plataforma: Android Studio y Gradle para Android (Google, s. f.) y Xcode/SwiftUI para Apple (Apple, s. f.).

## Resultados

La puntuación ponderada se calculó mediante la fórmula: **aporte = peso × calificación / 5**. No se interpretan los resultados en esta sección.

| Criterio | Peso | Flutter | Aporte Flutter | React Native | Aporte RN | Nativo Android/iOS | Aporte nativo |
|---|---:|---:|---:|---:|---:|---:|---:|
| Costo inicial y mantenimiento | 30% | 5 | 30,0 | 4 | 24,0 | 2 | 12,0 |
| Rendimiento previsto | 20% | 4 | 16,0 | 4 | 16,0 | 5 | 20,0 |
| Comunidad y ecosistema | 15% | 4 | 12,0 | 5 | 15,0 | 5 | 15,0 |
| Compatibilidad Android e iOS | 25% | 5 | 25,0 | 4 | 20,0 | 3 | 15,0 |
| Curva de aprendizaje | 10% | 4 | 8,0 | 4 | 8,0 | 2 | 4,0 |
| **Total** | **100%** |  | **91,0** |  | **83,0** |  | **66,0** |

## Discusión

Flutter obtiene 91,0 de 100 en esta matriz y se propone para ConectaCruz. La propuesta se sostiene principalmente en una base de código común para Android e iOS, una interfaz consistente y un costo de desarrollo más contenido que dos aplicaciones nativas separadas. Para una primera pantalla de catálogo, estas propiedades se ajustan al alcance planteado.

La elección también tiene límites. El equipo debe aprender Dart y verificar la disponibilidad y madurez de paquetes antes de incorporar funciones de WhatsApp, pagos, mapas o reservas. React Native puede ser preferible si el equipo ya domina React y JavaScript. El desarrollo nativo puede convenir cuando una experiencia muy específica por plataforma o integraciones de bajo nivel justifican mantener dos bases de código.

No se ejecutaron pruebas de rendimiento en un dispositivo físico ni en iOS para esta entrega. La documentación de Flutter recomienda medir rendimiento en un dispositivo real y en modo profile, pues un emulador y el modo debug no reflejan el comportamiento final (Flutter, s. f.-b). La evidencia local también registra que el entorno disponible bloqueó la ejecución de los comandos Flutter; por ello, la pantalla incluida debe validarse en Android cuando se libere ese bloqueo. La aplicación conserva el alcance de una churrasquería: presenta un catálogo de ejemplo y no implementa reservas, pedidos, autenticación ni backend.

## Referencias

Apple. (s. f.). *SwiftUI*. Recuperado el 8 de noviembre de 2026, de https://developer.apple.com/swiftui/

Corti, N. (2024, 25 de junio). *Use a framework to build React Native apps*. React Native. https://reactnative.dev/blog/2024/06/25/use-a-framework-to-build-react-native-apps

Flutter. (s. f.-a). *FAQ*. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/resources/faq

Flutter. (s. f.-b). *Flutter performance profiling*. Recuperado el 8 de noviembre de 2026, de https://docs.flutter.dev/perf/ui-performance

Google. (s. f.). *Develop for Android*. Recuperado el 8 de noviembre de 2026, de https://developer.android.com/develop

Meta. (s. f.). *Platform-specific code*. React Native. Recuperado el 8 de noviembre de 2026, de https://reactnative.dev/docs/platform-specific-code.html
