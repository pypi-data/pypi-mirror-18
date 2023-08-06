import copy
import os
import sys
from threading import RLock

from microtools.di import DiTools

_services={}  # type: dict[str, classobj]
_packages={}  # type: dict[str, classobj]

class Scope(object):
    def __init__(self):
        self.__objects={}
        self.__instances={}
        self.scopeLock=RLock()

    def get(self, name):
        self.scopeLock.acquire()
        try:
            name = DiTools.getSimpleClassNameFromObject(name)
            return self.__objects[name]
        finally:
            self.scopeLock.release()

    def registerService(self, name, service):
        name = DiTools.getSimpleClassNameFromObject(name)
        self.scopeLock.acquire()
        try:
            if name in self.__objects:
                raise Exception("Error, service {name} already exists".format(name=name))
            self.__objects[name] = service
        finally:
            self.scopeLock.release()

    def getInstance(self, name):
        name = DiTools.getSimpleClassNameFromObject(name)
        if name in self.__instances:
            return self.__instances[name]
        self.scopeLock.acquire()
        if not name in self.__instances:
            self.__instances[name] = self.__objects[name]()
            self.__instances[name].__scope = self
        self.scopeLock.release()
        return self.__instances[name]

    def registerInstance(self, name, instance):
        name = DiTools.getSimpleClassNameFromObject(name)
        if name in self.__instances:
            raise Exception("Error, instance for {name} already exists".format(name=name))
        self.__instances[name] = instance
        self.__instances[name].__scope = self

    def cloneScope(self):
        scope = Scope()
        self.scopeLock.acquire()
        try:
            scope.__objects = copy.copy(self.__objects)
        finally:
            self.scopeLock.release()
        return scope

class Locator(object):
    @staticmethod
    def registerService(scopeHolder, service=None):
        DiTools.getScope(scopeHolder).registerService(service, service)

    @staticmethod
    def registerInstance(scopeHolder, instance, name=None):
        DiTools.getScope(scopeHolder).registerInstance(name or instance.__class__, instance)

    @staticmethod
    def getInstance(scopeHolder, service):
        return DiTools.getScope(scopeHolder).getInstance(service)

def InjectClass(**kwargs_):
    def decorator(cls):
        old = None
        def injectedConstructor(*args, **kwargs):
            for name in kwargs_:
                setattr(args[0], name, Locator.getInstance(kwargs_[name]))
            return old(*args, **kwargs)
        old = cls.__init__
        cls.__init__ = injectedConstructor
        return cls
    return decorator

def Inject(**kwargss):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for arg in kwargss:
                kwargs[arg] = Locator.getInstance(kwargss[arg])
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def Service():
    def decorator(cls):
        _services[DiTools.getObjectPackage(cls)] = cls
        return cls
    return decorator