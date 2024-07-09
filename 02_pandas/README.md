# Pandas Library Overview

This repository provides a comprehensive overview of the Pandas library, covering its various functionalities and operations. The content is organized into different sections,
each focusing on a specific aspect of Pandas.

## Table of Contents

0. [Reference](https://pandas.pydata.org/docs/reference/)
1. [Data Structures](01_data_structures.ipynb)
2. [Data Creation](02_data_creation.ipynb)
3. [Data Import and Export](03_data_import_export.ipynb)
4. [Data Inspection and Summarization](04_data_inspection_summarization.ipynb)
5. [Data Selection and Indexing](05_data_selection_indexing.ipynb)
6. [Data Cleaning](06_data_cleaning.ipynb)
7. [Data Transformation](07_data_transformation.ipynb)
8. [Grouping and Aggregation](08_grouping_aggregation.ipynb)
9. [Merging and Joining](09_merging_joining.ipynb)
10. [Time Series](10_time_series.ipynb)
11. [Visualization](11_visualization.ipynb)

## 1. Data Structures

- **Series**: One-dimensional labeled array.
- **DataFrame**: Two-dimensional, size-mutable, heterogeneous tabular data.

## 2. Data Creation

- Create Series and DataFrames from dictionaries, lists, NumPy arrays, etc.

## 3. Data Import and Export

- **CSV**: `read_csv`, `to_csv`
- **Excel**: `read_excel`, `to_excel`
- **SQL**: `read_sql`, `to_sql`
- **JSON**: `read_json`, `to_json`
- **Other Formats**: `read_html`, `read_pickle`, `to_pickle`

## 4. Data Inspection and Summarization

- **Head and Tail**: `head()`, `tail()`
- **Info**: `info()`
- **Description**: `describe()`
- **Shape and Size**: `shape`, `size`

## 5. Data Selection and Indexing

- **Selection**: Using `[]`, `.loc`, `.iloc`, `.at`, `.iat`
- **Filtering**: Conditional selection with boolean indexing
- **Setting Values**: Direct assignment and `.loc`, `.iloc`

## 6. Data Cleaning

- **Handling Missing Data**: `isnull()`, `dropna()`, `fillna()`
- **Replacing Values**: `replace()`
- **Duplicated Data**: `duplicated()`, `drop_duplicates()`

## 7. Data Transformation

- **Renaming**: `rename()`
- **Mapping and Applying Functions**: `apply()`, `map()`, `applymap()`
- **Sorting**: `sort_values()`, `sort_index()`
- **Reshaping**: `pivot()`, `pivot_table()`, `melt()`

## 8. Grouping and Aggregation

- **Grouping**: `groupby()`
- **Aggregation**: `agg()`, `aggregate()`, `transform()`

## 9. Merging and Joining

- **Concatenation**: `concat()`
- **Merging**: `merge()`
- **Joining**: `join()`

## 10. Time Series

- **Date Range**: `date_range()`
- **Resampling**: `resample()`
- **Shifting**: `shift()`
- **Rolling and Expanding**: `rolling()`, `expanding()`

## 11. Visualization

- **Plotting**: `plot()`, integrated with Matplotlib

## Usage

Each section is accompanied by a Jupyter Notebook demonstrating the use of the respective operations and functions. You can find the notebooks in the corresponding directories.

Happy Learning!
