# <<<<<<< HEAD:ultralytics/LS_Modbus.py
from pymodbus.client import ModbusTcpClient
import pymodbus
import time
import interpolate as inter


# Example usage:

def write_detected(values):
  """Writes multiple registers to the PLC.

  Args:
    client: The Pymodbus client object.
    address: The address of the first register to write to.
    values: A list of values to write to the registers.

  Returns:
    True if the write was successful, False otherwise.
  """

  try:
    print('11111111111111')
    val = inter.alignment(values)
    print('22222222222222')
    print(val)
    print('33333333333333')
    client = ModbusTcpClient("192.168.1.2", port=502)
    print('44444444444444')
    return1 = client.write_registers(0x0009,val,1)
    print(return1)
    print('55555555555555')
    client.close()
    print('66666666666666')
    # print(return1)
    print('77777777777777')
    return True
  except Exception as e:
    print(e)
    return False
  


# x=500
# y=1000

# # Write 1 to register 0
# write_detected([1,x,y])
  