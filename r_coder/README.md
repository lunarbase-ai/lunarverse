# R coder

## Description

The **R coder** component executes customized R code and outputs the value assigned to the R variable `result` during the execution of the code. This component is particularly useful for dynamically evaluating R scripts and retrieving specific results from the code execution.

## Inputs

- `Code` (str): A string of the R code to execute. The R code can be inputted manually by the user.

## Output

- (Any): The value of the variable `result` in the R code after execution.

## Input Types

- `Code`: `R_CODE`

## Output Type

- `ANY`

## Configuration Parameters

- `openai_api_key`: The API key for accessing OpenAI services.
- `openai_api_base`: The base URL for accessing OpenAI services.

## Usage

To use the **R coder** component, provide a string containing the R code to be executed. Ensure that the R code assigns a value to the variable `result`, as this will be the output of the component. Configure the necessary parameters (`openai_api_key` and `openai_api_base`) to enable access to OpenAI's services.

This component is designed to facilitate the execution of dynamic and customized R scripts, making it a powerful tool for data analysis, statistical computing, and other R-based tasks.