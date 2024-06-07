#%%
"""First Qiskit Tests."""
import os

from config import API_KEY
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp

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

# The ZZ applies a Z operator on qubit 0, and a Z operator on qubit 1
ZZ = SparsePauliOp("ZZ")

# The ZI applies a Z operator on qubit 0, and an Identity operator on qubit 1
ZI = SparsePauliOp("ZI")

# The IX applies an Identity operator on qubit 0, and an X operator on qubit 1
IX = SparsePauliOp("IX")



### Write your code below here ###
### Follow the same naming convention we used above



## Don't change any code past this line, but remember to run the cell.

#observables = [IZ, IX, ZI, XI, ZZ, XX]
# %%
