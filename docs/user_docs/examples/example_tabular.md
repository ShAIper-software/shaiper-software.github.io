# Example Tabular (Random)

Here you can find an overview of a complete example in which you learn:

```
- How to define random Tabular datasets with various data subgroups
- How to process the dataset and export its various statistics
- How to define a basic loss function
- How to define optimizers
- How to define schedulers
- How to define and train a model
- How to use a trained model in search of optimal parameter configurations
```

The configuration scripts for this example can located at `conf/examples/random`.

To run this example, use the commands depicted in the [Overview](index_user.md).

## The Main configuration file
(`conf/examples/random/run_config.yml`)
This file defines a lot of aliases and the complete workflow in terms of the operational configuration files.
The system of aliases was chosen to simplify the definition of the model size, size of the dataset and datatype of the datasets and models being used.

```yaml
main:
  logging: info # possible values: info/debug
  logging_directory: logs/examples/random # default value: logs
  parallelization: distributed # possible values: distributed/isolated
  seed: 42

aliases:
  project_path: AI4SurrogateModelling.src
  dtype: float32

  input_key_known: inputs_group_known
  input_key_unknown: inputs_group_unknown
  output_key: outputs_group

  input_dim: 7
  output_dim: 4
  nrows: 10000

  ConfigDirectory: conf/examples/random

  DatabaseTabular: $project_path$.database.labeled.tabular.database_tabular.DatabaseTabular
  Importer: $project_path$.importer.tabular.database_importer_tabular_random.ImporterTabularRandom

  dim_layer_1: 256
  dim_layer_2: 128
  dim_layer_3: 64
  dropout_layer_1: 0.25
  dropout_layer_2: 0.25
  dropout_layer_3: 0.25

  Example_ID: random_example
  DatabaseDirectory: DATABASE_EXAMPLES/$Example_ID$
  results_dir: results/random_example

operations:
  operation_0: $ConfigDirectory$/data_create.yml
  operation_1: $ConfigDirectory$/data_export.yml
  operation_10: $ConfigDirectory$/define_models.yml
  operation_20: $ConfigDirectory$/define_optimizers.yml
  operation_30: $ConfigDirectory$/define_schedulers.yml
  operation_40: $ConfigDirectory$/define_losses.yml
  operation_51: $ConfigDirectory$/model_refine.yml
  operation_60: $ConfigDirectory$/find_parameters.yml
```

## Operation - Create Database
(`conf/examples/random/data_create.yml`)
The first operation performed is to define the dataset. For this we need to define two objects, the database itself and at least one importer. In our case, we use a tabular database and a random tabular importer (i.e. it fills the database with random data)

The database object has UID `database` and the importer object has UID `random_importer` for future reference in other operational configuration files. The random importer is tasked to define tabular data with 11 columns, 7 of wchich are inputs and 4 of which are the outputs. The 7 inputs are further divided into two groups. Group `$input_key_known$` represents those inputs, for which we prescribe known values in the utilization step. Group `$input_key_unknown$` represents a subset of inputs the values of which we are tasked to find during the utilization step.

After the object definition, several actions are defined.

- `action_0` clears the whole database by calling a member function `clear_database()` of the `TabularDatabase` class.
- `action 1` uses another member function of the TabularDatabase `add_data()`, which uses the supplied importers to fill the database.
- `action_2` takes the data in the database and transforms each column in each data group to fit into the specified range.
- `action_4` removes all columns which do not contain enough information, e.g. columns which are highly correlated to ther columns, or columns which do not contain enough variance in the data.
- `action_5` defines a split of the database into three groups, `train` with 80% of rows, `test` with 20% of rows and `validation` with 0% of rows.

In this example, the database is stored in the directory `DATABASE_EXAMPLES/random_example` is created.

```yaml
objects:
  database:
    constructor: $DatabaseTabular$
    parameters: 
      path_tgt: $DatabaseDirectory$

  random_importer:
    constructor: $Importer$
    parameters:
      nentries: $nrows$
      data_column_groups:
        $input_key_known$: [0, 1]
        $input_key_unknown$: [2, 3, 5, 7, 9]
        $output_key$: [4, 6, 8, 10]

actions:
  action_0:
    object_uid: database
    fname: clear_database

  action_1:
    object_uid: database
    fname: add_data
    parameters:
      importers: [
        random_importer,
      ]

  action_2:
    object_uid: database
    fname: transform_range
    parameters:
      keys: [$input_key_known$, $input_key_unknown$, $output_key$]
      target_range: (-1, 1)

  action_4:
    object_uid: database
    fname: cleanup_columns
    parameters:
      keys_to_consider: [$input_key_known$, $input_key_unknown$, $output_key$]
      correlation_eps: 1e-6
      variance_eps: 1e-6

  action_5:
    object_uid: database
    fname: train_test_split
    parameters:
      train_ratio: 0.8
      test_ratio: 0.2
      validation_ratio: 0.0
```

## Operation - Database Export

Each database can be analyzed and results presented. One of the methods is to generate a standalone HTML file containing predefined information. 

This operation file defines one object `database`, located at the path identical to the `database` in the previous configuration file.

There is only one action to be performed, to call the method `export_to_html` located deep in the source code hierarchy, which takes the supplied tabular database and exports various statistics to the specified file.

In this example, a file at `results/random_example/reports/database.html` is created.

```yaml
objects:
  database:
    constructor: $DatabaseTabular$
    parameters: 
      path_tgt: $DatabaseDirectory$

actions:
  action_20:
    fname: $project_path$.export.reports.tabular.ReporterTabular.export_to_html
    parameters:
      database: database
      tgt_fn: $results_dir$/reports/database.html
```


## Operation - Model Definition

This operational file showcases the possibilities of creating nested object dependencies and arbitrary dependent structures.
This file defines several pytorch models, all of them combining into a single `final_model` to be trained and used utilization.

```yaml
objects:

  block_model_MLP_01: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$dim_layer_1$, $dim_layer_1$]
      layer_activations: [['layer_norm_$dim_layer_1$', 'dropout_$dropout_layer_1$'], ['gelu']]
      layer_biases: [False, True]
      name: "The first hidden MLP block"
      input_keys: [$input_key_known$]
      output_keys: [$input_key_known$]

  block_model_MLP_02: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$dim_layer_2$, $dim_layer_2$]
      layer_activations: [['layer_norm_$dim_layer_2$', 'dropout_$dropout_layer_2$'], ['gelu']]
      layer_biases: [False, True]
      name: "The second hidden MLP block"
      input_keys: [$input_key_known$]
      output_keys: [$input_key_known$]

  block_model_MLP_03: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$dim_layer_3$, $dim_layer_3$]
      layer_activations: [['layer_norm_$dim_layer_3$', 'dropout_$dropout_layer_3$'], ['gelu']]
      layer_biases: [False, True]
      name: "The third hidden MLP block"
      input_keys: [$input_key_known$]
      output_keys: [$input_key_known$]

  block_model_MLP_input: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$input_dim$, $dim_layer_1$]
      layer_activations: [[None], ['gelu']]
      layer_biases: [False, True]
      name: "An input MLP block"
      input_keys: [$input_key_known$, $input_key_unknown$]
      output_keys: [$input_key_known$]

  transfer_layer_00: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$dim_layer_1$, $dim_layer_2$]
      layer_activations: [[None], ['gelu']]
      layer_biases: [False, True]
      name: "A transfer MLP block"
      input_keys: [$input_key_known$]
      output_keys: [$input_key_known$]

  transfer_layer_01: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$dim_layer_2$, $dim_layer_3$]
      layer_activations: [[None], ['gelu']]
      layer_biases: [False, True]
      name: "A transfer MLP block"
      input_keys: [$input_key_known$]
      output_keys: [$input_key_known$]

  transfer_layer_output: 
    constructor: $project_path$.model.models.other.mlp.MultiLayerPerceptron
    parameters:
      dtype: $dtype$
      layer_vertices: [$dim_layer_3$, $output_dim$]
      layer_activations: [[None], ['tanh']]
      layer_biases: [False, True]
      name: "A final output MLP block"
      input_keys: [$input_key_known$]
      output_keys: [$output_key$]

  residual_layer_00:
    constructor: $project_path$.model.models.layers.residual.ResidualLayer
    parameters:
      dtype: $dtype$
      model: block_model_MLP_01

  residual_layer_01:
    constructor: $project_path$.model.models.layers.residual.ResidualLayer
    parameters:
      dtype: $dtype$
      model: block_model_MLP_02

  residual_layer_02:
    constructor: $project_path$.model.models.layers.residual.ResidualLayer
    parameters:
      dtype: $dtype$
      model: block_model_MLP_03

  final_model:
    constructor: $project_path$.model.models.other.sequential.Sequential
    parameters:
      layers: [
        block_model_MLP_input,
        residual_layer_00,
        transfer_layer_00,
        residual_layer_01,
        transfer_layer_01,
        residual_layer_02,
        transfer_layer_output
      ]
      name: "A composite model for the vodik voltage prediction task"
```

## Operation - Optimizer Definition

This file contains a definition of three built-in optimizers with some of its most relevant parameters exposed. Users can reference any built in optimizers or custom-built ones.

```yaml
objects:
  optimizer_adam:
    constructor: torch.optim.Adam
    parameters:
      lr: 1e-3
      betas: (0.8, 0.99)
      eps: 1e-06
      weight_decay: 0
      amsgrad: False

  optimizer_adamW:
    constructor: torch.optim.AdamW
    parameters:
      lr: 1e-3
      weight_decay: 1e-5

  optimizer_SGD:
    constructor: torch.optim.SGD
    parameters:
      lr: 1e-3
      momentum: 0
      dampening: 0
      weight_decay: 0
      nesterov: False
```


## Operation - Scheduler Definition

This file contains a definition of one learning rate scheduler, namely the `LambdaLR` scheduler. User can reference any built in and applicable callable object to be used as the lambda function.

We offer one lambda function example located at `AI4SurrogateModelling.src.training.schedulers.lambdas.cyclical_lr.CyclicalLR` which serves as a cyclical learning rate manipulator.

```yaml
objects:
  lambda_scheduler_function_0:
    constructor: $project_path$.training.schedulers.lambdas.cyclical_lr.CyclicalLR
    parameters:
      log_factor_low: -1
      log_factor_high: 1
      periods: [500, 1000, 2000]

  scheduler_LAMBDA_0:
    constructor: torch.optim.lr_scheduler.LambdaLR
    parameters:
      lr_lambda: lambda_scheduler_function_0

```

## Operation - Loss Definition

This file contains an example of a very basic loss object used in the training procedure. The loss object has UID `loss_0` and the object constructor is located at `AI4SurrogateModelling.src.training.loss.loss_base.LossBase`. The constructor parameters allow the user to define losses based on the 

- weights & biases of the model
- difference in data calculated by the model specified by a nested dictionary. In this example, the loss is calculated between `real['outputs_group']` and `predicted['outputs_group']`
- partial derivatives of data calculated by the model with respect to other data, together with the prescription on the intervals in which the partial derivatives should lie.

The loss function keeps track of all individual losses with coefficients > 0 and provides a single criterion value to be used by a hyperparameter optimization procedure.

```yaml
objects:
  loss_0:
    constructor: $project_path$.training.loss.loss_base.LossBase
    parameters:
      model_parameters:
        mae: 0
        mse: 0
        rmae: 0
        rmse: 0

      outputs:
        # a key contained in the data provided by the model
        $output_key$: 
          # a key contained in the data provided by the dataloader
          $output_key$:
            mae: 0
            mse: 1
            rmae: 0
            rmse: 0
      
      # derivatives: 
      #   # a key contained in the data provided by the model
      #   $output_key$:
      #     # a key contained in the data provided by the dataloader
      #     $input_key_known$: 
      #       # partial derivative of output with index 0 w.r.t. input with index 0
      #       'out[0]/in[0]': 
      #         constraints: ['value >= 0', 'value <= 1'] # we want to enforce two constraints on the partial derivative
      #         mae: 0 # MAE loss component coefficient
      #         mse: 0 # MSE loss component coefficient
```

## Operation - Refine Model

This file initializes the database to be used during training and performs a single action located at `AI4SurrogateModelling.src.training.trainers.feed_forward.refine`. This action initializes a model (if it does not exist) and trains it for the specified number of epochs using the supplied scheduler, optimizer and loss function.

The training state and progress are stored inside the directory `results/random_example/training`. The standalone HTML report visualizing the training progress and best model properties is generated after the training finishes and is located in `results/random_example/reports/training.html`


```yaml
objects:
  database:
    constructor: $DatabaseTabular$
    parameters: 
      path_tgt: $DatabaseDirectory$

actions:
  action_0:
    # training function to be used
    fname: $project_path$.training.trainers.feed_forward.refine

    parameters:
      checkpoint_dir: $results_dir$/training
      number_of_epochs: 10
      batch_size: 1024
      dtype: $dtype$

      data_uid: database
      model_uid: final_model
      optimizer_uid: optimizer_adam
      scheduler_uid: scheduler_LAMBDA_0
      reset: True
      report_dir: $results_dir$/reports

      loss_uid: loss_0
```

## Operation - Model Utilization

Finally, we take the best model obtained via the refinement process with UID `loaded_model`, the underlying database with UID `database`, a gradient optimizer, scheduler and loss and perform a single action: gradient based parameter optimization located at `AI4SurrogateModelling.src.utilization.parameter_estimation.gradient_sampler.GradientParameterSampler.estimate_parameters_tabular`.

The optimization runs for the specified number of epochs and attempts to find the specified number of parameter configurations. The Parameters are kept inside the known value boundaries (inferred from the supplied database). The search space is restricted by a known set of input/output values. In this example, the inputs from the group `inputs_group_known` are to be found by the optimization, the inputs from group `inputs_group_unknown` and outputs `outputs_group` need to be specified by the user. 

The optimization attempts to find a `P` such that for all prescribed input values `X` and prescribed output values `Y`, the equality `model([P, X]) = Y` holds.

```yaml
objects:
  loaded_model:
    constructor: $project_path$.model.model_base.ModelBase.load_model
    parameters: 
      fn: '$results_dir$/training/model_best.bin'

  database:
    constructor: $DatabaseTabular$
    parameters: 
      path_tgt: $DatabaseDirectory$
  
  optimizer_adam_inverse:
    constructor: torch.optim.Adam
    parameters:
      lr: 1e-3
      betas: (0.8, 0.99)
      eps: 1e-12
      weight_decay: 0
      amsgrad: False

  lambda_scheduler_function_inverse:
    constructor: $project_path$.training.schedulers.lambdas.cyclical_lr.CyclicalLR
    parameters:
      log_factor_low: -1
      log_factor_high: 1
      periods: [500, 1000, 2000]

  scheduler_LAMBDA_inverse:
    constructor: torch.optim.lr_scheduler.LambdaLR
    parameters:
      lr_lambda: lambda_scheduler_function_inverse

  loss_inverse:
    constructor: $project_path$.training.loss.loss_base.LossBase
    parameters:
      outputs:
        $output_key$: 
          $output_key$:
            mae: 0
            mse: 1
            rmae: 0
            rmse: 0

actions:
  action_0:
    fname: $project_path$.utilization.parameter_estimation.gradient_sampler.GradientParameterSampler.estimate_parameters_tabular

    parameters:
        ncandidates: 50
        nepochs: 100
        dtype: $dtype$

        model_uid: loaded_model
        optimizer_uid: optimizer_adam_inverse
        scheduler_uid: scheduler_LAMBDA_inverse
        loss_uid: loss_inverse

        parameter_key: $input_key_unknown$ # assume the data is split so that one group contains the values to be optimized
        database_uid: database
        
        # some values may be known
        known_values:
            Column_000: [0.025, 0.025, 0.015]
            Column_001: [0.005, 0.015, 0.026]
            Column_004: [0.045, 0.039, 0.029]
            Column_006: [0.045, 0.039, 0.029]
            Column_008: [0.045, 0.039, 0.029]
            Column_010: [0.045, 0.039, 0.029]
        report_dir: '$results_dir$/reports'
```