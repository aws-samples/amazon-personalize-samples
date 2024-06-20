Casos de uso centrales de Amazon Personalize
---

Amazon Personalize es un servicio de machine learning que permite a los desarrolladores producir recomendaciones individualizadas para los clientes que utilizan sus aplicaciones. Refleja la vasta experiencia que tiene Amazon en la creación de sistemas personalizados. Puede utilizar Amazon Personalize en una variedad de escenarios, como brindar recomendaciones de usuarios basadas en sus preferencias y comportamiento, la reclasificación personalizada de los resultados y contenido personalizado para emails y notificaciones.

Como desarrollador, solo necesita realizar lo siguiente:

- Formatear los datos de entrada y cargarlos en el bucket de Amazon S3, o enviar datos de elementos, usuarios y eventos en tiempo real mediante el SDK personalizado.
- Seleccionar una receta de entrenamiento (algoritmo) para utilizar en los datos.
- Entrenar una versión de la solución por medio de la receta.
- Implementar la versión de la solución.

## Asignación de casos de uso a las recetas

| Caso de uso | Receta | Descripción
|-------- | -------- |:------------
| Personalización del usuario | aws-user-personalization | Esta receta está optimizada para todos los escenarios de recomendación de los usuarios. Predice los elementos con los que el usuario interactuará en función de los conjuntos de datos de interacciones, elementos y usuarios. Utiliza un algoritmo de HRNN para generar recomendaciones basadas en la relevancia (explotación) y en la exploración automática de elementos para recomendar elementos nuevos/fríos. Usted controla la importancia de la explotación frente a la exploración.
| Elementos relacionados | aws-sims | Calcula los elementos similares a un elemento determinado en función de la coocurrencia del elemento en el mismo historial del usuario en el conjunto de datos de interacciones.
| Clasificación personalizada | aws-personalized-ranking | Vuelve a clasificar una lista de elementos para un usuario. Entrena los conjuntos de datos de interacciones, elementos y usuarios.

*La tabla de arriba enumera las asignaciones principales y más recomendados de los casos de uso a las recetas. Personalize es compatible con otras recetas como aws-popularity-count y aws-hrnn, aws-hrnn-coldstart, and aws-hrnn-metadata de Legacy. Sin embargo, los algoritmos en las recetas aws-hrnn-* se incluyeron y ampliaron en la receta aws-user-personalization, por lo que ya no se recomiendan para casos de uso de personalización.*

## Contenido

En este directorio, tenemos ejemplos de varios casos de uso.

1. [Personalización del usuario](user_personalization/)
    - Predice los elementos con los que interactuará un usuario. Una red neuronal recurrente y jerárquica que puede modelar el orden temporal de las interacciones entre el usuario y el elemento combinada con exploración automática de elementos nuevos/fríos.
2. [Elementos relacionados](related_items/)
    - Calcula los elementos similares a un elemento determinado en función de la coocurrencia del elemento en el mismo historial del usuario en el conjunto de datos de interacción entre el usuario y el elemento.
3. [Clasificación personalizada](personalized_ranking/)
    - Clasifica una lista de elementos para un usuario basado en la relevancia.
4. [Recomendaciones por lote](batch_recommendations/)
    - Cree recomendaciones para múltiples usuarios o elementos en un solo trabajo por lote.
5. [Metadatos](metadata/)
    - Ejemplos de cómo preparar e incluir metadatos en tus conjuntos de datos.
5. [Optimización objetiva](objective_optimization/objective-optimization.ipynb)
    - Ejemplo de cómo equilibrar los objetivos de la empresa con las recomendaciones relevantes mediante la optimización objetiva.
## Resumen de la licencia

Este código de ejemplo está disponible por medio de una licencia MIT modificada. Consulte el archivo de la LICENCIA.
