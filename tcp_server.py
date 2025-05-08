import socket
import json  # Use JSON for unified data formatting
import sensor_novaPM_read
import sensor_bme280_read


def start_server(host='0.0.0.0', port=65432):
    """
    Starts a TCP server to send sensor data to a client.
    :param host: The IP address to bind to (default: all interfaces).
    :param port: The port to listen on.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on {host}:{port}")

        conn, addr = server_socket.accept()
        print(f"Connection established with {addr}")

        try:
            # Initialize data sources
            data_source_novaPM = sensor_novaPM_read.read_sensor_data()
            data_source_bme280 = sensor_bme280_read.read_sensor_data()

            while True:
                # Collect and send NovaPM data
                try:
                    nova_data = next(data_source_novaPM)
                    unified_nova_data = {
                        # Convert datetime to string
                        "timestamp": nova_data["timestamp"].isoformat(),
                        "sensor": "NovaPM",
                        "data": {
                            "pm2.5": nova_data["pm2.5"],
                            "pm10": nova_data["pm10"]
                        }
                    }
                    conn.sendall(
                        (json.dumps(unified_nova_data) + "\n").encode('utf-8'))
                except StopIteration:
                    print("NovaPM sensor data source exhausted.")
                except Exception as e:
                    print(f"Error reading NovaPM sensor data: {e}")

                # Collect and send BME280 data
                try:
                    bme_data = next(data_source_bme280)
                    unified_bme_data = {
                        "timestamp": bme_data["timestamp"] if isinstance(bme_data["timestamp"], str) else bme_data["timestamp"].isoformat(),
                        "sensor": "BME280",
                        "data": {
                            "temperature": bme_data["temperature"],
                            "humidity": bme_data["humidity"],
                            "pressure": bme_data["pressure"]
                        }
                    }
                    conn.sendall(
                        (json.dumps(unified_bme_data) + "\n").encode('utf-8'))
                except StopIteration:
                    print("BME280 sensor data source exhausted.")
                except Exception as e:
                    print(f"Error reading BME280 sensor data: {e}")

        except BrokenPipeError:
            print("Client disconnected.")
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            conn.close()


if __name__ == "__main__":
    start_server()
