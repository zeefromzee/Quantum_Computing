import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

#code for quantum coin flip simulation
def main():
    print("Quantum Coin Flip Simulation")
    
    print("Alice applies Hadamard gate ")
    print("State: (|0⟩ + |1⟩)/√2 [50% Heads, 50% tails in superposition]")

    quantum_coin = QuantumCircuit(1)
    #here, Alice applies Hadamard to create superposition -1
    quantum_coin.h(0) 

    input1 = input("Bob's turn: [Flip] or [Don't Flip]? ").strip().upper()# Bob chooses his operation
    
    if input1 == 'FLIP':
        quantum_coin.h(0)# Bob applies Hadamard to flip the state -2
        print("Bob chose: Flip")
    
    elif input1 == 'DONT FLIP':
        print("Bob chose: Don't Flip")
    
    else:
        print("Invalid input. No operation applied by Bob.")
    
    quantum_coin.measure_all() #measure the qubit
    quantum_coin.h(0) # Alice applies Hadamard again to bring back to basis states -3

    #here, we just create a simulator that allows us to run a quantum circuit on the backend
    simulator = AerSimulator()
    compiled_circuit = qiskit.transpile(quantum_coin, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(compiled_circuit)    
    
    print("Measurement Results:")
    print(counts)
    print("Quantum Coin Flip TCircuit:")
    print(quantum_coin)

    if counts == {'0': 1}: #{outcome: count}, 
        #initially making this condition, I thought of directly checking quantum_coin state but that was incorrect since you cannot check the state without measuring
        print("Result: Heads")#also if u forgot let me remind u that in quantum mechanics measuring the coin will collapse the superposition to one of the basis states 
        print("Alice wins")
    else:
        print("Result: Tails")
if __name__ == "__main__":
    main()
