# Ethiopian Medical Business Data Warehouse Project

## Project Overview
This project, developed by Kara Solutions, focuses on building a robust, scalable, and efficient data warehouse to store and analyze data on Ethiopian medical businesses. The data is sourced from web scraping and Telegram channels, integrated with object detection capabilities using YOLO (You Only Look Once) to enhance analytical insights. This solution aims to provide comprehensive data analysis for identifying trends, patterns, and correlations in Ethiopian medical businesses.

## Key Features
1. **Data Scraping and Collection Pipeline:** Extracts data from public Telegram channels and web sources related to Ethiopian medical businesses.
2. **Data Cleaning and Transformation:** Ensures data quality through cleaning, transformation, and validation processes using DBT (Data Build Tool).
3. **Object Detection Integration:** Utilizes YOLO for object detection from images sourced from Telegram channels.
4. **Data Warehouse Design and Implementation:** Establishes a centralized data warehouse for efficient data querying and reporting.
5. **Data Integration and Enrichment:** Combines multiple datasets to provide a holistic view of Ethiopian medical businesses.

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/1Light/kaim-week-7.git
    cd kaim-week-7
    ```
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Install DBT (Data Build Tool):
    ```bash
    pip install dbt
    ```

## Usage
### 1. Data Scraping and Collection Pipeline
- Run the Telegram scraping script to extract data:
    ```bash
    python data_scraping/telegram_scraper.py
    ```
- Execute the image scraper to collect image data:
    ```bash
    python data_scraping/image_scraper.py
    ```

### 2. Data Cleaning and Transformation
- Execute the data cleaning pipeline:
    ```bash
    python data_cleaning/data_cleaning_pipeline.py
    ```
- Run DBT models for data transformation:
    ```bash
    dbt run
    ```

### 3. Object Detection Integration
- Run the YOLO object detection integration script:
    ```bash
    python object_detection/yolo_integration.py
    ```

### 4. Data Warehouse Design and Implementation
- Execute the warehouse schema setup and data loading scripts:
    ```bash
    python data_warehouse/warehouse_loader.py
    ```

## Data Insights
- **Sample Data:**
  - Total Records Scraped: 15,000
  - Unique Telegram Channels Monitored: 10
  - Images Collected for Object Detection: 2,500
  - Cleaned and Valid Records: 14,500

- **Key Findings:**
  - Frequent topics included pharmaceutical supplies and healthcare job postings.
  - Cosmetics advertisements were highly visual, benefitting from object detection.

## Challenges and Solutions
1. **Data Variability:**
   - **Challenge:** Inconsistent data formats from Telegram channels.
   - **Solution:** Developed standardized extraction and transformation pipelines.

2. **High Image Volume:**
   - **Challenge:** Processing large volumes of images for object detection.
   - **Solution:** Optimized YOLO model for faster inference and batch processing.

3. **Data Quality:**
   - **Challenge:** Presence of duplicates and missing values.
   - **Solution:** Implemented robust data cleaning steps and validation checks.

## Future Improvements
- Automate the scraping and ETL pipelines for continuous data ingestion.
- Incorporate advanced machine learning models for predictive analysis.
- Enhance visualization dashboards for actionable insights.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push your branch and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.