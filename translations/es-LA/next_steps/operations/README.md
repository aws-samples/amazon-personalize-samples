# Operaciones de Amazon Personalize

En este apartado, se incluyen ejemplos de los siguientes temas:

* [Mantenimiento de experiencias personalizadas con machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
    - Esta solución de AWS le permite automatizar el proceso integral de importación de conjuntos de datos, creación de soluciones y versiones de soluciones, creación y actualización de campañas, creación de filtros y ejecución de trabajos de inferencia por lotes. Estos procesos pueden ejecutarse bajo demanda o activarse en función de un cronograma que se defina.

* MLOps (heredado)
    - Este es un proyecto para mostrar cómo implementar una campaña personalizada de forma completamente rápida y automatizada por medio de AWS Step Functions. Para comenzar, diríjase a la carpeta [ml_ops](ml_ops) y siga las instrucciones README. La solución [Mantenimiento de las experiencias personalizadas con machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) reemplazó este proyecto.

* SDK de ciencia de datos de AWS
    - Este es un proyecto para mostrar cómo implementar una campaña personalizada de forma completamente rápida y automatizada por medio del SDK de ciencia de datos de AWS. Para comenzar, diríjase a la carpeta [ml_ops_ds_sdk](ml_ops_ds_sdk) y siga las instrucciones README.

* [API de personalización](https://github.com/aws-samples/personalization-apis)
    - Marco de la API de baja latencia en tiempo real que se encuentra entre sus aplicaciones y los sistemas de recomendación como Amazon Personalize. Ofrece implementaciones de prácticas recomendadas de almacenamiento en caché de respuestas, configuraciones de API Gateway, pruebas A/B con [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), metadatos de elementos en tiempo de inferencia, recomendaciones contextuales automáticas y mucho más.

* Ejemplos de Lambda
    - Esta carpeta comienza con un ejemplo básico de integración de `put_events` en sus campañas de Personalize mediante el uso de funciones de Lambda que procesan datos nuevos desde S3. Para comenzar, diríjase a la carpeta [lambda_examples](lambda_examples/) y siga las instrucciones README.

* Eventos de streaming
    - Este es un proyecto para mostrar cómo implementar rápidamente una capa de API frente a su campaña de Amazon Personalize y su punto de conexión de seguimiento de eventos. Para comenzar, diríjase a la carpeta [streaming_events](streaming_events/) y siga las instrucciones README.

* Rotación de filtros
    - Esta [aplicación sin servidor](filter_rotator/) incluye una función de AWS Lambda que se ejecuta de acuerdo a un cronograma para rotar los filtros de Personalize que utilizan expresiones con valores fijos que deben cambiarse con el tiempo. Por ejemplo, el uso de un operador de rango basado en un valor de fecha o de hora que está diseñado para incluir o excluir elementos en función de un periodo rotativo.

* [Supervisión personalizada](https://github.com/aws-samples/amazon-personalize-monitor)
    - Con este proyecto, se agregan supervisión, alertas, un panel de control y herramientas de optimización para ejecutar Amazon Personalize en sus entornos de AWS.

## Resumen de la licencia

Este código de ejemplo está disponible por medio de una licencia MIT modificada. Consulte el archivo de la LICENCIA.
