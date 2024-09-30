# Elasticsearch Store Component

## Overview

The **Elasticsearch Store** component is designed to facilitate the storage of data in a specified Elasticsearch instance. By using this component, users can efficiently save data for future search and retrieval operations.

## Description

The Elasticsearch Store component takes a list of data entries as input and stores these entries in the designated Elasticsearch index. This component is ideal for applications that require robust search capabilities on large datasets.

## Input Types

- **Data**: The data to be stored, provided as a list. Each item in the list represents a single entry to be indexed in Elasticsearch.

## Output Type

- **JSON**: The output is a JSON object that contains the status and details of the data storage operation.

## Configuration Parameters

To properly configure the Elasticsearch Store component, you need to provide the following parameters:

- **hostname**: The hostname or IP address of the Elasticsearch instance.
- **port**: The port number on which the Elasticsearch instance is running.
- **username**: The username for authenticating with the Elasticsearch instance.
- **password**: The password for authenticating with the Elasticsearch instance.
- **index**: The name of the Elasticsearch index where the data will be stored.

## Summary

The Elasticsearch Store component is a powerful tool for storing data in Elasticsearch, making it easy to perform future searches on large datasets. By correctly configuring the necessary parameters, users can ensure seamless integration with their Elasticsearch instance and take advantage of its advanced search capabilities.