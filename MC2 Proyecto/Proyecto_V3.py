# Importar los módulos necesarios de Qiskit y matplotlib
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np

# Función para crear el circuito cuántico del semisumador
def crear_semisumador_cuantico(a_estado, b_estado):
    # Crear un circuito cuántico con 3 qubits:
    # Qubit 0 para A, qubit 1 para B, qubit 2 como ancilla (para acarreo)
    # Y 2 bits clásicos para almacenar los resultados de la suma y acarreo
    qc = QuantumCircuit(3, 2)

    # Inicializar los qubits A y B en los estados proporcionados (0 o 1)
    if a_estado == 1:
        qc.x(0)  # Aplicar la puerta X (NOT) en el qubit 0 para cambiar su estado a 1
    if b_estado == 1:
        qc.x(1)  # Aplicar la puerta X (NOT) en el qubit 1 para cambiar su estado a 1

    # Aplicar la puerta CNOT (Control-Not) para calcular la suma (A ⊕ B)
    qc.cx(0, 1)  # El qubit 1 (B) se invierte si el qubit 0 (A) está en estado 1

    # Aplicar la puerta Toffoli (CCNOT) para calcular el acarreo (A ∙ B)
    # La puerta Toffoli establece el qubit 2 (ancilla) a 1 si A y B son ambos 1
    qc.ccx(0, 1, 2)

    # Medir los qubits correctos y almacenar los resultados en los bits clásicos
    qc.measure(1, 0)  # Medir el qubit 1 (suma) y almacenar el resultado en el primer bit clásico
    qc.measure(2, 1)  # Medir el qubit 2 (acarreo) y almacenar el resultado en el segundo bit clásico

    # Devolver el circuito cuántico creado
    return qc

# Función para ejecutar el circuito cuántico en el simulador
def ejecutar_circuito(qc):
    # Usar el simulador cuántico de Qiskit para ejecutar el circuito
    simulator = Aer.get_backend('qasm_simulator')
    result = simulator.run(qc).result()  # Ejecutar el circuito y obtener el resultado

    # Obtener la distribución de probabilidad de las mediciones
    counts = result.get_counts(qc)

    # Extraer el resultado más probable de las mediciones
    resultado = max(counts, key=counts.get)  # Obtener el resultado que ocurrió con mayor frecuencia
    suma = resultado[0]  # Primer bit: resultado de la suma (S)
    acarreo = resultado[1]  # Segundo bit: resultado del acarreo (C)

    # Devolver los resultados de la suma y acarreo
    return suma, acarreo, counts

# Función para probar todas las combinaciones posibles de entrada (A, B)
def probar_todas_las_combinaciones():
    # Definir todas las combinaciones posibles de A y B (0 o 1)
    combinaciones = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    # Iterar a través de todas las combinaciones
    for (a, b) in combinaciones:
        print(f"\nProbando con A={a}, B={b}")
        
        # Crear el circuito cuántico para la combinación actual de A y B
        qc = crear_semisumador_cuantico(a, b)
        
        # Dibujar el circuito cuántico y guardar la imagen
        qc.draw(output='mpl', filename=f'circuit_A{a}_B{b}.png')

        # Ejecutar el circuito y obtener los resultados de suma y acarreo
        suma, acarreo, counts = ejecutar_circuito(qc)

        # Mostrar los resultados en el formato deseado
        print(f"A={a}, B={b} Resultado: {suma}{acarreo} (S = {suma}, C = {acarreo})")
        
        # Visualizar el estado de los qubits de entrada (A y B)
        mostrar_estado_qubits(a, b)

        # Mostrar la distribución de resultados en un histograma
        plot_histogram(counts)
        plt.title(f"Resultados para A={a}, B={b}")
        plt.show()

# Función para mostrar el estado de los qubits de entrada
def mostrar_estado_qubits(a_estado, b_estado):
    # Crear un gráfico simple para mostrar el estado de los qubits de entrada
    estados = ['0', '1']
    x_labels = ['A', 'B']
    y_values = [a_estado, b_estado]

    # Crear el gráfico de barras
    plt.bar(x_labels, y_values, color=['blue', 'orange'])
    plt.ylim(-0.5, 1.5)
    plt.ylabel('Estado del Qubit')
    plt.title('Estado de los Qubits de Entrada')
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.axhline(y=1, color='black', linewidth=0.5, linestyle='--')
    
    # Etiquetas de estado
    for i, v in enumerate(y_values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

    # Mostrar el gráfico
    plt.show()

# Ejecutar todas las pruebas para todas las combinaciones de A y B
probar_todas_las_combinaciones()
