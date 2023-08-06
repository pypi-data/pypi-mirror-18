# pyconfigvar

Manage required and optional environment variables in your Python scripts.

## Example

```sh
$ REQUIRED_VAR="something" python
```

```python
>>> import pyconfigvar
>>> pyconfigvar.requiredvar('REQUIRED_VAR')
'something'
>>> pyconfigvar.requiredvar('MISSING_VAR')
>>> pyconfigvar.requiredvar('MISSING_VAR')
MISSING_VAR was not supplied in the environment.
<drop back to shell>
```

## Usage

There are four functions available:

### `requiredvar(var)`

Returns the contents of the environment variable `var`. If `var` is not present in the environment, `sys.exit()` is invoked to terminate the interpreter.

### `optionalvar(var, default)`

Like `requiredvar()`, but instead of terminating, `default` is returned.

### `requiredbool(var)`

Like `requiredvar()`, but will coerce the value of `var` into a boolean and return that. Essentially, anything non-zero or non-empty will return True, otherwise it will return `False`.

### `optionalbool(var, default)`

Like `requiredbool()`, but will return `default` rather than terminate the interpreter.

## Contributing

Pull request away!


