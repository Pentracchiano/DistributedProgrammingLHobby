# LHobby

## Scope

This repository contains the code and the documentation of the final project for the Distributed Programming class 2020/21 of 
University of Salerno. The project intends to demonstrate and put to practice the knowledge acquired during the course. 

### Group

This project was made by group 7, composed by:

| __Name__    | __ID__      | __E-mail__  |
| ----------- | ----------- | ----------- |
| Davide Cafaro| 0622701062 | d.cafaro4@studenti.unisa.it|
| Emanuele D'Arminio | 0622701059 | e.darminio4@studenti.unisa.it|
| Marta Silla | 0622701337 | m.silla@studenti.unisa.it|


### Documentation

The full documentation can be read at [this link](https://pentracchiano.github.io/DistributedProgrammingLHobby/) directly online.

#### Building the documentation
The documentation can also be built using the [mkdocs](https://www.mkdocs.org/) utility.
Firstly, install it launching:

```bash
pip install mkdocs mkdocs-material
```

Then, you can build the static site with the files in `docs-src/` using the command:

```bash
mkdocs build
```

Then it is possible to navigate the documentation by accessing it in the `site/` directory with your favorite browser.
Alternatively, it is also possible to run:

```bash
mkdocs serve
```

which will launch a lightweight server on localhost on the port 8000, serving the documentation of the project.
