import warnings

from qiskit import QuantumCircuit, Aer
from qiskit.quantum_info import random_statevector, random_unitary

from case_studies.property_based_test_interface import PropertyBasedTestInterface
from dd_regression.assertions.statistical_analysis import assert_equal, assert_equal_state
from dd_regression.helper_functions import get_circuit_register, list_to_circuit

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

backend = Aer.get_backend('aer_simulator')


class DifferentPathsSameOutcomeProperty(PropertyBasedTestInterface):
    @staticmethod
    def property_based_test(circuit, inputs_to_generate=25, measurements=1000):
        # print("inside equal output property based test call")
        experiments = []

        for i in range(inputs_to_generate):
            # initialize to random state and append the applied delta modified circuit
            operator = random_unitary(2)
            # print(operator)

            qlength, clength = get_circuit_register(circuit)
            init_state = QuantumCircuit(qlength)
            init_vector = random_statevector(2)
            init_state.initialize(init_vector, 0)
            init_state.unitary(operator, 0)
            inputted_circuit_to_test = init_state.compose(circuit)

            # create a new circuit with just state initialization to compare with
            qlength, clength = get_circuit_register(circuit)
            qc = QuantumCircuit(qlength)
            qc.initialize(init_vector, 0)
            qc = qc.compose(circuit)
            qc.unitary(operator, 2)

            # print(inputted_circuit_to_test)
            # print(qc)

            # compare the output of the merged circuit to test, with an empty circuit initialised to expected state
            p_value_x, p_value_y, p_value_z, measurements_1, measurements_2 = \
                assert_equal(inputted_circuit_to_test, 2, qc, 2, measurements=measurements)

            # print(measurements_1)
            # print(measurements_2)

            # add a tuple of 3 elements index, initialised vector, p values, measurements
            experiments.append([i, init_vector, (p_value_x, p_value_y, p_value_z), (measurements_1, measurements_2),
                                operator])

        return experiments

    @staticmethod
    def verification_heuristic(property_idx, exp_idx, original_failing_circuit, output_distribution, input_state_list,
                               extra_info=None, measurements=1000):
        # print(extra_info)

        qlength, clength = get_circuit_register(original_failing_circuit)
        init_state = QuantumCircuit(qlength)

        init_state.initialize(input_state_list, 0)
        init_state.unitary(extra_info[0], 0)
        inputted_circuit_to_test = init_state.compose(list_to_circuit(original_failing_circuit))

        p_value_x, p_value_y, p_value_z, _, _ = assert_equal_state(inputted_circuit_to_test, 2, output_distribution,
                                                                   measurements=measurements)

        return [property_idx, exp_idx, (p_value_x, p_value_y, p_value_z)]
