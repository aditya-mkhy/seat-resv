# Seat-Resv (Seat Reservation Holder)

A smart automation tool that **holds seats temporarily** so no one else can book them — until you’re ready to confirm.  
Perfect for festival seasons, long weekends, or any time seats sell out fast before you’re sure to travel.

> 🧠 Imagine you want to travel but haven’t decided yet — this tool keeps your seats safe until you are!

---

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🚀 Features

- 🎟️ **Hold multiple seats** for multiple routes and dates.  
- ⏳ **Prevent others from booking** your chosen seats temporarily.  
- 🤖 **Automated browser control** using Selenium WebDriver.  
- 🌍 **Proxy rotation support** — bypass region/IP restrictions.  
- 🧩 **Parallel seat holding threads** — runs multiple holds simultaneously.  
- 🕵️ **Headless mode support** for silent background execution.  
- 💬 **Logging system** with date-wise log files.

---

## 📂 Project structure

```
seat-resv/
├─ holder.py         # Controls multiple reservation threads
├─ reserver.py       # Core seat holding logic (Selenium-based)
├─ prox.py           # Proxy fetcher and validator
├─ util.py           # Logging, JSON storage, utility functions
├─ data.dt           # Local lightweight data store
├─ name_list.csv     # Passenger or contact list
├─ requirements.txt  # Required Python libraries
├─ LICENSE
└─ README.md
```

---

## 🧩 Requirements

- Python **3.9 or newer**
- Mozilla Firefox (for Selenium)
- GeckoDriver installed (added to PATH)
- Python libraries:
  ```bash
  pip install selenium requests beautifulsoup4
  ```

---

## ⚙️ How It Works

1. **Seat discovery & selection**  
   The tool automates a web browser (Selenium) to visit your booking portal, search for your desired service, and pick seats.

2. **Seat hold logic**  
   Once seats are selected, it keeps the browser session alive and refreshes periodically to prevent timeout or release.

3. **Proxy management**  
   If the website limits repeated access, the tool fetches new proxies from multiple proxy sources and rotates them.

4. **Local database**  
   The `data.dt` file stores name, phone/email pointers, etc.

5. **Multi-threaded holder**  
   You can hold seats for multiple routes/dates at once using `SeatHolder` (in `holder.py`).

---

## 🧠 Example usage

### Multi-reserver (for multiple seats)

```python
from holder import SeatHolder

holder = SeatHolder(headless_mode=True)

# set time to stop this script
date_str = "26-10-2025"
time_str = "01:00"
seat_holder.run_until(date_str = date_str, time_str = time_str)

data = {
   "for 26-OCT" : {
      "date" : "26-10-2025",
      "from" : "kangra",
      "to"   : "Shimla isbt",
      "service_no" : "908",
      "seat" : ['25'],
   },

   "for 31-OCT" : {
      "date" : "31-10-2025",
      "from" : "kangra",
      "to"   : "Shimla isbt",
      "service_no" : "1721",
      "seat" : ['25'],
   },

}

seat_holder.hold_for_multiple_dates(data=data, use_proxy=False)# starts holding your selected seat
```

## ⚙️ Configuration options

- **Headless mode:** Run silently without GUI (`headless=True`)
- **Proxy support:** Automatically fetches and tests working proxies.
- **Time limit:** Can be configured to hold for a specific time before releasing.
- **Threaded operation:** Each seat-holder runs independently for different routes or dates.

---

## 📊 Data files

| File | Purpose |
|------|----------|
| `data.dt` | Local JSON-like DB storing state |
| `name_list.csv` | Passenger/contact list |
| `logs/` | Auto-created daily logs of operations |

---

## 🔒 Safety Notes

- The script **does not confirm any booking** — it only prevents others from booking temporarily.  
- Use it responsibly and ethically.  
- Works best for testing, demo, or personal backup of available seats.  
- Do not use to unfairly block large numbers of seats in production systems.

---

## 🧩 Developer Notes

- `Reserver` → core automation logic (browser, seat selection, holding).  
- `SeatHolder` → manages multiple `Reserver` threads.  
- `Proxy` → scrapes and rotates working IPs.  
- `PyDb` (in util.py) → simple file-based persistent storage.

---

## 🪄 License

This project is licensed under the **MIT License**.  
Free to use, modify, and share.

---

## ⚡ Credits

Developed to simplify travel planning by letting users **secure seats early without paying instantly**.  
Built with ❤️ in Python + Selenium.
