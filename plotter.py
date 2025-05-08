import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_sensor_data(data_source):
    """
    Plots PM2.5, PM10, temperature, humidity, and pressure data in real-time.
    :param data_source: A generator function that yields sensor data.
    """
    indices = []  # X-axis will be indices (1, 2, 3, ...)
    pm25_values = []
    pm10_values = []
    temperature_values = []
    humidity_values = []
    pressure_values = []

    def update(frame):
        data = next(data_source, None)
        if data:
            print(f"Received data: {data}")  # Debug: Print received data
            indices.append(len(indices) + 1)
            if "pm2.5" in data and "pm10" in data:
                pm25_values.append(data["pm2.5"])
                pm10_values.append(data["pm10"])
            if "temperature" in data and "humidity" in data and "pressure" in data:
                temperature_values.append(data["temperature"])
                humidity_values.append(data["humidity"])
                pressure_values.append(data["pressure"])

            # Clear and redraw the plots
            ax1.clear()
            ax2.clear()
            ax3.clear()

            ax1.plot(indices, pm25_values, label="PM2.5 (µg/m³)", color="blue")
            ax2.plot(indices, pm10_values, label="PM10 (µg/m³)", color="red")
            ax3.plot(indices, temperature_values,
                     label="Temperature (°C)", color="green")

            ax1.set_title("PM2.5 Concentration")
            ax2.set_title("PM10 Concentration")
            ax3.set_title("Temperature")
            ax1.set_ylabel("µg/m³")
            ax2.set_ylabel("µg/m³")
            ax3.set_ylabel("°C")
            ax3.set_xlabel("Measurement Index")
            ax1.legend()
            ax2.legend()
            ax3.legend()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
    ani = FuncAnimation(fig, update, interval=1000, save_count=100)
    plt.tight_layout()
    plt.show()
