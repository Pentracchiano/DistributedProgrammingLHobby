# Installation

## Get the source code

First of all, clone the [LHobby repository](https://github.com/Pentracchiano/DistributedProgrammingLHobby) from github into your system.


```bash
git clone https://github.com/Pentracchiano/DistributedProgrammingLHobby.git
```

## Install Dependencies

Two `requirements.txt` files are provided to install the dependencies. One is related to server dependencies and the other is
related to client dependencies.

It is recommended, not necessary, to install the dependencies into a [python virtual environment](https://docs.python.org/3/library/venv.html).

!!! info Python version
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

!!! tip
    
    To deactivate the virtual environment, simply launch `deactivate` into a shell.


Now you should navigate into the project directory.

```bash

cd DistributedProgrammingLHobby

```

Install the server dependencies.

```bash

pip install -r requirements.txt

```

If you want to test the client built for the project you must also install the client dependencies.

=== "Windows"
    ```
    
    pip install -r client\requirements.txt 
    
    ```
=== "Linux/macOS"
    ```bash
    
    pip install -r client/requirements.txt
    
    ```
    
After the installation, you are ready to discover how to use LHobby. Go to the next section for usage documentation. 


