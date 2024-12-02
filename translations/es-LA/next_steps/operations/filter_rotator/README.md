# Rotación de filtro de Amazon Personalize

Este proyecto contiene el código fuente y los archivos de respaldo para implementar una aplicación sin servidor que ofrece capacidades de rotación automática de [filtro](https://docs.aws.amazon.com/personalize/latest/dg/filter.html) de [Amazon Personalize](https://aws.amazon.com/personalize/), un servicio de inteligencia artificial de AWS que permite crear recomendadores personalizados de ML en función de sus datos. Los aspectos destacados del proyecto incluyen lo siguiente:

- Creación de filtros basados en una plantilla de denominación de filtros dinámica provista por usted
- Creación de expresiones de filtro basadas en una plantilla de expresión de filtro dinámica provista por usted
- Eliminación de filtros basados en una expresión de compatibilidad dinámica provista por usted (opcional)
- Publicación de eventos en [Amazon EventBridge](https://aws.amazon.com/eventbridge/) cuando se crean o se eliminan filtros (opcional)

## <a name='Whatarefilters'></a>¿Qué son los filtros?
Los filtros de Amazon Personalize son una buena forma para lograr que se apliquen las reglas empresariales a las recomendaciones antes de ser devueltas a su aplicación. Se pueden utilizar para incluir o excluir elementos de las recomendaciones para un usuario en base a una sintaxis similar a SQL que considera el historial de interacciones del usuario, los metadatos de los elementos y los metadatos del usuario. Por ejemplo, para insertar el widget “Ver otra vez”, los filtros solo recomiendan películas que el usuario haya visto o haya tenido como favoritas en el pasado.

```
INCLUDE ItemID WHERE Interactions.event_type IN ('watched','favorited')
```

O excluyen de las recomendaciones a aquellos productos de los que actualmente no hay stock.

```
EXCLUDE ItemID WHERE Items.out_of_stock IN ('yes')
```

Hasta puede utilizar filtros dinámicos cuando los valores de las expresiones de filtros se especifican en el tiempo de ejecución. Por ejemplo, solo recomiendan películas para un género específico.

```
INCLUDE ItemID WHERE Items.genre IN ($GENRES)
```

Para utilizar el filtro anterior, debería pasar el valor adecuado para la variable `$GENRE` al momento de recuperar recomendaciones mediante la [API GetRecommendations](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html).

Puede obtener más información sobre los filtros en el blog de AWS Personalize [aquí](https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) y [aquí](https://aws.amazon.com/blogs/machine-learning/amazon-personalize-now-supports-dynamic-filters-for-applying-business-rules-to-your-recommendations-on-the-fly/).

## <a name='Whyisfilterrotationnecessary'></a>¿Por qué es necesaria la rotación de filtros?
¡Los filtros son geniales! Sin embargo, estos tienen algunas limitaciones. Una de esas limitaciones es poder especificar un valor dinámico para una consulta de rango (es decir, `<`, `<=`, `>`, `>=`). Por ejemplo, **no** se admite el siguiente filtro para limitar recomendaciones para nuevos elementos que se crearon desde un punto de desplazamiento en el pasado.

**¡ESTO FUNCIONARÁ!**
```
INCLUDE ItemID WHERE Items.creation_timestamp > $NEW_ITEM_THRESHOLD
```

La solución para esta limitación es utilizar una expresión de filtro con un valor preprogramado para las consultas de rango.

**¡ESTO SÍ FUNCIONA!**
```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

Sin embargo, no es muy flexible o sostenible ya que el tiempo avanza pero la expresión de filtro no. La solución alternativa es actualizar la expresión de filtro de forma regular para mantener un periodo de desplazamiento en el tiempo. Desafortunadamente, los filtros no se pueden actualizar, por lo que se debe crear un filtro nuevo, la aplicación debe pasar a utilizar el nuevo filtro y solo así se puede eliminar el filtro anterior de forma segura.

La finalidad de esta aplicación sin servidor es hacer que el mantenimiento de este proceso sea más sencillo mediante la automatización de la creación y la eliminación de filtros y permitir que proporcione una expresión dinámica que se resuelva en el valor preprogramado adecuado cuando se crea un nuevo filtro.

## <a name='Hereshowitworks'></a>Funcionamiento

Esta aplicación implementa una [función](./src/filter_rotator_function/filter_rotator.py) de AWS Lambda a la que invoca de forma periódica. Usted controla el programa que puede ser una [expresión cron o rate](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html). La función solo creará un nuevo filtro si no existe un filtro que coincida con la plantilla de nombre de filtro actual y solo eliminará los filtros existentes que coincidan con la plantilla de eliminación. Por lo tanto, está bien que la función se ejecute con mayor frecuencia que la necesaria (es decir, si no cuenta con una hora predecible o coherente para la rotación de filtros).

La clave para la función de rotación de filtros son las plantillas utilizadas para verificar que la plantilla actual existe y si las plantillas existentes son aptas para su eliminación. Debido a que las plantillas se resuelven cada vez que la función se ejecuta, el valor resuelto puede cambiar con el tiempo. Veamos algunos ejemplos. Usted proporciona estos valores de la plantilla como parámetros de CloudFormation cuando implementa esta aplicación.

### <a name="Currentfilternametemplate"></a>Plantilla de filtro de nombre actual

Supongamos que desea utilizar un filtro que solo recomienda elementos que se crearon recientemente. La columna `CREATION_TIMESTAMP` en el conjunto de datos de los elementos es un campo adecuado para este propósito. Este nombre de columna está reservado y se utiliza para admitir la característica de exploración del elemento frío de la receta `aws-user-personalization`. Los valores de esta columna se deben expresar en el formato de marca temporal de Unix como `long` (es decir, la cantidad de segundos desde la época). Los siguientes son elementos de los límites de la expresión de filtro creados el mes pasado (`1633240824` es la marca temporal de Unix de hace 1 mes desde esta escritura).

```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

De forma opcional, puede utilizar la columna de metadatos personalizados para el filtro que utiliza un formato más burdo o legible para humanos, pero que aún es comparable para consultas de rango, como `YYYYMMDD`.

```
INCLUDE ItemID WHERE Items.published_date > 20211001
```

Como se observó anteriormente, no se puede actualizar los filtros. Por lo tanto, no puede simplemente modificar la expresión de filtro de un filtro. En cambio debe crear un nuevo filtro con una nueva expresión, modificar la aplicación para que utilice un nuevo filtro y luego elimine el antiguo. Esto requiere el uso de un estándar de nomenclatura predecible para filtros para que las aplicaciones puedan pasar a utilizar el nuevo filtro de forma automática sin necesidad de un cambio de código. Para continuar con el tema de la creación de una marca temporal, el nombre del filtro podría ser algo como:

```
filter-include-recent-items-20211101
```

Supongamos que queremos rotar este filtro todos los días, el nombre del filtro para el día siguiente sería `filter-include-recent-items-20211004`, el siguiente sería `filter-include-recent-items-20211005`, y así consecutivamente a medida que pasa el tiempo. Debido a que existen límites acerca de la cantidad de filtros activos que puede tener en cualquier momento, no puede crear una gran cantidad de filtros con anterioridad. En cambio, esta aplicación creará nuevos filtros de forma dinámica según sea necesario y eliminará los antiguos cuando corresponda. Lo que hace que esto funcione son las plantillas que define para el nombre y la expresión de filtro y que se resuelven en tiempo de ejecución. A continuación, podemos ver un ejemplo de una plantilla de nombre de filtro que coincide con el esquema que se describe anteriormente.

```
filter-include-recent-items-{{datetime_format(now,'%Y%m%d')}}
```

La plantilla de nombre de filtro anterior resolverá y reemplazará la expresión dentro de los caracteres `{{` y `}}` (llaves) en el tiempo de ejecución. En este caso, tomamos el tiempo actual expresado como `now` y lo formateamos mediante la expresión de formato de fecha `%Y%m%d`. El resultado (a partir de hoy) es `20211102`. Si la función de rotación encuentra un filtro existente con este nombre, no es necesario crear un nuevo filtro. De lo contrario, se crea un nuevo filtro que utiliza `filter-include-recent-items-20211102` como nombre.

El parámetro `PersonalizeCurrentFilterNameTemplate` de la plantilla de CloudFormation es la forma de especificar su propia plantilla de nombre de filtro personalizada.

A continuación, se describen las funciones y los operadores disponibles para su uso en la plantilla de sintaxis.

### <a name="Currentfilterexpressiontemplate"></a>Plantilla de la expresión de filtro actual

A veces, cuando se rota y crea un nuevo filtro, también debemos resolver la expresión de filtro actual de forma dinámica. El parámetro `PersonalizeCurrentFilterExpressionTemplate` de CloudFormation se puede utilizar para esto. Veamos algunos ejemplos.

```
INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > {{int(unixtime(now - timedelta_days(30)))}}
```

```
INCLUDE ItemID WHERE Items.published_date > {{datetime_format(now - timedelta_days(30),'%Y%m%d')}}
```

Las plantillas anteriores se resuelven en una expresión de filtro preprogramada basada en el tiempo actual al momento de ser resueltas. La primera produce una marca temporal de Unix (expresada en segundos como lo requiere Personalize para `CREATION_TIMESTAMP`) de hace 30 días. La segunda plantilla produce un entero que representa la fecha en formato `YYYYMMDD` de hace 30 días.

### <a name="Deletefiltermatchtemplate"></a>Eliminación de la plantilla de coincidencia de filtros

Por último, debemos limpiar los filtros antiguos luego de haberlos pasado a una versión más reciente del filtro. De lo contrario, nos encontraremos con un límite eventualmente. Una plantilla de coincidencia de nombres de filtros se puede utilizar para este propósito y se la puede escribir de forma tal que retrase la eliminación por un tiempo luego de que se crea el nuevo filtro. Esto le da tiempo a la aplicación para pasar del antiguo filtro al nuevo filtro antes de que se elimine el antiguo filtro. El parámetro `PersonalizeDeleteFilterMatchTemplate` de la plantilla de CloudFormation es donde usted especifica la plantilla de eliminación de coincidencias de filtros.

La siguiente plantilla de eliminación de coincidencias de filtros hará coincidir los filtros con los nombres de filtros que comiencen con `filter-include-recent-items-` y tengan un sufijo de más de un día anterior al actual. En otras palabras, tenemos 1 día para pasar las aplicaciones del cliente al nuevo filtro antes de que se elimine el antiguo filtro. Esto se puede personalizar para que se adecúe a su aplicación.

```
starts_with(filter.name,'filter-include-recent-items-') and int(end(filter.name,8)) < int(datetime_format(now - timedelta_days(1),'%Y%m%d'))
```

Se eliminarán todos los filtros que causen que esta plantilla resuelva como `true`. Los demás no serán modificados. Tenga en cuenta que todos los campos en [FilterSummary](https://docs.aws.amazon.com/personalize/latest/dg/API_FilterSummary.html) de la respuesta [de la API ListFilters](https://docs.aws.amazon.com/personalize/latest/dg/API_ListFilters.html) están disponibles para esta plantilla. Por ejemplo, la plantilla anterior coincide con `filter.name`. Además, puede revisar otros campos de resumen, como por ejemplo `filter.status`, `filter.creationDateTime` y `filter.lastUpdatedDateTime` en la lógica de la plantilla.

## <a name='Filterevents'></a>Filtro de eventos

Si desea sincronizar la configuración de la aplicación o recibir notificaciones cuando se crea o se elimina un filtro, puede configurar, de forma opcional, la función de rotación para publicar eventos en [Amazon EventBridge](https://aws.amazon.com/eventbridge/). Cuando se habilitan los eventos, la función de rotación pública tres tipos de detalles de eventos: `PersonalizeFilterCreated`, `PersonalizeFilterCreateFailed` y `PersonalizeFilterDeleted`. Cada uno tiene un evento `Source` de `personalize.filter.rotator` e incluye detalles acerca del filtro creado o eliminado. Esto permite configurar las reglas de EventBridge para procesar eventos según lo desee. Por ejemplo, cuando se crea un nuevo filtro, puede procesar el evento `PersonalizeFilterCreated` en una función de Lambda para actualizar la configuración de la aplicación de forma que pase a utilizar el nuevo filtro en las llamadas de inferencia.
## <a name='Filtertemplatesyntax'></a>Plantilla de sintaxis de filtros

La biblioteca [Simple Eval](https://github.com/danthedeckie/simpleeval) se utiliza como la base de la plantilla de sintaxis. Esta proporciona una alternativa más segura y blindada que el uso de la función [eval](https://docs.python.org/3/library/functions.html#eval) de Python. Para obtener más información sobre las funciones disponibles y los ejemplos, consulte la documentación de la biblioteca Simple Eval.

Las siguientes funciones adicionales se agregaron como parte de esta aplicación para lograr que la escritura de plantillas para la rotación de filtros sea más sencilla.

- `unixtime(value)`: devuelve el valor de marca temporal de Univex otorgado a una cadena, formato datetime, fecha u hora. Si se proporciona una cadena, primero se la analiza en el formato datetime.
- `datetime_format(date, pattern)`: establece un formato datetime, fecha u hora mediante el patrón específico.
- `timedelta_days(int)`: devuelve un formato timedelta para una cierta cantidad de días. Se puede utilizar para aritmética de fechas.
- `timedelta_hours(int)`: devuelve un formato timedelta para una cierta cantidad de horas. Se puede utilizar para aritmética de fechas.
- `timedelta_minutes(int)`: devuelve un formato timedelta para una cierta cantidad de minutos. Se puede utilizar para aritmética de fechas.
- `timedelta_seconds(int)`: devuelve un formato timedelta para una cierta cantidad de segundos. Se puede utilizar para aritmética de fechas.
- `starts_with(str, prefix)`: devuelve True (Verdadero) si el valor de la cadena comienza con un prefijo.
- `ends_with(str, suffix)`: devuelve True (Verdadero) si el valor de la cadena termina con un sufijo.
- `start(str, num)`: devuelve los caracteres first num del valor de la cadena.
- `end(str, num)`: devuelve los caracteres last num del valor de la cadena.
- `now`: formato datetime actual.

## <a name='Installingtheapplication'></a>Instalación de la aplicación

***NOTA IMPORTANTE:** La implementación de esta aplicación en la cuenta de AWS creará y consumirá recursos, lo que costará dinero. Se invoca a la función de Lambda según el programa que proporcione, pero normalmente no debería ser necesario invocarla más de una vez por hora. Personalize no cobra los filtros, pero su cuenta tiene un límite para la cantidad de filtros que están activos en cualquier momento. También existen límites para la cantidad de filtros que pueden estar en estado pendiente o en progreso en un momento determinado. Por lo tanto, si luego de instalar esta aplicación elije no utilizarla como parte de la solución, asegúrese de seguir las instrucciones de Desinstalación en la siguiente sección para evitar los cargos recurrentes y borrar todos los datos.*

Esta aplicación utiliza el [Modelo de aplicación sin servidor](https://aws.amazon.com/serverless/sam/) (SAM) de AWS para crear e implementar recursos en la cuenta de AWS.

Para utilizar la CLI de SAM, necesita tener las siguientes herramientas instaladas localmente.

* CLI de SAM - [Instalación de la CLI de SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 instalado](https://www.python.org/downloads/)
* Docker - [Instalación de la edición comunitaria de Docker](https://hub.docker.com/search/?type=edition&offering=community)

Para crear e implementar la aplicación por primera vez, ejecute lo siguiente en la shell:

```bash
sam build --use-container --cached
sam deploy --guided
```

Si recibe un mensaje de error del primer comando indicando que no se puede descargar la imagen Docker desde `public.ecr.aws`, quizá deba iniciar sesión. Ejecute el siguiente comando y luego vuelva a intentar con los dos comandos anteriores.

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

El primer comando creará el origen de la aplicación. El segundo comando empaquetará e implementará la aplicación en la cuenta de AWS con una serie de instrucciones:

| Instrucción/Parámetro | Descripción | Predeterminado |
| --- | --- | --- |
| Nombre de pila | El nombre de pila para que se implemente en CloudFormation. Esto debería ser propio de la cuenta y de la región. | `personalize-filter-rotator` |
| Región de AWS | La región de AWS en la que desea implementar esta aplicación. | La región actual |
| Parámetro PersonalizeDatasetGroupArn | ARN del grupo de conjunto de datos de Amazon Personalize para rotar los filtros. | |
| Parámetro PersonalizeCurrentFilterNameTemplate | Plantilla útil para verificar y crear el filtro actual. | |
| Parámetro PersonalizeCurrentFilterExpressionTemplate | Plantilla útil para crear la expresión de filtro cuando crea el filtro actual. | |
| Parámetro PersonalizeDeleteFilterMatchTemplate (optativo) | Plantilla útil para hacer coincidir los filtros existentes que se deberían eliminar. | |
| Parámetro RotationSchedule | Expresión cron o rate para controlar la frecuencia con la que se invoca a la función de rotación. | `rate(1 day)` |
| Parámetro Timezone | Configure la zona horaria de las funciones del rotador del entorno de Lambda para que coincidan con la suya. | `UTC` |
| Parámetro PublishFilterEvents | Para publicar eventos en el bus predeterminado de EventBridge cuando se crean y se eliminan los filtros. | `Yes` |
| Confirme los cambios antes de llevar a cabo la implementación | Si configura la opción en Yes (Sí), cualquier cambio que haga en CloudFormation se mostrará antes de su ejecución para revisión manual. Si configura la opción en No, la CLI de AWS SAM implementará los cambios de la aplicación automáticamente. | |
| Permita la creación de roles de la CLI de AWS IAM | Debido a que la aplicación crea roles de IAM para permitir que las funciones de Lambda accedan a los servicios de AWS, esta configuración debe ser `Yes`. | |
| Guarde los argumentos en samconfig.toml | Si configura la opción en Yes (Sí), se guardarán sus elecciones en un archivo de configuración dentro de la aplicación para que en el futuro simplemente pueda volver a ejecutar `sam deploy` sin ningún parámetro para implementar cambios en la aplicación. | |

**SUGERENCIA**: La herramienta de línea de comando de SAM ofrece la opción de guardar los valores del parámetro en un archivo local (`samconfig.toml`) para que estén disponibles como predeterminados la próxima vez que implemente la aplicación. Sin embargo, SAM envuelve los valores del parámetro entre comillas dobles. Por lo tanto, si los valores de parámetro de la plantilla contienen valores de cadena integrados (por ejemplo, las expresiones de formato de fecha que se muestran en los ejemplos anteriores), asegúrese de utilizar comillas simples para esos valores integrados. De lo contrario, los valores de parámetros no se conservarán de manera adecuada.

## <a name='Uninstallingtheapplication'></a>Desinstalación de la aplicación

Para eliminar los recursos creados por esta aplicación en la cuenta de AWS, utilice la AWS CLI. Si suponemos que utilizó el nombre predeterminado de la aplicación para el nombre de pila (`personalize-filter-rotator`), puede ejecutar lo siguiente:

```bash
aws cloudformation delete-stack --stack-name personalize-filter-rotator
```

De forma alternativa, puede eliminar la pila en CloudFormation en la consola de AWS.

## <a name='FAQs'></a>Preguntas frecuentes

***P: ¿Cómo puedo modificar la frecuencia en la que se ejecuta el script rotador una vez que se implementa la solución?***

***R:*** En este caso existen dos opciones: volver a implementar esta solución con una frecuencia distinta. Se creará un conjunto de cambios que solo actualizará la regla de EventBridge con la frecuencia nueva. De lo contrario, puede editar la regla de EventBridge creada por esta solución directamente en la cuenta de AWS.

***P: ¿Cómo utilizo esta solución para rotar varios filtros con diferentes plantillas y diferentes frecuencias de actualización?***

***R:*** Una vez que implemente esta solución, puede crear reglas de EventBridge adicionales que llamen a la función del rotador con diferentes valores de entrada. Para la regla meta, seleccione la función de rotador y especifique un valor de entrada que sea constante de JSON en el siguiente formato:

```javascript
{
    "datasetGroupArn": "[INSERT_PERSONALIZE_DATASET_GROUP_ARN]",
    "currentFilterNameTemplate": "[INSERT_CURRENT_FILTER_NAME_TEMPLATE]",
    "currentFilterExpressionTemplate": "[INSERT_CURRENT_FILTER_EXPRESSION_TEMPLATE]",
    "deleteFilterMatchTemplate": "[INSERT_DELETE_FILTER_MATCH_TEMPLATE]"
}
```

## <a name='Licensesummary'></a>Resumen de la licencia

Este código de ejemplo está disponible por medio de una licencia MIT modificada. Consulte el archivo de la LICENCIA.
