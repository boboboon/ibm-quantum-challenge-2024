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

"""
Exercise 1:
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

    # layout = ##your code here
    # fidelity = transpile_scoring(qc, layout, backend)
    # score = ##your code here

    # return score


# %%
# * Grading
grade_lab2_ex2(scoring)
