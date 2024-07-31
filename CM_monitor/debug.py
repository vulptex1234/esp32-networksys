import machine

i2c = machine.I2C(1, scl=machine.Pin(22), sda=machine.Pin(21))
ina219_address = 0x40  # INA219のI2Cアドレス

def write_register(register, value):
    register_bytes = bytearray([(value >> 8) & 0xFF, value & 0xFF])
    i2c.writeto_mem(ina219_address, register, register_bytes)

def read_register(register):
    register_bytes = i2c.readfrom_mem(ina219_address, register, 2)
    return int.from_bytes(register_bytes, 'big')

# レジスタへの書き込みテスト
test_register = 0x00  # CONFIGレジスタ
test_value = 0x399F  # テスト用の値

print("Writing to register 0x{:02X}: 0x{:04X}".format(test_register, test_value))
write_register(test_register, test_value)

# レジスタの読み取りテスト
read_value = read_register(test_register)
print("Read from register 0x{:02X}: 0x{:04X}".format(test_register, read_value))

# 一致確認
if read_value == test_value:
    print("Write and read test passed.")
else:
    print("Write and read test failed.")
