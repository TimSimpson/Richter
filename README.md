# RICHTER CONAN X

Contains Conan Recipes.

## Instructions

Conan needs to be set up using Python 3.

`cd` into `recipes/<project>` and run `conan create .`


## Richter's Tips

```
     _  E_E                             Richter is Conan's sidekick,
     -=-'_'                 \ | /       who vanquished Dracula in
      "''''--o::::::::::::::-(*)-       the year 1792.
      ''||                  / | \
       )) \                             He contributed these tips.
      /   |
```

* Remember to re-read the Conan [documentation on packaging workflow](https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html) for time to time.

* This project uses [.ok bash](https://github.com/secretGeek/ok-bash) to walk through the Conan package workflow.

* The `cmake_paths` generator is cooler than the `cmake` generator. Ideally a project should be able to work with CMake, export CMake package stuff so it works with tools like [cget](https://github.com/pfultz2/cget) and standard CMake as well as with Conan.
