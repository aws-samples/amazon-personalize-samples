Personalización del usuario de Amazon Personalize
---

La receta aws-user-personalization brinda la mayor flexibilidad al momento de crear un caso de uso de personalización del usuario mediante la combinación de un algoritmo basado en HRNN para relevancia con exploración automática de recomendaciones de elementos nuevos/recientes. Aunque el conjunto de datos de interacciones es el único conjunto de datos requerido, esta utilizará los tres tipos de conjunto de datos (de interacciones, de elementos y de usuarios) si se los provee. Además, puede modelar datos de impresión, de forma opcional, si se proporcionan en el conjunto de datos de interacciones y, cuando transmita eventos en tiempo real, mediante un rastreador de eventos.

Se recomienda comenzar con la receta user-personalization, nosotros le brindamos cuadernos de muestra para las recetas de HRNN-* para la posteridad.
## Ejemplos

### User-Personalization 

El archivo [user-personalization-with-exploration.ipynb](user-personalization-with-exploration.ipynb) demuestra cómo utilizar un conjunto de datos de interacciones y elementos para crear una solución y una campaña que equilibre la acción de crear recomendaciones basadas en la relevancia (explotación) y de explorar la recomendación de elementos nuevos/recientes. También, se podría haber utilizado un conjunto de datos de usuario, pero no se incluye en este ejemplo. Este ejemplo demuestra cómo incluir datos de impresión en el conjunto de datos de interacciones y en las llamadas de la API de PutEvents.

### Recomendaciones contextuales + rastreador de eventos

En este ejemplo, analizaremos cómo hacer uso de los metadatos y el contexto para brindar las mejores recomendaciones de aerolíneas para los usuarios basadas en las calificaciones históricas de estas, en múltiples tipos de cabina, con la ubicación de los usuarios como metadatos de los usuarios

El archivo [user-personalization-with-contextual-recommendations.ipynb](user-personalization-with-contextual-recommendations.ipynb) muestra cómo cargar esta información útil a nuestro sistema para apoyar las recomendaciones. Tenga en cuenta que las mejoras en las recetas de metadatos dependen de cuánta información pueda extraerse desde los metadatos provistos.


*Tenga en cuenta que se prefieren las capacidades de arranque en frío de los elementos de la receta User-Personalization por sobre las de la receta de arranque en frío de HRNN de Legacy. Por lo tanto, se recomienda que comience con la receta User-Personalization para escenarios de elementos con arranque en frío.*

## Resumen de la licencia

Este código de ejemplo está disponible por medio de una licencia MIT modificada. Consulte el archivo de la LICENCIA.
