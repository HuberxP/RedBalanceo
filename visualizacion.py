import matplotlib.pyplot as plt
import networkx as nx

def crear_grafico_red(tareas, tiempos, procedencia, estaciones):
    G = nx.DiGraph()

    # Agregar nodos y sus atributos
    for tarea, tiempo in zip(tareas, tiempos):
        G.add_node(tarea, time=tiempo)

    # Agregar aristas (dependencias entre tareas)
    for tarea, deps in procedencia.items():
        for dep in deps:
            if dep:  # Evita agregar aristas vacías
                G.add_edge(dep, tarea)

    # Crear las etiquetas con el atributo 'time', verificando que exista
    labels = {}
    for node in G.nodes():
        time = G.nodes[node].get('time', 'N/A')  # Usa 'N/A' si no existe el atributo 'time'
        labels[node] = f"{node}\n({time})"

    # Dibujar el grafo
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))

    for estacion in estaciones:
        tareas_estacion = estacion['tareas_disponibles']
        subgraph = G.subgraph(tareas_estacion)
        pos_sub = {n: pos[n] for n in tareas_estacion}

        nx.draw_networkx_nodes(subgraph, pos_sub, node_color='skyblue', node_size=2000)
        nx.draw_networkx_edges(subgraph, pos_sub, arrowstyle='->', arrowsize=20)
        nx.draw_networkx_labels(subgraph, pos_sub, {n: labels[n] for n in tareas_estacion}, font_size=10)

    plt.title("Red de Tareas y Precedencias por Estaciones")
    plt.axis('off')
    plt.tight_layout()

    plt.savefig('static/grafico_estaciones.png')
    plt.close()

    return 'static/grafico_estaciones.png'
