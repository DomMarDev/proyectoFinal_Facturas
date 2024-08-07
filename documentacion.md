# Documentación PreProyecto Domingo Marchan del Pino

## 1. Introducción

### Proyecto: FacturacionDM

### Descripción: una breve descripción del proyecto, sus objetivos y su importancia.

#### Descripción breve:

- El proyecto se basará en un programa que permita al usuario crear, de forma local (de momento), facturas para un negocio. Además, el usuario tendrá control sobre estas y las podrá modificar, eliminar, mostrar o buscar.

#### Objetivos:

1. Generar una interfaz agradable para el usuario y que asegure que sólo puede acceder a ella aquel que tenga credenciales. (Usuario: user, Contraseña: 1234)
2. Como mínimo se deberá poder generar facturas en formato PDF dados unos datos en formato json.
3. Además, se podrán eliminar las facturas, mostrarlas, modificarlas y tener una idea de cuanto se ha facturado.

#### Importancia:

Es un programa que facilita al usuario el realizar facturas con un formato estándar sin tener que preocuparse de desajustes en word. Será una herramienta sencilla y visual para que personas con bajo nivel en ofimática puedan realizar esta actividad con normalidad.

## 2. Requisitos

### Lista de requisitos: herramientas y bibliotecas necesarias para ejecutar el proyecto.

#### Librerías:

Persistencia = datos de una api los tenemos que guardar en un json o csv

    - Archivos: **JSON**, txt, CSV

    - Bases de datos (BBDD): SQlite

Analisis de datos con: Numpy, Pandas, **Matplotlib**



Aún podrían faltar o quitarse algunas librerías.

1) PIL / Pillow ->  poder ajustar imagenes (pip install Pillow)
2) datetime -> dar la fecha cuando se crea la factura y fecha límite de pago.
3) fpdf -> generador de archivo PDF ( pip install fpdf)
4) tkinter como interfaz (alomejor kivy en un futuro)
5) pathlib -> Necesario para la manipulación de rutas
6) os -> Obtener rutas del sistema operativo y abrir documentos
7) random -> generador de números aleatórios (no usada al final, pero podría usarse para generar números de facturas)
8) json -> manipulación de archivos json
9) Matplotlib -> Analisis de datos
10) webbrowser -> Incorporar la función de ir a la web de la empresa o al correo de esta
11) sys -> Necesario para que no haya errores a la hora de importar módulos
12) 

## 2. Diseño del proyecto:

### Descripción del diseño: una descripción de alto nivel de cómo se estructurará el código

#### Login screen:

Va a aparecer una ventana para que el usuario verifique sus credenciales ( de momento no quiero registrar usuarios).

Las credenciales por defecto serán:

- Usuario: user
- Contraseña: 1234

#### Menú principal:

Se muestra un menú donde clicando en los recuadros se podrán realizar las acciones de:

*1) Crear Factura

*2) Eliminar Factura

*3) Buscar Factura

*4) Mostrar Facturas

*5) Salir (esta de momento la dejo como opción, pero con cerrar la pestaña ya estaría hecho)

*6) Analítica datos: Balance facturas del mes o  Nº Facturas del mes

Se baraja la opción de incorporar un menú superior con las mismas funcionalidades u otras que por el momento no tengo pensadas.

##### Opción 1: Crear factura

Se piden los datos al usuario (Pedir), los demás vendrán configurados por defecto (a medida del usuario) o se rellenarán automáticamente. La interfaz gráfica hará visibles los campos rellenados por el usuario (en principio).

Datos presentes en una factura:

    * Logo empresa

    * Datos de la localización de la empresa:

    * calle/ localiz/ CP / TLF / C.I.F o NIF de la empresa / correo

    * Nombre empresa (Pedir)

    * Fecha factura (Pedir)

    * Cliente (Pedir)

    * DNI/NIF cliente (Pedir)

    * Datos de la localización del cliente: (Pedir)

    * calle/ localiz/ CP / TLF

    Tabla 1: (Pedir)

    * Unidades del elemento

    * Elementos de la factura

    * Precio del elemento

    * Precio total del elemento

    Tabla 2:

    * Importe Bruto

    * IVA % *

    * Base imponible

    * IVA *

    * Total Factura

    Tabla 3:

    * Fecha vencimiento factura (a 30 días después de la creación de la factura, pero he de mirar si quiero que sea a día 1 del siguiente més)

    * Forma de Pago

    * Banco

    * IBAN

Al acabar con la introducción de datos, el usuario podrá indicarlo mediante un botón de "Generar Factura" y se generará un PDF, con un nombre autogenerado. Además, se guardará dicho arvhivo en la carpeta de "PDF" previamente creada.

Todos los datos introducidos por el usuario se guardarán en un documento json autogenerado (con el nombre de la factura) que contendrá una lista de un diccionarios correspondiente a la factura. (aún no sé si voy a poder implementar una base de datos)

##### Opción 2: Eliminar factura

Se procederá a mostrar las facturas y se podrán eliminar dado un cliente y un código que se mostrará en pantalla que el usuario deberá de introducir. Si no introduce los datos de forma correcta se mostrará un mensaje.

Otra opción será abrir una ventana con todos los archivos PDF correspondientes a las facturas ya hechas y se podrá eliminar clicando y dandole a suprimir (tengo que darle una vuelta para que sea más fácil aún)

##### Opción 3: Buscar factura

Se mostrarán las facturas que hay en la base de datos y se podrán buscar según cliente y un código / número que aparecerá al lado de la factura.

Otra opción será abrir una ventana y realizar una búsqueda normal como siempre se ha hecho mediante windows (he de hacerlo más fácil incluso).

##### Opción 4: Mostrar facturas

Se mostrarán las facturas que hay en la base de datos (bien el directorio con los PDF, o las que constan en la base de datos de las facturas introducidas por el usuario en un formato json).

##### Opción 5: Salir

##### Opción 6: Analítica datos: Balance facturas del mes o  Nº Facturas del mes

Gestión de datos para que muestre el balance de las facturas del mes o bien el Nº de facturas hechas del mes.

## Diagrama de flujo aproximado de la ejecución del programa. Como mínimo del script principal y una de las funcionalidades.

Programa principal/Menú:

![1719507314727](image/documentacion/1719507314727.png)

![1719507361289](image/documentacion/1719507361289.png)

Verifciación user y pass:

![1719507388187](image/documentacion/1719507388187.png)

Crear PDF:

![1719507415117](image/documentacion/1719507415117.png)

![1719507439470](image/documentacion/1719507439470.png)

![1719507463485](image/documentacion/1719507463485.png)

![1719507507758](image/documentacion/1719507507758.png)

![1719507524803](image/documentacion/1719507524803.png)
