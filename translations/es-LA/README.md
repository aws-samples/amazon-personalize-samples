# Ejemplos de Amazon Personalize

Cuadernos y ejemplos sobre cómo incorporar y utilizar diversas funciones de Amazon Personalize

## Cómo empezar con Amazon Personalize

La carpeta [getting_started/](getting_started/) contiene una plantilla de CloudFormation que desplegará todos los recursos que necesita para crear su primera campaña con Amazon Personalize.

Los cuadernos proporcionados también pueden servir de plantilla para crear sus propios modelos con sus propios datos. Este repositorio se clona en el entorno para que pueda explorar los cuadernos más avanzados también con este enfoque.

## Próximos pasos de Amazon Personalize

La carpeta [next_steps/](next_steps/) contiene ejemplos detallados de los próximos pasos típicos en su recorrido de Amazon Personalize. Esta carpeta incluye el siguiente contenido avanzado:

* Casos de uso básicos
  - [Personalización del usuario](next_steps/core_use_cases/user_personalization)
  - [Clasificación personalizada](next_steps/core_use_cases/personalized_ranking)
  - [Elementos relacionados](next_steps/core_use_cases/related_items)
  - [Recomendaciones por lote](next_steps/core_use_cases/batch_recommendations)
  - [Segmentación de usuarios](next_steps/core_use_cases/user_segmentation)

* Ejemplos de operaciones escalables para sus implementaciones de Amazon Personalize
    - [Mantenimiento de experiencias personalizadas con machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
        - Esta solución de AWS le permite automatizar el proceso integral de importación de conjuntos de datos, creación de soluciones y versiones de soluciones, creación y actualización de campañas, creación de filtros y ejecución de trabajos de inferencia por lotes. Estos procesos pueden ejecutarse bajo demanda o activarse en base a un programa que se defina.
    - [Función MLOps Step](next_steps/operations/ml_ops) (heredado)
        - Este es un proyecto para mostrar cómo implementar una campaña personalizada de forma completamente rápida y automatizada por medio de AWS Step Functions. Para comenzar, diríjase a la carpeta [ml_ops](next_steps/operations/ml_ops) y siga las instrucciones README. Este ejemplo se reemplazó por la solución [Mantenimiento de las experiencias personalizadas con machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) de AWS.
    - [SDK de ciencia de datos de MLOps](next_steps/operations/ml_ops_ds_sdk)
        - Este es un proyecto para mostrar cómo implementar una campaña personalizada de forma completamente rápida y automatizada por medio del SDK de ciencia de datos de AWS. Para comenzar, diríjase a la carpeta [ml_ops_ds_sdk](next_steps/operations/ml_ops_ds_sdk) y siga las instrucciones README.
    - [API de personalización](https://github.com/aws-samples/personalization-apis)
        - Marco de la API de baja latencia en tiempo real que se encuentra entre sus aplicaciones y los sistemas de recomendación como Amazon Personalize. Ofrece implementaciones de prácticas recomendadas de almacenamiento en caché de respuestas, configuraciones de API Gateway, pruebas A/B con [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), metadatos de elementos en tiempo de inferencia, recomendaciones contextuales automáticas y mucho más.
    - [Ejemplos de Lambda](next_steps/operations/lambda_examples)
        - Esta carpeta comienza con un ejemplo básico de integración de `put_events` en sus campañas de Personalize mediante el uso de funciones de Lambda que procesan datos nuevos desde S3. Para comenzar, diríjase a la carpeta [lambda_examples](next_steps/operations/lambda_examples) y siga las instrucciones README.
    - [Supervisión personalizada](https://github.com/aws-samples/amazon-personalize-monitor)
        - Con este proyecto, se agregan supervisión, alertas, un panel de control y herramientas de optimización para ejecutar Amazon Personalize en sus entornos de AWS.
    - [Eventos de streaming](next_steps/operations/streaming_events)
        - Este es un proyecto para mostrar cómo implementar rápidamente una capa de API frente a su campaña de Amazon Personalize y su punto de conexión de seguimiento de eventos. Para comenzar, diríjase a la carpeta [streaming_events](operations/streaming_events/) y siga las instrucciones README.
    - [Rotación de filtros](next_steps/operations/filter_rotator)
        - Esta aplicación sin servidor incluye una función de AWS Lambda que se ejecuta de acuerdo a un cronograma para rotar los filtros de Personalize que utilizan expresiones con valores fijos que deben cambiarse con el tiempo. Por ejemplo, el uso de un operador de rango basado en un valor de fecha o de hora que está diseñado para incluir o excluir elementos en función de un periodo rotativo.

* Talleres
    - La carpeta [Workshops/](next_steps/workshops/) contiene una lista de nuestros talleres más recientes:
        - [POC in a Box](next_steps/workshops/POC_in_a_box)
        - [re:Invent 2019](next_steps/workshops/Reinvent_2019)
        - [Día de inmersión](next_steps/workshops/Immersion_Day)
    - [Integraciones de socios](https://github.com/aws-samples/retail-demo-store#partner-integrations)
        - Explore los talleres que demuestran cómo utilizar Personalize con socios como Amplitude, Braze, Optimizely y Segment.

* Herramientas de ciencia de datos
    - La carpeta [data_science/](next_steps/data_science/) contiene un ejemplo sobre cómo abordar la visualización de las propiedades clave de sus conjuntos de datos de entrada.
        - Datos faltantes, eventos duplicados y consumos de elementos repetidos
        - Distribución de la ley de potencia de los campos categóricos
        - Análisis de la derivación temporal para la aplicación del arranque en frío
        - Análisis de la distribución de las sesiones de los usuarios

* Demostraciones/Arquitecturas de referencia
    - [Tienda de demostración minorista](https://github.com/aws-samples/retail-demo-store)
        - Ejemplo de aplicación web minorista y plataforma de taller que demuestra cómo ofrecer experiencias de cliente personalizadas en todos los canales utilizando Amazon Personalize.

## Resumen de la licencia

Este código de ejemplo está disponible por medio de una licencia MIT modificada. Consulte el archivo de la LICENCIA.
