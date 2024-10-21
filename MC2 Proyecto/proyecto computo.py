    from qiskit_aer import Aer
    from qiskit import QuantumCircuit
    from qiskit.visualization import plot_histogram
    import matplotlib.pyplot as plt

    print("hola mundo")

    # Crear un circuito cuántico con 3 qubits (A, B, ancilla) y 2 bits clásicos
    qc = QuantumCircuit(3, 2)

    # Inicializar los qubits A y B en los estados que desees probar (por ejemplo, (A, B) = (1, 0))
    qc.x(0)  # Cambia el estado de A a 1 (X gate). Comenta esta línea para probar (A, B) = (0, 0)
    # qc.x(1)  # Cambia el estado de B a 1 si lo deseas. Comenta/descomenta según las pruebas

    # Aplicar la puerta CNOT para la suma (A ⊕ B)
    qc.cx(0, 1)

    # Aplicar la puerta Toffoli (CCNOT) para el acarreo (A ∙ B)
    qc.ccx(0, 1, 2)

    # Medir los qubits
    qc.measure([1, 2], [0, 1])  # Medimos B para la suma (S) y el ancilla para el acarreo (C)

    # Dibujar el circuito y crear la imagen en la carpeta raiz
    qc.draw(output='mpl', filename='circuit.png')

    # Simular el circuito cuántico
    simulator = Aer.get_backend('qasm_simulator')
    result = simulator.run(qc).result()

    # Obtener la distribución de probabilidad de las mediciones
    counts = result.get_counts(qc)
    # mostramos counts
    print(counts)

    #visualizar los resultados con un histograma utilizando plt y guardar la iamgen en la carpeta raiz
    plot_histogram(counts)
    plt.savefig('histogram.png')
    plt.show()



