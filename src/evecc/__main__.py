#!/usr/bin/env python

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
import sys
import asyncio
from .argParser import ArgParser
from .evecc import EVECC

################################################################################
# Variables
################################################################################

_LOGGER = logging.getLogger(__file__)

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

def main():
    """The program entry point function.

    Returns:
        int: System exit status
    """
    status      = 0
    argParser   = ArgParser()

    logging.basicConfig(
        format="%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s",
        level=argParser.getArgs().loglevel,
    )

    _LOGGER.debug("args: %s", argParser.getArgs())

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    evecc = EVECC(
        argParser.getArgs().username,
        argParser.getArgs().password,
        argParser.getArgs().siteKey,
        argParser.getArgs().circuitPanelId
    )

    if ("getCircuitPowerLimit" == argParser.getArgs().cmd):
        status, circuitPowerLimit = asyncio.run(evecc.getCircuitPowerLimit())
        print(circuitPowerLimit)
    elif ("setCircuitPowerLimit" == argParser.getArgs().cmd):
        status = asyncio.run(evecc.setCircuitPowerLimit(argParser.getArgs().circuitPowerLimit[0]))
    else:
        print("Command is missing.")
        status = 1

    return status

################################################################################
# Main
################################################################################

if ("__main__" == __name__):
    sys.exit(main())
