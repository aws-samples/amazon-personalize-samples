# Introducción

Este ejemplo presenta una pieza clave que puede utilizar para crear una capa de API para consumir las recomendaciones de Amazon Personalize y producir eventos en tiempo real

Como se puede apreciar más abajo, esta es la arquitectura que implementará desde este proyecto.

![Architecture Diagram](images/architecture.png)

**Nota:** Las campañas de Amazon Personalize y los rastreadores de eventos necesitan implementarse de forma independiente de antemano para poder completar este tutorial. Puede implementar la campaña de Amazon Personalize mediante el siguiente ejemplo de automatización en la carpeta MLOps o mediante la carpeta de introducción.

## Requisitos previos

### Instalación de AWS SAM

El Modelo de aplicación sin servidor (SAM) de AWS es un marco de trabajo de código abierto para la creación de aplicaciones sin servidor. Proporciona la sintaxis abreviada para expresar las funciones, las API, las bases de datos y el mapeo del origen de los eventos. Con solo unas pocas líneas por recurso, puede definir la aplicación que desea y modelarla mediante YAML. Durante la implementación, el SAM transforma y expande la sintaxis SAM a la sintaxis de AWS CloudFormation, lo que permite crear aplicaciones sin servidor de forma más rápida.

**Instale** la [CLI de AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
Esto instalará las herramientas necesarias para crear su proyecto, implementarlo y probarlo de manera local. En este ejemplo en particular, solo utilizaremos AWS SAM para crear e implementar. Para obtener más información, consulte nuestra [documentación](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).

### Cree sus componentes de Personalize 

Después de seguir nuestras [instrucciones](https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started) de introducción, **cree** una campaña de Amazon Personalize y adjúntele un rastreador de eventos.

También, podría automatizar esta parte si hace uso de este [ejemplo](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops) de MLOps

## Creación e implementación

Para implementar el proyecto, necesitará ejecutar los siguientes comandos:

1. Clone el repositorio de Amazon Personalize Samples
    - `git clone https://github.com/aws-samples/amazon-personalize-samples.git`
2. Navegue al directorio *next_steps/operations/streaming_events*
    - `cd amazon-personalize-samples/next_steps/operations/streaming_events`
3. Cree su proyecto de SAM. [Instrucciones de instalación](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    - `sam build`
4. Implemente su proyecto. El SAM ofrece una opción de implementación guiada, tenga en cuenta que necesitará proveer su dirección de email como parámetro para recibir una notificación.
    - `sam deploy --guided`
5. Ingrese el bucket de S3 donde desea almacenar los datos de eventos, el ARN de la campaña de Personalize y el ID del rastreador de eventos.

## Prueba de los puntos de conexión

- Navegue a la [consola](https://console.aws.amazon.com/cloudformation/home?region=us-east-1) de Amazon CloudFormation.
- Seleccione la pila que implementó el SAM.
- Navegue a las secciones de salida, donde encontrará 2 puntos de conexión y una clave API:
    1. Punto de conexión POST getRecommendations
    2. Punto de conexión POST Events
    3. Regrese a la consola de API Gateway donde puede hacer clic en la sección Show key (Mostrar clave) para ver la clave de la API

Si utiliza PostMan o similares, necesitará proveer un encabezado con:
`x-api-key: <YOUR API KEY VALUE>`

**Ejemplo de POST getRecommendations:**

*Parámetro del cuerpo:*
```
{
    "userId":"12345"
    
}
```

*Punto de conexión:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev2/recommendations`


**Ejemplo de evento POST**

Para el punto de conexión POST, necesitará enviar un evento similar al siguiente ejemplo en el *cuerpo* de la solicitud:

*Punto de conexión:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev2/history`

*Cuerpo:*
```
{
    "Event":{
        "itemId": "ITEMID",
        "eventValue": EVENT-VALUE,
        "CONTEXT": "VALUE" //optional
    },
    "SessionId": "SESSION-ID-IDENTIFIER",
    "EventType": "YOUR-EVENT-TYPE",
    "UserId": "USERID"
}
```

## Resumen

Ahora que tiene esta arquitectura en su cuenta, puede consumir las recomendaciones de Amazon Personalize por encima del punto de conexión de recomendaciones de POST de API Gateway y transmitir datos de interacción en tiempo real al punto de conexión de eventos de POST.

Hay dos características adicionales de esta arquitectura:

- Un bucket de S3 que contiene sus eventos persiste desde su Kinesis Stream. Puede ejecutar análisis en este bucket mediante otros servicios de AWS como Glue y Athena. Por ejemplo, puede seguir este [blog](https://aws.amazon.com/blogs/big-data/build-and-automate-a-serverless-data-lake-using-an-aws-glue-trigger-for-the-data-catalog-and-etl-jobs/) sobre cómo automatizar una canalización de ETL.



## Próximos pasos

¡Felicitaciones! Implementó y probó la capa de API en su implementación de Amazon Personalize de forma exitosa.

Para obtener más información sobre la obtención de recomendaciones, consulte nuestra [documentación](https://docs.aws.amazon.com/personalize/latest/dg/getting-recommendations.html)
