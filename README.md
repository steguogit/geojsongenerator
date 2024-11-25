# geojsongenerator
This project is for Public Transport Enquiry Service (PTES) Data Generator. 
# PTES Data Generator

**Public Transport Enquiry Service (PTES) Data Generator**

Welcome to the **PTES Data Generator** project! This repository contains a Python script designed to reset and populate your MongoDB Atlas database with realistic testing data for the **Public Transport Enquiry Service (PTES)**. This service simulates various aspects of public transportation in Hong Kong, including multiple transport modes, routes, stops, fares, and journeys.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Script Structure](#script-structure)
- [Verification](#verification)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

The **PTES Data Generator** is a comprehensive tool that automates the process of resetting and populating MongoDB collections with test data tailored for the Public Transport Enquiry Service. This ensures a consistent and reliable testing environment, facilitating efficient development and robust testing of PTES functionalities.

---

## Features

- **Reset Functionality:** Drops existing collections to ensure a clean state before data generation.
- **Data Generation:**
  - **Transport Modes:** Predefined modes such as MTR, LRT, Bus, etc.
  - **Locations:** Randomly generated geographical points within Hong Kong.
  - **Routes:** Simulated transport routes with associated transport modes and locations.
  - **Stops:** Random stops for each route, linked to locations.
  - **Journeys:** Possible journey options based on origin, destination, and available routes.
- **Geospatial Indexing:** Creates `2dsphere` indexes on location fields to optimize geospatial queries.
- **Logging:** Provides real-time logging for monitoring progress and diagnosing issues.
- **Data Type Compatibility:** Ensures all numerical fields are compatible with MongoDB BSON specifications.

---

## Prerequisites

Before getting started, ensure you have the following:

1. **MongoDB Atlas Account:**
   - Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) if you don't have an account.
   
2. **MongoDB Atlas Cluster:**
   - Set up a MongoDB Atlas cluster where the testing data will be stored.
   
3. **MongoDB Atlas Connection String:**
   - Obtain your cluster's connection string from the MongoDB Atlas dashboard.
   - Format: `mongodb+srv://<username>:<password>@<cluster-url>/ptes?retryWrites=true&w=majority`
   
4. **Python Environment:**
   - Python 3.6 or higher installed.
   - It's recommended to use a virtual environment to manage dependencies.

---

## Installation

Follow these steps to set up the PTES Data Generator on your local machine:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/PTES-Data-Generator.git
   cd PTES-Data-Generator
   ```

2. **Set Up a Virtual Environment (Optional but Recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

   *If a `requirements.txt` file is not provided, install the necessary packages manually:*

   ```bash
   pip install pymongo faker
   ```

---

## Configuration

Before running the script, configure the necessary settings:

1. **Update the MongoDB Connection String:**

   Open the `reset_and_generate_ptes_data.py` script and locate the `MONGO_URI` variable. Replace the placeholders with your actual MongoDB Atlas credentials and cluster information.

   ```python
   MONGO_URI = "mongodb+srv://<username>:<password>@<your-cluster-url>/ptes?retryWrites=true&w=majority"
   ```

   **Example:**

   ```python
   MONGO_URI = "mongodb+srv://stevenguo:YourPassword@cluster0.mongodb.net/ptes?retryWrites=true&w=majority"
   ```

2. **Adjust Data Generation Parameters (Optional):**

   The script includes variables to control the volume of generated data. Modify these as needed.

   ```python
   NUMBER_OF_LOCATIONS = 100          # Number of geographical locations
   NUMBER_OF_ROUTES = 500             # Number of transport routes
   NUMBER_OF_JOURNEYS = 1000          # Number of journey options
   ```

3. **Secure Sensitive Information:**

   For enhanced security, consider using environment variables to store sensitive information like the MongoDB URI.

   **Example:**

   ```python
   import os

   MONGO_URI = os.getenv("MONGO_URI")
   ```

   **Set the Environment Variable:**

   ```bash
   export MONGO_URI="mongodb+srv://<username>:<password>@<your-cluster-url>/ptes?retryWrites=true&w=majority"
   ```

---

## Usage

Once configured, follow these steps to reset and generate testing data:

1. **Run the Script:**

   ```bash
   python reset_and_generate_ptes_data.py
   ```

2. **Monitor the Output:**

   The script utilizes the `logging` module to provide real-time feedback. You should see log messages indicating the progress of each step.

   **Sample Output:**

   ```
   INFO:__main__:Connected to MongoDB Atlas database: ptes
   INFO:__main__:Dropped collection: locations
   INFO:__main__:Dropped collection: transport_modes
   INFO:__main__:Dropped collection: routes
   INFO:__main__:Dropped collection: stops
   INFO:__main__:Dropped collection: journeys
   INFO:__main__:Created geospatial index on 'location' field in 'locations' collection.
   INFO:__main__:Inserted 9 transport modes.
   INFO:__main__:Inserted 100 locations.
   INFO:__main__:Prepared 100 routes.
   INFO:__main__:Inserted 500 routes.
   INFO:__main__:Inserted 7500 stops.
   INFO:__main__:Inserted 1000 journeys.
   INFO:__main__:Reset and data generation completed successfully.
   ```

3. **Post-Execution:**

   After successful execution, your MongoDB Atlas database named `ptes` will have the following collections populated with test data:

   - `transport_modes`
   - `locations`
   - `routes`
   - `stops`
   - `journeys`

---

## Script Structure

The `reset_and_generate_ptes_data.py` script is organized into several key functions to streamline the process:

1. **`reset_collections(db)`:**
   - Drops existing collections (`locations`, `transport_modes`, `routes`, `stops`, `journeys`) to reset the database.

2. **`create_geospatial_index(db)`:**
   - Creates a `2dsphere` index on the `location` field in the `locations` collection to optimize geospatial queries.

3. **`generate_transport_modes(db)`:**
   - Inserts predefined transport modes into the `transport_modes` collection.

4. **`generate_locations(db)`:**
   - Generates and inserts random geographical locations into the `locations` collection.

5. **`generate_routes(db)`:**
   - Generates and inserts transport routes associated with transport modes and locations into the `routes` collection.

6. **`generate_stops(db, route_ids)`:**
   - Generates and inserts stops for each route into the `stops` collection.

7. **`generate_journeys(db)`:**
   - Generates and inserts possible journey options based on origins, destinations, and available routes into the `journeys` collection.

8. **`convert_decimals(obj)`:**
   - Recursively converts any `Decimal` instances in a document to `float` to ensure BSON compatibility.

9. **`main()`:**
   - Orchestrates the execution flow by calling the above functions in the appropriate order.

---

## Verification

After running the script, verify that the data has been inserted correctly:

1. **Using MongoDB Atlas UI:**
   - Log in to your [MongoDB Atlas](https://cloud.mongodb.com/) account.
   - Navigate to your cluster and select the `ptes` database.
   - Examine each collection (`transport_modes`, `locations`, `routes`, `stops`, `journeys`) to ensure data has been populated.

2. **Using MongoDB Shell or a Client:**

   ```bash
   mongo "mongodb+srv://<your-cluster-url>/ptes" --username <username>
   ```

   Once connected, run the following commands:

   ```javascript
   use ptes

   db.transport_modes.countDocuments()    // Should return 9
   db.locations.countDocuments()          // Should return 100
   db.routes.countDocuments()             // Should return 500
   db.stops.countDocuments()              // Should return between 2500 and 10000 (500 routes * 5-20 stops)
   db.journeys.countDocuments()           // Should return up to 1000, may be less if some journeys were skipped
   ```

   **Sample Document Retrieval:**

   ```javascript
   db.locations.findOne().pretty()
   db.transport_modes.findOne().pretty()
   db.routes.findOne().pretty()
   db.stops.findOne().pretty()
   db.journeys.findOne().pretty()
   ```

3. **Test Geospatial Queries:**

   Ensure that the `locations` collection supports geospatial queries by performing a sample query.

   **Using MongoDB Shell:**

   ```javascript
   db.locations.find({
       location: {
           $near: {
               $geometry: { type: "Point", coordinates: [114.1694, 22.3193] }, // Example coordinates
               $maxDistance: 500 // in meters
           }
       }
   }).limit(10).pretty()
   ```

   **Expected Outcome:**

   - The query should return locations near the specified coordinates within a 500-meter radius.

---

## Customization

Customize the data generation process to better fit your testing requirements:

1. **Adjust Data Volume:**

   Modify the following variables in the script to generate more or fewer documents:

   ```python
   NUMBER_OF_LOCATIONS = 100          # Number of geographical locations
   NUMBER_OF_ROUTES = 500             # Number of transport routes
   NUMBER_OF_JOURNEYS = 1000          # Number of journey options
   ```

2. **Change Geographical Boundaries:**

   Update the bounding box coordinates to target a different geographical area.

   ```python
   # Bounding Box for Coordinates (Currently set to Hong Kong)
   MIN_LONGITUDE = 113.8
   MAX_LONGITUDE = 114.4
   MIN_LATITUDE = 22.25
   MAX_LATITUDE = 22.55
   ```

3. **Enhance Data Realism:**

   - **Route Numbering:**
     Implement more realistic route numbering schemes based on actual transport standards.
   
   - **Service Types:**
     Expand or modify service types to include more variations.

   ```python
   service_type = random.choice(["Express", "Regular", "Night", "Limited"])
   ```

4. **Expand Schema:**

   Add additional fields to collections as needed, such as `ratings`, `operational_status`, or `additional amenities`.

   ```python
   # Example: Adding 'status' to routes
   route = {
       ...
       "status": random.choice(["Operational", "Under Maintenance", "Suspended"]),
       ...
   }
   ```

5. **Implement Multi-Modal Journeys:**

   Extend the `generate_journeys` function to include interchanges between different transport modes for more complex journey simulations.

   ```python
   # Example: Including interchanges
   journey = {
       ...
       "routes": [
           {
               "route_id": route1["_id"],
               "mode_id": route1["mode_id"],
               ...
           },
           {
               "route_id": route2["_id"],
               "mode_id": route2["mode_id"],
               ...
           }
       ],
       ...
   }
   ```

---

## Troubleshooting

Encountering issues while running the script? Here are common problems and their solutions:

### 1. **Connection Errors**

**Error Message:**

```
pymongo.errors.OperationFailure: command delete not found, ...
```

**Solution:**

- **Check Connection String:**
  - Ensure that the `MONGO_URI` is correctly formatted with the right username, password, and cluster URL.
  
- **Verify User Permissions:**
  - Ensure the MongoDB user has `readWrite` permissions on the `ptes` database.
  
- **Confirm Collection Type:**
  - Ensure that the target collections are regular collections, not views, as views do not support write operations.

### 2. **Data Type Errors**

**Error Message:**

```
bson.errors.InvalidDocument: cannot encode object: Decimal('-113.966888'), of type: <class 'decimal.Decimal'>
```

**Solution:**

- **Ensure Numerical Fields Use Floats or Integers:**
  - The script includes a `convert_decimals` function to handle this. Ensure it's properly implemented.
  
- **Review Custom Data Fields:**
  - If you've added new fields, verify their data types.

### 3. **Insufficient Data Insertion**

**Issue:**

- Fewer documents are inserted than expected.

**Solution:**

- **Check Generation Logic:**
  - Ensure that the script isn't skipping document insertions due to missing references or failed criteria.
  
- **Review Logs:**
  - Use the logging output to identify where the script might be skipping or failing to insert documents.

### 4. **Script Crashes or Hangs**

**Solution:**

- **Check for Infinite Loops:**
  - Ensure that loops in the script have proper termination conditions.
  
- **Monitor Resource Usage:**
  - For large data volumes, ensure your machine has sufficient memory and processing power.

### 5. **Environment Issues**

**Solution:**

- **Python Version:**
  - Ensure you're using Python 3.6 or higher.
  
- **Dependency Versions:**
  - Ensure that `pymongo` and `faker` are up-to-date.

   ```bash
   pip install --upgrade pymongo faker
   ```

---

## Security

- **Protect Sensitive Credentials:**
  - **Avoid Hardcoding:** Do not hardcode sensitive information like the MongoDB URI in your scripts.
  
  - **Use Environment Variables:** Store sensitive data in environment variables or secure configuration files.

    **Example Using Python's `os` Module:**

    ```python
    import os

    MONGO_URI = os.getenv("MONGO_URI")
    ```

    **Set Environment Variable:**

    ```bash
    export MONGO_URI="mongodb+srv://<username>:<password>@<your-cluster-url>/ptes?retryWrites=true&w=majority"
    ```

- **Limit Network Access:**
  - **IP Whitelisting:** In MongoDB Atlas, restrict network access to trusted IP addresses.
  
  - **Use Strong Passwords:** Ensure that MongoDB users have strong, unique passwords.

---

## Contributing

Contributions are welcome! If you'd like to enhance the PTES Data Generator, consider the following steps:

1. **Fork the Repository:**

   Click the [Fork](https://github.com/yourusername/PTES-Data-Generator/fork) button at the top right of this page.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/yourusername/PTES-Data-Generator.git
   cd PTES-Data-Generator
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes:**

   Implement your feature or fix.

5. **Commit Your Changes:**

   ```bash
   git commit -m "Add your descriptive commit message"
   ```

6. **Push to Your Fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request:**

   Navigate to the original repository and create a pull request detailing your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any questions, issues, or suggestions, please contact:

**Steven Guo**

- **Email:** stevenguo@example.com
- **GitHub:** [@stevenguo](https://github.com/stevenguo)
- **LinkedIn:** [Steven Guo](https://www.linkedin.com/in/stevenguo)

Feel free to reach out, and I'll be happy to assist!

---

**Happy Testing! 🚍🚌🚇**
