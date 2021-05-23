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
import argparse

################################################################################
# Variables
################################################################################

################################################################################
# Classes
################################################################################

class ArgParser():
    """Parses all program arguments according to its configuration.
    """

    def __init__(self):
        """Configure parser and parse program arguments.
        """
        self._parser = self._createParser()
        self._args = self._parser.parse_args()

    def _createParser(self):
        mainParser = self._createMainParser()
        subParsers = mainParser.add_subparsers(dest="cmd")
        self._createGetCircuitPowerLimitSubParser(subParsers)
        self._createSetCircuitPowerLimitSubParser(subParsers)

        return mainParser

    def _createMainParser(self):
        mainParser = argparse.ArgumentParser(description="Electric Vehicle Easee Charge Controller (EVECC)")
        mainParser.set_defaults(which="")

        # Arguments in alphabetic ascending order
        mainParser.add_argument(
            "-cpi",
            "--circuitPanelId",
            help="Circuit panel id of the given site, see in your Easee cloud account.",
            type=int,
            required=True
        )
        mainParser.add_argument(
            "-d",
            "--debug",
            help="Print debugging statements.",
            action="store_const",
            dest="loglevel",
            const=logging.DEBUG,
            default=logging.WARNING,
        )
        mainParser.add_argument(
            "-p",
            "--password",
            help="Login user account password.",
            type=str,
            required=True
        )
        mainParser.add_argument(
            "-sk",
            "--siteKey",
            help="Site key, see in your Easee cloud account.",
            type=str,
            required=True
        )
        mainParser.add_argument(
            "-u",
            "--username",
            help="Login user account name.",
            type=str,
            required=True
        )
        mainParser.add_argument(
            "-v",
            "--verbose",
            help="Be verbose.",
            action="store_const",
            dest="loglevel",
            const=logging.INFO,
        )

        return mainParser

    def _createGetCircuitPowerLimitSubParser(self, subParsers):
        subParsers.add_parser(
            "getCircuitPowerLimit",
            help="Get the circuit power limit."
        )

    def _createSetCircuitPowerLimitSubParser(self, subParsers):
        parser = subParsers.add_parser(
            "setCircuitPowerLimit",
            help="Set the circuit power limit."
        )
        parser.add_argument(
            "circuitPowerLimit",
            metavar="P",
            type=int,
            nargs=1,
            help="Circuit power limit in W"
        )

    def getArgs(self):
        """Get parsed arguments.

        Returns:
            dict: Arguments
        """
        return self._args

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################
