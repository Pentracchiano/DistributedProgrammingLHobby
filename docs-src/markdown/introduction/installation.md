# Installation

## Get the source code

First of all, clone the [LHobby repository](https://github.com/Pentracchiano/DistributedProgrammingLHobby) from github into your system.


```bash
git clone https://github.com/Pentracchiano/DistributedProgrammingLHobby.git
```

## Dependencies

Two `requirements.txt` files are provided to install the dependencies. One is related to server dependencies and the other is
related to client dependencies.

It is recommended, not necessary, to install the dependencies into a [python virtual environment](https://docs.python.org/3/library/venv.html).

!!! note Python version
    The code has been tested only with `Python 3.6` and `Python 3.7`.

First of all create the virtual environment (you can skip this procedure).

```bash

python3 -m venv venv

```

From the same folder you executed the previous command, activate the python environment.

=== "Windows"

    ```
    
    venv\Scripts\activate
    
    ```

=== "Linux/macOS"

    ```bash
    
    source venv/bin/activate  # sh, bash, or zsh
    
    . ./venv/bin/activate.fish  # fish
    
    source venv/bin/activate.csh  # csh or tcsh
        
    ```

!!! note
    
    To deactivate the virtual environment simply launch `deactivate` into a shell


Install the server dependencies.



#####


