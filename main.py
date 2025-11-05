import random
import time
import folium
import webbrowser
import html
from datetime import datetime
import requests
import os
import threading
import tkinter as tk
from tkinter import ttk

# ========== CONFIG ==========
MAP_PATH = r"C:\Users\adity\Downloads\map\india_weather_live.html"
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
UPDATE_INTERVAL = 5
TOTAL_UPDATES = 10

# ========== LOCATIONS ==========
LOCATIONS = [
    ("Delhi", 28.6139, 77.2090),
    ("Mumbai", 19.0760, 72.8777),
    ("Chennai", 13.0827, 80.2707),
    ("Kolkata", 22.5726, 88.3639),
    ("Bengaluru", 12.9716, 77.5946),
    ("Hyderabad", 17.3850, 78.4867),
    ("Ahmedabad", 23.0225, 72.5714),
    ("Pune", 18.5204, 73.8567),
    ("Jaipur", 26.9124, 75.7873),
    ("Lucknow", 26.8467, 80.9462),
    ("Bhopal", 23.2599, 77.4126),
    ("Patna", 25.5941, 85.1376),
    ("Indore", 22.7196, 75.8577),
    ("Chandigarh", 30.7333, 76.7794),
    ("Nagpur", 21.1458, 79.0882),
    ("Surat", 21.1702, 72.8311),
    ("Kanpur", 26.4499, 80.3319),
    ("Visakhapatnam", 17.6868, 83.2185),
    ("Thiruvananthapuram", 8.5241, 76.9366),
    ("Ranchi", 23.3441, 85.3096),
    ("Varanasi", 25.3176, 82.9739),
    ("Guwahati", 26.1445, 91.7362),
    ("Shimla", 31.1048, 77.1734),
    ("Mysuru", 12.2958, 76.6394),
    ("Agra", 27.1767, 78.0081),
    ("Amritsar", 31.6340, 74.8723),
    ("Nashik", 19.9975, 73.7898),
    ("Vadodara", 22.3072, 73.1812),
    ("Coimbatore", 11.0168, 76.9558),
    ("Udaipur", 24.5854, 73.7125),
    ("Dehradun", 30.3165, 78.0322),
    ("Raipur", 21.2514, 81.6296),
    ("Mangalore", 12.9141, 74.8560),
    ("Bareilly", 28.3670, 79.4304),
    ("Jammu", 32.7266, 74.8570),
    ("Gwalior", 26.2183, 78.1828),
    ("Jodhpur", 26.2389, 73.0243),
    ("Kochi", 9.9312, 76.2673),
    ("Madurai", 9.9252, 78.1198),
    ("Allahabad", 25.4358, 81.8463),
]

# ========== CONDITIONS ==========
CONDITIONS = [
    ("Sunny", "🌞", "orange"), ("Rainy", "🌧", "blue"),
    ("Thunderstorm", "⛈", "purple"), ("Cloudy", "☁️", "gray"),
    ("Foggy", "🌫", "lightgray"), ("Windy", "🌬", "cadetblue"),
    ("Snow", "❄️", "white")
]

# ========== CORE FUNCTIONS ==========
def generate_weather_data():
    data = []
    for name, lat, lon in LOCATIONS:
        cond, emoji, color = random.choice(CONDITIONS)
        temp = random.randint(10, 42)
        humidity = random.randint(20, 100)
        wind = random.randint(1, 25)
        impact = random.choice(["Low", "Moderate", "Severe"])
        data.append({
            "name": name, "lat": lat, "lon": lon,
            "condition": cond, "emoji": emoji, "color": color,
            "temperature": temp, "humidity": humidity, "wind": wind, "impact": impact
        })
    return data

def send_telegram_update(weather_data):
    msg = f"🌦 India Live Weather ({datetime.now().strftime('%H:%M:%S')}):\n\n"
    for d in weather_data:
        msg += f"{d['emoji']} {d['name']}: {d['condition']} | {d['temperature']}°C | H:{d['humidity']}% | W:{d['wind']}km/h | Impact: {d['impact']}\n"
    parts = [msg[i:i + 4000] for i in range(0, len(msg), 4000)]
    for part in parts:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": TELEGRAM_CHAT_ID, "text": part}, timeout=5
            )
        except Exception as e:
            print("⚠️ Telegram error:", e)

def plot_map(weather_data):
    center_lat = sum(d["lat"] for d in weather_data) / len(weather_data)
    center_lon = sum(d["lon"] for d in weather_data) / len(weather_data)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Imagery"
    ).add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Labels", overlay=True, control=False
    ).add_to(m)
    for loc in weather_data:
        popup_html = (
            f"<b>{html.escape(loc['emoji'] + ' ' + loc['name'])}</b><br>"
            f"{html.escape(loc['condition'])}<br>"
            f"Temp: {loc['temperature']}°C<br>"
            f"Humidity: {loc['humidity']}%<br>"
            f"Wind: {loc['wind']} km/h<br>"
            f"Impact: {html.escape(loc['impact'])}"
        )
        folium.CircleMarker(
            location=[loc["lat"], loc["lon"]], radius=9, color="black", weight=1.5,
            fill=True, fill_color=loc["color"], fill_opacity=0.9,
            popup=popup_html, tooltip=f"{loc['emoji']} {loc['name']}"
        ).add_to(m)
    refresh_script = f"<script>setTimeout(() => location.reload(), {UPDATE_INTERVAL * 1000});</script>"
    m.get_root().html.add_child(folium.Element(refresh_script))
    m.save(MAP_PATH)

# ========== THREAD CONTROL ==========
running = False

def main_process():
    global running
    os.makedirs(os.path.dirname(MAP_PATH), exist_ok=True)
    opened = False
    for i in range(1, TOTAL_UPDATES + 1):
        if not running:
            update_status("🛑 Simulation stopped.", "#e63946")
            return
        data = generate_weather_data()
        plot_map(data)
        send_telegram_update(data)
        if not opened:
            webbrowser.open(MAP_PATH)
            opened = True
        update_status(f"✅ Update {i}/{TOTAL_UPDATES} sent.", "#60a5fa")
        update_counter(i)
        time.sleep(UPDATE_INTERVAL)
    update_status("✔️ All updates completed successfully.", "#3b82f6")
    running = False

# ========== GUI ==========
def start_process():
    global running
    if not running:
        running = True
        update_status("Starting simulation...", "#ffd166")
        threading.Thread(target=main_process, daemon=True).start()
    else:
        update_status("Already running!", "#8d99ae")

def stop_process():
    global running
    running = False
    update_status("Stopping process...", "#ef476f")

def update_status(text, color):
    status_label.config(text=text, fg=color)

def update_counter(value):
    counter_label.config(text=f"Updates sent: {value}")

# --- GRAPHITE BLUE THEME ---
root = tk.Tk()
root.title("🌦 Live India Weather Monitor")
root.geometry("440x280")
root.resizable(False, False)
root.configure(bg="#1c1f26")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 11, "bold"),
                padding=8,
                background="#3b82f6",
                foreground="#e5e7eb",
                borderwidth=0)
style.map("TButton",
          background=[("active", "#60a5fa"), ("pressed", "#1c1f26")],
          foreground=[("active", "white")])

card = tk.Frame(root, bg="#2a2f38", bd=1, relief="ridge", highlightthickness=0)
card.pack(padx=20, pady=20, fill="both", expand=True)

title_label = tk.Label(card, text="🌦 Live India Weather Monitor",
                       font=("Segoe UI Semibold", 15),
                       bg="#2a2f38", fg="#e5e7eb")
title_label.pack(pady=15)

btn_frame = tk.Frame(card, bg="#2a2f38")
btn_frame.pack(pady=10)

start_btn = ttk.Button(btn_frame, text="▶ Start Monitoring", command=start_process)
stop_btn = ttk.Button(btn_frame, text="⏹ Stop Monitoring", command=stop_process)
start_btn.grid(row=0, column=0, padx=12)
stop_btn.grid(row=0, column=1, padx=12)

status_label = tk.Label(card, text="Idle", font=("Segoe UI", 11),
                        bg="#2a2f38", fg="#9ca3af")
status_label.pack(pady=10)

counter_label = tk.Label(card, text="Updates sent: 0",
                         font=("Segoe UI", 10), bg="#2a2f38", fg="#d1d5db")
counter_label.pack(pady=5)

footer = tk.Label(root, text="Developed by Aditya",
                  font=("Segoe UI", 9), bg="#1c1f26", fg="#6b7280")
footer.pack(side="bottom", pady=8)

root.mainloop()
