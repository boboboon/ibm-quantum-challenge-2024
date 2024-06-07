# %%
"""Lab 1."""

import os
from typing import Callable, List

import matplotlib.pyplot as plt
import numpy as np
from config import API_KEY
from loguru import logger
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
from qiskit.primitives import PrimitiveJob, StatevectorSampler
from qiskit.quantum_info import Operator, SparsePauliOp, Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import Session
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from scipy.optimize import minimize
from scipy.optimize._optimize import OptimizeResult

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

result_sampler = job_sampler.result()
counts_sampler = result_sampler[0].data.meas.get_counts()  # type: ignore

logger.info(counts_sampler)

### Don't change any code past this line ###

result_sampler = job_sampler.result()
counts_sampler = result_sampler[0].data.meas.get_counts()  # type: ignore
# %%
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
