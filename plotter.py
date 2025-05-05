import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_sensor_data(data_source):
    """
    Plots PM2.5 and PM10 data in real-time.
    :param data_source: A generator function that yields sensor data.
    """
    timestamps = []
    pm25_values = []
    pm10_values = []

    def update(frame):
        data = next(data_source, None)
        if data:
            timestamps.append(data["timestamp"])
            pm25_values.append(data["pm2.5"])
            pm10_values.append(data["pm10"])

            # Limit the number of points displayed
            if len(timestamps) > 100:
                timestamps.pop(0)
                pm25_values.pop(0)
                pm10_values.pop(0)

            ax1.clear()
            ax2.clear()

            ax1.plot(timestamps, pm25_values,
                     label="PM2.5 (µg/m³)", color="blue")
            ax2.plot(timestamps, pm10_values,
                     label="PM10 (µg/m³)", color="red")

            ax1.set_title("PM2.5 Concentration")
            ax2.set_title("PM10 Concentration")
            ax1.set_ylabel("µg/m³")
            ax2.set_ylabel("µg/m³")
            ax2.set_xlabel("Time")
            ax1.legend()
            ax2.legend()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ani = FuncAnimation(fig, update, interval=1000)
    plt.tight_layout()
    plt.show()
