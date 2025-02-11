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
    print('11111111111111')
    val = inter.alignment(values)
    print('22222222222222')
    print(val)
    print('33333333333333')
    # client = ModbusTcpClient("192.168.1.2", port=502)
    print('44444444444444')
    if val == [0, 0, 0]:
      # print('44444444444444-[1,0,0]')
      # return1 = client.write_registers(0x0009,[1, 0, 0],1)
      # print('--------------time.sleep(0.5)')
      # time.sleep(0.5)
      print('44444444444444-[0,0,0]')
      return1 = client.write_registers(0x0009,[0, 0, 0],1)
      print("-------------------------------sent [0,0,0]")
      print("-------------------------------sent [0,0,0]")
      # print('--------------time.sleep(0.5)')
      # time.sleep(0.5)
    else:
      print('44444444444444-', val)
      return1 = client.write_registers(0x0009,val,1)
      print("-------------------------------sent ", val)
      print("-------------------------------sent ", val)
      # print('--------------time.sleep(0.5)')
      # time.sleep(0.5)
    print('55555555555555')
    print(return1)
    print('66666666666666')
    # client.close()
    print('77777777777777')
    # print(return1)
    print('88888888888888')
    return True
  except Exception as e:
    print(e)
    return False
  


# x=500
# y=1000

# # Write 1 to register 0
# write_detected([1,x,y])
if __name__ == "__main__":
  values = [[1,0,0],[1,150,0],[1,40,30],[1,21022,130]]
  client = ModbusTcpClient("192.168.9.1", port=502)
  write_detected(values, client)
  # val = inter.alignment_multi(values)
  # print(val)
  print(client)
