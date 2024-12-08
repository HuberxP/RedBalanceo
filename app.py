
from flask import Flask, render_template, request
from calculos import calcular_tiempo_ciclo, asignar_estaciones
from visualizacion import crear_grafico_red

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'calcular' in request.form:
            # Recopilar datos del formulario
            tareas = request.form.getlist('tareas')
            tiempos = list(map(int, request.form.getlist('tiempos')))
            procedencia = request.form.getlist('procedencia')
            produccion = int(request.form['produccion'])
            horas_trabajo = int(request.form['horas-trabajo'])
            unidad_tiempo = request.form['unidad-tiempo']

            # Verificar longitudes
            if not (len(tareas) == len(tiempos) == len(procedencia)):
                error = "El número de tareas, tiempos y procedencias debe ser el mismo."
                return render_template('index.html', error=error, grafico=None)

            # Crear diccionario de precedencias
            precedencias = {}
            for tarea, dep in zip(tareas, procedencia):
                if dep.strip() == '':
                    precedencias[tarea] = []
                else:
                    deps = [d.strip() for d in dep.split(',') if d.strip()]
                    precedencias[tarea] = deps

            # Calcular tiempo de ciclo
            tiempo_ciclo = calcular_tiempo_ciclo(produccion, horas_trabajo, unidad_tiempo)

            # Calcular tiempo de producción disponible
            factor = {
                'segundos': 3600,
                'minutos': 60,
                'horas': 1,
                'dias': 1/24
            }
            tiempo_produccion_disponible = horas_trabajo * factor[unidad_tiempo]

            # Asignar estaciones según la lógica de tiempo mayor
            estaciones = asignar_estaciones(tareas, tiempos, precedencias, tiempo_ciclo)

            # Crear el gráfico
            grafico = crear_grafico_red(tareas, tiempos, precedencias, estaciones)

            # Calcular sum_tiempos
            sum_tiempos = sum(tiempos)
            numero_estaciones = len(estaciones)

            # Calcular eficiencia total
            eficiencia_total = 0
            if numero_estaciones > 0 and tiempo_ciclo > 0:
                eficiencia_total = round((sum_tiempos / (numero_estaciones * tiempo_ciclo)) * 100, 2)

            estaciones_detalle = []
            for estacion in estaciones:
                estaciones_detalle.append({
                    "estacion": estacion['estacion'],
                    "tareas_disponibles": estacion['tareas_disponibles'],
                    "tiempos_tarea": estacion['tiempos_tarea'],
                    "tiempo_restante": estacion['tiempo_restante'],
                    "tareas_factibles": [t for t in tareas if t not in estacion['tareas_disponibles'] and t not in estacion['tiempos_tarea']],
                    "tareas_seleccionadas": estacion['tareas_disponibles'],
                    "eficiencia": round(estacion['eficiencia'] * 100, 2)
                })

            resultado = {
                "sum_tiempos": sum_tiempos,
                "tiempo_produccion_disponible": tiempo_produccion_disponible,
                "tiempo_ciclo": tiempo_ciclo,
                "numero_estaciones": numero_estaciones,
                "estaciones_detalle": estaciones_detalle,
                "eficiencia_total": eficiencia_total
            }

            return render_template('index.html', 
                                   tareas=tareas, 
                                   tiempos=tiempos, 
                                   procedencia=precedencias, 
                                   grafico=grafico, 
                                   resultado=resultado)

    return render_template('index.html', grafico=None)

if __name__ == "__main__":
    app.run(debug=True)
