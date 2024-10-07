```markdown
# Cyclistic Data Analysis Project

The .csv files can be found here https://divvy-tripdata.s3.amazonaws.com/index.html
They must be in the "ridedata" directory in the project.

## Steps to Run the Project

### 1. Set Up the Environment

Make sure you have Python 3.8+ installed. Then, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### 2. Load the Data into DuckDB

First, generate the DuckDB database by loading the 12 CSV files into the `rides` table. Use the `gen_db.py` script:

```bash
python3 gen_db.py
```

This script will create a DuckDB database named `ridedata.ddb` and load all 12 CSV files (from September 2023 to August 2024) into a consolidated table.

### 3. Clean the Data

After the database is generated, the next step is to clean outliers from the dataset. This process will remove records with unrealistic values, such as negative ride durations or missing location data.

To clean the data, run the `clean_outliers.py` script:

```bash
python3 clean_outliers.py
```

The script will:
- Filter out rides with negative durations, rides longer than 3 hours, rides shorter than 1 minute, rides with distances greater than 25 km, and rides with missing location information.
- Report how many outliers were removed for each condition.
- Verify if any outliers remain after the cleaning process.

### 4. Run the Flask Application

Once the data has been cleaned, run the Flask app to explore the analysis and visualizations. You can start the application with the following command:

```bash
python3 app.py
```

By default, the application will be accessible at `http://127.0.0.1:5000`.
