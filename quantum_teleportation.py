import qiskit
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from math import pi
from qiskit.quantum_info import Statevector

# code for Quantum Teleportation algorithm

# Building a gate in a simulator here
def Simulator(qubit):
    global counts 
    qubit.measure_all()
    simulator = AerSimulator()
    compiled_circuit = qiskit.transpile(qubit, simulator)
    job = simulator.run(compiled_circuit, shots=1)
    result = job.result()
    counts = result.get_counts(compiled_circuit) 

    print("The required state is: ", counts)
    print("The requied circuit for current quantum state is:")
    print(compiled_circuit)

# The stage Alice will send Bob-
def initial_state_alice():
    # For setting the initial stage I was slightly conflicted whether to apply no gates, rotation gates or H gate
    initial_qubit=QuantumCircuit(1)

    user_selection=input("What state would You like the qubit to be in ?\nSelect 1 for either |0⟩ or |1⟩\nSelect 2 for superposition\nSelect 3 for arbitrary state :  ")

    if user_selection=='1':
        # selecting |0⟩ or |1⟩
        select=(input("Enter 0 for |0⟩ and 1 for |1⟩: "))
        
        if select=='0':
            return 0
        elif select =='1':
            initial_qubit.x(0)
        else:
            print("Invalid Input")

    elif user_selection == '2':
        # Creating superposition
        initial_qubit.h(0)

    elif user_selection == '3':
        # Creating an arbitrary state
        initial_qubit.ry(pi/2, 0)
        initial_qubit.rz(pi/2, 0)
        # One could also directly access the states through U gate 
        # initial_qubit.u(pi/2, 0, pi/2, 0) 

    else:
        print("Invalid Input. Please Retry")


# quantum Entanglement channel which will make teleportation possible
def Create_Entanglement():
    
    # We will create a Bell Pair here
    global qubits 
    global cr
    qubits= QuantumCircuit(3,3)
    cr = qubits.cregs[0]
    
    
    # Applying H gate to control qubit
    qubits.h(0)
    
    # Applying Controlled NOT gate
    qubits.cx(0, 2)
    Simulator(qubits)

# Alice entangles the qubit she wants to send with her half of entangled pair
def Entangled_qubit():
    # Applying CNOT Gate
    qubits.cx(0, 1)
    qubits.h(0)

# Alice measures her qubits 
def Measure_qubit():

    # storing the state in a classical bit
    qubits.measure([0, 1], [0, 1])
    
# Classical Communication happens implicitly here so we dont need to define a function for communication here

# Bob's Corrections
def Communication():
    # personaly I decided it would be much easier to read the measurements from the circuit register rather than parsing the qubits from count(I'm tired)
    true_body_x = QuantumCircuit(1)  # Circuit with 1 qubit
    true_body_x.x(0)  # Apply X to that qubit
    
    true_body_z = QuantumCircuit(1)
    true_body_z.z(0)
    
    # Calling if_test() with: the condition to check, the mini circuit, and which qubit in the main circuit to apply it to
    qubits.if_test((cr[1], 1), true_body_x, [2], [])  # If bit 1 is 1, apply X to qubit 2
    qubits.if_test((cr[0], 1), true_body_z, [2], []) 


def verify():
    """Simple verification by testing known states"""
    
    print("\n=== TELEPORTATION VERIFICATION ===\n")
    
    # Test 1: Teleporting |0⟩
    print("Test 1: Teleporting |0⟩")
    qc = QuantumCircuit(3, 3)
    cr = qc.cregs[0]
    
    # Alice prepares |0⟩ (do nothing, already in |0⟩)
    
    # Create entanglement
    qc.h(1)
    qc.cx(1, 2)
    
    # Alice entangles and measures
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])
    
    # Bob's corrections
    true_body_x = QuantumCircuit(1)
    true_body_x.x(0)
    true_body_z = QuantumCircuit(1)
    true_body_z.z(0)
    qc.if_test((cr[1], 1), true_body_x, [2], [])
    qc.if_test((cr[0], 1), true_body_z, [2], [])
    
    # Measure Bob's qubit
    qc.measure(2, 2)
    
    # Run it
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    # Check Bob's results (last bit in the string)
    bob_got_0 = sum(count for bits, count in counts.items() if bits[0] == '0')
    bob_got_1 = sum(count for bits, count in counts.items() if bits[0] == '1')
    
    print(f"Bob measured 0: {bob_got_0} times")
    print(f"Bob measured 1: {bob_got_1} times")
    print(f"Expected: ~1000 times 0")
    print(f"Success: {bob_got_0 > 900}\n")  # Should be mostly 0
    
    # Test 2: Teleporting |1⟩
    print("Test 2: Teleporting |1⟩")
    # here, we need 3 qubits for Alice's message, Alices bell half and Bob's bell half
    # and the 3 classical bits are for storing those measurement values
    qc2 = QuantumCircuit(3, 3)
    cr2 = qc2.cregs[0]
    
    # Alice prepares |1⟩
    qc2.x(0)
    
    # Create entanglement
    qc2.h(1)
    qc2.cx(1, 2)
    
    # Alice entangles and measures
    qc2.cx(0, 1)
    qc2.h(0)
    qc2.measure([0, 1], [0, 1])
    
    # Bob's corrections
    qc2.if_test((cr2[1], 1), true_body_x, [2], [])
    qc2.if_test((cr2[0], 1), true_body_z, [2], [])
    
    # Measure Bob's qubit
    qc2.measure(2, 2)
    
    # Run it
    job2 = simulator.run(qc2, shots=1000)
    result2 = job2.result()
    counts2 = result2.get_counts()
    
    # Check Bob's results
    # filtering and summing results where Bob's bit (first character in string) is '0' or '1'
    bob_got_0_2 = sum(count for bits, count in counts2.items() if bits[0] == '0')
    bob_got_1_2 = sum(count for bits, count in counts2.items() if bits[0] == '1')
    
    print(f"Bob measured 0: {bob_got_0_2} times")
    print(f"Bob measured 1: {bob_got_1_2} times")
    print(f"Expected: ~1000 times 1")
    print(f"Success: {bob_got_1_2 > 900}\n")

def main():
    initial_state_alice()
    Create_Entanglement()
    Entangled_qubit()
    Measure_qubit()
    Communication()
    verify()

if __name__ == "__main__":
    main()
