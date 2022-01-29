# centralized-blockchain
A Centralized Blockchain Implementation using remote procedure call (RPC).

# requirements

    pip install pyro4

# run 

Run the followings in SEPERATE terminals.

    python BTCServer.py

    python ETCServer.py

    python firstClient.py

    python secondClient.py

# implementation notes

First you should run this on terminal, otherwise serialization errors may arise:

    export PYRO_SERIALIZERS_ACCEPTED=serpent,json,marshal,pickle

    pyro4-ns

# specifications

Please click [here](https://github.com/alaattinyilmaz/centralized-blockchain/blob/main/centralized-blockchain-specs.pdf) link to read all spesifications.
