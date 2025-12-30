# Ejemplos de Lambda

Esta carpeta comienza con un ejemplo básico de integración de `put_events` en sus campañas de Personalize mediante el uso de funciones de Lambda que procesan datos nuevos desde S3.

Para comenzar, primero complete la recopilación de cuadernos `getting_started`, que incluyen el segundo cuaderno que crea su rastreador de eventos inicial.


## Envío de eventos a S3

Dentro de esta carpeta, verá el cuaderno `Sending_Events_to_S3.ipynb` que contiene el código estandarizado para enviar una serie de mensajes al bucket de S3.

Este paso será clave para utilizar la función de Lambda, que luego los enviará a Personalize.

## Función de Lambda

Ahora, el cuaderno escribirá archivos de manera fiable en el bucket de S3. La próxima tarea es crear una función de Lambda para invocar el desencadenador de S3. Dentro, se brinda el código para Lambda. `event_processor.py`


En primer lugar, visite la consola de Lambda y haga clic en `Create Function` (Crear función). Nombre la función como desee y seleccione Python 3.6 para el tiempo de ejecución.

Necesitará un rol de IAM nuevo para esta función de Lambda. En primer lugar, permita un rol predeterminado. Luego, se actualizará para trabajar con Personalize y S3. A continuación, seleccione `Create function`


Ahora, haga clic en `+ Add trigger` (Agregar desencadenador), busque S3, seleccione su bucket, seleccione `All object create events` (Todos los objetos crean eventos) para esta demostración y, luego, en la sección del sufijo, agregue `.json`. Por último, en esta página, haga clic en `Add`

A continuación, haga clic en el icono de su función de Lambda. En el editor que aparece a continuación, copie los contenidos de `event_processor.py` en este y guárdelo. Reemplace todos los contenidos existentes.

Desplácese hacia abajo en el editor y en `Environment Variables` (Variables del entorno), escriba la clave `trackingId`. En el valor, escriba su ID de rastreador del segundo cuaderno.

Ya casi está listo. El último paso es configurar IAM. Desplácese hacia abajo hasta `Execution role` (Rol de ejecución). Al final, verá el enlace `View the ....` (Ver…), haga clic derecho en el enlace y ábralo en una pestaña nueva.

Haga clic en `Attach policies` (Adjuntar políticas), agregue las políticas `AmazonS3FullAccess` y `AmazonPersonalizeFullAccess`, y haga clic en `Attach policy` (Adjuntar política). Si bien estas configuraciones no son ideales para la seguridad, servirán a modo de ilustración. Para una carga de trabajo de producción, cree políticas personalizadas que se adapten de manera explícita a los recursos con los que está trabajando.

Cuando adjunte las políticas, cierre la pestaña y regrese a la página de la consola de Lambda. Haga clic en `Save` (Guardar) en la esquina superior derecha.

Desplácese hacia arriba y seleccione `Monitoring` (Supervisión), luego, regrese al cuaderno que simula los eventos y ejecute esa celda nuevamente para escribir archivos nuevos y ejecutar la función de Lambda.

Después de unos segundos, puede actualizar la página y ver las invocaciones que se realizaron correctamente.
