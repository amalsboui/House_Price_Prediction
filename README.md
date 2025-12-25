# House Price Prediction

This project aims to predict house prices in Tunisia based on various features such as surface area, number of rooms, and location. We use machine learning models to predict the prices of houses and provide a comprehensive analysis.

## Table of Contents
1. [Overview](#overview)
2. [Data Collection](#data-collection)
3. [Data Preprocessing](#data-preprocessing)
4. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
5. [Modeling](#modeling)
   - [Linear Regression](#linear-regression)
   - [Random Forest](#random-forest)
   - [Hyperparameter Tuning](#hyperparameter-tuning)
6. [Evaluation Metrics](#evaluation-metrics)
7. [Ongoing Work](#ongoing-work)

---

## Overview

The goal of this project is to estimate house prices in Tunisia based on several features including:
- Surface area (m²)
- Number of rooms
- Property type (apartment vs house)
- Governorate (location)

We perform exploratory data analysis (EDA) to understand the relationships between the features and target variable (price). The project uses machine learning models to predict the log-transformed price (`log(price)`), with various models and their performances evaluated.

---

## Data Collection

The dataset is collected by scraping **real estate listings** from three sources:
1. **Mubawab.tn**: 6,588 listings
2. **Tayara.tn**: 1,922 listings
3. **Immobilier.tn**: 726 listings

Each listing contains information like:
- Price
- Surface area (m²)
- Number of rooms
- Location (governorate)
- Property type (apartment or house)

### Web Scraping with Scrapy

The data collection was done using **Scrapy**, a powerful web scraping framework. We created a **spider** for each website to crawl and extract relevant data.

### Pipelines and Items

We used Scrapy items and pipelines to process the scraped data.

- **Items**: Defined the fields for the scraped data (price, surface, rooms, etc.) for easy handling and export.

- **Pipelines**: These were used to clean and process the data, such as removing rows with missing values or cleaning inconsistent entries.


The collected data was merged and cleaned for further analysis.

---

## Data Preprocessing

### 1. **Handling Missing Values**
- The columns with missing values were **dropped** to ensure data integrity.
- Rows with invalid or missing values were removed.

### 2. **Normalization and Transformation**
- The column `prix` (price) was **log-transformed** (`log(1 + price)`) to make it more normally distributed.
- Locations (cities) were normalized to match the **governorates** in Tunisia for better consistency.
  
### 3. **Outliers Removal**
- Outliers in the price and surface columns were **handled** by keeping extreme but plausible values, as some high-end properties with larger areas were still valid.
  

---

## Exploratory Data Analysis (EDA)

EDA was performed to understand the data and uncover insights:
- **Histograms** of price and surface distribution to assess data skewness.
- **Log-transformation** was applied to both price and surface to normalize the data and reduce skew.
- **Location-wise analysis** showed that most properties are concentrated in urban governorates like **Tunis**, **Nabeul**, and **Ariana**.
- The most important features affecting price were identified as:
  - **Surface area**
  - **Number of rooms**
  - **Location (governorates)**
  - **Property type (apartment vs house)**

---

## Modeling

### Linear Regression (Baseline Model)
We started with a **Linear Regression** model to set a **baseline performance**.

- **RMSE**: 0.5529
- **R²**: 0.5168

This model helped us understand the relationship between the features and price in a very simple, interpretable way.

### Random Forest
Next, we trained a **Random Forest Regressor**, a non-linear model that can capture complex interactions between features. We performed hyperparameter tuning and evaluated the model.

- **Initial RMSE**: 0.5119
- **Initial R²**: 0.5857

We tuned hyperparameters like `max_depth`, `min_samples_leaf`, and `n_estimators` using **GridSearchCV** to optimize performance.

- **Best RMSE** after tuning: 0.4819
- **Best R²** after tuning: 0.6330

### Hyperparameter Tuning
We performed **hyperparameter tuning** on the **Random Forest** model using **GridSearchCV** to identify the best parameters. After tuning, we achieved better accuracy and performance.

---

## Evaluation Metrics

For model evaluation, we used the following metrics:
- **RMSE (Root Mean Squared Error)**: Measures the average error in the predictions.
- **R² (Coefficient of Determination)**: Measures how well the model explains the variance in the target variable.

The best performance was achieved with **Random Forest** with **RMSE = 0.4819** and **R² = 0.6330**, indicating that the model is **reasonably accurate** at predicting house prices.

---

## Ongoing Work

This project is **ongoing**, and there are several potential directions for further work:
- **Try more advanced models** like **XGBoost** or **LightGBM** to see if they can further improve the performance.
- **Model Improvement** through additional **feature engineering**, hyperparameter tuning, and the use of **ensemble methods**.
- **Model Deployment**: The trained model can be deployed as a **web API** for real-time predictions.
- **MLOps**....
