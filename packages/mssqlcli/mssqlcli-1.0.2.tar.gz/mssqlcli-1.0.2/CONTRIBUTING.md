# Contributing

MS-SQL CLI is an open-source project, hosted [on GitHub][1]. All Contributors are welcome, a current list of open issues is available [here][2].

## Development Environment

No additional dependencies are required for development, simpy follow the installation instructions. We recommend that you use `python setup.py develop`, rather than `install` to allow quick code changes.

## Testing

To test your code prior to submission, simply:

```bash
python setup.py test
```

This will ensure that tox and virtualenv are installed, and then run the test suite against the interpreters available locally.

## Acceptance Criteria

- Pull requests should follow full pep8 guidelines (the above testing will verify this).
- Pull requests should not reduce test coverage.
- Pull requests should have thought-out test cases for any new code.

The above requirements are verified via Travis-CI and Coveralls for Python versions 2.7, 3.4, and 3.5.


[1]: https://github.com/rtrox/mssqlcli
[2]: https://github.com/rtrox/mssqlcli/issues
