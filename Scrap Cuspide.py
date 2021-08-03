from datetime import date
import mysql.connector
import requests
from bs4 import BeautifulSoup as BS

hoy = date.today()
hoy = str(hoy)


#Abro conexion con la base de datos

while True:
    host_1 = input('Ingrese el nombre del "host":  ')
    database_1 = input('Ingrese el nombre de la "database":  ')
    user_1 = input('Ingrese el "user":  ')
    password_1 = input('Ingrese la "password":  ')
    try:
        conexion = mysql.connector.connect(
                            host = host_1,
                            database = database_1,
                            user = user_1,
                            password = password_1)
        False
    except: print('Alguno de los datos es incorrecto, intente nuevamente.')

conexion.close()
            
while True:
    try:
        #Definir nombre de tabla
        nombre_tabla = ("Libros mas vendidos de la semana " + hoy)
        #Creat tabla
        
        cursor = conexion.cursor()
        sql = "CREATE TABLE `pdp_base003`.`"+nombre_tabla+"` \
            ( `Nombre_libro` VARCHAR(200) NOT NULL , `Precio_libro` FLOAT(10) NOT NULL , \
            `ID_libro` INT(8) NOT NULL AUTO_INCREMENT , PRIMARY KEY (`ID_libro`)) \
            ENGINE = InnoDB;"        
        cursor.execute(sql)
        False
    except: continue    
    
    #Extraigo el html del objetivo
    url = 'https://www.cuspide.com/cienmasvendidos'
    response = requests.get(url)
    response.encoding = 'utf-8'
    archivo_html = response.text
    dom = BS(archivo_html, features='html.parser')
    #Filtro los tag de la info que me interesa
    articles = dom.find_all('article')
    
    #Extraigo la informacion
    for libro in range(len(articles)):
        #filtro errores por falta de info
        try:
            #extraigo el nombre del libro
            atributo_title= articles[libro].figure.div.a['title']
            nombre_libro= atributo_title
            atributo_href= 'https://www.cuspide.com'+ articles[libro].figure.div.a['href']
            #Sacando link de cada libro
            url_libro= atributo_href 
            response_libro = requests.get(url_libro)
            response_libro.encoding = 'utf-8'
            archivo_html_libro= response_libro.text
            dom_libro = BS(archivo_html_libro, features='html.parser')
            #buscando el precio
            etiqueta_clase_precio = dom_libro.find_all('meta', itemprop='price')
            precio_meta = str(etiqueta_clase_precio)
            #Precio del libro
            pos = precio_meta.find('"')
            pos_final= precio_meta.find('" ')
            precio_libro = (precio_meta[pos+2:pos_final])
            precio_libro = precio_libro.replace('.','')
            precio_libro = precio_libro.replace(',','.')
            precio_libro = str(precio_libro)
            
            sql= "INSERT INTO `"+nombre_tabla+"` (`Nombre_libro`, `Precio_libro`, `ID_libro`) \
                VALUES ('"+nombre_libro+"', '"+precio_libro+"', NULL);"
            cursor.execute(sql)
            conexion.commit()     
        except: continue
            
    cursor.close()
    conexion.close()