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
    val = inter.alignment(values)
    print('----------------')
    print(val)
    client = ModbusTcpClient("192.168.1.2", port=502)
    return1 = client.write_registers(0x0900,val,1)
    client.close()
    print(return1)
    return True
  except Exception as e:
    print(e)
    return False
  


# x=100
# y=100

# # Write 1 to register 0
# write_detected('',[x,y])

# client.close()

