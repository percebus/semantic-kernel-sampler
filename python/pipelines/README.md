# pypyr tasks

[`TODO`s](./TODO.md)

## About

See [pypyr.io](https://pypyr.io/)

## RANT

I'm not a fan of the `pypyr` file discovery system.

- Either you dump all `.yaml` files in root
- Or you use a `pipelines/` folder, which is misleading. `/tasks` would be a better name.

## Tasks

| Task     | Command       | Notes                         |
| -------- | ------------- | ----------------------------- |
| Clean    | `pypyr clean` | Removes `__pycache__` files   |
| Lint     | `pypyr lint`  | Checks for lint               |
| Reformat | `pypyr style` | Reformats code, `lint`        |
| Test     | `pypyr test`  | `lint`s code, then runs tests |

### Convinience

| Task | Command     | Notes                                                     | defaults                            |
| ---- | ----------- | --------------------------------------------------------- | ----------------------------------- |
| Q.A. | `pypyr qa`  | Invokes `style`, `lint`, `test` & `test integration=True` | `style`, `lint`, `test` w/ `stats`  |
| R&D  | `pypyr dev` | Invokes `qa`                                              | `style`, `lint`, `test` w/o `stats` |
| CI   | `pypyr ci`  | Invokes `qa`                                              | `lint`, `test` w/ `stats`           |

### Flags

| flag          | values       | notes                                                                             |
| ------------- | ------------ | --------------------------------------------------------------------------------- |
| `npm`         | `True/False` | Enables/disables tasks that involve `npm` (i.e. `prettier`)                       |
| `style`       | `True/False` | Enables/disables `style`                                                          |
| `lint`        | `True/False` | Enables/disables `lint`                                                           |
| `test`        | `True/False` | Enables/disables unit `test`                                                      |
| `integration` | `True/False` | Enables/disables `integration` tests                                              |
| `stats`       | `True/False` | Enables/disables outputting `stats` (like `pylint --report y`, or `pytest --cov`) |
