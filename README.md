# IDX Exchange MLS Analytics Internship Project

## Project Overview

This repository contains my project work for the IDX Exchange Data Analyst Internship Program. The project focuses on cleaning, validating, aggregating, and analyzing MLS listing and sold transaction datasets using Python and Tableau. The goal of this project is to transform raw monthly MLS CSV files into analysis-ready datasets and build market intelligence dashboards that summarize housing market trends, property activity, and competitive performance across agents, offices, cities, counties, and ZIP codes.

## Tools Used

* Python
* Pandas
* Jupyter Notebook
* VS Code
* Tableau Public Desktop
* GitHub

## Project Workflow

The project follows a weekly data analytics pipeline:

1. Download and organize monthly MLS listing and sold transaction CSV files
2. Aggregate monthly CSV files into two main datasets:

   * `listings.csv`
   * `sold.csv`
4. Filter records to residential properties
5. Validate data quality and inspect missing values
6. Clean and transform date, numeric, geographic, and property fields
7. Engineer market metrics such as:

   * Price per square foot
   * Close-to-list price ratio
   * Days on market
   * Listing-to-contract days
   * Contract-to-close days
   * Year/month fields for time-series analysis
8. Detect and flag outliers
9. Build Tableau dashboards for market analysis and competitive intelligence
10. Prepare a final market intelligence report and presentation

## Data Notice

The raw and processed MLS CSV files are not included in this repository.

All datasets used in this project are provided through the IDX Exchange internship program and may contain confidential MLS transaction records. To protect data privacy and comply with program requirements, raw CSV files, processed CSV files, and source data files are excluded from GitHub.

## Current Progress

* Set up VS Code and Python environment
* Downloaded MLS CSV files from FTP
* Created an individual GitHub repository
* Verified that Python can locate the listing and sold CSV files
* Confirmed file counts for listing and sold datasets
* Started initial data exploration in Jupyter Notebook

## Author

Yue Gao
MSBA 1-year Student, University of Southern California
IDX Exchange Data Analyst Intern
