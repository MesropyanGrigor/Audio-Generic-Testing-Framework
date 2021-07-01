Generic Testing Framework
-------------------------

Framework should allow to run separate and collection tests. 
For that purpose I used pytest framework as it has many features already
and has many plugins which can be adopted.(ex. pytest-html, to generate html report)
TODO

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
usage: tester.py [-h] [-config CONFIG] [-np NP] [-l] [-log LOG] [-filter FILTER [FILTER ...]] [-files [FILES [FILES ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -config CONFIG        Config file path
  -np NP                Running in parallel mode, using provided value as number of cores
  -l                    Show available tests
  -log LOG              Keep pytest output into that log file
  -filter FILTER [FILTER ...]
                        Running tests by defined patterns
  -files [FILES [FILES ...]]
                        files paths or files path paterns


Examples
--------
* python tester.py -l # will show all available tests

*  python .\tester.py -n 8 -filter "test_up_or_down_sampling" # will run only tests which names have "test_up_or_down_sampling" word in 8 processes

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


