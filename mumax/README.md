# MuMax3 Simulator Component

## Description

The `MuMax3 Simulator` component provides an interface to run MuMax3 simulations. It processes an input `.mx3` script, sends it to a remote simulation server, executes the simulation, and retrieves the results. This component is useful for automating micromagnetic simulations using MuMax3.

## Inputs

- **Input `.mx3` File** (`str`): The path to the `.mx3` file containing the MuMax3 simulation script.

## Output

- **JSON Response**: The output consists of a JSON object containing the simulation result.
  - **`result`** (`str`): A success message or error message if the simulation fails.
  - **`images`** (`list`): A list of generated image file paths if the simulation is successful.

## Input Types

- **Input `.mx3` File**: `TEXT`

## Output Type

- **JSON**

## Usage

To use the `MuMax3 Simulator` component, provide a valid `.mx3` file as input. The component will upload the file to the MuMax3 simulation server, execute the simulation, and return the results in JSON format.

Example response:
```json
{
  "result": "Success",
  "images": ["image1.png", "image2.png"]
}
```
If there is an error during execution, the response will include an error message instead:
```json
{
  "result": "There has been an error 500",
  "images": []
}
```

## Summary

The `MuMax3 Simulator` component automates the execution of MuMax3 simulations by sending `.mx3` scripts to a remote server. It handles file uploads, execution requests, and result retrieval, providing a structured JSON response with the simulation results and any generated images.

