<h1 style="text-align: center;">
SHAIPER - AI for Surrogate Modelling
</p>
<div>
  <a href="assets/LICENSE">
    <img 
        src="https://img.shields.io/badge/License-MIT-yellow.svg" 
        alt="License: MIT">
    </img>
  </a>
</div>

</h1>

<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 30%;"
    src="assets/images/logo_large.png" 
    alt="SHAIPER LOGO">
</img>

## About
Welcome to the `SHAIPER - AI for Surrogate Modelling` community!

`SHAIPER` is currently being developed at the IT4Innovations National Supercomputing Center. Its purpose is to offer a comprehensive toolbox for experimentation with and the utilization of various models for surrogate modelling. The goal is to implement a state of the art software with respect to parallel scalability and efficiency while letting the researchers focus on more interesting aspects of their work, i.e. experiment with novel architectures, optimization methods etc.

`SHAIPER` is designed to offer comprehensive toolbox for:

- Efficient massivelly parallel dataset manipulation, analysis and information exports to standalone files.
- Modular AI models assembly.
- Hyperparameter space exploration for finding optimal model structures and learning behaviour.
- Model training monitoring and reporting.
- Feature optimizations based on gradient/genetic and mixed algorithms using the trained models.

### Current Capabilities
In the current state, the software is usable for the following tasks:

- Tabular Database creation, augmentation, transformation, utilization in training and statistics calculation + report exporting.
- Modular model assembly and utilization in training and parameter optimization
- Arbitrary Optimizer and Scheduler utilization
- Basic Loss function utilization
- Training progress reporting
- Parameter search via first order gradient methods

## Current status of the development with respect to ecosystem around the source codes

<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 30%;"
    src="assets/images/design_process/design_process.drawio.svg" 
    alt="Status">
</img>

## Data management Design Intention and Development Status

<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 60%;"
    src="assets/images/data/data_global.drawio.svg" 
    alt="Data">
</img>

## Training Workflow and Development Status

<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 90%;"
    src="assets/images/training/training_global.drawio.svg" 
    alt="Training">
</img>

## Utilization Development Status

<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 30%;"
    src="assets/images/utilization/utilization.drawio.svg" 
    alt="Utilization">
</img>

## Design Pillars of required UIX

<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 30%;"
    src="assets/images/UI/UIX_global.drawio.svg" 
    alt="Utilization">
</img>


<!-- # Feature Set

## AI dataset manipulation, analysis and report exports
Currently, the software contains tools for analysis and reporting on Tabular datasets. Other planned features are for:

- Mesh datasets
- Image datasets
- Time series datasets

The data management and manipulation is fully parallelized via the utilization of [MPI](https://www.open-mpi.org/) and [LMDB](https://lmdb.readthedocs.io).

## Model creation
The intended use of this software is for researchers to experiment with vast model collections. To this end, there are se -->

# Installation
For the installation steps, refer to the [Installation Tutorial](installation_docs/index_installation.md).

# How to run the software
To learn about how to run & utilize the software, refer to the [Guide for Users](user_docs/index_user.md).

# Want to participate in development?
If you are a contributing developer, please refer to the [Note for Developers](developer_docs/index_developer.md).

