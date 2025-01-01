# pypyr tasks

## TODOs

### path

- [ ] Ensure a custom `path` works where applicable
- [ ] Pass `path` as an [`argList` instead of a `kwarg`](https://pypyr.io/docs/context-parsers/argskwargs/)
  - Before: `pypyr lint flag1=True path=./some/folder`
  - After: `pypyr lint flag1=True ./some/folder`
