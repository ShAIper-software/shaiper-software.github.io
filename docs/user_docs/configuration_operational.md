# Operational Configuration

The [main](configuration_main.md) configuration file describes the top-level configuration, which contains operations linking to the operational configuration files.

Each operational configuration file contains two basic sections: `objects` and `actions`.

### `objects`
The object section contains the specification of objects used during the program for objects/actions specified in this operational file and all successive operational files.

```
objects:
    object_UID_0:
        constructor: path.to.class.definition_0
        parameters: 
            parameter_name_0: parameter_value_0
            parameter_name_1: parameter_value_1
                        ...

    object_UID_1:
        constructor: path.to.class.definition_1
        parameters: 
            parameter_name_0: parameter_value_0
            parameter_name_1: parameter_value_1
                        ...
```

This allows the user to specify any objects contained in the software. In the snippet above, the user specified two objects, each with a unique ID (the configuration parser checks the uniqueness requirement). Each objects needs to point to a method or a class in the code-base which returns the instance of the object initialized with the supplied parameters.

So, the user can use any objects, but needs to know how to construct them. The objects can be referenced by their unique IDs in the configuration files. For example, an action can be done using an object, or an object can use another object in its constructor, etc.

Object UIDs, paths to constructors, parameter names and values can use [aliases](configuration_main.md#aliases) specified in the main configuration file.

### `actions`

Constructing objects and not using them is not very productive. Thus, the final building block of our configuration system is the system of `actions`. An action can reference an instance of an object, a static function or a global function. 

In the snippet below, you can see `action_0` referencing an instance of the object specified above with UID `object_UID_0` and calling its member function `class_function_name` with the supplied parameters (if any).

The action `action_42` references either a static function or a global function with the supplied parameters.

The system performs the actions in order with respect the the integer suffix. A check is performed whether the referenced functions are available in the code-base and whether the objects have been specified in the configuration files (i.e. the program knows how to construct them).

```
actions:
  action_0:
    object_uid: object_UID_0
    fname: class_function_name
    parameters: 
        parameter_name_0: parameter_value_0
        parameter_name_1: parameter_value_1
                    ...

  action_42:
    fname: path.to.function.call
    parameters: 
        parameter_name_0: parameter_value_0
        parameter_name_1: parameter_value_1
                    ...

```