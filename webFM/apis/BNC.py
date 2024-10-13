import bcchapi
import pandas as pd
import numpy as np

siete = bcchapi.Siete(file="credenciales.txt")

# resultado_busqueda = siete.buscar("paridad")
# print("Series encontradas para el tipo de cambio del dólar:")
# print(resultado_busqueda)

cuadro = siete.cuadro(
    series=["F073.TCO.PRE.Z.D"],
    nombres=["dolar_observado"],
    desde="2024-10-01",
    hasta="2024-10-04",
    # variacion=1,
    # frecuencia="D",
    # observado={"dolar_observado":"last"}
)
print("\nCuadro de datos:")
print(cuadro)


#"BRL": "F072.BRL.USD.N.O.D",  # Brasil: Real
#"CLP": "F073.TCO.PRE.Z.D",    # Chile: Peso chileno (observado)
#"CNY": "F072.CNY.USD.N.O.D",  # China: Yuan Renminbi
#"JPY": "F072.JPY.USD.N.O.D",  # Japón: Yen
#"ARS": "F072.ARS.USD.N.O.D",  # Argentina: Peso argentino