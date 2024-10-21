# Importar los módulos necesarios de Qiskit y matplotlib
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

# Crear un simulador cuántico
simulator = Aer.get_backend('qasm_simulator')

# Definir todas las combinaciones posibles de entrada A y B (0 o 1)
combinaciones = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Recorrer todas las combinaciones de A y B
for (a, b) in combinaciones:
    # Crear una carpeta para cada combinación de A y B
    carpeta = f"Reporte_A_{a}_B_{b}"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Crear un circuito cuántico con 3 qubits y 2 bits clásicos
    qc = QuantumCircuit(3, 2)
    
    # Inicializar los qubits A y B en los estados proporcionados
    if a == 1:
        qc.x(0)  # Aplicar la puerta X (NOT) al qubit A para cambiar su estado a 1
    if b == 1:
        qc.x(1)  # Aplicar la puerta X (NOT) al qubit B para cambiar su estado a 1
    
    # Visualizar y guardar el circuito cuántico inicial
    qc.draw(output='mpl')
    plt.title(f"Circuito cuántico inicial para A={a}, B={b}")
    plt.savefig(f"{carpeta}/Circuito_inicial_A_{a}_B_{b}(1).png")
    plt.close()

    # Aplicar la puerta CNOT para calcular la suma (A ⊕ B)
    qc.cx(0, 1)

    # Visualizar y guardar el circuito después de aplicar CNOT (suma)
    qc.draw(output='mpl')
    plt.title(f"Circuito cuántico después de CNOT (Suma) para A={a}, B={b}")
    plt.savefig(f"{carpeta}/Circuito_suma_A_{a}_B_{b}(2).png")
    plt.close()

    # Aplicar la puerta Toffoli (CCNOT) para calcular el acarreo (A ∙ B)
    qc.ccx(0, 1, 2)

    # Visualizar y guardar el circuito después de aplicar Toffoli (acarreo)
    qc.draw(output='mpl')
    plt.title(f"Circuito cuántico después de Toffoli (Acarreo) para A={a}, B={b}")
    plt.savefig(f"{carpeta}/Circuito_acarreo_A_{a}_B_{b}(3).png")
    plt.close()

    # Medir los resultados
    qc.measure(1, 0)  # Medir el qubit de la suma (S)
    qc.measure(2, 1)  # Medir el qubit del acarreo (C)
    
    # Visualizar y guardar el circuito final con las mediciones
    qc.draw(output='mpl')
    plt.title(f"Circuito final con mediciones para A={a}, B={b}")
    plt.savefig(f"{carpeta}/Circuito_final_A_{a}_B_{b}(4).png")
    plt.close()

    # Ejecutar el circuito en el simulador cuántico
    result = simulator.run(qc).result()
    
    # Obtener la distribución de probabilidad de las mediciones
    counts = result.get_counts(qc)
    
    # Mostrar y guardar la distribución de resultados en un histograma
    plot_histogram(counts)
    plt.title(f"Distribución de resultados para A={a}, B={b}")
    plt.savefig(f"{carpeta}/Histograma_A_{a}_B_{b}(5).png")
    plt.close()

    # Mostrar el resultado más probable
    resultado = max(counts, key=counts.get)  # Obtener el resultado con mayor frecuencia
    suma = resultado[0]  # Primer bit: resultado de la suma (S)
    acarreo = resultado[1]  # Segundo bit: resultado del acarreo (C)
    
    # Guardar los resultados en un archivo de texto
    with open(f"{carpeta}/Resultados_A_{a}_B_{b}(6).txt", 'w') as f:
        f.write(f"A={a}, B={b} Resultado más probable: Suma = {suma}, Acarreo = {acarreo}\n")
        f.write(f"Distribución completa de resultados: {counts}\n")

    # Visualizar y guardar el estado de los qubits de entrada
    estados = ['0', '1']
    x_labels = ['A', 'B']
    y_values = [a, b]

    plt.bar(x_labels, y_values, color=['blue', 'orange'])
    plt.ylim(-0.5, 1.5)
    plt.ylabel('Estado del Qubit')
    plt.title(f"Estado de los Qubits de Entrada para A={a}, B={b}")
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.axhline(y=1, color='black', linewidth=0.5, linestyle='--')

    for i, v in enumerate(y_values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

    # Guardar el gráfico de los estados de los qubits de entrada
    plt.savefig(f"{carpeta}/Estado_Qubits_A_{a}_B_{b}(7).png")
    plt.close()

    # Guardar un resumen detallado de lo que ocurrió en el circuito
    with open(f"{carpeta}/Resumen_A_{a}_B_{b}(8).txt", 'w') as f:
        f.write(f"Resumen para A={a}, B={b}:\n")
        f.write(f"- Se inicializan los qubits A y B en los estados {a} y {b}, respectivamente.\n")
        f.write(f"- Se aplica la puerta CNOT para obtener la suma (A xor B).\n")
        f.write(f"- Se aplica la puerta Toffoli (CCNOT) para obtener el acarreo (A . B).\n")
        f.write(f"- Se mide el qubit 1 para la suma y el qubit 2 para el acarreo.\n")
        f.write(f"- El resultado más probable es suma = {suma}, acarreo = {acarreo}.\n")
        f.write(f"- Se genera un histograma que muestra la probabilidad de cada resultado posible.\n")
        f.write(f"- Finalmente, se muestran los estados de entrada de los qubits A y B en un gráfico.\n")
