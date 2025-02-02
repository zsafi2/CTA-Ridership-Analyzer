### **CTA Ridership Analyzer**
#### *Analyze and visualize CTA ridership data using SQLite and Python.*

---

## **Table of Contents**
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Database Structure](#database-structure)
- [Technologies Used](#technologies-used)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## **Description**
CTA Ridership Analyzer is a Python-based application that provides insights into the ridership statistics of the Chicago Transit Authority (CTA). The program utilizes an SQLite database to analyze ridership trends, station information, and commuter behaviors. Users can query the database for station details, historical ridership, stop accessibility, and even compare ridership trends across different stations and years.

---

## **Features**
- Retrieve general statistics about CTA ridership.
- Search for station details based on partial names.
- Analyze ridership distribution across weekdays, Saturdays, and Sundays.
- Display ridership trends for specific stations and years.
- List stops by train line color and direction.
- Compare daily ridership between two stations.
- Locate CTA stations near a given latitude/longitude.
- Generate visualizations using Matplotlib.

---

## **Installation**
### **Prerequisites**
Ensure you have the following installed on your system:
- Python 3.x
- SQLite3
- Required Python libraries: `matplotlib`, `sqlite3`

### **Clone the Repository**
```bash
git clone https://github.com/yourusername/cta-ridership-analyzer.git
cd cta-ridership-analyzer
```

### **Install Dependencies**
```bash
pip install matplotlib
```

### **Prepare the Database**
Ensure the SQLite database file (`CTA2_L_daily_ridership.db`) is present in the project directory. If not, download or generate the database before running the program.

---

## **Usage**
Run the program using:
```bash
python main.py
```
The program will display an interactive terminal-based interface, where you can enter numerical commands to perform different queries.

---

## **Commands**
| Command | Description |
|---------|------------|
| `1` | Search for station details by name (supports wildcards `%` and `_`). |
| `2` | Get weekday, Saturday, and Sunday/holiday ridership percentages for a station. |
| `3` | List ridership on weekdays for each station, ordered by highest ridership. |
| `4` | Display all stops for a given line color and direction. |
| `5` | Show the number of stops for each train line by direction. |
| `6` | Get yearly ridership for a station with a visualization option. |
| `7` | Show monthly ridership for a station in a specific year. |
| `8` | Compare daily ridership trends between two stations for a given year. |
| `9` | Find CTA stations within a 1-mile radius of a given latitude/longitude. |
| `x` | Exit the application. |

---

## **Database Structure**
The application interacts with an SQLite database consisting of the following key tables:

- **`Stations`**: Contains station IDs and names.
- **`Stops`**: Stores stop details, including latitude, longitude, and accessibility.
- **`Ridership`**: Contains historical ridership data with station IDs and daily counts.
- **`Lines`**: Represents different CTA train lines with color-coded identifiers.
- **`StopDetails`**: Links stops with corresponding lines.

---

## **Technologies Used**
- **Python**: Core programming language.
- **SQLite3**: Lightweight database for efficient data queries.
- **Matplotlib**: Data visualization for plotting ridership trends.

---

## **Future Improvements**
- Implement a web-based or GUI interface.
- Add real-time ridership data (if available).
- Optimize queries for better performance on large datasets.
- Improve data visualization with interactive charts.

---

## **Contributing**
Contributions are welcome! If you’d like to improve this project:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

