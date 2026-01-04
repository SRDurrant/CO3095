# CO3095
## Software Measurement and Quality Assurance
### School Evaluation Platform (CO3095)

# School Evaluation Platform (CO3095)

This repository contains the **School Evaluation Platform**, a text-based backend system implemented in **Python** for the **CO3095 – Software Measurement and Quality Assurance** module.

The system supports authentication, school browsing and search, ratings and reviews, favourites, role-based administrative functionality, and JSON-based persistence. A comprehensive automated test suite is included, covering **black-box**, **white-box**, **symbolic**, and **concolic** testing techniques as required by the assignment specification.

---

## Contents
1. Loading the project on a Charles Wilson laboratory PC  
2. Uncompressing the submission ZIP  
3. Prerequisites  
4. Environment setup  
5. Running the application  
6. Running all test cases  
7. Running tests by directory 
8. Running coverage measurement  
9. Persistence behaviour  
10. Public GitHub repository

---

## 1. Loading the project on a Charles Wilson laboratory PC

### Option A – Using the public GitHub repository
1. Open **PowerShell**.
2. Navigate to a writable location:
   ```bash
   cd Desktop
3. Clone the respository:
    ```bash
   git clone https://github.com/SRDurrant/CO3095.git
4. Enter the project directory:
    ```bash
   cd SM&QA_Project

### Option B - Using the submitted ZIP file
1. Copy the ZIP file to the lab PC
2. Follow the extraction steps below

## 2. Uncompressing the submission ZIP (Windows)
1. Right-click the ZIP file
2. Select Extract All...
3. Choose a destination 
4. Open the extracted folder

You Should see:
- app/
- tests/
- README.md

## 3. Prerequisites
### Required Software
- Python 3.10 or later
- pip

Verify Python:
```bash
python --version
pip --version
```

## 4. Environment Setup
### 4.1 Create an environment 
From the project root directory:
```bash
python -m venv .venv
```
Activate it:
```bash
.\.venv\Scripts\Activate.ps1
```

### 4.2 Install dependencies
```bash
pip install pytest coverage
```

## 5. Running the Application
Go onto the main.py file, there should be __main__ at the bottom of the file. This should then run the main system.

## 6. Running all test cases
To run every test in the project:
```bash
pytest -v
```

## 7. Running Tests by directory
The test suite is structured by team member and testing technique. Running tests by directory path is the most reliable method.

Run all tests for a team member:
```bash
pytest tests/DD264
pytest tests/PJ143
pytest tests/TJ129
pytest tests/SD611
```
Run all black-box tests
```bash
pytest tests/DD264/blackbox
pytest tests/PJ143/blackbox
pytest tests/TJ129/blackbox
pytest tests/SD611/blackbox
```

run all white-box test
```bash
pytest tests/DD264/whitebox
pytest tests/PJ143/whitebox
pytest tests/TJ129/whitebox
pytest tests/SD611/whitebox
```

### Run specific white-box techniques
Branch-based tests
```bash
pytest tests/DD264/whitebox/branch_based
pytest tests/PJ143/whitebox/branch_based
pytest tests/TJ129/whitebox/branch_based
pytest tests/SD611/whitebox/branch_based
```

Symbolic execution tests
```bash
pytest tests/DD264/whitebox/symbolic_execution
pytest tests/PJ143/whitebox/symbolic_execution
pytest tests/TJ129/whitebox/symbolic_execution
pytest tests/SD611/whitebox/symbolic_execution
```
Concolic testing
```bash
pytest tests/DD264/whitebox/concolic_testing
pytest tests/PJ143/whitebox/concolic_testing
pytest tests/TJ129/whitebox/concolic_testing
pytest tests/SD611/whitebox/concolic_testing
```

Run specification-based black-box tests
```bash
pytest tests/DD264/blackbox/specification_based
pytest tests/PJ143/blackbox/specification_based
pytest tests/TJ129/blackbox/specification_based
pytest tests/SD611/blackbox/specification_based
```

Run boundary value tests
```bash
pytest tests/DD264/blackbox/boundary_value
pytest tests/PJ143/blackbox/boundary_value
pytest tests/TJ129/blackbox/boundary_value
pytest tests/SD611/blackbox/boundary_value
```

Run random-based tests
```bash
pytest tests/DD264/blackbox/random_based
pytest tests/PJ143/blackbox/random_based
pytest tests/TJ129/blackbox/random_based
pytest tests/SD611/blackbox/random_based
```
## 8. Test Coverage Measurement
Run coverage with pytest
```bash
coverage run -m pytest
coverage report -m
```

Generate HTML Coverage Report
```bash
coverage html
```

Then Open:
```bash
htmlcov/index.html
```

## 9. Persistence Behaviour
- The system uses JSON-based file persistence
- The save file does not exist by default
- It is created only after the system runs and saves
- if not file exists, the system starts with in-memory defaults
- Auto-save and Auto-load are triggered by system lifecycle logic (US40)

You may safely delete the JSON file between runs to reset the system state

## 10. Public GitHub Repository

https://github.com/SRDurrant/CO3095.git

Contains:
- full source code
- test suite
- commit history
- documentation