#%%
"""First Qiskit Tests."""
import os

import matplotlib.pyplot as plt
from config import API_KEY
from qc_grader.challenges.iqc_2024 import grade_lab0_ex1
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import EstimatorV2 as Estimator

#%%
os.environ["QXToken"] = API_KEY  # noqa: SIM112
#%%
#? Initial Quantum Circuit
qc = QuantumCircuit(1)

qc.x(0)

qc.draw()
# %%
#? Step 1: Map circuits and operators <a name="step-1"></a>
qc = QuantumCircuit(2)

qc.h(0)

qc.cx(0, 1)

#%%%
#? Exercise 1


ZZ = SparsePauliOp("ZZ")
ZI = SparsePauliOp("ZI")
IX = SparsePauliOp("IX")
IZ = SparsePauliOp("IZ")
XI = SparsePauliOp("XI")
XX = SparsePauliOp("XX")

### Follow the same naming convention we used above



## Don't change any code past this line, but remember to run the cell.

observables = [IZ, IX, ZI, XI, ZZ, XX]
# %%
grade_lab0_ex1(observables)
# %%
# Set up the Estimator
estimator = Estimator(backend=AerSimulator()) # type: ignore

# Submit the circuit to Estimator
pub = (qc, observables)

job = estimator.run(pubs=[pub])
#%%
data = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
values = job.result()[0].data.evs

# Set up our graph
container = plt.plot(data, values, "-o")

# Label each axis
plt.xlabel("Observables")
plt.ylabel("Values")
# %%
