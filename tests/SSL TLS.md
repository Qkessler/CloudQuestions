# SSL/TLS

Class: SSTT
Created: Apr 16, 2020 10:39 AM
Modified: Apr 22, 2020 12:04 PM
Reviewed: No

Estas son las preguntas de los 900 vídeos que tenemos del tema 9.

# Questions:

## Introducción:

- ¿Qué nos garantiza SSL?

    SSL supone que nos conectaremos al 443, SSL nos garantiza una protección mediante un tunel SSL, de forma que toda la información que se va a intercambiar va a ir protegida.

- ¿Cómo se identifican las entidades?

    Mediante certificados y claves asociadas.

- ¿Cómo funciona el intercambio SSL?

    Conexión TCP sobre el protocolo HTTPS(443)

    Hacemos entonces el handshake protocol, que nos da la información necesaria para crear el túnel:

    - Negociación de la suite criptográfica: materiales necesarios para cifrar la conexión.
    - Autenticación del servidor.
    - Autenticación del cliente. OPCIONAL
    - Negociar un secreto compartido, que es utilizado para proteger las comunicaciones.

    Después de este paso se hace el record protocol que es el intercambio de datos que nos interesaba.

## Protocolos Handshake - CCSP:

- ¿Qué otros protocolos pueden usar SSL?

    SMTP, FTP, POP3...

- ¿Qué es una suite criptográfica?

    Los diferentes algoritmos que vamos a usar para cifrar una conexión.

- ¿En qué se basa la primera fase del handshake?

    Cada una de las partes va a tener una tabla de sesión dónde guarda información acerca de la sesión. Se hace entonces una conexión HTTPS. Después el cliente hace su mensaje client_hello, en el que se incluye la información. Por último, el servidor envía un server_hello en el que envía la información como la versión que soporta el servidor, un server_random, un identifidor de sesión y una respuesta a la suite criptográfica. 

- ¿Qué contiene la tabla de sesión?
    - identificador de sesión.
    - Certificado de peer.
    - Método de compresión.
    - Especificación del algoritmo de cipher.
    - master_secret.
    - is_resumable.
- ¿Qué contiene una cipher_spec?

    PROTOCOLO_MÉTODO DE INTERCAMBIO DE CLAVE_ALGORITMO DE CIFRADO_TAMAÑO CLAVE DE CIFRADO_MODO DE CIFRADO DE BLOQUE_ALGORITMO MAC.

- ¿En qué se basa la segunda fase del handshake?

    El servidor envía su certificado y el cliente lo almacena en su tabla de sesión. El servidor envía el server_hello_done que es vacío. El cliente genera una master_secret.

- ¿En qué se basa la tercera fase del handshake?

    El cliente envía el mensaje client_key_exchange, dónde el cliente envía la clave generada cifrada con la clave pública del servidor, obtenida mediante el certificado.

- ¿Cómo se genera la master_secret_key?

    Se crea primero una pre_master_secret, a la que se aplican 3 operaciones de concatenación para llegar a la clave maestra derivada.

    La longitud de master_secret es 128*3 = 384bits.

- ¿En qué se basa la cuarta fase del handshake?

    El cliente envía un mensaje change cipher spec, en el que se indica al servidor que se use el material criptográfico negociado. Se crea una tabla de conexión en la que se encuentra los valores aleatorios generados por los mensajes hello, además de claves de probar identidad mediante MAC y claves de cifrado. Tenemos también un contador de secuencia.

    Por último, envía un mensaje finish para indicar que se termina el handshake.

    El servidor también envía un change cipher spec con los mismos valores, probando que conoce la clave privada. Además, envía un finish.

- ¿Cuáles son las siglas de CCSP?

    Change Cipher Spec Protocol.

- ¿Para qué vale CCSP?

    Intercambio de mensajes para decir que usamos los valores de criptografía negociados. Todos los siguientes mensajes ya están encriptados. Tiene un byte que fuera a actualizar los parámetros de cifrado si está a 1.

## Protocolo Record:

- ¿Cómo funciona el cifrado del record protocol?

    Se divide la petición en varias partes a las que les vamos a aplicar una serie de operaciones para llegar al Application Data.

- ¿Cuáles son las operaciones que se hacen a las peticiones y a las respuestas?

    En el orden siguiente.

    - Compresión.
    - Autenticación con K2.
    - Cifrado con K4 y vector de inicialización.
-