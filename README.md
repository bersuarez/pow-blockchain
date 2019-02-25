# POW Blockchain demonstration
This is a flask based blockchain that makes use of the following concepts:
* Coin minting
* Mining
* Transaction and block hashing for Proof of Work
* Chain validation to prevent unauthorized block addition, modification and deletion
* Transaction signing
* Blockchain file creation
* Wallet creation and use with a UI
* Node network:
    *Node creation, connection and consensus

## Usage
Currently the blockchain has to be used locally, so the project has to be cloned (it will soon be running on a public server). 
The file `node.py` handles the flask application and creates the routing for all the functions. Running `python3 node.py` on the command shell starts up a local server to be accesed via a browser at `localhost:5000`.

### Dependencies
This project relies on some packages and libraries which can be installed using `pip3 install` or by using a package manager like `Anaconda` by creating a virtual environment which contains the packages and running `source active NAME_OF_ENVIRONMENT` before running `node.py`.
* flask : webserver framework
* pycrypto : generate RSA key pairs

## Relevant files and functions
This project is object-based and divided amongst functions and classes. The most important classes are the following:
* Blockchain: Specified in `blockchain.py`, manages the chain of blocks as well as open transaction and the node on which it's running.
* Block: Specified in `block.py`, used for creation of singles blocks of the blockchain
* Transaction: Specified in `transaction.py`, used for transaction creation and helps to add them to blocks
* Wallet: Specified in `wallet.py`, manages key creation, saving, loading, transaction signing and verification
 
Another important file is a utility file called `verification.py`, which contains several verification and validation methods including the POW mining proof

## Known bugs 
None at the moment

## Next steps
* Add mining process visibility
* Dynamic mining difficulty and reward
* Migrating blockchain file to database
* Async broadcasting
* Merkle Tree to scale validation
* Improve error handling
## License
MIT License

Copyright (c) 2019 Bernardo Suárez Sepúlveda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
