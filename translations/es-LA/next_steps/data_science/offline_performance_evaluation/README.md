Evaluación del rendimiento sin conexión
===

Tiene algunos datos históricos y necesita saber cómo Personalize actúa sobre sus datos. Sugerimos lo siguiente:

1. Divida sus datos en un conjunto de entrenamiento 'pasado' y en uno 'futuro'.
2. Cargue los datos del 'pasado' en Amazon Personalize, entrene una solución e implemente una campaña.
3. Utilice su campaña para obtener una recomendación para todos los usuarios y compárelas con el conjunto de entrenamiento 'futuro'.

Este es un ejemplo para completar los pasos anteriores [personalize_temporal_holdout.ipynb](personalize_temporal_holdout.ipynb/). Incluimos una recomendación básica, basada en la popularidad, que debería ser sencilla de superar. Se utiliza para propósitos de verificación de estado. Un paso siguiente común, es mantener las mismas divisiones de prueba, pero probarlas con diferentes modelos para comparaciones sin conexión más serias.

## Resumen de la licencia

Este código de ejemplo está disponible por medio de una licencia MIT modificada. Consulte el archivo de la LICENCIA.
