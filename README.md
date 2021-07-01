Generic Testing Framework
-------------------------

Framework should allow to run separate and collection tests. TODO

Requirements
------------
* Run individual test cases
* Run collection(s) tests
* Calculate the energy on the output files and compare with predefined golden thresholds
* Provide status and report for correspondng test executions

Inputs
------
* Audio files in uncompressed wav format (PCM)
* Some configuration file

Usage
-----


Constrains
----------

* Have ability to run tests in parallel 

Tests
-----

For testing used pytest package as it alread has some good features.
Created wraper on that package to run tests.

Available the following tests:

* test_is_wav_file
* test_file_size_is_not_zero
* test_file_ends_with_wav
* test_compare_energy_value_with_threshold
* test_up_or_down_sampling

Output
------
*Processed audio files in wav format
*Output test report file with following information
**Show which test has been run
**Show status of the execution of the particular test
**Actual vs Expected output
**Information about (detailed) log of execution


