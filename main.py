import sensor_novaPM_read  # Replace with the actual module and class name
import plotter


def main():
    data_source = sensor_novaPM_read.read_sds011()
    plotter.plot_sensor_data(data_source)


if __name__ == "__main__":
    main()
