hhic (homomorphic hash integrity checker) python package:

This python package aims to realize a possibility to check the integrity of homomorphic ciphers. It uses homomorphic hashes to achieve this goal. Based on this a protocol for data analyzation is possible with multiple parties involved. The protocol is described in the thesis. The package contains of:

-connector.py:            TLS Handshake for data distribution.

-hh.py (homomorphic hash): Library to hash plaintexts. Hashes are homomorphically 
                           additive.

-tools.py:                 All necessary tools to realize the protocol of the thesis.

The tools library uses another external library ’phe’ (paillier homomorphic encryption), which should have been installed after installing this package.

To see if this package is installed properly run all three demos given in the demo folder. For this simply run one demo after another. To run the demos successfully simulator.py has to be executed every time in another shell/terminal. It simulates a network connection on localhost.

For Demo1 run:

python3 demo1.py     (terminal 1)
python3 simulator.py (terminal 2)

Demo1 contains of a small database which uses log1.txt. To see, if the package was installed correctly, the result in the end must be: 1400 and 2202. (Example for legal operation).


For Demo2 run:

python3 demo2.py     (terminal 1)
python3 simulator.py (terminal 2)

Demo2 contains of a medium database which uses log2.txt. To see, if the package was installed correctly, the result in the end must be: None and None. (Example for illegal operation).

For Demo3 run:

python3 demo3.py     (terminal 1)
python3 simulator.py (terminal 2)

Demo3 contains of a large database which uses log3.txt. To see, if the package was installed correctly, the result in the end must be: 347742 and 342391. It is the same as demo1, just with more than 50times more plaintexts. This is to show the differences in complexity.

Own log files can be used, when correct format is kept. Correct format:

ID A B C
1 a b c
2 d e f
. . . .
.
.
.


Important is, that ID has to be continued from 1 to n. Between every value is only one space. After the last value needs to be a newline without any spaces in between.
Last line should not be empty!