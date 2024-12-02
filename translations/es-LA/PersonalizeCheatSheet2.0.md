# Hoja de referencia de Amazon Personalize

## ¿Amazon Personalize es una opción adecuada?

Amazon Personalize es una excelente plataforma para utilizar un sistema de recomendación a escala en AWS, pero no es adecuada para todos los escenarios de personalización o recomendación. La siguiente tabla es una guía aproximada de opciones adecuadas y no adecuadas.

|Opción adecuada	|Opción no adecuada	|
|---	|---	|
|Recomendación de elementos a usuarios conocidos. Películas a los usuarios en función de su historial de visualización.	|Recomendaciones basadas en marcadores de metadatos explícitos. Cuando un usuario nuevo responde a las preferencias para orientar sus recomendaciones.	|
|Recomendación de elementos nuevos a usuarios conocidos. Un sitio de venta minorista que agrega elementos nuevos a los usuarios actuales.	|Bajos volúmenes de datos de usuarios, elementos e interacciones (consulte el gráfico a continuación).	|
|Recomendación de elementos a usuarios nuevos. Un usuario acaba de registrarse y recibe recomendaciones rápidamente.	|En su mayoría, usuarios sin identificar. Una aplicación en la que no hay un registro histórico de la actividad de los usuarios.	|
|Recomendación de elementos nuevos a usuarios nuevos. Un sitio de venta minorista que recomienda elementos nuevos a un usuario nuevo.	|**Cargas de trabajo de la siguiente mejor acción:** Personalize recomienda elementos probables, y no comprende los flujos de trabajo y las secuencias adecuados.	|

### Volumen de datos mínimo sugerido

1. Más de 50 usuarios
2. Más de 50 elementos
3. Más de 1500 interacciones

Si sus conjuntos de datos no se ajustan, es demasiado pronto para utilizar Amazon Personalize.


## Caso de uso por receta

¿Qué tipo de casos de uso se pueden resolver y de qué forma?

1. **Recomendaciones personalizadas** `User-Personalization`:
    1. Se trata de un caso de uso principal de Amazon Personalize, en donde se utilizan los datos de interacción entre los elementos y los usuarios para crear un modelo de recomendación que apunta directamente a cada usuario, y permite agregar usuarios nuevos sobre la marcha con PutEvents sin necesidad de volver a entrenarlos. PutEvents también permite que los usuarios vean las recomendaciones que se basan en su comportamiento más reciente para que no se pierda esa información adicional. También puede introducir componentes específicos del contexto, como el tipo de dispositivo o la ubicación, para mejorar los resultados.
    2. También puede agregar metadatos de elementos y usuarios para enriquecer más el modelo o para filtrar las recomendaciones por atributo.
    3. Para los casos de uso de video bajo demanda y de venta minorista, los recomendadores de dominio “Principales selecciones para usted” y “Recomendado para usted” le permiten ponerse en marcha rápidamente y con menor sobrecarga operativa.
2. **Recomendación de elementos a usuarios nuevos** `User-Personalization`:
    1. Se pueden agregar usuarios nuevos (también conocidos como usuarios fríos) a sus soluciones de personalización de usuarios existentes aprovechando la función PutEvents. Cada usuario nuevo comienza con una representación en el servicio que devuelve los elementos populares. El comportamiento del usuario desplaza esta representación. A medida que interactúan con el contenido dentro de la aplicación y la aplicación envía los eventos a Personalize, las recomendaciones se actualizan sin necesidad de volver a entrenar el modelo. De esta forma, se obtiene una personalización actualizada sin que se tengan que reentrenar los modelos de forma constante.
3. **Recomendación de elementos nuevos** `User-Personalization`:
    1. Esto es sumamente útil cuando su cliente tiene elementos nuevos (también conocidos como elementos fríos) que deben mostrarse a sus usuarios con algún tipo de personalización. Esto permite que se recomienden los elementos sin precedentes históricos en función de factores de los metadatos.
    2. También se puede utilizar con el entrenamiento y la actualización incrementales de su conjunto de datos para iniciar los nuevos elementos fríos con mayor facilidad.
    3. Por último, con este enfoque se aprovecha una capacidad de exploración similar a la de un ladrón para ayudarlo a determinar rápidamente qué resultados son lógicos y cuáles no para las recomendaciones. Es un enfoque mucho mejor que aquel en el que simplemente se ofrece el contenido nuevo sin pensar.
4. **Reordenación por relevancia** `Personalized-Ranking`:
    1. Se utiliza el mismo algoritmo de HRNN en la personalización del usuario, pero acepta un usuario Y una colección de elementos. Entonces, luego se analizará la colección de elementos y se clasificarán en orden de mayor a menor relevancia para el usuario. Esto es ideal para promocionar una colección de elementos preseleccionados y saber qué es lo correcto para promocionar a un usuario en particular.
5. **Elementos relacionados** `Similar-Items`/`SIMS`:
    1. `Similar-Items`: modelo de aprendizaje profundo que tiene en cuenta tanto los datos de las interacciones como los metadatos de los elementos para equilibrar las recomendaciones de elementos relacionados en función del historial de interacción y la similitud de los metadatos de los elementos. Es útil cuando se tienen menos datos de interacción pero se tienen metadatos de elementos de calidad o cuando con frecuencia se introducen elementos fríos o nuevos.
    2. `SIMS`: una idea bastante sencilla, que se implementa a través del filtrado colaborativo entre elementos, pero que básicamente analiza cómo las personas interactúan junto con elementos particulares y luego determina el nivel de similitud de los elementos a nivel global en función de los datos de interacción. No tiene en cuenta los metadatos de los elementos o de los usuarios y no está personalizado para cada usuario. Es útil cuando se tienen muchos datos de interacción relevantes, cuando no se tienen muchos elementos fríos (catálogo cambiante) o cuando se carece de metadatos de los elementos.
    3. Para los casos de uso de video bajo demanda y de venta minorista, los recomendadores de dominio “Porque vio X”, “Más como X”, “Con frecuencia comprados juntos” y “Los clientes que vieron X también lo vieron” le permiten ponerse en marcha rápidamente y con menor sobrecarga operativa.
6. `Similar-Items`/`SIMS` **que con frecuencia se compran juntos**:
    1. La clave está en preparar los datos adecuados para entrenar un modelo en Personalize y elegir la receta correcta. Por ejemplo, entrenar un modelo SIMS solo con los datos de compra y, si es posible, entrenar solo con los datos de compra en donde los clientes hayan comprado varios elementos o hayan comprado elementos de varias categorías. Esto hará que el modelo tenga el comportamiento deseado y que las recomendaciones sean diversas (que es lo que usted desea para este caso de uso).
    2. SIMS también puede combinarse con Personalized-Ranking para reordenar las recomendaciones de SIMS antes de presentarlas al usuario. De esta forma, los elementos que se compran juntos con frecuencia se ofrecen en un orden personalizado.
    3. El recomendador de dominio “Con frecuencia comprados juntos” le permitirá ponerse en marcha rápidamente y con menor sobrecarga operativa.
7. `Popularity-Count` **en general más popular**:
    1. No es machine learning, solo una base de referencia a partir del recuento de los elementos con los que más se interactúa. Esta receta es útil para las recomendaciones de elementos populares o para crear una base de referencia de métricas sin conexión que puede utilizarse para la comparación con versiones de soluciones creadas por medio de otras recetas de personalización de usuarios con los mismos conjuntos de datos.
    2. Para los casos de uso de video bajo demanda y de venta minorista, los recomendadores de dominio “Más populares”, “Más vistos” y “Más vendidos” le permiten ponerse en marcha rápidamente y con menor sobrecarga operativa.
8. **Segmentación de usuarios** `Item-Affinity`/`Item-Attribute-Affinity`:
    1. Cree segmentos de usuarios en función de su afinidad con elementos específicos de su catálogo o su afinidad con atributos de los elementos. Es una excelente opción para las campañas de marketing en las que busca dirigirse a los usuarios que tienen interés en elementos específicos que desea promocionar o en elementos similares a los existentes.

## Características estupendas:

1. [Grupos de conjuntos de datos de dominio](https://docs.aws.amazon.com/personalize/latest/dg/domain-dataset-groups.html): recomendadores para casos de uso de video bajo demanda y de venta minorista
    1. Un *grupo de conjuntos de datos de dominio* es un contenedor de Amazon Personalize para recursos preconfigurados específicos del dominio, incluidos conjuntos de datos, recomendadores y filtros. Utilice un grupo de conjuntos de datos de dominio si tiene una aplicación de video en streaming o de comercio electrónico y desea que Amazon Personalize encuentre las mejores configuraciones para sus recomendadores.
2. Recomendaciones contextuales
    1. Le permite definir el alcance de las recomendaciones para indicar que varía según la interacción en lugar de ser específico para el usuario o el elemento. Tiene en cuenta la ubicación actual del usuario, el dispositivo o canal que se utiliza, la hora del día, el día de la semana, etc.
    2. Consulte un ejemplo detallado en la siguiente publicación en el blog: https://aws.amazon.com/blogs/machine-learning/increasing-the-relevance-of-your-amazon-personalize-recommendations-by-leveraging-contextual-information/
3. Filtrado de interacciones y metadatos
    1. Filtre las recomendaciones en función del historial de interacción del usuario o de los atributos de los metadatos para los elementos o el usuario actual. Muy útil en casi todas las cargas de trabajo de medios de comunicación o minoristas. Por ejemplo, se pueden excluir elementos comprados recientemente o agotados, o incluir y excluir elementos recomendados en función de la categoría o el género.
    2. Consulte la siguiente publicación en el blog para obtener más información: https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/
4. Inferencia por lotes
    1. Ideal para exportar grandes cantidades de recomendaciones a archivos para cachés, para campañas de email o simplemente para el análisis general.
5. Campañas de AutoScaling
    1. El servicio se escalará de forma automática para satisfacer las demandas de tráfico si una campaña en particular está sobrecargada. También se reducirá a la capacidad mínima solicitada cuando disminuya el volumen de tráfico.
6. Texto no estructurado como metadatos del elemento
    1. Agregue las descripciones de sus productos, la sinopsis de sus videos o el contenido de sus elementos como un campo de metadatos de los elementos y deje que Personalize utilice el procesamiento del lenguaje natural (NLP) para extraer características ocultas de su texto y mejorar la relevancia de las recomendaciones.
7. Eventos PUT
    1. Permite que las aplicaciones actualicen Personalize en tiempo real con los cambios de las intenciones del comportamiento del usuario. Esto significa que cada solicitud posterior puede adaptarse a esa intención SIN necesidad de repetir el entrenamiento.
8. Elementos PUT/Usuarios PUT
    1. Permite que las aplicaciones agreguen o actualicen lotes individuales o minilotes de elementos o usuarios sin tener que cargar todos los conjuntos de datos de elementos y usuarios.
    2. Para obtener más información, consulte las preguntas frecuentes a continuación.
9. Integración de KMS
    1. Todos los datos se pueden cifrar con una clave administrada por el cliente. Todos los datos se cifran independientemente.
10. No se comparte la información
    1. Todos los datos del cliente están completamente aislados y no se aprovechan para mejorar las recomendaciones de Amazon o de cualquier otra parte.
    2. Los modelos son privados para la cuenta de AWS del cliente.

## Serie de videos:

1. Introducción a Amazon Personalize: https://www.youtube.com/c/amazonwebservices/videos
2. Comprensión de sus datos con Amazon Personalize: https://www.youtube.com/watch?v=TEioktJD1GE
3. Resolución de casos de uso reales con Amazon Personalize: https://www.youtube.com/watch?v=9N7s_dVVWBE
4. Poner a disposición de los usuarios las recomendaciones de Amazon Personalize: https://www.youtube.com/watch?v=oeVYCOFNFMI
5. Poner en marcha la POC de Amazon Personalize: https://www.youtube.com/watch?v=3YawVCO6H14

## Preguntas frecuentes:

1. ¿Con qué frecuencia se debe volver a entrenar?
    1. La frecuencia del reentrenamiento se determina según las necesidades de la empresa. ¿Con qué frecuencia necesita conocer de forma global a sus usuarios y su comportamiento con los elementos? ¿Con qué frecuencia necesita incluir elementos nuevos? Las respuestas determinan la frecuencia de entrenamiento. Por lo general, la mayoría de los clientes lo hacen de forma semanal. Consulte a continuación para obtener una orientación más detallada.
    2. Si utiliza la receta “aws-user-personalization”, el servicio actualizará de forma automática la versión de la solución en segundo plano cada 2 horas (sin costo adicional). Este proceso de actualización automática incorporará los nuevos elementos agregados desde la última actualización para que puedan empezar a ser recomendados a los usuarios (es decir, elementos de arranque en frío). Esto funciona en coordinación con el parámetro explorationWeight establecido en la campaña para controlar la importancia que se le da a la recomendación de elementos nuevos o fríos frente a los elementos relevantes (analizar/utilizar).
    3. Si la actualización automática de 2 horas no es lo suficientemente frecuente para incorporar elementos nuevos, puede crear de forma manual una nueva versión de la solución con trainingMode=UPDATE y actualizar la campaña con mayor frecuencia (es decir, cada hora). Esto hace básicamente lo mismo que la actualización automática, solo que con una frecuencia definida por el cliente. Sin embargo, hay un costo por horas de entrenamiento para hacer esto de forma manual.
    4. Independientemente de si el proceso de modo de actualización es automático o manual, el modelo no se vuelve a entrenar completamente. El cliente aún tendría que crear de vez en cuando una nueva versión de la solución con trainingMode=FULL para volver a entrenar completamente el modelo. Es importante hacerlo ocasionalmente para volver a calcular el nivel de importancia en el modelo teniendo en cuenta todos los datos. Sin embargo, el proceso de actualización automática hace que el reentrenamiento completo sea necesario con menos frecuencia. Aquí es donde entra en juego la orientación semanal. Deje que la actualización automática se ejecute toda la semana y vuelva a realizar un entrenamiento completo una vez a la semana.
    5. Para obtener más precisión en la frecuencia del reentrenamiento, otro enfoque consiste en supervisar las métricas en línea. Cuando empiecen a disminuir (es decir, la desviación de un modelo), es el momento de volver a entrenar.
2. ¿Cómo agrego un usuario nuevo?
    1. Si utiliza la API PutEvents, el usuario nuevo existe tan pronto como se registra su primera acción. Si no aprovecha esto, el usuario aparecerá en el sistema tan pronto como haya vuelto a entrenar un modelo que contenga su comportamiento en su conjunto de datos de interacciones.
    2. Si su usuario no se conoce (un nuevo usuario anónimo antes del registro) todavía puede trabajar para arrancarlo en frío. Si puede asignar un nuevo UUID para su usuario y sessionID de forma inmediata, entonces puede continuar el proceso como se definió anteriormente para arrancar un usuario en frío.
    3. Si esa opción no funciona, aún puede generar un nuevo UUID para el sessionID, llamar a PutEvents sin un userID y luego continuar especificando el mismo sessionID después de que se haya generado un userID válido para ellos. Cuando vuelva a entrenar, Personalize combinará los datos históricos con los datos de PutEvents, y cuando identifique algunos sessionID que coincidan, combinará todas las interacciones anónimas anteriores junto con las interacciones no anónimas del usuario. Esto le permitirá especificar el historial antes de tener un userID interno válido.
    4. Puede agregar y actualizar usuarios individualmente o en minilotes con la API PutUsers. Sin embargo, solo los usuarios con interacciones recibirán recomendaciones personalizadas después del (re)entrenamiento o cuando se arranque en frío con la API PutEvents.
3. ¿Cómo agrego un elemento nuevo?
    1. Hay dos formas de agregar elementos al conjunto de datos de elementos: 1) Agregar elementos nuevos al conjunto de datos de elementos cargando el conjunto de datos completo mediante un trabajo de importación de conjuntos de datos. 2) Agregar elementos individualmente o en minilotes mediante la API PutItems.
    2. Los nuevos elementos se incorporarán a las recomendaciones después del reentrenamiento si también existen interacciones (todas las fórmulas) o a nuevas recomendaciones de elementos de arranque en frío con o sin interacciones después de actualizar la solución (trainingMode = FULL/UPDATE solo para aws-user-personalization y HRNN-Coldstart).
    3. Por ejemplo, puede transmitir elementos nuevos de forma orgánica en su conjunto de datos históricos colocando anuncios para los lanzamientos nuevos. Todo lo que haga que un usuario interactúe con los elementos nuevos y que esa acción se registre puede mejorar las recomendaciones después del siguiente entrenamiento.
4. ¿Cómo puedo filtrar los resultados para determinadas condiciones?
    1. Utilizando la característica de filtros para la interacción (https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) o la información de los metadatos (https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/).
    2. En la actualidad, el filtrado que se basa en el historial de interacciones solo tiene en cuenta las 100 interacciones en tiempo real más recientes (API PutEvents) y las 200 interacciones históricas más recientes del conjunto de datos en el momento del reentrenamiento. Todos los tipos de eventos están incluidos en límites entre 100 y 200.
5. Necesito filtrar los elementos en función de un valor de fecha variable, pero los filtros no admiten valores dinámicos para los operadores de intervalo. ¿Qué opciones tengo?
    1. En la actualidad, los operadores de intervalo no pueden utilizarse con valores dinámicos, por lo que debe crear una expresión de filtro con un valor fijo y luego rotar el filtro de forma periódica para actualizar dicho valor. La solución del [rotador de filtros](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/filter_rotator) puede utilizarse para automatizar el proceso de rotación.
6. ¿Por qué debería utilizar Amazon Personalize en lugar de una solución personalizada?
    1. Suponiendo que sus datos y casos de uso se encuentran en consonancia, esta es una excelente manera de obtener un modelo de primera clase frente a los usuarios finales más rápido. Personalize no solo gestiona la carga operativa que implica ejecutar un sistema de recomendación a escala, sino que también lo libera para mejorar la ingeniería de características, la recopilación de datos y las experiencias de los usuarios o para resolver otros problemas.
7. Tengo un caso de uso en el que mis clientes compran o interactúan con elementos de mi catálogo con poca frecuencia (por ejemplo, la compra de un automóvil). ¿Amazon Personalize es todavía una opción adecuada?
    1. Sí, Personalize aún se puede utilizar de forma eficaz para este tipo de casos de uso. Por ejemplo, se puede entrenar un modelo SIMS en función de toda la actividad del usuario, como el historial de navegación o de compras (en línea o sin conexión), y luego utilizarlo para hacer recomendaciones de elementos similares en las páginas de detalles de los elementos. Esto le permite aprovechar la actividad reciente de todos los usuarios activos para hacer recomendaciones relevantes a los usuarios que regresan.
    2. Las recomendaciones en tiempo real también son eficaces en este caso, ya que Personalize puede aprender del interés actual de un usuario y adaptar las recomendaciones rápidamente. Por ejemplo, en un principio puede recomendar elementos populares y luego personalizar rápidamente las recomendaciones después de que se produzcan algunas interacciones utilizando la API PutEvents.
8. ¿Debo utilizar AutoML?
    1. No, las recetas resuelven diferentes casos de uso. Tómese el tiempo necesario para seleccionar la receta más apropiada para el caso de uso y omita esta característica.
9. ¿Debo optimizar los hiperparámetros (HPO)? ¿Con qué frecuencia?
    1. Ocasionalmente. Tome los resultados de un trabajo de HPO y utilícelos de forma explícita en la configuración de la solución para varios reentrenamientos. A continuación, ejecute la HPO de nuevo y repita. Los parámetros ajustados de forma realista no deberían cambiar mucho entre los trabajos de entrenamiento. Con este enfoque se mantendrán los tiempos de entrenamiento y, por lo tanto, los costos, que son más bajos que si se ejecutara la HPO para todos los trabajos de entrenamiento sin sacrificar la precisión del modelo.
10. ¿Cómo puedo prever el precio del entrenamiento?
    1. Lamentablemente, no hay una manera certera de saberlo de antemano, pero tenemos algunas pruebas que se han realizado en el conjunto de datos de MovieLens. Por ejemplo, utilizando `User-Personalization`, se necesitan alrededor de 6 horas persona para el entrenamiento de 25 millones de interacciones, pero menos de 1 hora persona para entrenar 100 000 interacciones. Como el entrenamiento se divide entre varios alojamientos, las horas reales son 53,9 horas para 50 millones y 2,135 horas para 100 000. La facturación se realiza sobre las horas reales, no horas persona.
11. ¿Qué es una hora TPS y cómo se relaciona con el precio y la usabilidad?
    1. Amazon Personalize activa recursos de computación dedicados que permanecerán aprovisionados para cumplir con sus requisitos mínimos de rendimiento esperados (Transacciones por Segundo o TPS). Se facturan según las horas que estos recursos están asignados, por lo tanto una hora TPS. 1 hora TPS es la cantidad de capacidad de computación necesaria para ofrecer 1 recomendación por segundo durante toda una hora.
    2. El uso se mide en incrementos de 5 minutos, donde el máximo de la cantidad promedio de solicitudes y el rendimiento mínimo aprovisionado en cada incremento se utilizan como el valor de la hora TPS. Por lo tanto, cuando el servicio escala por encima del valor de TPS mínimo aprovisionado, al cliente solo se le factura la capacidad realmente consumida. Las horas TPS de todos los incrementos de 5 minutos se suman durante el periodo de facturación para determinar el total de horas TPS para los cálculos de facturación.
    3. El servicio se ampliará de forma automática si su tráfico supera el valor de TPS mínimo aprovisionado en la campaña. Además, ha demostrado ser una herramienta valiosa para muchos de nuestros clientes. Se asigna un búfer de capacidad cuando se supera el valor de TPS mínimo aprovisionado para permitir que el servicio absorba los aumentos en la carga de solicitudes mientras escala horizontalmente.
    4. Si su cliente sabe que habrá un pico de actividad, como una venta relámpago o un evento promocional, haga que utilice algún proceso automatizado para actualizar la capacidad aprovisionada para satisfacer la nueva necesidad. Luego, redúzcalo si no puede esperar 5 a 10 minutos para que el servicio escale automáticamente por ellos.
    5. El proyecto Amazon Personalize Monitor ofrece un panel de CloudWatch, métricas personalizadas, alarmas de utilización y funciones de optimización de costos para las campañas de Personalize: https://github.com/aws-samples/amazon-personalize-monitor
12. ¿Cómo puedo saber si un modelo de Personalize ofrece recomendaciones de alta calidad?
    1. Personalize ofrece métricas sin conexión para cada versión de la solución que miden la precisión de las predicciones del modelo en comparación con la división de los datos del conjunto de datos de interacciones. Utilice estas métricas para proporcionar un sentido direccional de la calidad de una versión de la solución en comparación con otras versiones.
    2. Las pruebas en línea (es decir, las pruebas A/B) siempre serán la mejor medida del impacto de un modelo en las métricas empresariales.
    3. Cuando se comparan los modelos de Personalize frente a un sistema de recomendación existente, en un principio todos los datos históricos están sesgados hacia el enfoque existente. A menudo, las métricas sin conexión no reflejan lo que un usuario PODRÍA haber hecho si estuviera expuesto a otra cosa (los datos no reflejan cómo podrían hacerlo). De manera que vale la pena señalar este efecto y el análisis basado en el ladrón que Personalize puede hacer para aprender de sus usuarios de forma más orgánica y mejorada. Por lo tanto, se recomienda realizar una prueba en línea algunas semanas **antes** de iniciar realmente una prueba para medir los resultados.
    4. Consulte la siguiente publicación en el blog para obtener más información: https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/
13. ¿Cómo puedo optimizar los costos?
    1. ¡NO UTILICE AUTOML!
    2. NO COMIENCE CON LA HPO: diseñe algo que funcione primero y optimícelo al final.
    3. Vuelva a entrenar únicamente según los requisitos de la empresa. Consulte las preguntas frecuentes para obtener más información.
    4. Utilice mucho en el escalado automático y establezca el valor de TPS mínimo aprovisionado bajo a menos que afecte de forma negativa a sus objetivos de rendimiento o latencia.
    5. Considere el uso de las recomendaciones por lotes cuando el caso de uso corresponda a un proceso por lotes posterior, como el marketing por email. Dado que las recomendaciones por lotes se ejecutan en una versión de la solución, no requieren una campaña.
    6. El proyecto Amazon Personalize Monitor ofrece algunas características de optimización de costos para optimizar el aprovisionamiento de campañas, además de alertar sobre campañas inactivas o abandonadas y eliminarlas: https://github.com/aws-samples/amazon-personalize-monitor
14. ¿Cuáles son las mejores formas de utilizar el almacenamiento en caché con Amazon Personalize? ¿Cómo debo integrar Personalize con mis aplicaciones existentes?
    1. Consulte la solución de las [API de personalización](_https://github.com/aws-samples/personalization-apis_): Marco de la API de baja latencia en tiempo real que se encuentra entre sus aplicaciones y los sistemas de recomendación como Amazon Personalize. Ofrece implementaciones de prácticas recomendadas de almacenamiento en caché de respuestas, configuraciones de API Gateway, pruebas A/B con [Amazon CloudWatch Evidently](_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_), metadatos de elementos en tiempo de inferencia, recomendaciones contextuales automáticas y mucho más.
15. ¿Cuál es la mejor forma de comparar Personalize con una experiencia de usuario existente u otro sistema de recomendación?
    1. Las pruebas A/B son la técnica más común para evaluar la eficacia de Personalize con respecto a las métricas en línea.  [Amazon CloudWatch Evidently]([_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html)) es una herramienta de pruebas A/B de AWS que puede utilizarse con Personalize. El proyecto de las [API de personalización]([_https://github.com/aws-samples/personalization-apis_](https://github.com/aws-samples/personalization-apis)) ofrece una solución que se puede implementar y una arquitectura de referencia.
16. ¿Cómo influyen los registros incrementales en las recomendaciones para el usuario actual?
    1. Amazon Personalize permite importar [interacciones](https://docs.aws.amazon.com/personalize/latest/dg/importing-interactions.html), [usuarios](https://docs.aws.amazon.com/personalize/latest/dg/importing-users.html) y [elementos](https://docs.aws.amazon.com/personalize/latest/dg/importing-items.html) de forma incremental. Estos pueden afectar las recomendaciones para el usuario actual de diferentes maneras, dependiendo de si se entrenó una nueva versión de la solución y del tipo de trainingMode que se utilizó:

|Incremento	|Receta	|Sin reentrenamiento	|Reentrenamiento trainingMode=UPDATE	|Reentrenamiento trainingMode=FULL	|Comentarios	|
|---	|---	|---	|---	|---	|---	|
|putEvent con un usuario nuevo	|Personalización del usuario	|La personalización comienza después del primer evento, pero será más visible después de 2 a 5 eventos con 1 a 2 segundos de retraso después de la llamada de PutEvents después del registro de cada evento.	|Ningún efecto adicional más allá de los efectos descritos en “Sin reentrenamiento”.	|Recomendaciones personalizadas	|Cuantos más eventos se transmitan, más personalizadas serán las recomendaciones. El descuento de impresiones se aplicará a los elementos de arranque en frío cuando los registros de los usuarios nuevos incluyan datos de las impresiones.	|
|putEvent con un usuario nuevo	|Clasificación personalizada	|La personalización comienza después del primer evento, pero será más visible después de 2 a 5 eventos con 1 a 2 segundos de retraso después de la llamada de PutEvents después del registro de cada evento.	|-	|Recomendaciones personalizadas	|Cuando se utiliza la clasificación personalizada, en muchos casos es más difícil ver el impacto directo de los registros de putEvents, ya que se vuelve a clasificar una lista seleccionada que suministra el cliente (en comparación con la personalización del usuario, donde las recomendaciones se generan a partir del vocabulario completo de los elementos en el catálogo en función de las características de metadatos o comportamiento del modelo aprendido y el historial de interacción del usuario).	|
|putEvent con un usuario nuevo	|SIMS	|-	|-	|Se incluye en el modelo para generar las recomendaciones	|En verdad, SIMS no realiza la personalización, por lo que en el contexto de los usuarios nuevos que se agregan con PutEvents, los eventos de un usuario nuevo se consideran en las recomendaciones de elementos similares solo después de reentrenamiento.	|
|putUser	|Personalización del usuario	|-	|-	|Recomendaciones personalizadas	|Los usuarios agregados con putUser serán usuarios intermedios en función de la combinación de su historial de interacción conocido y su userID después del siguiente reentrenamiento completo.	|
|putUser	|Clasificación personalizada	|-	|-	|Recomendaciones personalizadas	|Los usuarios agregados con putUser serán usuarios intermedios en función de la combinación de su historial de interacción conocido y su userID después del siguiente reentrenamiento completo.	|
|putUser	|SIMS	|-	|-	|Sin efecto	|En verdad, SIMS no realiza la personalización, por lo que en el contexto de los usuarios nuevos que se agregan con PutUsers, los eventos de un usuario nuevo se consideran en las recomendaciones de elementos similares solo después de reentrenamiento.	|
|putItem	|Personalización del usuario	|-	|Aparecen como elementos de arranque en frío elegibles en función del límite de tiempo de análisis cuando el mismo ya está activado.	|Recomendaciones personalizadas	|Para los elementos nuevos o de arranque en frío, las recomendaciones se personalizan en función del historial de interacción del usuario y de los metadatos de este tipo de elementos. Los elementos de arranque en frío (elegibles en función del límite de tiempo de análisis cuando el mismo ya está activado) se incluirán durante la próxima actualización. Los elementos de arranque en frío se actualizarán de forma automática en función del descuento de impresiones de la interacción generada durante el análisis. Esta ponderación no es lineal y se combina con las características basadas en los metadatos, pero los elementos de arranque en frío que son menos populares (proporcionados en el campo de impresiones a través de putEvents) recibirán menos ponderación de análisis con el tiempo.	|
|putItem	|Clasificación personalizada	|-	|-	|Personalizado solo después de algunas interacciones	|-	|
|putItem	|SIMS	|-	|-	|Se incluyen interacciones nuevas en el modelo para generar recomendaciones de elementos similares basadas en la coocurrencia.	|En verdad, SIMS no realiza la personalización, por lo que en el contexto de los usuarios nuevos que se agregan con PutEvents, los eventos de un usuario nuevo se consideran en las recomendaciones de elementos similares solo después de reentrenamiento.	|

## Enlaces de habilitación técnica:

1. Ejemplos generales: https://github.com/aws-samples/amazon-personalize-samples
2. Introducción: https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started
3. POC in a Box 2.0: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/workshops/POC_in_a_box
4. Cuadernos basados en casos de uso: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/core_use_cases
5. Herramientas de ciencia de datos: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/data_science
6. MLOps para Personalize: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops
7. Supervisión, alertas y optimización de costos: https://github.com/aws-samples/amazon-personalize-monitor

## Demostraciones y talleres:

* Medios y entretenimiento
    * Unicorn Flix
        * Instancia en ejecución: [https://unicornflix.amplify-video.com](https://unicornflix.amplify-video.com/)
* Minorista
    * Tienda de demostración minorista
        * Fuente: https://github.com/aws-samples/retail-demo-store
        * Talleres: https://github.com/aws-samples/retail-demo-store#hands-on-workshops
        * Instancia en ejecución: [http://retaildemostore.jory.cloud/](http://retaildemostore.jory.cloud/#/)

## Socios tecnológicos:

Existen varios socios tecnológicos que ofrecen funcionalidades complementarias a Personalize que pueden acelerar la llegada a la etapa de producción con Personalize o mejorar el ROI de la implementación de la personalización con Personalize.

### Plataformas de datos de clientes: Recopilación de eventos y activación de recomendaciones

**Segment** es una [plataforma de datos de clientes](https://en.wikipedia.org/wiki/Customer_data_platform). Son un socio tecnológico avanzado de AWS y cuentan con las competencias de [experiencia digital del cliente](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) y de [venta minorista](https://aws.amazon.com/retail/partner-solutions/).

Segment ayuda a los clientes con Personalize de las siguientes formas:

* Recopilación de eventos: esta es una capacidad central de Segment. Los clientes utilizan Segment para recopilar los eventos de secuencias de clics en su aplicación web, aplicaciones móviles y otras integraciones. Estos eventos se recopilan, se validan y se distribuyen en destinos posteriores configurados por el cliente. Uno de estos destinos es Amazon Personalize.
* Resolución de la identidad del perfil del cliente o usuario: como Segment ve los eventos en todos los canales de los usuarios de un cliente, puede crear un perfil de cliente unificado. Este perfil o identidad es clave para poder ofrecer una personalización omnicanal.
* Activación a través de otras herramientas de marketing de una organización: como Segment permite a los clientes establecer conexiones con otras herramientas de marketing, adjuntar recomendaciones personalizadas de Personalize a los perfiles en Segment permite a los clientes y a los socios posteriores aprovechar esas recomendaciones en sus herramientas.

**Recursos**

* Video del CTO de Segment: https://www.youtube.com/watch?v=LQSGz8ryvXU
* Publicación en el blog: https://segment.com/blog/introducing-amazon-personalize/
* Talleres de AWS y Segment
    * Eventos de personalización en tiempo real: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-5-Real-time-events-Segment.ipynb
    * Plataformas de datos de clientes y Personalize: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.1-Segment.ipynb
    * Segment/Personalize (taller heredado): https://github.com/james-jory/segment-personalize-workshop
* Documentación: https://segment.com/docs/connections/destinations/catalog/amazon-personalize/

**mParticle** es una plataforma de datos de clientes. Son un socio tecnológico avanzado de AWS y cuentan con las competencias de [experiencia digital del cliente](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) y de [venta minorista](https://aws.amazon.com/retail/partner-solutions/).

mParticle ayuda a los clientes con Personalize de las siguientes formas:

* Recopilación de eventos: esta es una capacidad central de mParticle. Los clientes utilizan mParticle para recopilar los eventos de secuencias de clics en su aplicación web, aplicaciones móviles y otras integraciones. Estos eventos se recopilan, se validan y se distribuyen en destinos posteriores configurados por el cliente.
* Resolución de la identidad del perfil del cliente o usuario: como mParticle ve los eventos en todos los canales de los usuarios de un cliente, puede crear un perfil de cliente unificado. Este perfil o identidad es clave para poder ofrecer una personalización omnicanal.
* Activación a través de otras herramientas de marketing de una organización: como mParticle permite a los clientes establecer conexiones con otras herramientas de marketing, adjuntar recomendaciones personalizadas de Personalize a los perfiles en mParticle permite a los clientes y a los socios posteriores aprovechar esas recomendaciones en sus herramientas.

**Recursos**

* Talleres de AWS y mParticle
    * Eventos de personalización en tiempo real: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-6-Real-time-events-mParticle.ipynb
    * Plataformas de datos de clientes y Personalize: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.2-mParticle.ipynb

### Análisis, medición y experimentación

**Amplitude** es un socio tecnológico avanzado de AWS y cuenta con competencias de [experiencia digital del cliente](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX).
Amplitude ayuda a los clientes con Personalize de las siguientes formas:

* Información del producto: Amplitude proporciona visibilidad de los tipos de eventos que conducen a la conversión mediante un sofisticado análisis del embudo. Esto proporciona la información que los clientes necesitan para optimizar su taxonomía de eventos y seleccionar los eventos y campos de metadatos adecuados para entrenar los modelos en Personalize.
* Evaluación de pruebas A/B: Amplitude ofrece mediciones en línea de las pruebas A/B que pueden ser representadas por las experiencias personalizadas de los clientes con tecnología de Personalize.

**Recursos**

* Taller: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.5-Amplitude-Performance-Metrics.ipynb
* Publicación en el blog: https://aws.amazon.com/blogs/apn/measuring-the-effectiveness-of-personalization-with-amplitude-and-amazon-personalize/

**Optimizely** es una plataforma de pruebas A/B líder en el mercado. Es un socio tecnológico avanzado de AWS y cuenta con competencias de [experiencia digital del cliente](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX).

Optimizely ayuda a los clientes con Personalize de las siguientes formas:

* Resultados de las pruebas A/B: una de las principales ofertas de Optimizely es la medición y la elaboración de informes de experimentos como las técnicas de personalización.
* Marcado de las características: habilitar y deshabilitar las experiencias personalizadas

**Recursos**

* Taller: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.6-Optimizely-AB-Experiment.ipynb

### Mensajería

**Braze** es una plataforma de mensajería líder en el mercado (email, push, SMS). Son un socio tecnológico avanzado de AWS y cuentan con las competencias de [experiencia digital del cliente](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) y de [venta minorista](https://aws.amazon.com/retail/partner-solutions/).

Braze ayuda a los clientes con Personalize de las siguientes formas:

* Envía mensajes personalizados a los clientes en los canales de comunicación adecuados a través de una integración en tiempo real o por lotes.

**Recursos**

* Documentación de Braze: https://www.braze.com/docs/partners/data_augmentation/recommendation/amazon_personalize/
* Publicación en el blog de AWS ML: https://aws.amazon.com/blogs/machine-learning/optimizing-your-engagement-marketing-with-personalized-recommendations-using-amazon-personalize-and-braze/
* Publicación en el blog de los servicios multimedia de AWS: https://aws.amazon.com/blogs/media/speed-relevance-insight-how-streaming-services-can-master-effective-content-discovery-and-engagement/
* Taller: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/4-Messaging/4.2-Braze.ipynb

### Integraciones directas

**Magento 2**: Un socio de Magento y AWS llamado Customer Paradigm desarrolló una extensión de Magento 2. Adobe Magento NO desarrolló la extensión.

La extensión puede instalarse con facilidad en cualquier tienda de Magento 2, ya sea que se ejecute en las instalaciones, en otro proveedor de nube o en AWS. Siempre se accede a Amazon Personalize en la cuenta de AWS del cliente.

**Recursos**

* Sitio web del socio: https://www.customerparadigm.com/amazon-personalize-magento/
* Tienda de Magento: https://marketplace.magento.com/customerparadigm-amazon-personalize-extension.html


**Shopify:** [Obviyo](https://www.obviyo.com/) (antes conocido como HiConversion) creó una integración administrada con Personalize para las tiendas de Shopify. Esto significa que Obviyo administra Personalize en su entorno de AWS y los comerciantes de Shopify pagan a Obviyo por las capacidades de personalización con tecnología de Personalize.

**Recursos**

* Sitio web del socio: https://www.obviyo.com/

**WooCommerce (BETA):** [WP-Engine](https://wpengine.com/) creó una integración de Personalize en el complemento de AWS para WordPress que permite agregar recomendaciones de productos de Personalize a un sitio de WooCommerce en solo unos clics.

**Recursos**

* Página de recursos de WP-Engine: https://wpengine.com/resources/webinar-amazon-com-personalization-for-your-woocommerce-store/
