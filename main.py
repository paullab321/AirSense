import sensor_novaPM_read  # Replace with the actual module and class name
import tcp_server


def main():
    tcp_server.start_server()
    data_source = sensor_novaPM_read.read_sds011()


if __name__ == "__main__":
    main()
