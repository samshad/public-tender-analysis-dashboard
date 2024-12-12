# Public Tender Analysis Dashboard - Nova Scotia

## Overview

This project aims to visualize and analyze public tender data from Nova Scotia. The goal is to provide insights into public tender activities, such as identifying trends, evaluating vendor performance, and understanding the distribution of awarded contracts. This project is a Python-based tool using Dash to create interactive visualizations for procurement data. It generates descriptive messages for visualizations like bar plots and word clouds, highlighting key trends and insights. The project leverages BERTopic for topic modeling.

## Dataset

The dataset used in this project is sourced from the Nova Scotia Open Data Portal. Dataset: [Awarded Public Tenders dataset](https://data.novascotia.ca/Procurement-and-Contracts/Awarded-Public-Tenders/m6ps-8j6u/about_data).

## Installation

### Prerequisites

- Python 3.12
- Docker

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/samshad/public-tender-analysis-dashboard.git
    cd public-tender-analysis-dashboard
    ```

2. Build and run the project using Docker Compose:
    ```sh
    docker-compose up -d
    ```

3. Access the application at `http://localhost:8050`.

## Usage

The application provides a dashboard to visualize and analyze public tender data. It includes features such as:

- **Clustering Analysis**: Grouping entities using KMeans and Agglomerative Clustering.
- **Trend Analysis**: Visualizing trends in awarded tenders over time.
- **Vendor Performance**: Evaluating the performance of different vendors.
- **BERTopic**: Topic modeling to get context from tender descriptions using the BERTopic model.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- Nova Scotia Open Data Portal for providing the [Awarded Public Tenders dataset](https://data.novascotia.ca/Procurement-and-Contracts/Awarded-Public-Tenders/m6ps-8j6u/about_data).
- [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/) for the visualization framework.
- [BERTopic](https://maartengr.github.io/BERTopic/index.html) for topic modeling.
