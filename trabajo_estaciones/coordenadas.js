// Se podría considerar la utilización de un servicio de geocodificación o una base de datos de coordenadas geográficas en este punto.
// A continuación, se crea un objeto con coordenadas de algunos países.
let coordenadas = {
    "CO": [-74.2973, 4.5709],
    "AR": [-64.1833, -31.4167],
    "MX": [-102.5528, 23.6345],
    "PE": [-77.0428, -12.0464],
    "BR": [-47.9292, -15.7801],
    "US": [-95.7129, 37.0902],
    "CA": [-106.3468, 56.1304],
    "SP": [-3.7492, 40.4637],
    "FR": [2.2137, 46.2276],
    "UK": [-3.4359, 55.3781],
    "IT": [12.5674, 41.8719],
    "JA": [138.2529, 36.2048],
    "KN": [127.7669, 35.9078],
    "AS": [133.7751, -25.2744],
    "CH": [104.1953, 35.8616]
};

// Exportamos este objeto para que sea utilizado en la función obtenerCoordenadas()
export default coordenadas;
