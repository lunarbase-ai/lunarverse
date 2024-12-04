## Range Component

The Range component generates a sequence of numbers, starting from a specified number, incrementing by a specified step, and stopping before a specified number.

### Inputs

The input consists of three fields: `start`, `stop`, and `step`.

| input name | input data type | example value | description |
|------------|-----------------|---------------|-------------|
| start      | int             | 0             | The number to start from. |
| stop       | int             | 10            | The stopping number - it stops before it. |
| step       | int             | 1             | The value of the increment. |

### Output

The component will output the generated sequence as a generator, which needs to be consumed by some downstream component.

### Example

See [Lunar](https://lunarbase.ai/) for an example of how to use this component in a workflow and much more.

## Usage

To use the Range component, provide the `start`, `stop`, and `step` values as inputs. The component will generate a sequence of numbers based on these inputs.

If the inputs are:

```python
start = 0
stop = 10
step = 2
```

The output will be a list generator that can be consumed by downstream components.

```python
<generator object Range.run at 0x7f11f8b1b120>
```

### Example

See [Lunar](https://lunarbase.ai/) for an example of how to use this component in a workflow and much more.