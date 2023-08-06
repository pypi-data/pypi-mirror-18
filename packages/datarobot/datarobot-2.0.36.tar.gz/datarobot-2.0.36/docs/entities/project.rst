########
Projects
########

All of the modeling within DataRobot happens within a project. Each project
has one dataset that is used as the source from which to train models.

Create a Project
****************
You can use the following command to create a new project. You must specify a path to data file or ``pandas.DataFrame`` object when creating a new project.
Path to file can be either a path to a local file or a publicly accessible URL.

.. code-block:: python

    from datarobot import Project
    project = Project.create('/home/user/data/last_week_data.csv',
                             project_name='New Project')
                                                          

You can use the following commands to view the project ID and name:

.. code-block:: python

    project.id
    >>> u'5506fcd38bd88f5953219da0'
    project.project_name
    >>> u'New Project'

Select Modeling Parameters
**************************
The final information needed to begin modeling includes the target feature'rea, the queue mode, the metric for comparing models, and an optional weights parameter.

Target
======
The target must be the name of one of the columns of data uploaded to the
project.

Metric
======
The optimization metric used to compare models is an important factor in building accurate models. If a metric is not specified, the default metric recommended by DataRobot will be used. You can use the following code to view a list of valid metrics for a specified target:

.. code-block:: python

    target_name = 'ItemsPurchased'
    project.get_metrics(target_name)
    >>> {'available_metrics': [
             'Gini Norm',
             'Weighted Gini Norm',
             'Weighted R Squared',
             'Weighted RMSLE',
             'Weighted MAPE',
             'Weighted Gamma Deviance',
             'Gamma Deviance',
             'RMSE',
             'Weighted MAD',
             'Tweedie Deviance',
             'MAD',
             'RMSLE',
             'Weighted Tweedie Deviance',
             'Weighted RMSE',
             'MAPE',
             'Weighted Poisson Deviance',
             'R Squared',
             'Poisson Deviance'],
         'feature_name': 'SalePrice'}

Queue Mode
==========
You can use the API to set the DataRobot modeling process to run in either automatic or manual mode. 

**Autopilot** mode means that the modeling process will proceed completely
automatically, including running recommended models, running at
different sample sizes, and blending.

**Manual** mode means that DataRobot will populate a list of recommended models, but will not insert any of them into the queue. Manual mode lets you select which models to execute before starting the modeling process. 

Quick run
=========
Modelling process can be set to run in ``quick run`` mode. In it, smaller set of Blueprints is used, so autopilot finishes faster.

Weights
=======
DataRobot also supports using a weight parameter. A full discussion of the use of weights in data science is not within the scope of this document, but weights are often used to help compensate for rare events in data. You can specify a column name in the project dataset to be used as a weight column.

Start Modeling
**************

Once you have selected modeling parameters, you can use the following code structure to specify parameters and start the modeling process.

.. code-block:: python

    import datarobot as dr
    project.set_target(target='ItemsPurchased',
                       metric='Tweedie Deviance',
                       mode=dr.AUTOPILOT_MODE.FULL_AUTO)

You can also pass additional optional parameters to ``project.set_target`` to change parameters of modelling process. Currently supported parameters are:

* ``quickrun`` -- bool, if set to ``True`` starts project in ``quick run`` mode.
* ``worker_count`` -- int, sets number of workers used for modelling.
* ``recommender_settings`` -- ``RecommenderSettings`` object, columns specified in this object tell the system how to set up the recommender system
* ``partitioning_method`` -- ``PartitioningMethod`` object.
* ``positive_class`` -- str, float, or int; specifies a level of the target column that should be used for binary classification. Use it to specify any of the available levels as the binary target - all other levels will be treated as a single negative class.
* ``advanced_options`` -- :doc:`AdvancedOptions </api/advanced_options>` object, used to set advanced options of modelling process.


Quickly start Project
*********************

Project creation, file upload and target selection are all combined in ``Project.start`` method:

.. code-block:: python

    from datarobot import Project
    project = Project.start('/home/user/data/last_week_data.csv',
                            target='ItemsPurchased',
                            project_name='New Project')

You can also pass additional optional parameters to ``Project.start``:

* ``worker_count`` -- int, sets number of workers used for modelling.
* ``metric`` - str, name of metric to use.
* ``autopilot_on`` - boolean, defaults to ``True``; set whether or not to begin modeling automatically.
* ``recommender_settings`` -- ``RecommenderSettings`` object, columns specified in this object tell the system how to set up the recommender system
* ``recommendation_settings`` -- **Deprecated**, please use ``recommender_settings``
  instead. If both ``recommendation_settings`` and ``recommender_settings``
  parameters are provided the latter would be used
* ``blueprint_threshold`` -- int, number of hours the model is permitted to run. Minimum 1.
* ``response_cap`` -- float, Quantile of the response distribution to use for response capping. Must be in range 0.5..1.0
* ``partitioning_method`` -- ``PartitioningMethod`` object.
* ``positive_class`` -- str, float, or int; specifies a level of the target column that should be used for binary classification. Use it to specify any of the available levels as the binary target - all other levels will be treated as a single negative class.


Interact with a Project
***********************

The following commands can be used to manage DataRobot projects. 

List Projects
=============
Returns a list of projects associated with current API user.

.. code-block:: python

    from datarobot import Project
    Project.list()
    >>> [Project(Project One), Project(Two)]

    Project.list(search_params={'project_name': 'One'})
    >>> [Project(One)]

    Project.list(order_by='-projectName')
    >>> [Project(Two), Project(Project One)]

You can pass following parameters to change result:

* ``search_params`` -- dict, used to filter returned projects. Currently you can query projects only by ``project_name``
* ``order_by`` -- str or list, if passed returned projects are ordered by this attribute or attributes.

Get an existing project
=======================
Rather than querying the full list of projects every time you need
to interact with a project, you can retrieve its ``id`` value and use that to reference the project.

.. code-block:: python

    from datarobot import Project
    project = Project.get(project_id='5506fcd38bd88f5953219da0')
    project.id
    >>> '5506fcd38bd88f5953219da0'
    project.project_name
    >>> 'Churn Projection'

Update a project
================
You can use the following command format to update project information:

.. code-block:: python

    project.update(**params)

Currently you can update your project by passing following parameters:

* ``project_name`` -- string, new project name.
* ``holdout_unlocked`` -- can only have value of ``True``. If passed, unlocks holdout.
* ``worker_count`` -- int, sets number of workers used for modelling.

**Project Update Example:**

.. code-block:: python

    project.update(
        project_name='October Outcomes',
        holdout_unlocked=True,
        worker_count=20,
    )

Delete a project
================

Use the following command to delete a project: 

.. code-block:: python

    project.delete()

Play/Pause the autopilot
========================
If your project is running in autopilot mode, it will continually use
available workers, subject to the number of workers allocated to the project
and the total number of simultaneous workers allowed according to the user
permissions.

To pause a project running in autopilot mode: 

.. code-block:: python

    project.pause_autopilot()

To resume running a paused project: 

.. code-block:: python

    project.unpause_autopilot()

.. note::

    If you attempt to pause the autopilot when it is already paused, or unpause
    it while it is already running, it will return an error telling you that
    it can't carry out your request (because it's already happening)

Further reading
***************
The Blueprints and Models sections of this document will describe how to create
new models based on the Blueprints recommended by DataRobot.
