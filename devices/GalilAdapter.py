import asyncio

import gclib.gclib as gclib
from .GalilAxis import GalilAxis

class GalilAdapter:
    """Interface adapter between application and galil"""
    def __init__(self, address: str,
                 axis_names: dict[str, str]) -> None:
        """Set up adapter with all devices' axes visible from controller

        Args:
            address: IP address of controller as string, e.g. "192.168.1.19"
            axis_names: mapping of name to axis channel identifier
                e.g. {"gimbal 1 elevation": "A", "gimbal 2 azimuth": "D"}
        """

        self.address = address
        self.axis_names = axis_names
        self.axes: dict[str, GalilAxis] = {}
        
        print("Connecting to Galil devices... ", end='')
        self.g = gclib.py()
        self.g.GOpen(self.address + " -s ALL")
        print("connected.")
        
        for a_nm, a_ch in self.axis_names.items():
            print("Finding " + a_nm + " (" + a_ch + ")... ", end='')
            try:
                # test if we can get the axis position
                self.g.GCommand("TP{}".format(a_ch))
                self.axes[a_nm] = GalilAxis(a_nm, a_ch, self.g)
                print("OK.")
            except gclib.GclibError:
                print("not found.") # device not found
            except Exception as e:
                print(e) # can't make Axis, other errors

    @property
    def connection(self):
        return self.g

    async def update(self):
        """Update all devices on this adapter"""
        pass

    async def update_loop(self, interval: float = 1):
        """Update self in a loop
                
        interval: time in seconds between updates
        """
        while True:
           await asyncio.gather(self.update(), asyncio.sleep(interval))
