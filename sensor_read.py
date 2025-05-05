import sys  # Unused import, consider removing if not needed
import board  # Ensure the 'board' module is installed
import busio  # Ensure the 'busio' module is installed

i2c = busio.I2C(board.SCL, board.SDA)

try:
    if not i2c.try_lock():
        raise RuntimeError("Unable to lock the I2C bus.")
    print(f"Found I2C devices: {[hex(i) for i in i2c.scan()]}")
finally:
    i2c.unlock()

bme280 = 0x76  # Replace with the actual I2C address of your BME280 sensor

if not bme280 in i2c.scan():
    raise RuntimeError(f"BME280 sensor not found at address {hex(bme280)}.")
    sys.exit()


def get_bme280_id():
    i2c.writeto(bme280, bytes([0xD0]), stop=False)  # Register address for ID
    result = bytearray(1)
    i2c.readfrom_into(bme280, result)
    print(f"BME280 ID: {result[0]:#04x}")


if __name__ == "__main__":
    get_bme280_id()
    print("BME280 sensor is connected and operational.")
