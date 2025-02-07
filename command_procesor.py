from hardware import *
from time import sleep
import gc

class CoreLink:
    command = []
    
    @classmethod
    def write_command(cls,func,arg):
        cls.command = [func,arg]
    
    @classmethod
    def pop_command(cls):
        buff = cls.command
        self.command = []
        return buff
    
    @classmethod
    def has_command(cls):
        return cls.command != []
    