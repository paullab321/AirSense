import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plot_sensor_data(data_source):
    pm25_values, pm10_values, pm_indices = [], [], []
    temperature_values, humidity_values, pressure_values, env_indices = [], [], [], []

    def update_pm(frame):
        try:
            data = next(data_source, None)
            if data:
                if "pm2.5" in data and "pm10" in data:
                    pm_indices.append(len(pm_indices) + 1)
                    pm25_values.append(data["pm2.5"])
                    pm10_values.append(data["pm10"])
        except Exception as e:
            print(f"Error in update_pm function: {e}")

        ax1.clear()
        ax2.clear()
        if pm25_values:
            ax1.plot(pm_indices, pm25_values,
                     label="PM2.5 (µg/m³)", color="blue")
        if pm10_values:
            ax2.plot(pm_indices, pm10_values,
                     label="PM10 (µg/m³)", color="red")
        ax1.set_title("PM2.5 Concentration")
        ax2.set_title("PM10 Concentration")
        ax1.set_ylabel("µg/m³")
        ax2.set_ylabel("µg/m³")
        ax2.set_xlabel("Measurement Index")
        ax1.legend()
        ax2.legend()

    def update_env(frame):
        try:
            data = next(data_source, None)
            if data:
                if "temperature" in data and "humidity" in data and "pressure" in data:
                    env_indices.append(len(env_indices) + 1)
                    temperature_values.append(data["temperature"])
                    humidity_values.append(data["humidity"])
                    pressure_values.append(data["pressure"])
        except Exception as e:
            print(f"Error in update_env function: {e}")

        ax3.clear()
        ax4.clear()
        ax5.clear()
        if temperature_values:
            ax3.plot(env_indices, temperature_values,
                     label="Temperature (°C)", color="green")
        if humidity_values:
            ax4.plot(env_indices, humidity_values,
                     label="Humidity (%)", color="purple")
        if pressure_values:
            ax5.plot(env_indices, pressure_values,
                     label="Pressure (hPa)", color="orange")
        ax3.set_title("Temperature")
        ax4.set_title("Humidity")
        ax5.set_title("Pressure")
        ax3.set_ylabel("°C")
        ax4.set_ylabel("%")
        ax5.set_ylabel("hPa")
        ax5.set_xlabel("Measurement Index")
        ax3.legend()
        ax4.legend()
        ax5.legend()

    # Figure 1: PM2.5 and PM10
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ani1 = FuncAnimation(fig1, update_pm, interval=1000, save_count=100)
    fig1.tight_layout()

    # Figure 2: Temperature, Humidity, Pressure
    fig2, (ax3, ax4, ax5) = plt.subplots(3, 1, figsize=(10, 12))
    ani2 = FuncAnimation(fig2, update_env, interval=1000, save_count=100)
    fig2.tight_layout()

    plt.show()
