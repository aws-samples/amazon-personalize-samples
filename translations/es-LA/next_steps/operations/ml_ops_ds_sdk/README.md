## Automatice su flujo de trabajo de Personalize con el SDK de ciencia de datos de AWS Step Functions

A medida que el machine learning (ML) se convierte cada vez más en una parte crucial del núcleo de las empresas, surge un énfasis mayor para reducir el tiempo desde la creación de un modelo a su implementación. En noviembre de 2019, AWS lanzó el SDK de ciencia de datos de AWS Step Functions para Amazon SageMaker, un SDK de código abierto que permite a los desarrolladores crear flujos de trabajo de machine learning en Python basados en Step Functions. Ahora, puede utilizar el SDK para crear flujos de trabajo de implementación de modelos reutilizables con las mismas herramientas que utiliza para desarrollar modelos. EL cuaderno completo para esta solución se encuentra en la carpeta “automate_personalize_workflow” en nuestro repositorio de GitHub.

Este repositorio demuestra las capacidades del SDK de ciencia de datos con un caso de uso común: cómo automatizar Personalize. En esta publicación, se crea un flujo de trabajo sin servidor para entrenar un motor de recomendación de películas. Por último, muestra como activar un flujo de trabajo basado en un programa periódico.

### Esta publicación utiliza los siguientes servicios de AWS:
•	AWS Step Functions permite la coordinación de varios servicios de AWS en un flujo de trabajo sin servidor. Puede diseñar y ejecutar flujos de trabajo, en los cuales el resultado de un paso actúa como la entrada del siguiente, e integrar el manejo de errores en el flujo de trabajo.\
•	AWS Lambda es un servicio de computación que permite ejecutar códigos sin aprovisionamiento o servidores de administración. Lambda ejecuta el código solo cuando se activa y escala de forma automática, desde unas pocas solicitudes diarias a miles por segundo.\
•	Amazon Personalize es un servicio de machine learning que permite la personalización de sitios web, aplicaciones, emails y anuncios, entre otros, con modelos personalizados de machine learning que pueden crearse en Amazon Personalize, sin tener experiencia previa en machine learning.

## Información general del SDK
El SDK brinda una manera nueva para utilizar AWS Step Functions. Una función escalonada es una máquina de estados que consiste de una serie de pasos distintos. Cada paso puede ejecutar trabajo, tomar decisiones, iniciar una ejecución paralela o administrar los tiempos de espera. Puede desarrollar pasos individuales y utilizar Step Functions para controlar los disparadores, la coordinación y el estado general del flujo de trabajo. Antes del SDK de ciencia de datos, había que definir las funciones escalonadas mediante Amazon States Language basado en JSON. Ahora, con el SDK, puede crear, ejecutar y visualizar funciones escalonadas con facilidad mediante el código de Python.

Este repositorio ofrece información general del SDK, que incluye cómo crear pasos de Step Function, trabajar con parámetros, integrar capacidades específicas del servicio y enlazar estos pasos para crear y visualizar un flujo de trabajo. Puede encontrar varios ejemplos de código en esta publicación; sin embargo, creamos un cuaderno de Amazon SageMaker que detalla el proceso completo.

## Información general de Amazon Personalize
Amazon Personalize es un servicio de machine learning que facilita a los desarrolladores la creación de recomendaciones individualizadas para los clientes que utilizan sus aplicaciones.

El machine learning se utiliza cada vez más para mejorar el compromiso con el cliente, ya que impulsa recomendaciones personalizadas de productos y contenidos, resultados de búsqueda individualizados y promociones de marketing orientadas al usuario. Sin embargo, en la actualidad y debido a su complejidad, el desarrollo de las capacidades del machine learning necesarias para producir estos sistemas de recomendaciones sofisticadas ha estado fuera del alcance de la mayor parte de las organizaciones. Amazon Personalize permite a los desarrolladores sin experiencia previa en machine learning crear con facilidad capacidades de personalización sofisticadas en sus aplicaciones, mediante el uso de la tecnología de machine learning perfeccionada, luego de años de uso, en Amazon.com.

Con Amazon Personalize, se provee un flujo de actividad desde la aplicación, clics, visitas a la página, registros, compras y demás, así como también un inventario de los elementos que quiere recomendar, como artículos, productos, videos o música. También, se puede proveer a Amazon Personalize con información demográfica adicional de sus usuarios, como edad o ubicación geográfica. Amazon Personalize procesará y examinará los datos, identificará qué parte de estos es significativa, seleccionará los algoritmos correctos y probará y optimizará un modelo de personalización que estará hecho a la medida de los datos. Todos los datos que Amazon Personalize analiza se almacenan de forma segura y privada, solo se utilizan para las recomendaciones personalizadas. Puede empezar a proveer recomendaciones personalizadas mediante una simple llamada a la API. Paga solo por que utiliza, no hay cargos mínimos ni compromisos por adelantado.

Amazon Personalize es como tener su propio equipo de personalización de machine learning de Amazon.com a su disposición, las 24 horas del día.



## Instrucciones
Cargue el cuaderno y siga las instrucciones.

## Licencia

Esta biblioteca tiene licencia de MIT-0 License. Consulte el archivo de la LICENCIA.


