def calcular_tiempo_ciclo(produccion_requerida, horas_trabajo, unidad_tiempo):
    factor = {
        'segundos': 3600,
        'minutos': 60,
        'horas': 1,
        'dias': 1/24
    }
    return (horas_trabajo * factor[unidad_tiempo]) / produccion_requerida

def asignar_estaciones(tareas, tiempos, precedencias, tiempo_ciclo):
    tiempo_por_tarea = {t: tiempos[i] for i, t in enumerate(tareas)}
    tareas_restantes_pre = {t: len(precedencias.get(t, [])) for t in tareas}
    factibles = [t for t in tareas if tareas_restantes_pre[t] == 0]

    estaciones_asignadas = []
    estacion_actual = {
        'estacion': 1,
        'tareas_disponibles': [],
        'tiempos_tarea': [],
        'tiempo_restante': tiempo_ciclo,
        'eficiencia': 0
    }

    asignadas = set()

    while len(asignadas) < len(tareas):
        factibles_actuales = [t for t in factibles if t not in asignadas]

        if not factibles_actuales:
            if estacion_actual['tiempos_tarea']:
                estacion_actual['eficiencia'] = sum(estacion_actual['tiempos_tarea']) / tiempo_ciclo
            estaciones_asignadas.append(estacion_actual)

            if len(asignadas) < len(tareas):
                estacion_actual = {
                    'estacion': len(estaciones_asignadas) + 1,
                    'tareas_disponibles': [],
                    'tiempos_tarea': [],
                    'tiempo_restante': tiempo_ciclo,
                    'eficiencia': 0
                }
            else:
                break
        else:
            tarea_seleccionada = max(factibles_actuales, key=lambda x: tiempo_por_tarea[x])
            tiempo_tarea = tiempo_por_tarea[tarea_seleccionada]

            if tiempo_tarea <= estacion_actual['tiempo_restante']:
                estacion_actual['tareas_disponibles'].append(tarea_seleccionada)
                estacion_actual['tiempos_tarea'].append(tiempo_tarea)
                estacion_actual['tiempo_restante'] -= tiempo_tarea
                asignadas.add(tarea_seleccionada)

                for t in tareas:
                    if tarea_seleccionada in precedencias.get(t, []):
                        tareas_restantes_pre[t] -= 1
                        if tareas_restantes_pre[t] == 0:
                            factibles.append(t)
            else:
                estacion_actual['eficiencia'] = sum(estacion_actual['tiempos_tarea']) / tiempo_ciclo
                estaciones_asignadas.append(estacion_actual)

                estacion_actual = {
                    'estacion': len(estaciones_asignadas) + 1,
                    'tareas_disponibles': [],
                    'tiempos_tarea': [],
                    'tiempo_restante': tiempo_ciclo,
                    'eficiencia': 0
                }

    if estacion_actual['tareas_disponibles']:
        estacion_actual['eficiencia'] = sum(estacion_actual['tiempos_tarea']) / tiempo_ciclo
        estaciones_asignadas.append(estacion_actual)

    return estaciones_asignadas
