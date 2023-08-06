======
Models
======

When a blueprint has been trained on a specific dataset at a specified sample
size, the result is a model. Models can be inspected to analyze their accuracy.

Quick Reference
***************

.. code-block:: python

    # Get all models of an existing project

    from datarobot import Project
    my_projects = Project.list()
    project = my_projects[0]
    models = project.get_models()

List Finished Models
********************
You can use the ``get_models`` method to return a list of the project models
that have finished training:

.. code-block:: python

    import datarobot as dr
    project = dr.Project.get('5506fcd38bd88f5953219da0')
    models = project.get_models()
    print(models[:5])
    >>> [Model(Decision Tree Classifier (Gini)),
         Model(Auto-tuned K-Nearest Neighbors Classifier (Minkowski Distance)),
         Model(Gradient Boosted Trees Classifier (R)),
         Model(Gradient Boosted Trees Classifier),
         Model(Logistic Regression)]
    model = models[0]

    project.id
    >>> u'5506fcd38bd88f5953219da0'
    model.id
    >>> u'5506fcd98bd88f1641a720a3'

You can pass following parameters to change result:

* ``search_params`` -- dict, used to filter returned projects. Currently you can query models by

    * ``name``
    * ``sample_pct``
    * ``start_time``
    * ``finish_time``

* ``order_by`` -- str or list, if passed returned models are ordered by this attribute or attributes.
* ``with_metric`` -- str, If not `None`, the returned models will only have scores for this metric. Otherwise all the metrics are returned.

**List Models Example:**

.. code-block:: python

    Project('pid').get_models(order_by=['-created_time', 'sample_pct', 'metric'])

    # Getting models that contain "Ridge" in name
    # created within the last day and with sample_pct more than 64
    import datetime
    day_before = datetime.datetime.now() - datetime.timedelta(days=1)
    Project('pid').get_models(
        search_params={
            'sample_pct__gt': 64,
            'start_time__gte': day_before,
            'name': "Ridge"
        })


Retrieve a Known Model
**********************
If you know the ``model_id`` and ``project_id`` values of a model, you can
retrieve it directly:

.. code-block:: python

    import datarobot as dr
    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = dr.Model.get(project=project_id,
                         model_id=model_id)

You can also use an instance of ``Project`` as the parameter for ``get``

.. code-block:: python

    model = dr.Model.get(project=project,
                         model_id=model_id)


Train a Model on a Different Sample Size
****************************************
One of the key insights into a model and the data behind it is how its
performance varies with more training data. In Autopilot mode, DataRobot will run at several sample sizes by default, but you can also create a job that will run at a specific sample size.
``train`` method of ``Model`` instance will put a new modeling job into the queue and return id of created
:doc:`ModelJob </entities/model_job>`.
You can pass ModelJob id to :ref:`wait_for_async_model_creation<wait_for_async_model_creation-label>` function,
that polls async model creation status and returns newly created model when it's finished.


.. code-block:: python

    model_job_id = model.train(sample_pct=33)

Find the Features Used
**********************
Because each project can have many associated feature lists, it is
important to know which features a model requires in order to run. This helps ensure that the the necessary features are provided when generating predictions.

.. code-block:: python

    feature_names = model.get_features_used()
    print(feature_names)
    >>> ['MonthlyIncome',
         'VisitsLast8Weeks',
         'Age']

Predict new data
****************
After creating models you can use them to generate predictions on new data.
Use :doc:`PredictJob </entities/predict_job>` class for this.

Model IDs Vs. Blueprint IDs
***************************
Each model has both an ``model_id`` and a ``blueprint_id``. What is the difference between these two IDs?

A model is the result of training a blueprint on a dataset at a specified
sample percentage. The ``blueprint_id`` is used to keep track of which
blueprint was used to train the model, while the ``model_id`` is used to
locate the trained model in the system.
