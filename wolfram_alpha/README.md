# WolframAlpha Client Component

## Description

The **WolframAlpha Client** component is designed to interact with the WolframAlpha API to obtain responses based on user queries. This component sends a query to the WolframAlpha API and retrieves the resulting response in text format.

## Inputs

- **Query**: This is a required input parameter of type `TEXT`. This parameter represents the query string that will be sent to the WolframAlpha API.

## Output

- **Response**: The output of this component is of type `TEXT`. This represents the textual response received from the WolframAlpha API based on the input query.

## Configuration Parameters

- **wolfram_alpha_appid**: This configuration parameter is required to authenticate with the WolframAlpha API. You must provide a valid WolframAlpha App ID to use this component.

## Usage

To use the WolframAlpha Client component, you need to provide a query string and ensure that the WolframAlpha App ID is correctly configured. The component will send the query to the WolframAlpha API and return the response as text.

## Example Configuration

To set up the WolframAlpha Client component, you need to configure the `wolfram_alpha_appid` as shown below:

```json
{
  "wolfram_alpha_appid": "YOUR_APP_ID_HERE"
}
```

Replace `YOUR_APP_ID_HERE` with your actual WolframAlpha App ID.

## Notes

- Ensure that your WolframAlpha App ID is valid and has the necessary permissions to access the WolframAlpha API.
- This component only supports text-based queries and responses.

This completes the documentation for the WolframAlpha Client component. For further assistance, please refer to the official WolframAlpha API documentation or contact support.