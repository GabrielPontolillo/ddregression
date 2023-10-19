import warnings

import numpy as np
from qiskit import QuantumCircuit, Aer
import random
from qiskit.extensions import UnitaryGate
from qiskit.quantum_info import random_statevector, Statevector, Operator

from case_studies.property_based_test_interface import PropertyBasedTestInterface
from dd_regression.assertions.assert_equal import assert_equal, assert_equal_state, measure_qubits, \
    assert_equal_distributions
from dd_regression.helper_functions import get_circuit_register, list_to_circuit

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=DeprecationWarning)

backend = Aer.get_backend('aer_simulator')


class PhaseDifferenceProperty(PropertyBasedTestInterface):
    @staticmethod
    def property_based_test(circuit, inputs_to_generate=25, measurements=1000):
        # print("inside equal output property based test call")
        log = False
        experiments = []

        for i in range(inputs_to_generate):
            # unitary_matrix = [
            #     [1, 1, 1, 1, 1, 1, 1, 1],
            #     [1, ((1 / np.sqrt(2)) + (1j / np.sqrt(2))), 1j, ((-1 / np.sqrt(2)) + (1j / np.sqrt(2))), -1, ((-1 / np.sqrt(2)) + (-1j / np.sqrt(2))), -1j, ((1 / np.sqrt(2)) + (-1j / np.sqrt(2)))],
            #     [1, 1j, -1, -1j, 1, 1j, -1, -1j],
            #     [1, ((-1 / np.sqrt(2)) + (1j / np.sqrt(2))), -1j, ((1 / np.sqrt(2)) + (1j / np.sqrt(2))), -1, ((1 / np.sqrt(2)) + (-1j / np.sqrt(2))), 1j, ((-1 / np.sqrt(2)) + (-1j / np.sqrt(2)))],
            #     [1, -1, 1, -1, 1, -1, 1, -1],
            #     [1, ((-1 / np.sqrt(2)) + (-1j / np.sqrt(2))), 1j, ((1 / np.sqrt(2)) + (-1j / np.sqrt(2))), -1, ((1 / np.sqrt(2)) + (1j / np.sqrt(2))), -1j, ((-1 / np.sqrt(2)) + (1j / np.sqrt(2)))],
            #     [1, -1j, -1, 1j, 1, -1j, -1, 1j],
            #     [1, ((1 / np.sqrt(2)) + (-1j / np.sqrt(2))), -1j, ((-1 / np.sqrt(2)) + (-1j / np.sqrt(2))), -1, ((-1 / np.sqrt(2)) + (1j / np.sqrt(2))), 1j, ((1 / np.sqrt(2)) + (1j / np.sqrt(2)))],
            # ]
            #
            # unitary_matrix = 1/np.sqrt(8)*np.array(unitary_matrix)
            # print(unitary_matrix[1])
            # print(Operator(circuit).data[1])

            # initialize to random state and append the applied delta modified circuit
            qlength, clength = get_circuit_register(circuit)
            init_int = random.randint(0, 7)
            # print(init_int)
            init_vect = np.zeros(8)
            init_vect[init_int] = 1
            shifted_vector = [init_vect[1], init_vect[2], init_vect[3], init_vect[4], init_vect[5], init_vect[6],
                              init_vect[7], init_vect[0]]

            init_state_circuit = QuantumCircuit(qlength)
            init_state_circuit.initialize(init_vect, [2, 1, 0])
            inputted_circuit_to_test = init_state_circuit.compose(circuit)
            phase_shifted_circuit_to_test = PhaseDifferenceProperty.phase_shift(inputted_circuit_to_test)

            up_shifted_circuit = QuantumCircuit(qlength)
            up_shifted_circuit.initialize(shifted_vector, [2, 1, 0])
            up_shifted_circuit_to_test = up_shifted_circuit.compose(circuit)

            if log:
                print(phase_shifted_circuit_to_test.draw(vertical_compression='high', fold=300))
                print(up_shifted_circuit_to_test.draw(vertical_compression='high', fold=300))

            phase_shifted_measurements = measure_qubits(phase_shifted_circuit_to_test, [0, 1, 2], measurements=measurements)
            up_shifted_measurements = measure_qubits(up_shifted_circuit_to_test, [0, 1, 2], measurements=measurements)

            # p_list = assert_equal_distributions(modified_measurements, shifted_measurements)

            if log:
                print(phase_shifted_measurements)
                print(up_shifted_measurements)

            # compare the output of the merged circuit to test, with an empty circuit initialised to expected state
            p_list = assert_equal_distributions(phase_shifted_measurements, up_shifted_measurements)
            if log:
                print(p_list)

            # add a tuple of 3 elements index, initialised vector, p values, measurements
            experiments.append([i, init_vect, (p_list[0], p_list[1], p_list[2], p_list[3], p_list[4], p_list[5], p_list[6], p_list[7], p_list[8]),
                                (phase_shifted_measurements, up_shifted_measurements)])

        return experiments

    # @staticmethod
    # def property_based_test(circuit, inputs_to_generate=25, measurements=1000):
    #     # print("inside equal output property based test call")
    #     experiments = []
    #
    #     for i in range(inputs_to_generate):
    #         print(Operator(circuit))
    #
    #         # initialize to random state and append the applied delta modified circuit
    #         qlength, clength = get_quantum_register(circuit)
    #         circ1 = QuantumCircuit(qlength)
    #         circ2 = QuantumCircuit(qlength)
    #
    #         init_vector = random_statevector(8)
    #         evolved_vector = init_vector.evolve(Operator(circuit))
    #
    #         circ1.initialize(evolved_vector, [0, 1, 2])
    #         inputted_circuit_to_test = circ1
    #
    #         vector_dict = init_vector.to_dict()
    #         shifted_vector = Statevector(
    #             [vector_dict.get('001', 0), vector_dict.get('010', 0), vector_dict.get('011', 0),
    #              vector_dict.get('100', 0), vector_dict.get('101', 0), vector_dict.get('110', 0),
    #              vector_dict.get('111', 0), vector_dict.get('000', 0)])
    #
    #         # shifted_init_state_circuit.initialize(shifted_vector, [0, 1, 2])
    #         shifted_init_state_circuit.initialize(init_vector, [0, 1, 2])
    #         shifted_circuit_to_test = shifted_init_state_circuit.compose(circuit)
    #
    #         base_measurements = measure_qubits(inputted_circuit_to_test, [0, 1, 2], measurements=measurements)
    #         shifted_measurements = measure_qubits(shifted_circuit_to_test, [0, 1, 2], measurements=measurements)
    #
    #         modified_measurements = [
    #             {'z0': base_measurements[0].get('z0'), 'z1': base_measurements[0].get('z1'),
    #              'x1': base_measurements[0].get('x0'), 'x0': base_measurements[0].get('x1'),
    #              'y1': base_measurements[0].get('y0'), 'y0': base_measurements[0].get('y1')},
    #
    #             {'z0': base_measurements[1].get('z0'), 'z1': base_measurements[1].get('z1'),
    #              'x0': base_measurements[1].get('y0'), 'x1': base_measurements[1].get('y1'),
    #              'y0': base_measurements[1].get('x1'), 'y1': base_measurements[1].get('x0')}
    #         ]
    #
    #         # p_list = assert_equal_distributions(modified_measurements, shifted_measurements)
    #
    #         print(base_measurements)
    #         print(shifted_measurements)
    #
    #         # compare the output of the merged circuit to test, with an empty circuit initialised to expected state
    #         # p_value_x, p_value_y, p_value_z, measurements_1, measurements_2 = \
    #         #     assert_equal(inputted_circuit_to_test, 2, qc, 0, measurements=measurements)
    #         #
    #         # # add a tuple of 3 elements index, initialised vector, p values, measurements
    #         # experiments.append([i, init_vector, (p_value_x, p_value_y, p_value_z), (measurements_1, measurements_2)])
    #
    #     return experiments

    @staticmethod
    def verification_heuristic(property_idx, exp_idx, original_failing_circuit, output_distribution, input_state_list,
                               extra_info=None, measurements=1000):
        log = False
        if log:
            print("verification heuristic")

        qlength, clength = get_circuit_register(original_failing_circuit)
        init_state = QuantumCircuit(qlength)

        init_state.initialize(input_state_list, [2, 1, 0])
        inputted_circuit_to_test = init_state.compose(list_to_circuit(original_failing_circuit))
        inputted_circuit_to_test = PhaseDifferenceProperty.phase_shift(inputted_circuit_to_test)

        if log:
            print(inputted_circuit_to_test)

        measurements_1 = measure_qubits(inputted_circuit_to_test, [0, 1, 2], measurements=measurements)

        if log:
            print(measurements_1)
            print(output_distribution)

        p_list = assert_equal_distributions(measurements_1, output_distribution)

        return [property_idx, exp_idx, (p_list[0], p_list[1], p_list[2], p_list[3], p_list[4], p_list[5], p_list[6], p_list[7], p_list[8])]

    @staticmethod
    def phase_shift(qc):
        qc.p(-np.pi/4, 0)
        qc.p(-np.pi/2, 1)
        qc.p(-np.pi/1, 2)
        return qc
