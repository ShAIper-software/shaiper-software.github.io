# Main Configuration

The software uses a system of configuration files controlling the flow of the program. The aim is to lessen the hardships imposed by efficient parallel implementations, sofisticated reporting, database management, consistent training procedures and parallel I/O. Below we describe the basic structure of the configuration files. See [Examples](examples/example_tabular.md) for more concrete tutorials.


## Main Configuration File
So, you have run the software with the attribute `--config path/to/main/config.yml`, which points to the main configuration file.
The main configuration YAML file consists of three components.

### `main`
The top-level behaviour of the software is described inside the main section.
```
main:
    logging: info/debug                     # specifies the loggin level
    logging_directory: path/to/logs/storage # where should the logs be stored
    parallelization: distributed/isolated   # should all processes train a single model, or should each process do its own thing?
    seed: int                               # sets all random seeds to this value, for reproducibility purposes
```

### `aliases`
Writing configuration files may contain very long and/or repeating values. To ease the writing of the configurations, the user can specify so-called aliases in the form of `alias_key: alias_value`. This tells the configuration parser, that all values inside the configuration files in the form `$alias_key$` should be replaced by the corresponding value `alias_value`.

Aliases can be recursively defined, i.e. one alias can use other alias in its value. Aliases cannot use aliases in their keys. The software checks if the aliases are defined correctly, i.e. that all aliases are replaced by an alias value and that nested aliases do not form a cyclic alias definition.
```
aliases:
    alias_key_0: alias_value_0
    alias_key_1: alias_value_1
    alias_key_2: alias_value_2-$alias_key_1$
```

### `operations`
The last component of the main configuration file contains the operations to be performed by the program. Each operation has its unique numerical suffix which specifies the order of operations. The configuration parser checks the correctness of the operational IDs.

```
operations:
    operation_0: path/to/config_0.yml
    operation_25: path/to/config_25.yml
    operation_15: path/to/config_15.yml
    operation_10: path/to/config_10.yml
```
As you can see, the numerical suffices need not to form a sequence and do not need to be ordered in the configuration file. The existence of the files the operation points to is verified before any computation takes place.

