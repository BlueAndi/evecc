# MIT License
#
# Copyright (c) 2021 Andreas Merkle (web@blue-andi.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

################################################################################
# Imports
################################################################################
import logging
import pprint
from pyeasee import Easee, Charger, Site
from enum import Enum

################################################################################
# Variables
################################################################################

_LOGGER = logging.getLogger(__file__)

################################################################################
# Classes
################################################################################

class SysExitStatus(Enum):
    """System exit status codes, which will be returned to the console.
    """
    SUCCESS = 0,
    FAILED = 1

class EVECC:
    """Electric Vehicle Easee Charge Controller
    """
    def __init__(self, username, password, siteKey, circuitKey, powerLimit):
        """Creates a EV Easee charger controller.

        Args:
            username (str): Easee cloud user login name
            password (str): Easee cloud user login password
            siteKey (str): Easee cloud registered site key
            circuitKey (str): Circuit key of the given site
            powerLimit (int): Power limit in W
        """
        self.__username             = username
        self.__password             = password
        self.__siteKey              = siteKey
        self.__circuitKey           = circuitKey
        self.__powerLimit           = powerLimit
        self.__easee                = None
        self.__VOLTAGE              = 230 # [V]
        self.__PHASE_CURRENT_MAX    = 16 # [A]
    
    async def __getSite(self, siteKey):
        """Find the site with the given site key and return it.

        Args:
            siteKey (str): The site key which identifies the site.

        Returns:
            dist: Site information
        """
        foundSite = None

        sites = await self.__easee.get_sites()

        for site in sites:
            if (siteKey == site["siteKey"]):
                foundSite = site
                break
        
        return foundSite

    def __getCircuit(self, site, circuitKey):
        """Find the circuit with the given circuit key in the site and return it.

        Args:
            site (dict): Site information
            circuitKey (str): The circuit key which identifies the circuit.

        Returns:
            dict: Circuit information
        """
        foundCircuit = None

        circuits = site.get_circuits()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(site))

        for circuit in circuits:
            if (circuitKey == circuit["circuitPanelId"]):
                foundCircuit = circuit
                break

        return foundCircuit

    async def __setCircuitPowerLimit(self, circuit, powerLimit):
        """Set the circuit power limit and determines 1 or 3 phase loading.

        Args:
            circuit (dict): Circuit information
            powerLimit (int): Circuit power limit in W
        """
        phasePowerMax       = self.__VOLTAGE * self.__PHASE_CURRENT_MAX
        phase1CurrentLimit  = None
        phase2CurrentLimit  = None
        phase3CurrentLimit  = None

        if (powerLimit >= phasePowerMax):
            phase1CurrentLimit = powerLimit / self.__VOLTAGE
        else:
            phase1CurrentLimit  = powerLimit / (3 * self.__VOLTAGE)
            phase2CurrentLimit  = powerLimit / (3 * self.__VOLTAGE)
            phase3CurrentLimit  = powerLimit / (3 * self.__VOLTAGE)

        await circuit.set_max_current(phase1CurrentLimit, phase2CurrentLimit, phase3CurrentLimit)

    async def run(self):
        """Run the EV Easee charger controller just once and limit charging current.

        Returns:
            int: If successful, it will return 0 otherwise non-zero.
        """
        status = SysExitStatus.SUCCESS
        self.__easee = Easee(self.__username, self.__password)
        site = await self.__getSite(self.__siteKey)

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(vars(site))
        
        if (None == site):
            print("No site with key %s found." % self.__siteKey)
            status = SysExitStatus.FAILED
        else:
            _LOGGER.info("Site: %s", site["createdOn"])
            circuit = self.__getCircuit(site, self.__circuitKey)

            if (None == circuit):
                print("No circuit with key %s found." % self.__circuitKey)
                status = SysExitStatus.FAILED
            else:
                self.__setCircuitPowerLimit(circuit, self.__powerLimit)

        await self.__easee.close()

        return status

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
