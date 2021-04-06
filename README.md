# evecc
Electric Vehicle Easee Charge Controller

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://choosealicense.com/licenses/mit/)
[![Repo Status](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# Purpose
The idea is to drive the electric vehicle charging according to the available solar power.

The EVECC just limits the charging current of the site circuit. A circuit may have one or more chargers. For most users a circuit will have just one charger.

Currently its just a small script, but may change in the future.

Its a early bird! I couldn't test it completly, because my chargers are not registered in the Easee cloud yet. Hopefully it will change in the upcoming weeks.

# Overview
![Overview](http://www.plantuml.com/plantuml/proxy?idx=0&src=https://raw.github.com/BlueAndi/evecc/master/doc/principle.plantuml)

# Design

Possible ways to influence the charging current:
* Per charger
    * maxChargerCurrent
        * Stored non-volatile, which means will survive a powerloss.
        * ```/api/chargers/{id}/settings```
        * Max. access frequcency: 20 requests per minute.
    * dynamicChargerCurrent
        * Stored volatile, which means will not survice a powerloss.
        * ```/api/chargers/{id}/settings```
        * Max. access frequcency: 20 requests per minute.
* Per circuit
    * maxCircuitCurrent{phase}
        * Stored non-volatile, which means will survive a powerloss.
        * ```/api/sites/{siteId}/circuits/{circuitId}/settings```
        * Max. access frequcency: 20 requests per minute.
    * dynamicCircuitCurrent{phase}
        * Stored volatile, which means will not survice a powerloss.
        * ```/api/sites/{siteId}/circuits/{circuitId}/settings```
        * Max. access frequcency: 20 requests per minute.
        * **Used by EVECC.**

# Installation
```cmd
$ git clone https://github.com/BlueAndi/evecc.git
$ cd evecc
$ python setup.py install
```

# Usage

Show help information:
```cmd
$ evecc --help
```

Limit charging power, e.g. to 3.6kW:
```cmd
$ evecc --username <username> --password <password> --siteKey <site-key> --circuitKey <circuit-key> --powerLimit 3600
```

If the power limit is lower or equal than 3.6kW, charging will be done via single phase otherwise with all 3 phases.

# Setup Development Toolchain
* Install [python 3.9.x](https://www.python.org/)
* Ensure pip, setuptools and wheel are up to date:
```cmd
$ python -m pip install --upgrade pip setuptools wheel
```

# Informations about Easee Charger
* [Official Easee Homepage (eng. variant)](https://easee-international.com/uk/)
* [Easee Cloud REST API](https://api.easee.cloud/index.html)

# Used Libraries
* [Easee EV Charger library](https://github.com/fondberg/pyeasee) - MIT License

# Issues, Ideas And Bugs
If you have further ideas or you found some bugs, great! Create a [issue](https://github.com/BlueAndi/evecc/issues) or if you are able and willing to fix it by yourself, clone the repository and create a pull request.

# License
The whole source code is published under the [MIT license](http://choosealicense.com/licenses/mit/).
Consider the different licenses of the used third party libraries too!

# Contribution
Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, shall be licensed as above, without any additional terms or conditions.
