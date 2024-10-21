# Importar los módulos necesarios de Qiskit y matplotlib
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Crear un simulador cuántico
simulator = Aer.get_backend('qasm_simulator')

# Definir todas las combinaciones posibles de entrada A y B (0 o 1)
combinaciones = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Recorrer todas las combinaciones de A y B
for (a, b) in combinaciones:
    # Crear un circuito cuántico con 3 qubits y 2 bits clásicos
    qc = QuantumCircuit(3, 2)
    
    # Inicializar los qubits A y B en los estados proporcionados
    if a == 1:
        qc.x(0)  # Aplicar la puerta X (NOT) al qubit A para cambiar su estado a 1
    if b == 1:
        qc.x(1)  # Aplicar la puerta X (NOT) al qubit B para cambiar su estado a 1
    
    # Visualizar el circuito cuántico inicial con los qubits A y B
    qc.draw(output='mpl')
    plt.title(f"Circuito cuántico inicial para A="+str(a)+", B="+str(b)+"")
    plt.show()

    # Aplicar la puerta CNOT para calcular la suma (A ⊕ B)
    qc.cx(0, 1)

    # Visualizar el circuito después de aplicar CNOT (suma)
    qc.draw(output='mpl')
    plt.title(f"Circuito cuántico después de CNOT (Suma) para A="+str(a)+", B="+str(b)+"")
    plt.show()

    # Aplicar la puerta Toffoli (CCNOT) para calcular el acarreo (A ∙ B)
    qc.ccx(0, 1, 2)

    # Visualizar el circuito después de aplicar Toffoli (acarreo)
    qc.draw(output='mpl')
    plt.title(f"Circuito cuántico después de Toffoli (Acarreo) para A="+str(a)+", B="+str(b)+"")
    plt.show()

    # Medir los resultados
    qc.measure(1, 0)  # Medir el qubit de la suma (S)
    qc.measure(2, 1)  # Medir el qubit del acarreo (C)
    
    # Visualizar el circuito final con las mediciones
    qc.draw(output='mpl')
    plt.title("Circuito cuántico final con mediciones para A="+str(a)+", B="+str(b)+"\n")
    plt.show()

    # Ejecutar el circuito en el simulador cuántico
    result = simulator.run(qc).result()
    
    # Obtener la distribución de probabilidad de las mediciones
    counts = result.get_counts(qc)
    
    # Mostrar la distribución de resultados en un histograma
    plot_histogram(counts)
    plt.title(f"Distribución de resultados para A="+str(a)+", B="+str(b)+"\n")
    plt.show()

    # Mostrar el resultado más probable
    resultado = max(counts, key=counts.get)  # Obtener el resultado con mayor frecuencia
    suma = resultado[0]  # Primer bit: resultado de la suma (S)
    acarreo = resultado[1]  # Segundo bit: resultado del acarreo (C)
    
    # Mostrar los resultados
    print("A="+str(a)+", B="+str(b)+" Resultado más probable: Suma = "+str(suma)+", Acarreo = "+str(acarreo)+"\n")
    print("Distribución completa de resultados:"+str(counts)+"\n")

    # Visualizar el estado de los qubits de entrada
    estados = ['0', '1']
    x_labels = ['A', 'B']
    y_values = [a, b]

    # Crear un gráfico de barras para mostrar el estado de los qubits de entrada
    plt.bar(x_labels, y_values, color=['blue', 'orange'])
    plt.ylim(-0.5, 1.5)
    plt.ylabel('Estado del Qubit')
    plt.title("Estado de los Qubits de Entrada para A="+str(a)+", B="+str(b)+"\n")
    plt.axhline(y=0, color='black', linewidth=0.5, linestyle='--')
    plt.axhline(y=1, color='black', linewidth=0.5, linestyle='--')
    
    # Etiquetas de estado
    for i, v in enumerate(y_values):
        plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

    # Mostrar el gráfico
    plt.show()

    # Mostrar un resumen detallado de lo que ha ocurrido en el circuito
    print("Resumen para A="+str(a)+", B="+str(b)+"+:\n")
    print("- Se inicializan los qubits A y B en los estados "+str(a)+" y "+str(b)+", respectivamente.\n")
    print("- Se aplica la puerta CNOT para obtener la suma (A xor B).\n")
    print("- Se aplica la puerta Toffoli (CCNOT) para obtener el acarreo (A . B).\n")
    print("- Se mide el qubit 1 para la suma y el qubit 2 para el acarreo.\n")
    print("- El resultado más probable es suma ="+str(suma)+", acarreo = "+str(acarreo)+".\n")
    print("- Se genera un histograma que muestra la probabilidad de cada resultado posible.\n")
    print("- Finalmente, se muestran los estados de entrada de los qubits A y B en un gráfico.\n")
