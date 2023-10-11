# Delta Debugging for the Regression testing of quantum programs.

### Repository layout and description:

- **case_studies** (package): Contains experiment set-ups (passing and failing versions of a quantum algorithm, property based test oracle, regression tests) for each quantum algorithm being tested.
    - **(name_of_algorithm)** (package): Contains files relating to an algorithm.
        - ***oracle.py**: Contains an oracle that evaluates multiple properties, verifies the properties to identify inconclusive outcomes, and performs the Holm-Bonferroni correction to correct the error rate due to running multiple statistical tests.
        - ***property.py**: Contains an individual property based test, which contains to components: A method to run the property based test to evaluate the property, and a method to verify whether an observed failure is the same as the original failure.
        - **(name_of_algorithm).py**: Contains passing and failing versions of the algorithm, regression test, test function that calls the oracle, main method that runs the case with multiple configurations.
        
    - **case_study_interface.py**: The interface that is implementeed by (name_of_algorithm.py) files, contains code to run the case study experiment and store the results to a file, as well as describes expected methods for each case study.
    - **property_based_test_interface.py**: The interface that is implemented by *property.py files, describes the two methods that are expected to be contained within proeprty based test files.
    - **property_based_test_oracle_interface.py**: The interface that is implemented by *oracle.py files, describes the structure of property based test oracles.
    
- **dd_regression** (package): Contains all code related to the execution of delta debugging, property based testing, and diffing
    - **assertions.py**: Contains statistical assertions that may be called within property based tests.
    - **dd_algorithm.py**: Contains the delta debugging algorithm, and related functions.
    - **diff_algorithm.py**: Contains the diffing algorithm, as well as an algorithm to apply diffs to a circuit, and classes for each diff type: Addition, Removal.
    - **helper_functions.py**: Contains loose function that may be used throughout the project.
    - **result_classes.py**: Contains classes for property based test oracle outcomes: Passed, Failed and Inconclusive. 