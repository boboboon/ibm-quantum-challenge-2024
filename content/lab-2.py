# %%
"""Lab 2."""

import os

import matplotlib.pyplot as plt
import numpy as np
from config import API_KEY
from qc_grader.challenges.iqc_2024 import (
    grade_lab2_ex1,
    grade_lab2_ex2,
    grade_lab2_ex3,
    grade_lab2_ex4,
    grade_lab2_ex5,
)
from qiskit.circuit.library import XGate, YGate
from qiskit.circuit.random import random_circuit
from qiskit.transpiler import InstructionProperties, PassManager, StagedPassManager
from qiskit.transpiler.passes.scheduling import ASAPScheduleAnalysis, PadDynamicalDecoupling
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler.preset_passmanagers.plugin import list_stage_plugins
from qiskit.transpiler.timing_constraints import TimingConstraints
from qiskit.visualization import plot_circuit_layout
from qiskit.visualization.timeline import IQXStandard, draw
from qiskit_ibm_runtime.fake_provider import FakeOsaka, FakeTorino
from util import version_check

os.environ["QXToken"] = API_KEY
version_check()


# %%

""" Exercise 1:
Your Task: Please match the description of what happens in each stage with the corresponding
transpilation stage name in the code cell below.

A. This stage centers around reducing the number of circuit operations and the depth of
circuits with several optimization options.

B. This stage inserts the appropriate number of SWAP gates in order to execute the
circuits using the selected layout.

C. this stage is used to translate any gates that operate on more than two qubits,
into gates that only operate on one or two qubits.

D. This stage executes a sequence of gates, a one-to-one mapping from the "virtual"
qubits to the "physical" qubits in an actual quantum device.

E. this pass can be thought of as explicitly inserting hardware-aware operations like delay
instructions to account for the idle time between gate executions.

F. This stage translates (or unrolls) the gates specified in a circuit to the native basis
gates of a specified backend.

HINT: The answer will always be a single capital letter with quotation marks. For example: "A"
"""
ans = {}

ans["init"] = "C"
ans["layout"] = "D"
ans["routing"] = "B"
ans["translation"] = "F"
ans["optimization"] = "A"
ans["scheduling"] = "E"
# Submit your answer using following code
# %%
# * Grading
grade_lab2_ex1(ans)

# %%
"""Exercise 2: Build a function to evaluate transpiled circuit
Since the goal of transpiling is to improve the actual execution performance of the circuit,
your goal is to create a function that measures the performance of the translated circuit.
You will use this function later in this lab.

Your Task: Create a function called scoring. The function should receives the transpiled circuit,
its final layout, and its target backend as its inputs. The function should then return a
circuit score. The closer the score is to 0, the better.

Other notes:

Please use FakeTorino from the qiskit-ibm-runtime package for this whole lab.
The algorithm for calculating the actual score in util.py is from Mapomatic, and the main code has
been updated to suit PrimitiveV2.
We have constructed some of this function for you.
"""
### Create the scoring function


def scoring(qc, backend):
    from util import transpile_scoring

    # Get the final layout of the transpiled circuit
    layout = qc

    # Compute the fidelity using the transpile_scoring function
    fidelity = transpile_scoring(qc, layout, backend)

    # Calculate the score (you can adjust this calculation as needed)
    score = 1 - fidelity

    return score


# %%
# * Grading
grade_lab2_ex2(scoring)
# %%
""" Now you have a function to measure the performance of a transpiled circuit.
Before we move on to the next part, let's finish setting up everything we need
to properly test our circuit on a fake backend.

Namely, a circuit, and a fake backend!
"""
### Create a random circuit

## DO NOT CHANGE THE SEED NUMBER
seed = 10000

## Create circuit

num_qubits = 6
depth = 4
qc = random_circuit(num_qubits, depth, measure=False, seed=seed)

qc.draw("mpl")

backend = FakeTorino()

circuit_depths = {
    "opt_lv_0": None,
    "opt_lv_1": None,
    "opt_lv_2": None,
    "opt_lv_3": None,
}
gate_counts = {
    "opt_lv_0": None,
    "opt_lv_1": None,
    "opt_lv_2": None,
    "opt_lv_3": None,
}

scores = {
    "opt_lv_0": None,
    "opt_lv_1": None,
    "opt_lv_2": None,
    "opt_lv_3": None,
}
# %%
"""Optimization level = 0
If at any point during these four sections you need help or clarification,
please refer to this documentation for a better understanding of optimization_level.

Optimization level 0 is intended for device characterization experiments
and, as such, only maps the input circuit to the constraints
of the target backend without performing any optimizations.
It performs layout/routing with TrivialLayout, where it selects the same
physical qubit numbers as virtual and inserts SWAPs to make it work (using StochasticSwap).

Let's make a pass manager with optimization level = 0 using our FakeTorino
backend and see the result.
"""
# Make a pass manager with our desired optimization level and backend
pm_lv0 = generate_preset_pass_manager(backend=backend, optimization_level=0, seed_transpiler=seed)

# Run for our random circuit
tr_lv0 = pm_lv0.run(qc)
# %%
"""Exercise 3: (Start)
Your Task: Find the circuit depth of the random circuit, the sum of the total gate number,
and compute the performance score of this circuit using scoring.
Use the provided code to save each of these results to our previously made array.
"""
### Your code here ###

circuit_depths["opt_lv_0"] = tr_lv0.depth()
gate_counts["opt_lv_0"] = sum(tr_lv0.count_ops().values())
scores["opt_lv_0"] = scoring(tr_lv0, backend)

### Don't change code after this line ###

print("Optimization level 0 results")
print("====================")
print("Circuit depth:", circuit_depths["opt_lv_0"])
print("Gate count:", gate_counts["opt_lv_0"])
print("Score:", scores["opt_lv_0"])

# %%
"""Optimization level = 1
Optimization level 1 performs a light optimization. Here's what that means:

- Layout/Routing: Layout is first attempted with TrivialLayout. If additional SWAPs are
required, a layout with a minimum number of SWAPs is found by using SabreSWAP,
then it uses VF2LayoutPostLayout` to try to select the best qubits in the graph.

- InverseCancellation

- 1Q gate optimization

Try making a pass manager on your own this time. Once again use the FakeTorino backend with
generate_preset_pass_manager. Please also set the optimization_level to 1,
and seed_transpiler = seed
"""
# Make a pass manager with our desired optimization level and backend
pm_lv1 = generate_preset_pass_manager(backend=backend, optimization_level=1, seed_transpiler=seed)

# Run for our random circuit
tr_lv1 = pm_lv1.run(qc)


circuit_depths["opt_lv_1"] = tr_lv1.depth()
gate_counts["opt_lv_1"] = sum(tr_lv1.count_ops().values())
scores["opt_lv_1"] = scoring(tr_lv1, backend)

### Don't change code after this line ###

print("Optimization level 1 results")
print("====================")
print("Circuit depth:", circuit_depths["opt_lv_1"])
print("Gate count:", gate_counts["opt_lv_1"])
print("Score:", scores["opt_lv_1"])

# %%
"""Optimization level = 2
Optimization level 2 performs a medium optimization, which means:

- Layout/Routing: Optimization level 1 (without trivial) + heuristic optimized with greater
search depth and trials of optimization function. Because TrivialLayout is not used,
there is no attempt to use the same physical and virtual qubit numbers.

- CommutativeCancellation

Let's make a pass manager with optimization_level of 2 this time,
again using generate_preset_pass_manager with the FakeTorino backend and seed_transpiler = seed.
"""
# Make a pass manager with our desired optimization level and backend
pm_lv2 = generate_preset_pass_manager(backend=backend, optimization_level=2, seed_transpiler=seed)

# Run for our random circuit
tr_lv2 = pm_lv2.run(qc)

circuit_depths["opt_lv_2"] = tr_lv2.depth()
gate_counts["opt_lv_2"] = sum(tr_lv2.count_ops().values())
scores["opt_lv_2"] = scoring(tr_lv2, backend)
### Don't change code after this line ###

print("Optimization level 2 results")
print("====================")
print("Circuit depth:", circuit_depths["opt_lv_2"])
print("Gate count:", gate_counts["opt_lv_2"])
print("Score:", scores["opt_lv_2"])

# %%
"""Optimization level = 3
Optimization level 3 performs a high optimization:

- Optimization level 2 + heuristic optimized on layout/routing further with greater effort/trials

- Resynthesis of two-qubit blocks using Cartan's KAK Decomposition.

- Unitarity-breaking passes: the classical bit of the measure instruction to avoid SWAPs
    - OptimizeSwapBeforeMeasure: Remove swaps in front of measurements by re-targeting
    - RemoveDiagonalGatesBeforeMeasure: Remove diagonal gates (like RZ, T, Z, etc.)
    before a measurement. Including diagonal 2Q gates.

You know what to do next!
"""
pm_lv3 = generate_preset_pass_manager(backend=backend, optimization_level=3, seed_transpiler=seed)

tr_lv3 = pm_lv2.run(qc)

circuit_depths["opt_lv_3"] = tr_lv3.depth()
gate_counts["opt_lv_3"] = sum(tr_lv3.count_ops().values())
scores["opt_lv_3"] = scoring(tr_lv3, backend)

print("Optimization level 3 results")
print("====================")
print("Circuit depth:", circuit_depths["opt_lv_3"])
print("Gate count:", gate_counts["opt_lv_3"])
print("Score:", scores["opt_lv_3"])

# %%
# * Grading
ans = [pm_lv0, pm_lv1, pm_lv2, pm_lv3]

grade_lab2_ex3(ans)
# %%
