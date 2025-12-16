# Overview

This software has a single entry point, which parses the provided configuration file and performs the operations specified therein.

If you are using the installed package vie pip, the following commands will initiate the program.
```
. $ai_for_surrogate_modelling_path/bin/activate
mpirun -n N ai4sm --config path/to/main/config.yml
```

or alternatively, when you are working directly in the code-base (e.g. developing the software):
```
. $ai_for_surrogate_modelling_path/bin/activate
mpirun -n N python -m AI4SurrogateModelling.entry_point --config path/to/main/config.yml
```

where `N` denotes the desired number of mpi processes and `path/to/main/config.yml` denotes the main configuration file.

