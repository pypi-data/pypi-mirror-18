##########
PredictJob
##########

Predictions generation is an asynchronous process. This means than when starting
predictions generation with ``PredictJob.create`` you will receive back the id of
the process responsible for fulfilling your request.

With this id you can get info about the predictions generation process before it
has finished and be rerouted to the predictions themselves when the
process is finished. For this you should use the **PredictJob**
(:doc:`API reference </api/predict_job>`) class.

Starting predictions generation
*******************************
To start predicting on new data using a finished model use ``PredictJob.create``.
It will create a new predictions generation process and return
this process' identifier, which the PredictJob class can use to reference it. With the id, you
can look up an existing PredictJob and retrieve generated predictions when the corresponding
PredictJob is finished.

You need to specify the model that should be used for predictions generation.
You also must provide data to be predicted. For this you can pass the path to a local
file, a file object, raw file content or a ``pandas.DataFrame`` object

.. code-block:: python

    from datarobot import Model, PredictJob

    project_id = '5506fcd38bd88f5953219da0'
    model_id = '5506fcd98bd88f1641a720a3'
    model = Model.get(project=project_id,
                      model_id=model_id)
    # Using path to local file to generate predictions
    predict_job_id = PredictJob.create(model, './data_to_predict.csv')

    # Using file object to generate predictions
    with open('./data_to_predict.csv') as data_to_predict:
        predict_job_id = PredictJob.create(model, data_to_predict)


Get an existing PredictJob
**************************

To retrieve an existing PredictJob use the ``PredictJob.get`` method. This will give you
a PredictJob matching the latest status of the job if it has not completed.

If predictions have finished building, ``PredictJob.get`` will raise a ``PendingJobFinished``
exception.


.. code-block:: python

    import time

    from datarobot import PredictJob

    predict_job = PredictJob.get(project_id=project_id,
                                 predict_job_id=predict_job_id)
    predict_job.status
    >>> 'queue'

    # wait for generation of predictions (in a very inefficient way)
    time.sleep(10 * 60)
    predict_job = PredictJob.get(project_id=project_id,
                                 predict_job_id=predict_job_id)
    >>> datarobot.errors.PendingJobFinished

    # now the predictions are finished
    predictions = PredictJob.get_predictions(project_id=project.id,
                                             predict_job_id=predict_job_id)

Get generated predictions
*************************

After predictions are generated, you can use ``PredictJob.get_predictions``
to get newly generated predictions.

If predictions have not yet been finished, it will raise a ``JobNotFinished`` exception.

.. code-block:: python

    from datarobot import PredictJob

    predictions = PredictJob.get_predictions(project_id=project.id,
                                             predict_job_id=predict_job_id)

wait_for_async_predictions function
***********************************
If you just want to get generated predictions after getting PredictJob id, you
can use :ref:`wait_for_async_predictions<wait_for_async_predictions-api-label>` function.
It will poll the status of predictions generation process until it has finished, and
then will return predictions.

.. code-block:: python

    from datarobot.models.predict_job import wait_for_async_predictions

    predict_job_id = PredictJob.create(model, data_to_predict)
    predictions = wait_for_async_predictions(
        project_id=project.id,
        predict_job_id=predict_job_id,
    )
