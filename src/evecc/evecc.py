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
    def __init__(self, username, password, siteKey, circuitPanelId):
        """Creates a EV Easee charger controller.

        Args:
            username (str): Easee cloud user login name
            password (str): Easee cloud user login password
            siteKey (str): Easee cloud registered site key
            circuitPanelId (int): Circuit panel id of the given site
        """
        self._username          = username
        self._password          = password
        self._siteKey           = siteKey
        self._circuitPanelId    = circuitPanelId
        self._easee             = None
        self._VOLTAGE           = 230 # [V]
        self._PHASE_CURRENT_MAX = 16 # [A]
    
    async def _getSite(self, siteKey):
        """Find the site with the given site key and return it.

        Args:
            siteKey (str): The site key which identifies the site.

        Returns:
            dist: Site information
        """
        foundSite = None

        sites = await self._easee.get_sites()

        for site in sites:
            if (siteKey == site["siteKey"]):
                foundSite = site
                break
        
        return foundSite

    def _getCircuit(self, site, circuitPanelId):
        """Find the circuit with the given circuit panel id in the site and return it.

        Args:
            site (dict): Site information
            circuitPanelId (int): The circuit panel id which identifies the circuit.

        Returns:
            dict: Circuit information
        """
        foundCircuit = None

        circuits = site.get_circuits()

        for circuit in circuits:
            if (circuitPanelId == circuit["circuitPanelId"]):
                foundCircuit = circuit
                break

        return foundCircuit

    def _calcCircuitPowerLimit(self, settings):
        """Calculate the circuit power limit, based on each phase current limitation.

        Args:
            settings (dict): EASEE cloud response

        Returns:
            int: Circuit power limit in W
        """
        phase1PowerLimit = self._VOLTAGE * settings["dynamicCircuitCurrentP1"]
        phase2PowerLimit = self._VOLTAGE * settings["dynamicCircuitCurrentP2"]
        phase3PowerLimit = self._VOLTAGE * settings["dynamicCircuitCurrentP3"]

        return phase1PowerLimit + phase2PowerLimit + phase3PowerLimit

    async def _setCircuitPowerLimit(self, circuit, powerLimit):
        """Set the circuit power limit and determines 1 or 3 phase charging.

        Args:
            circuit (dict): Circuit information
            powerLimit (int): Circuit power limit in W
        """
        phasePowerMax       = self._VOLTAGE * self._PHASE_CURRENT_MAX
        phase1CurrentLimit  = None
        phase2CurrentLimit  = None
        phase3CurrentLimit  = None

        # Charging single phase enough?
        if (powerLimit <= phasePowerMax):
            phase1CurrentLimit = powerLimit / self._VOLTAGE
            phase2CurrentLimit = 0
            phase3CurrentLimit = 0

            print("Single phase loading enabled: %d A" % phase1CurrentLimit)
        else:
            # Charging over all three phases is necessary
            phase1CurrentLimit  = powerLimit / (3 * self._VOLTAGE)
            phase2CurrentLimit  = powerLimit / (3 * self._VOLTAGE)
            phase3CurrentLimit  = powerLimit / (3 * self._VOLTAGE)

            print("Triple phase loading enabled: %d A per phase" % phase1CurrentLimit)

        await circuit.set_dynamic_current(phase1CurrentLimit, phase2CurrentLimit, phase3CurrentLimit)

    async def getCircuitPowerLimit(self):
        status = SysExitStatus.SUCCESS
        settings = None
        circuitPowerLimit = 0

        self._easee = Easee(self._username, self._password)
        site = await self._getSite(self._siteKey)
        
        if (None == site):
            print("No site with key %s found." % self._siteKey)
            status = SysExitStatus.FAILED
        else:
            _LOGGER.info("Site: %s", site["createdOn"])
            circuit = self._getCircuit(site, self._circuitPanelId)

            if (None == circuit):
                print("No circuit with panel id %s found." % self._circuitPanelId)
                status = SysExitStatus.FAILED
            else:
                settings = await (await self._easee.get(f"/api/sites/{site.id}/circuits/{circuit.id}/settings")).json()
                circuitPowerLimit = self._calcCircuitPowerLimit(settings)

        await self._easee.close()

        return status, circuitPowerLimit

    async def setCircuitPowerLimit(self, powerLimit):
        status = SysExitStatus.SUCCESS
        self._easee = Easee(self._username, self._password)
        site = await self._getSite(self._siteKey)
        
        if (None == site):
            print("No site with key %s found." % self._siteKey)
            status = SysExitStatus.FAILED
        else:
            _LOGGER.info("Site: %s", site["createdOn"])
            circuit = self._getCircuit(site, self._circuitPanelId)

            if (None == circuit):
                print("No circuit with panel id %s found." % self._circuitPanelId)
                status = SysExitStatus.FAILED
            else:
                await self._setCircuitPowerLimit(circuit, powerLimit)

        await self._easee.close()

        return status

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
