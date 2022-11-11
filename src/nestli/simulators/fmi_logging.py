from ctypes import *
from fmpy.fmi2 import (
    fmi2CallbackFunctions,
    fmi2CallbackLoggerTYPE,
    fmi2CallbackAllocateMemoryTYPE,
    fmi2CallbackFreeMemoryTYPE,
)
from fmpy import free, calloc


def printLogMessage(component, instanceName, status, category, message):
    pass


def get_callbacks_logger(console=False):
    if console:
        return None
    callbacks = fmi2CallbackFunctions()
    callbacks.logger = fmi2CallbackLoggerTYPE(printLogMessage)
    callbacks.allocateMemory = fmi2CallbackAllocateMemoryTYPE(calloc)
    callbacks.freeMemory = fmi2CallbackFreeMemoryTYPE(free)
    return callbacks
