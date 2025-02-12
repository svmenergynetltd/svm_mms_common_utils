# SVM MMS Common Utilities

This repository contains common utilities for the SVM MMS project. The utilities are written in Python and are used to perform various tasks such as reading configuration files, logging, etc.

## Installation

1. Include this repository as a submodule in your project.
   ```bash
   git submodule add https://github.com/svmenergynetltd/svm_mms_common_utils
   ```
2. Add the following line to your project's `requirements.txt` file:
   ```
   -e ./svm-mms-common-utilities
   ```
3. Also include the [svm_mms_xml](https://github.com/svmenergynetltd/svm_mms_xml) repository as a submodule in your project.
4. Add the following line to your project's `requirements.txt` file:
   ```
   -e ./svm-mms-xml
   ```
5. import any needed utility from the `svm_mms_common_utilities` package in your project.
   ```python
   from svm_mms_common_utils.constants import MMS_CONSTANTS
   ```
