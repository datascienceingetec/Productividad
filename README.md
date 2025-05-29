# IngetecProductivity

IngetecProductivity is a project designed to calculate and visualize employee productivity. It achieves this by:

- **Collecting data from various sources:** This includes Autodesk usage, meeting records, chat logs, VPN activity, and interactions with other files.
- **Weighting activities:** The system allows for different activities to be assigned different weights, reflecting their relative importance in overall productivity metrics.
- **Visualizing data:** Productivity data is presented through a user-friendly, web-based dashboard, enabling easy monitoring and analysis.

## Frontend

The frontend is a React-based dashboard responsible for visualizing the processed productivity data. It is built using `frontend/index.html` and `frontend/dashboard.js`.

Key features of the dashboard include:

### Charts
The dashboard utilizes various charts to represent productivity insights:
- **Productivity Over Time:** A Line Chart showing productivity trends.
- **Distribution of Productivity:** A Pie Chart illustrating the spread of productivity levels.
- **Average Productivity:** An Area Chart depicting the average productivity.
- **Activity Breakdown:** A Radar Chart that breaks down activities for a selected employee.
- **Productivity by Category:** A Bar Chart comparing productivity across different categories.

### Tables
Tabular data provides detailed views:
- **Monthly Average Table:** Displays average productivity on a monthly basis.
- **Low Connectivity Employees Table:** Lists employees experiencing low connectivity, which might impact productivity.

### Filters
To refine the data displayed, the dashboard offers several filters:
- Division
- Department
- Category
- Employee
- Date Range

### Technologies
The frontend is built with a modern JavaScript stack:
- **React:** For building the user interface components.
- **Recharts:** A composable charting library used for rendering the various charts.
- **TailwindCSS:** A utility-first CSS framework for styling the application.
- **Lodash:** A JavaScript utility library providing helpful functions.
- **D3.js:** A powerful library for data visualization, likely used in conjunction with Recharts or for custom visualizations.

## Backend and Data Processing

The backend is responsible for collecting, cleaning, and processing data from various sources to calculate employee productivity metrics. The core logic resides in Python scripts located in the `scripts/` directory.

### Key Scripts and Workflow

1.  **`scripts/main_advanced.py`**: This script orchestrates the entire data processing pipeline.
    *   It is presumed to first call `scripts/clean_main_file.py` (though its specific contents are not detailed here, its name suggests a role in preprocessing or cleaning an initial dataset).
    *   Following preprocessing, it executes `scripts/calculate_productivity.py` to perform the core productivity calculations.

2.  **`scripts/calculate_productivity.py`**: This is the central script for computing productivity.
    *   **Functionality**: It calculates both daily and aggregated monthly productivity scores for employees.
    *   **Inputs**:
        *   Cleaned Excel data (likely `data_cleaned.xlsx`, an output of `scripts/clean_main_file.py`).
        *   Autodesk usage data (`Autodesk.xlsx`).
        *   Meeting data (`Meetings.xlsx`).
        *   Chat data (`chats_source.csv`).
        *   VPN connection data (`VPN.csv`).
        *   Employee information (`INFORME_PERSONAL.xlsx`), which includes details like employee category.
    *   **Activity Weighting**: The script uses coefficients defined in `scripts/initial_parameters.json` to weigh different activities (e.g., Autodesk usage, meeting participation) based on the employee's category (e.g., modelers, cat12345, others). This allows for a nuanced calculation of productivity that reflects the varying importance of tasks across different roles.
    *   **Outputs**:
        *   `productivity_by_day.xlsx`: Contains daily productivity scores for each employee.
        *   `final_table_with_results.xlsx`: Presents aggregated monthly productivity results, suitable for final review and visualization.

3.  **`scripts/initial_parameters.json`**: This JSON file is crucial for configuring the data processing and productivity calculation.
    *   **`EMAILS_TO_DELETE`**: A list of email addresses to be excluded from processing.
    *   **`YEAR`**, **`MONTH`**: Define the specific period for which productivity is being calculated. This allows for targeted analysis of different timeframes.
    *   **`COEFFICIENTS`**: Contains the weighting factors for different activities (e.g., `AUTODESK_TIME_COEFFICIENT`, `MEETINGS_COEFFICIENT`, `CHATS_COEFFICIENT`) and how these apply to various employee categories. This is fundamental to tailoring the productivity metric to the specific nature of work within the organization.

The data processing pipeline is designed to transform raw activity data into actionable productivity insights, with configurable parameters ensuring flexibility in the calculation logic.

## How to Run the Project

This section provides instructions on how to set up and run the IngetecProductivity project.

### 1. Prerequisites

*   **Python:** Ensure you have Python 3.x installed.
*   **Python Libraries:** Install the necessary Python libraries using pip:
    ```bash
    pip install pandas xlsxwriter
    ```
*   **Input Data Files:**
    *   All input Excel files (`.xlsx`) and CSV files (`.csv`) detailed in the "Backend and Data Processing" section (e.g., `Autodesk.xlsx`, `Meetings.xlsx`, `chats_source.csv`, `VPN.csv`, `INFORME_PERSONAL.xlsx`, and the initial cleaned data file) must be present.
    *   These files should be located in the directory structure expected by the scripts, which is typically `C:\Productividad\{YEAR}-{MONTH}\` (replace `{YEAR}` and `{MONTH}` with the actual year and month of the data being processed). Adjust paths in `scripts/initial_parameters.json` if your structure differs.

### 2. Data Processing (Backend)

1.  **Configure Parameters:**
    *   Open `scripts/initial_parameters.json`.
    *   Set the `YEAR` and `MONTH` variables to match the period of the data you wish to process.
    *   Update `EMAILS_TO_DELETE` with any email addresses that should be excluded from the analysis.
    *   Verify and adjust the file paths for all input data sources if they differ from the defaults.
    *   Review and modify the `COEFFICIENTS` for activity weighting if necessary, to align with your organization's productivity metrics.

2.  **Run the Main Script:**
    *   Navigate to the project's root directory in your terminal.
    *   Execute the main processing script:
        ```bash
        python scripts/main_advanced.py
        ```
    *   This script will perform data cleaning (via `scripts/clean_main_file.py` implicitly) and then calculate productivity (via `scripts/calculate_productivity.py`).

3.  **Review Outputs:**
    *   Upon successful execution, the script will generate output files in the relevant `C:\Productividad\{YEAR}-{MONTH}\` directory (or the configured output path).
    *   Key output files include:
        *   `productivity_by_day.xlsx`: Daily productivity scores.
        *   `final_table_with_results.xlsx`: Aggregated monthly productivity results.

### 3. Viewing the Dashboard (Frontend)

*   **Current State (Mock Data):** The frontend dashboard (`frontend/index.html` and `frontend/dashboard.js`) is currently set up to use mock data for demonstration purposes.
    *   To view it, simply open `frontend/index.html` directly in a web browser.

*   **Displaying Real Data (Future Enhancement):**
    *   To connect the dashboard to the actual data generated by the Python backend, modifications to `frontend/dashboard.js` would be required.
    *   This would involve:
        *   Fetching the data from the output Excel files (e.g., by converting them to a JSON format that the frontend can consume).
        *   Alternatively, developing a simple backend API (perhaps using Flask or FastAPI, potentially leveraging the placeholder `app/main.py`) to serve the productivity data to the frontend.
    *   This integration step is not yet implemented in the current version.

## Project Structure

The repository is organized into several key directories:

-   **`app/`**: This directory is intended for a backend API application.
    -   `main.py`: Main application file (currently a placeholder).
    -   `api/v1/endpoints.py`: API endpoint definitions (currently a placeholder).
-   **`frontend/`**: Contains all files related to the React-based frontend dashboard.
    -   `index.html`: The main HTML file for the dashboard.
    -   `dashboard.js`: The core JavaScript file containing the React application and chart logic.
    -   `styles.css`: CSS styles for the dashboard.
-   **`scripts/`**: Houses the Python scripts responsible for data processing and productivity calculations.
    -   `main_advanced.py`: Orchestrates the data cleaning and calculation workflow.
    -   `calculate_productivity.py`: Performs the core productivity calculations based on various inputs and configured weights.
    -   `clean_main_file.py`: (Assumed) Handles preprocessing and cleaning of initial data.
    -   `initial_parameters.json`: Configuration file for the backend scripts, defining processing period, file paths, and activity weighting coefficients.
-   **`.github/`**: Contains GitHub-specific configurations.
    -   `settings.yml`: Repository-level settings for GitHub.
    -   `workflows/`: Defines CI/CD pipelines.
        -   `lint.yml`: Workflow for code linting.
        -   `test.yml`: Workflow for running automated tests.
-   **`CONTRIBUTING.md`**: Provides detailed guidelines for contributing to the project, including branch strategy, commit conventions, and pull request processes.
-   **`README.md`**: This file – providing an overview and documentation for the project.

## Contributing

Contributions to the IngetecProductivity project are welcome!

For detailed information on how to contribute, please refer to the `CONTRIBUTING.md` file. This document includes guidelines on:

-   Branching strategy
-   Commit message conventions
-   Pull Request (PR) process
-   Coding standards
-   General development workflow

Adhering to these guidelines will help ensure a smooth and effective collaboration process.

## License

This project does not currently have a license. This means that standard copyright laws apply, and usage, distribution, or modification by others may be restricted.

It is highly recommended to add a `LICENSE` file to the repository to clarify the terms under which this software can be used, modified, and distributed.

If an open-source license is desired, a common choice is the MIT License. If the MIT License were adopted, you could include a badge like this in the README:

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Please consider adding a `LICENSE` file to define the project's usage terms.
