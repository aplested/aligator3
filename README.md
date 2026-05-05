Python 3 revision of Aligator, including a bug fix for the microscopic reversibility code
2026-05-04

```
python3 aligator.py
```

For doing Realistic Concentration Jumps, use the script rcj.py

Install miniconda then issue:
```
conda create -n rcj
conda activate rcj
conda install numpy
```
Navigate to the directory where the Aligator scripts are and issue:

```
python3 rcj.py
```

The script will automatically scan the subdirectory "tests" for any mechanism files to simulate. The file dck_d_rcjm.txt is provided for this purpose. 

_rcjm.txt files are used for input to specify the receptor mechanism and will be handled automatically.

Further examples of input files (one other rcjm and one HJCFIT .prt file) are provided in the input_files directory

Alter values in rcj.py script to change parameters.

See file rcj_instructions.txt for more details.
