Here’s a polished, professional **`README.md`** file ready for GitHub — written with markdown formatting, emojis, and clear structure for easy readability 👇

---

````markdown
# 🌦️ Live India Weather Monitoring Dashboard

A **Python-based real-time weather simulation and monitoring system** for India 🇮🇳 that:

- Generates live-style random weather data for 40+ major Indian cities.  
- Displays it on an interactive **satellite map** that updates automatically.  
- Sends periodic **Telegram weather notifications** for all cities.  

---

## 🗺️ Features

✅ Interactive **Folium map** with live weather updates  
✅ **Satellite + label layers** for high clarity  
✅ **Telegram bot integration** for live alerts  
✅ Automatically **refreshing dashboard** (no manual reloads)  
✅ Covers **40+ major Indian cities**  
✅ Easy to run — just copy, paste, and execute  

---

## ⚙️ Requirements

Ensure you have **Python 3.8+** installed.

### Install dependencies:
```bash
pip install folium requests
````

---

## 🧩 Configuration

Edit these variables at the top of the script as per your setup:

```python
MAP_PATH = r"C:\Users\adity\Downloads\map\india_weather_live.html"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
UPDATE_INTERVAL = 5          # Time (in seconds) between updates
TOTAL_UPDATES = 10           # Number of cycles before stopping
```

### 🪄 How to get your Telegram Bot Token and Chat ID

1. Go to [@BotFather](https://t.me/BotFather) on Telegram.
2. Create a new bot → copy the **bot token**.
3. Send a message to your bot, then visit:

   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```

   Copy the `chat.id` from the JSON response.

---

## 🚀 How It Works

1. The program generates **randomized weather data** (temperature, humidity, wind, etc.) for each city.
2. It sends this data as a **Telegram message** to your configured chat.
3. It creates a **live satellite map** of India marking every city with:

   * Color-coded weather markers
   * Emojis representing conditions
   * Clickable popups for detailed info
4. The map **auto-refreshes** every few seconds, showing new simulated conditions.

---

## 🧭 Project Structure

```
📁 weather-live-monitor/
 ┣ 📜 weather_live.py          # Main Python script
 ┣ 📜 README.md                # Documentation file
 ┗ 📂 map/
    ┗ 📄 india_weather_live.html   # Live map file generated at runtime
```

---

## 🧠 Example Telegram Message

```
🌦 India Live Weather (12:30:45):

🌞 Delhi: Sunny | 33°C | H:56% | W:12km/h | Impact: Low
🌧 Mumbai: Rainy | 27°C | H:78% | W:18km/h | Impact: Moderate
☁️ Kolkata: Cloudy | 29°C | H:64% | W:10km/h | Impact: Low
🌬 Chennai: Windy | 31°C | H:44% | W:22km/h | Impact: Moderate
```

---

## 🌍 Example Map View

The generated map (`india_weather_live.html`) includes:

* **Satellite imagery base layer** (Esri World Imagery)
* **City labels overlay**
* Weather points showing:

  * City name
  * Temperature, humidity, and wind speed
  * Visual emoji icons for easy identification

Each marker refreshes every few seconds to simulate **live changes**.

---

## 🧪 Code Summary

| Component                 | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| `generate_weather_data()` | Creates random weather info for each city |
| `send_telegram_update()`  | Sends full weather summary to Telegram    |
| `plot_map()`              | Draws/upgrades the live satellite map     |
| `main()`                  | Controls execution loop and timing        |

---

## 🖥️ Running the Program

1. Copy the full script into a file named `weather_live.py`.
2. Edit the configuration (map path + Telegram details).
3. Run:

```bash
python weather_live.py
```

4. Your default browser will open the **live weather map**.
5. Telegram will start receiving **real-time updates**.

---

## 🌐 Output Demo

| Platform                 | Output                                              |
| ------------------------ | --------------------------------------------------- |
| **Browser (Folium Map)** | Satellite view of India with weather icons & popups |
| **Telegram Bot**         | Text-based weather updates for all cities           |

---

## 🔮 Future Enhancements

* Integrate **real API-based weather data** (OpenWeatherMap / IMD)
* Add **rain animation and temperature gradients**
* Store history for trend visualization
* Convert simulation into a **Flask web app**

---

## 👨‍💻 Author

**Aditya’s Weather Simulation Project**
Developed using Python, Folium & Telegram API

---

## 🪪 License

This project is released under the **MIT License**.
You are free to modify and use it for learning or development.

---

> “Turning data into dynamic, visual weather intelligence.”

```

```
