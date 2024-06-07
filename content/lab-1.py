# %%
"""Lab 1."""

import os

import numpy as np
from config import API_KEY
from qc_grader.challenges.iqc_2024 import (
    grade_lab1_ex1,
    grade_lab1_ex2,
    grade_lab1_ex3,
    grade_lab1_ex4,
    grade_lab1_ex5,
    grade_lab1_ex6,
    grade_lab1_ex7,
)
from qiskit import QuantumCircuit
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import Session
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from scipy.optimize import minimize

os.environ["QXToken"] = API_KEY  # noqa: SIM112
# %%
"""
Exercise 1: Create and draw a singlet Bell state circuit

Bell circuits are specific circuits which generate Bell states, or EPR pairs, a form of entangled
and normalized basis vectors. In other words, they are the circuits we use to generate entangled
states, a key ingredient in quantum computations.

There exist 4 different Bell states. You can learn about each from the Basics of Quantum Information
page

Your Task: please build a circuit that generates the psi minus Bell state.
"""

qc = QuantumCircuit(2)

qc.h(0)
qc.cx(0, 1)
qc.z(0)
qc.x(1)


qc.measure_all()
qc.draw("mpl")
# %%
# * Grading

grade_lab1_ex1(qc)
# %%
"""
Exercise 2: Use Sampler.run

The Qiskit Sampler primitive (more info on Primitives here) returns the sampled result according to
the specified output type. It allows us to efficiently sample quantum states by executing quantum
circuits and providing probability distributions of the quantum states.

Your Task: use the Qiskit StatevectorSampler to obtain the counts resulting from our circuit.
"""
params = np.zeros((1, 0))


sampler = StatevectorSampler()

pub = (qc, params)
job_sampler = sampler.run([pub], shots=256)  # type: ignore
### Don't change any code past this line ###
result_sampler = job_sampler.result()
counts_sampler = result_sampler[0].data.meas.get_counts()


### Don't change any code past this line ###

result_sampler = job_sampler.result()
counts_sampler = result_sampler[0].data.meas.get_counts()  # type: ignore
# %%
# * Grading
grade_lab1_ex2(job_sampler)
# %%
"""
Exercise 3: Create and draw a W-state circuit

Next, we will develop a slightly more complicated circuit. Similarly to Bell states circuit
producing Bell states, W-state circuits produce W states. Although Bell states entangle two qubits,
W-states entangle three qubits. To build our W-state, we will follow 6 simple steps:

Initialize our 3 qubit circuit
Perform an Ry rotation on our qubit. The specifics of this operation are provided.
Perform a controlled hadamard gate on qubit 1, with control qubit 0
Add a CNOT gate with control qubit 1 and target qubit 2
Add a CNOT gate with control qubit 0 and target qubit 1
Add a X gate on qubit 0
Your Task: Follow the steps to build the W-state circuit
"""

qc = QuantumCircuit(3)
qc.ry(1.91063324, 0)
qc.ch(0, 1)
qc.cx(1, 2)
qc.cx(0, 1)
qc.x(0)


# %%
# * Grading
grade_lab1_ex3(qc)
# %%
"""
Exercise 4: Create a parameterized circuit to serve as the ansatz

Our first task will be to set up our ansatz, or a trial solution, for our problem which we will
compare against.

For this we can use Qiskit's TwoLocal circuit, a pre-built circuit that can be used to prepare trial
wave functions for variational quantum algorithms or classification circuits for machine learning.
TwoLocal circuits are parameterized circuits consisting of alternating rotation layers and
entanglement layers. You can find more information about them in Qiskit's documentation.

Your Task: Set up a 3-qubit TwoLocal circuit using Ry and Rz rotations. Entanglement should be set
to full, and entanglement blocks should use the Cz gate. Make sure you set reps=1 and
insert_barriers=True.
"""
# Parameters for the TwoLocal circuit
num_qubits = 3
rotation_blocks = ["ry", "rz"]
entanglement_blocks = "cz"
entanglement = "full"

# Create the TwoLocal ansatz
ansatz = TwoLocal(
    num_qubits=num_qubits,
    rotation_blocks=rotation_blocks,
    entanglement_blocks=entanglement_blocks,
    entanglement=entanglement,
    reps=1,
    insert_barriers=True,
)

### Don't change any code past this line ###
ansatz.decompose().draw("mpl")
# %%
# * Grading
grade_lab1_ex4(num_qubits, rotation_blocks, entanglement_blocks, entanglement)

# %%
"""
Exercise 5: Transpile to ISA circuits

In this example we will use the FakeSherbrooke, a fake (simulated) 127-qubit backend, useful for
testing the transpiler and other backend-facing functionalities.

Preset pass managers are the default pass managers used by the transpile() function. transpile()
provides a convenient and simple method to construct a standalone PassManager object that mirrors
what the transpile function does when optimizing and transforming a quantum circuit for execution
on a specific backend.

Your Task: Define the pass manager. Reference the Qiskit documentation for more info.
"""
backend_answer = FakeSherbrooke()
optimization_level_answer = 0
pm = generate_preset_pass_manager(optimization_level=0, backend=backend_answer)
isa_circuit = pm.run(ansatz)
isa_circuit.draw(
    "mpl",
    idle_wires=False,
)
# %%
# * Grading
grade_lab1_ex5(isa_circuit)
# %%
"""
Exercise 6: Defining the cost function

Like many classical optimization problems, the solution to a VQE problem can be formulated as
minimization of a scalar cost function. The cost function for our VQE is simple: the energy!

Your Task: Define a cost function by using Qiskit Runtime Estimator to find the energy for a
given parameterized state and our Hamiltonian.
"""

pauli_op = SparsePauliOp(["ZII", "IZI", "IIZ"])
hamiltonian_isa = pauli_op.apply_layout(layout=isa_circuit.layout)


def cost_func(params, ansatz, hamiltonian, estimator, callback_dict):
    """Return estimate of energy from estimator.

    Parameters:
        params (ndarray): Array of ansatz parameters
        ansatz (QuantumCircuit): Parameterized ansatz circuit
        hamiltonian (SparsePauliOp): Operator representation of Hamiltonian
        estimator (EstimatorV2): Estimator primitive instance

    Returns:
        float: Energy estimate
    """
    pub = (ansatz, [hamiltonian], [params])
    result = estimator.run(pubs=[pub]).result()
    energy = result[0].data.evs[0]

    callback_dict["iters"] += 1
    callback_dict["prev_vector"] = params
    callback_dict["cost_history"].append(energy)

    ### Don't change any code past this line ###
    print(energy)
    return energy, result


# %%
# * Grading
grade_lab1_ex6(cost_func)

# %%
"""Exercise 7: QiskitRuntimeService V2 Primitives, local testing mode and Sessions, a first look

Next, we will use the new QiskitRuntimeService V2 primitives: EstimatorV2 and SamplerV2.

The new Estimator interface lets you specify a single circuit and multiple observables and parameter
value sets for that circuit, so that sweeps over parameter value sets and observables can be
efficiently specified. Previously, you had to specify the same circuit multiple times to match the
size of the data to be combined. Also, while you can still use optimization_level and
resilience_level as the simple knobs, V2 primitives give you the flexibility to turn on or
off individual error mitigation / suppression methods to customize them for your needs.

SamplerV2 is simplified to focus on its core task of sampling the quantum register from the
execution of quantum circuits. It returns the samples, whose type is defined by the program,
without weights. The output data is also separated by the output register names defined by the
program. This change enables future support for circuits with classical control flow.

We will also use Qiskit's 1.0 local testing mode. Local testing mode (available with
qiskit-ibm-runtime 0.22.0 or later) can be used to help develop and test programs before fine-tuning
them and sending them to real quantum hardware.

Your Task: After using local testing mode to verify your program, all you need to do is change the
backend name to run it on an IBM Quantum system.
"""
num_params = ansatz.num_parameters
x0 = 2 * np.pi * np.random.random(num_params)  # noqa: NPY002
callback_dict = {
    "prev_vector": None,
    "iters": 0,
    "cost_history": [],
}

### Select a Backend
## Use FakeSherbrooke to simulate with noise that matches closer to the real
# experiment. This will run slower.
## Use AerSimulator to simulate without noise to quickly iterate. This will run faster.

backend = AerSimulator()

# ### Don't change any code past this line ###


# Here we have updated the cost function to return only the energy to be
# compatible with recent scipy versions (>=1.10)
def cost_func_2(*args, **kwargs):
    energy, result = cost_func(*args, **kwargs)
    return energy


with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    res = minimize(
        cost_func_2,
        x0,
        args=(isa_circuit, hamiltonian_isa, estimator, callback_dict),
        method="cobyla",
        options={"maxiter": 100},
    )

# %%
# * Grading
grade_lab1_ex7(res)

# %%
