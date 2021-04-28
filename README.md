# TP1-RIT

El objetivo un sistema que permita realizar consultas de texto en archivos (documentos) que se encuentran almacenados recursivamente bajo un directorio dado, por lo tanto, se va a tener que elaborar 3 herramientas: 
Una herramienta que índice la colección
Una herramienta que permita procesar consultas
Una herramienta que permita explorar los archivos generados por la primera herramienta

##### Indización

La primera herramienta procesa los documentos de una colección dada (directorio) y crea un conjunto de archivos que permite realizar las búsquedas posteriores (índice). Esta herramienta debe calcular y almacenar toda la información necesaria para implementar el modelo BM25.
Los archivos creados den ser almacenados en disco. Esto es, el resultado de la indización no debe perderse al terminar la ejecución de esta herramienta; no es aceptable que solo exista en memoria.

Para cada término de la colección contiene una línea con la siguiente información:
	término
	ni (cantidad de documentos distintos en los que aparece)
valor idfi usado en BM-25:
	〖idf〗_i=∙〖log〗_2 (((N-n_i-0.5))⁄((n_i-0.5) ))
si ni aparece en más de la mitad de los documentos este valor sería negativo, poner un cero en su lugar.

##### Busqueda

La segunda herramienta del sistema realiza consultas tomando como base los archivos generados anteriormente.  Las consultas consisten de una lista de términos (los cuales pueden repetirse); por ejemplo:
	compresión de archivos y manejo de archivos comprimidos

Las consultas serán procesadas usando el modelo probabilístico Okapi BM25. Esto es, se usará la siguiente función de similitud.
Dada una consulta Q con términos q1, ..., qn, y un documento D
sim(D,Q)=∑_(i=1)^n(〖IDF(q_i )∙(f(q_i,D)∙(k+1))/(f(q_i,D)+k∙(1-b+b∙|D|/avgdl) )〗)
donde
	f(qi,D) es la frecuencia con que aparece el término qi en el documento D
	|D| es la longitud del documento D en palabras (suma de las frecuencias de sus términos)
	avgdl es la longitud promedio de los documentos de la colección
	k es un parámetro que calibra la escala de la frecuencia del término qi en el documento D
k=0, sería frecuencia binaria (0 si no aparece, 1 si aparece sin importar las veces)
k grande, se usa la frecuencia cruda sin ninguna escala
Usualmente se toma k  [1.2, 2.0], se usará k=1.2.
	b es otro parámetro, 0≤b ≤1, determina la escala de la longitud del documento
b=1 corresponde a normalizar completamente usando la longitud del documento
b=0 corresponde a no normalizar, no tomar en cuenta la longitud del documento
Se tomará b=0.75.

Para IDF(qi) se usará la siguiente fórmula:
IDF(q_i )=log (N-n_i+0.5)/(n_i+0.5)
donde
N es el número total de documentos de la colección
ni es el número de documentos de la colección que contienen el término qi.

Esta fórmula de problemas si un término aparece en más de la mitad de los documentos de la colección (el logaritmo se vuelve negativo). Por eso, se deben descartar de la consulta aquellos términos que aparezcan en más de la mitad de los documentos de la colección. 


##### Salida

Cada consulta debe producir dos archivos de salida:
•	Un archivo con el escalafón completo del resultado de la consulta. Esto es, un archivo de texto que para todos los documentos con similitud mayor que cero, contenga una línea con la posición en el escalafón, el identificador del documento y el valor de similitud obtenido por ese documento. Este archivo debe venir ordenado descendentemente por similitud.
•	Un archivo HTML que para cada uno de los primeros documentos del escalafón incluya su posición en el escalafón, la similitud con la consulta y su ruta. Además, para cada documento se deben listar los primeros 200 caracteres que aparecen después de la línea que dice “DESCRIPCIÓN”; antes de contar los 200 caracteres, se deben reemplazar los cambios de línea por un espacio en blanco y se deben consolidar dos o más espacios en blanco en uno solo. El usuario debe tener la posibilidad de poder la cantidad de documentos que se muestran en la página HTML.

##### Herramienta de inspección

Se debe desarrollar una herramienta que permita inspeccionar los archivos creados. En particular, debe proveer la siguiente funcionalidad:
•	Si se le da a la herramienta un índice y el nombre de un documento (por ejemplo, chown.2) la herramienta mostraría toda la información almacenada en ese índice para ese documento: términos, frecuencias, pesos, norma, longitud, etc. 
•	Por otro lado, si se le da a la herramienta un índice y un término (por ejemplo, memoria), la herramienta mostraría toda la información almacenada en ese índice para ese término: ni, idfi. y para sus términos vecinos: los 5 anteriores y los 5 posteriores. (Los términos deben estar ordenados alfabéticamente)


## Installation

Es necesario instalar la biblioteca “tabulate” para poder ejecutar el programa, dicha biblioteca se puede instalar con el siguiente comando:
A continuación, se van a mencionar las instrucciones para ejecutar los programas:

Primero, es necesario instalar la biblioteca “tabulate” para poder ejecutar el programa; esta se utiliza para tabular o formatear los datos, de modo que se puedan visualizar la información solicitada de manera ordenada. Dicha biblioteca se puede instalar con el siguiente comando:


pip install tabulate

Al haber finalizado la instalación de la biblioteca “tabulate”, se debe ejecutar el siguiente comando en una terminal.

python main.py -sw .\stopwords.txt

Donde:

.\stopwords.txt representa el archivo donde se encuentran las palabras no significativas.
