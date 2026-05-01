import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import random

def alice():
	# prepare circuit
	qc = QuantumCircuit(1,1)
	alice_basis = ["X", "Z"] # diagonal or rectillinear basis selection
	select = random.choice(alice_basis)
	alice_bit = random.randint(0, 1)
	if select == "Z" and alice_bit == 0:
		pass
	elif select == "Z" and alice_bit == 1:
		qc.x(0)
	elif select == "X" and alice_bit == 0:
		qc.h(0)
	elif select == "X" and alice_bit == 1:
		qc.x(0)
		qc.h(0)
		
	return qc, alice_bit, select

def measuring(qc):
#here, we just create a simulator that allows us to run a quantum circuit on the backend
	simulator = AerSimulator()
	compiled_circuit = qiskit.transpile(qc, simulator)
	job = simulator.run(compiled_circuit, shots=1)
	result = job.result()
	counts = result.get_counts(compiled_circuit)	
	bits = next(iter(counts))
	measured = int(bits)# convert "0"/"1" -> 0/1
	return measured

def bob(qc):
	bob_basis = ["X", "Z"] # diagonal or rectillinear basis selection
	select1 = random.choice(bob_basis)
	#measure the qubit	
	if select1 == "X":
		qc.h(0)
		qc.measure(0,0)
		bob_bit = measuring(qc)
	elif select1 == "Z":
		qc.measure(0,0)
		bob_bit = measuring(qc)	
	return select1, bob_bit

def eve(qc):
	eve_basis = ["X", "Z"] 
	select2 = random.choice(eve_basis)
	#measure the qubit	
	if select2 == "X":
		qc.h(0)
		qc.measure(0,0)
		eve_bit = measuring(qc)
	elif select2 == "Z":
		qc.measure(0,0)
		eve_bit = measuring(qc)	
	qc_E = QuantumCircuit(1,1)
	if select2 == "Z" and eve_bit == 0:
		pass
	elif select2 == "Z" and eve_bit == 1:
		qc_E.x(0)
	elif select2 == "X" and eve_bit == 0:
		qc_E.h(0)
	elif select2 == "X" and eve_bit == 1:
		qc_E.x(0)
		qc_E.h(0)
	return select2, eve_bit, qc_E



def sift(alice_bit, select, select1):
	if select == select1:
		return alice_bit
	return None


def main(eve_present = True):
	qc, alice_bit, select = alice()
	if eve_present:
		select2, eve_bit, qc = eve(qc)
	select1, bob_bit = bob(qc)
	key = sift (alice_bit, select, select1)
	print("Alice basis: ", select)
	print("Bob basis: ", select1)
	print("Alice bit: ", alice_bit)
	print("Bob bit: ", bob_bit)
	print("Shared key bit: ", key)

if __name__ == "__main__":
    main()
