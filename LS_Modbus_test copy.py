# <<<<<<< HEAD:ultralytics/LS_Modbus.py
from pymodbus.client import ModbusTcpClient
import pymodbus
import time
import interpolate as inter


# Example usage:

def write_detected(values, client):
  """Writes multiple registers to the PLC.

  Args:
    client: The Pymodbus client object.
    address: The address of the first register to write to.
    values: A list of values to write to the registers.

  Returns:
    True if the write was successful, False otherwise.
  """

  try:
    val = inter.alignment(values)
    if val == [0, 0, 0]:
      return1 = client.write_registers(0x0009,[0, 0, 0],1)
    else:
      return1 = client.write_registers(0x0009,val,1)
    return True
  except Exception as e:
    print(e)
    return False
  


  