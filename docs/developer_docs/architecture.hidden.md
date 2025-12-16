# Structure of the Software

This software consists of three main components.

- Data management and analysis toolbox.
- Neural networks assembly and training toolbox.
- Neural network utilization toolbox.

## Data toolbox
This part of the software aims to represent training data efficiently for parallel I/O, analysis, utilization and reporting. 

In order for database to be created, an importer needs to be used. Importers are tailored converters which take an existing data format (like CSV, PNG, ...) and trasnform it to the internal database format. Each importer has its specific attributes which need to verbosely documented so they can be used by the users (see an example in the user's documentation [here](...)).

> The internal database uses [LMBD](https://lmdb.readthedocs.io) under the hood for fast and parallel file access and to **limit then number of files** on disk.

Currently, labeled tabular databases are supported with the following principles in mind.

### Labeled Database

Serves as overarching class 

