from .celery_app import celery_app

from ..manager.tasks import execute_pipeline


@celery_app.task
def execute_pipeline_task(pipeline_id, pipeline_steps, pipeline_cwd, trigger):
    execute_pipeline(pipeline_id,
                     pipeline_steps,
                     pipeline_cwd,
                     trigger,
                     False)
