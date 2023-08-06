Introduction
============

SciExp² (aka *SciExp square* or simply *SciExp2*) stands for *Scientific Experiment Exploration*, which provides a framework for easing the workflow of creating, executing and evaluating experiments.

The driving idea of SciExp² is that of quick and effortless *design-space exploration*. It is divided into the following main pieces:

* **Launchgen**: Aids in defining experiments as a permutation of different parameters in the design space. It creates the necessary files to run these experiments (configuration files, scripts, etc.), which you define as templates that get substituted with the specific parameter values of each experiment.

* **Launcher**: Takes the files of `~sciexp2.launchgen` and runs these experiments on different execution platforms like regular local scripts or cluster jobs. It takes care of tracking their correct execution, and allows selecting which experiments to run (e.g., those with specific parameter values, or those that were not successfully run yet).

* **Data**: Aids in the process of collecting and analyzing the results of the experiments. Results are automatically collected into a data structure that maintains the relationship between each result and the parameters of the experiment that produced it. With this you can effortlessly perform complex tasks such as inspecting the results or calculating statistics of experiments sub-sets, based on their parameter values.

The framework is available in the form of Python modules which can be easily integrated into your own applications or used as a scripting environment.


Quick example
-------------

As a quick example, we'll see how to generate scripts to run an application, run these scripts, and evaluate their results. First, we'll start by generating the per-experiment scripts in the ``experiments`` directory, which will basically execute ``my-program`` with different values of the ``--size`` argument, generating a CSV file with results for each experiment::


  #!/usr/bin/env python
  # -*- python -*-

  from sciexp2.launchgen.env import *

  l = Launchgen(out="experiments")
  l.pack("/path/to/my-program", "bin/my-program")
  l.params(size=[1, 2, 4, 8])
  l.launchgen("shell", "scripts/@size@.sh",
              CMD="bin/my-program --size=@size@ --out=results/@size@.csv")


The ``experiments`` directory now contains all the files we need. Then, we'll execute all the experiments with::

  ./experiments/jobs.jd submit

The relevant contents of the ``experiments`` directory after executing the experiments are thus::

  experiments
  |- bin
  |  `- my-program
  |- scripts
  |  |- 1.sh
  |  |- 2.sh
  |  |- 4.sh
  |  `- 8.sh
  `- results
     |- 1.csv
     |- 2.csv
     |- 4.csv
     `- 8.csv

Let's assume that ``my-program`` runs the same operation multiple times, and the output CSV files contain a line with the execution time for each of these runs, like::

  run,time(sec)
  0,3.2
  1,2.9
  ...

Finally, we'll gather the results of all experiments and print the average execution time across runs for each value of the ``size`` parameter::

  #!/usr/bin/env python
  # -*- python -*-

  from sciexp2.data.env import *

  # auto-extract all results
  d = extract_txt('experiments/results/@size@.csv',
                  fields_to_vars=["run"])
  # experiment size as first dimension, run number as second
  d = d.reshape(["size"], ["run"])
  # get mean of all runs (one mean per size)
  d = d.mean(axis="run")
  # print CSV-like mean of each size
  print("size, time")
  for foo in d.dims["size"]:
      print("%4d," % size, d[size])

The result could be something like::

  size, time
     1, 3.05
     2, 3.39
     4, 4.61
     8, 6.37
