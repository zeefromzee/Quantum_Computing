import qiskit
# from qiskit import QuantumCircuit, transpile, Aer, execute
print("Qiskit imported successfully!")
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def create_bell_state():
    simulator= AerSimulator()
    qc =QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)

    return qc

def transpile_circuit(circuit):
    simulator =AerSimulator()
    transpiled_circuit= transpile(circuit, simulator)

    return transpiled_circuit

def run_circuit(circuit):
    simulator =AerSimulator()
    compiled_circuit=transpile(circuit, simulator)
    job=simulator.run(compiled_circuit, shots=1024)
    result=job.result()
    counts=result.get_counts(compiled_circuit)

    return counts 

def circuit_with_measurements(circuit):
    qc = circuit.copy()
    qc.measure_all()
    return qc

def circuit_fun( ):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc

def main():
    bell_circuit = create_bell_state()
    print("Bell State Circuit:")
    print(bell_circuit) 
    transpiled_circuit=transpile_circuit(bell_circuit)
    print("Transpiled Circuit:")
    print(transpiled_circuit)
    measured_circuit=circuit_with_measurements(bell_circuit)
    counts=run_circuit(measured_circuit)
    print("Measurement Results:")
    print(counts)
    print("Circuit with Measurements:")
    print(measured_circuit)
    another_circuit=circuit_fun()
    print("Another Circuit with Measurements:")
    print(another_circuit)

if __name__ == "__main__":
    main()
