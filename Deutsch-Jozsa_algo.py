import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import random

# code for Deutsch-Jozsa algorithm

def mystery_function():
    func_type = random.choice(["constant", "balanced"])
    
    if func_type == "constant":
        constant_value = random.choice([0, 1])
        return ("constant", constant_value)
    else:
        return ("balanced", None)

def algo():

    n = 6
    qc = QuantumCircuit(n+1, n)
    qc.x(n)
    qc.h(range(n+1))
    
    # Generate mystery function (don't reveal it yet!)
    func_type = mystery_function()
    
    # Implement oracle based on function type
    if func_type[0] == "constant":
        if func_type[1] == 1:
            qc.x(n)
    else:  # balanced
        for i in range(n):
            qc.cx(i, n)
    
    # Continue with algorithm
    qc.h(range(n))
    qc.measure(range(n), range(n))
    
    # Run circuit
    simulator = AerSimulator()
    compiled_circuit = qiskit.transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    print("Measurement Results:")
    print(counts)
    print("Deutsch-Jozsa Circuit:")
    print(qc)
    
    # Determine result from measurement
    if all(bit == '0' for bit in list(counts.keys())[0]):
        determined = "constant"
    else:
        determined = "balanced"
    
    print(f"Algorithm determined: Function is {determined}")
    print(f"Actual function type: {func_type[0]}")
    
    if determined == func_type[0]:
        print("Correct!")
    else:
        print("Error!")

def main():
    print("Deutsch-Jozsa Algorithm Simulation")
    algo()

if __name__ == "__main__":
    main()
