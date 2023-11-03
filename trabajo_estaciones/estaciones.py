# Importar las bibliotecas necesarias
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, when, col
import json
import tkinter as tk

# Crear una sesión de Spark
spark = SparkSession.builder.appName("estaciones").getOrCreate()

# Definir las rutas de los archivos
ruta_datos = '/home/gjhosep/trabajo_estaciones/isd-history.csv'
ruta_json = '/home/gjhosep/trabajo_estaciones/resultFiltrado.json'

# Función de Spark que procesa la consulta del usuario
def procesar_consulta(texto):
    # Crear una lista con nombres de columnas para el DataFrame
    columnas_df = ["USAF", "WBAN", "STATION_NAME", "Country", "ST", "CALL", "Latitud", "Longitud", "ELEV", "BEGIN", "END"]

    # Leer el archivo en la ruta específica con SparkSession
    archivo = spark.read.csv(ruta_datos)

    # Cambiar el nombre de las columnas en el DataFrame
    archivo = archivo.toDF(*columnas_df)

    # Seleccionar las columnas de interés
    archivo = archivo.select(col('Country'), col('Latitud'), col('Longitud'))

    # Aplicar transformaciones necesarias en las columnas
    archivo = archivo.select(
        when(archivo.Country.isNull(), '0').otherwise(archivo.Country).alias('Country'),
        regexp_replace(when(archivo.Latitud.isNull() |
                            (archivo.Latitud == '+00.000') |
                            (archivo.Latitud == '+000.000'), '0.000').otherwise(archivo.Latitud), r'^\+', '').alias('Latitud'),
        regexp_replace(when(archivo.Longitud.isNull() |
                            (archivo.Longitud == '+00.000') |
                            (archivo.Longitud == '+000.000'), '00.000').otherwise(archivo.Longitud), r'^\+', '').alias('Longitud')
    )

    # Eliminar los ceros a la izquierda en las coordenadas, manteniendo el signo "-"
    archivo = archivo.withColumn("Longitud", regexp_replace("Longitud", "^(-)?0+(?!\\.)(?=\\d)", "$1"))
    archivo = archivo.withColumn("Latitud", regexp_replace("Latitud", "^(-)?0+(?!\\.)(?=\\d)", "$1"))

    # Filtrar los datos del país especificado
    query = archivo.filter(archivo['Country'] == texto)

    # Formato de datos para la conversión a JSON
    json_result = []
    for row in query.rdd.collect():
        json_data = {
            "country": row.Country,
            "latitude": row.Latitud,
            "longitude": row.Longitud
        }
        json_result.append(json_data)

    # Escribir en el archivo resultFiltrado.json
    with open(ruta_json, 'w') as f:
        f.write(json.dumps(json_result))
    query.show()

# Función que se ejecuta al presionar el botón en la interfaz gráfica
def procesar():
    texto = entrada.get().upper()
    procesar_consulta(texto)

# Función que se ejecuta al presionar el enlace en la interfaz gráfica
def abrir_enlace():
    import webbrowser
    webbrowser.open("http://localhost:8000/trabajo_estaciones/mapa.html")

# Diccionario de códigos de países y nombres
paises = {
    "CO": "Colombia",
    "AR": "Argentina",
    "MX": "México",
    "PE": "Perú",
    "BR": "Brasil",
    "US": "Estados Unidos",
    "CA": "Canadá",
    "SP": "España",
    "FR": "Francia",
    "UK": "Reino Unido",
    "IT": "Italia",
    "JA": "Japón",
    "KN": "Corea del Sur",
    "AS": "Australia",
    "CH": "China"
}

# Crear la ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("APP Estaciones Climatológicas")

# Paleta de colores
color_fondo = "#353535"
color_texto = "#FFFFFF"
color_boton = "#FF6B6B"
color_enlace = "#4DB2EC"

# Establecer configuración general de la ventana
ventana.configure(background=color_fondo)
ventana.geometry("600x320")

# Crear el contenedor central
contenedor = tk.Frame(ventana, background=color_fondo)
contenedor.pack(fill="both", expand=True)

# Crear el contenedor lateral con los códigos de los países
frame_lateral = tk.Frame(contenedor, bg=color_fondo)
titulo_lateral = tk.Label(frame_lateral, text="Códigos de Países", fg=color_texto, bg=color_fondo, font=('default', 12))
titulo_lateral.pack()
lista_paises = tk.Listbox(frame_lateral, selectbackground=color_boton)
for codigo, nombre in paises.items():
    lista_paises.insert("end", f"{codigo}: {nombre}")
lista_paises.pack(side="left")

# Crear el formulario principal
frame_principal = tk.Frame(contenedor, bg=color_fondo)
label = tk.Label(frame_principal, text="Ingrese el país a filtrar:", fg=color_texto, bg=color_fondo, font=('default', 20))
label.pack(pady=20)
entrada = tk.Entry(frame_principal, font=('default', 20), justify="center", fg=color_texto, bg=color_fondo)
entrada.pack()
boton = tk.Button(frame_principal, text="Filtrar", command=procesar, font=('default', 12), fg="white", bg=color_boton)
boton.pack(pady=20)
enlace = tk.Label(frame_principal, text="Ver en mapa", fg=color_enlace, cursor="hand2")
enlace.configure(bg=color_fondo, font=('default', 12), borderwidth=2, relief="groove")
enlace.pack(pady=20)

# Configurar el enlace
enlace.bind("<Button-1>", lambda e: abrir_enlace())

# Empaquetar contenedores laterales y principales
frame_lateral.pack(side="left", fill="y")
frame_principal.pack(side="right", fill="both", expand=True)

# Ejecutar la ventana
ventana.mainloop()
