import socket
import sensor_novaPM_read


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
            for data in sensor_novaPM_read.read_sds011():
                # Send sensor data as a string
                message = f"{data['timestamp']}, PM2.5: {data['pm2.5']} µg/m³, PM10: {data['pm10']} µg/m³\n"
                conn.sendall(message.encode('utf-8'))
        except BrokenPipeError:
            print("Client disconnected.")
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            conn.close()


if __name__ == "__main__":
    start_server()
