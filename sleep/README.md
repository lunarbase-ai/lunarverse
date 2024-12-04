<!--
SPDX-FileCopyrightText: Copyright © 2024 Lunarbase (https://lunarbase.ai/) <contact@lunarbase.ai>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Sleep Component

A sleep component enables delaying execution for a specified number of seconds. The component consists of a timeout field that accepts the number of seconds to delay and an input field that accepts any data. The provided input data will be passed through after the delay.

## Inputs

As mentioned above, the input consists of a timeout field and an input field.

| input name | input data type | example value | description |
|------------|-----------------|----------------|-------------|
| timeout    | int             | 5              | The number of seconds to delay. |
| input      | any             | "Hello World"  | The data to pass over after the delay. |

## Output

The component will output the input data after the specified delay.

## Example

See [Lunar](https://lunarbase.ai/) for an example of how to use this component in a workflow and much more.