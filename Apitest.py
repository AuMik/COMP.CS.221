import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

#Api keys hidden for obvious reasons
def get_api_keys():
    with open("keys.json") as f:
        keys = json.load(f)
        return  keys["elecApiKey"]
    
def get_energy_info():
    url = "https://api.energy-charts.info/cbet?country=de&start=2025-02-18&end=2025-02-19"

    response = requests.get(url)

    # Check if response is valid JSON
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except ValueError:
            print("Received non-JSON response")
            print("Response Text:", response.text)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def get_electricity_info(API_KEY):
    response = requests.get(
    "https://api.electricitymap.org/v3/power-breakdown/history?zone=DE",
    headers={
        "auth-token": f"{API_KEY}"
    }
    )
    return response.json()

def draw_figure(energ_dict,elect_dict):
    # Create subplots: 2 plots in one figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Plot energy data on the first subplot
    ax1.plot(energ_dict.keys(), energ_dict.values(), marker='o', color='g', label='Electricity Import/Export (GW)')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Electricity Import/Export (GW)')
    ax1.set_title('Electricity Import/Export Over Time')
    ax1.grid(True)
    ax1.legend()

    # Manually set x-ticks for energy data plot
    tick_interval = 15  # Every 15th data point for ticks
    x_ticks = list(energ_dict.keys())[::tick_interval]  # Take every 15th date from the list
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_ticks, rotation=45)  # Rotate x-axis labels for readability
    
    # Plot electricity data on the second subplot
    ax2.plot(elect_dict.keys(), elect_dict.values(), marker='o', color='b', label='Electricity Production (MW)')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Electricity Import/Export (MW)')
    ax2.set_title('Electricity Production Over Time')
    ax2.grid(True)
    ax2.legend()

    # Manually set x-ticks for electricity data plot
    x_ticks = list(elect_dict.keys())[::tick_interval]  # Take every 15th date from the list
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(x_ticks, rotation=45)  # Rotate x-axis labels for readability

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    elecKey = get_api_keys()
    elecData = get_electricity_info(elecKey)
    energData = get_energy_info()
    dates = energData["unix_seconds"]
    energSum = energData["countries"][-1]["data"]
    convertedDates = []
    for date in dates: 
        convertedDates.append(datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S'))

    
    energ_dict = dict(zip(convertedDates,energSum))
    elect_dict = dict()
    for entry in elecData["history"]:
        date =  entry["datetime"].rstrip("Z")
        niceDate = datetime.fromisoformat(date).strftime('%Y-%m-%d %H:%M:%S')
        powerTotal = entry["powerProductionTotal"]
        elect_dict[niceDate] = powerTotal


    draw_figure(energ_dict,elect_dict)
    
    
