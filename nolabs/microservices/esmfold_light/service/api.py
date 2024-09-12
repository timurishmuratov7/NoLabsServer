from log import logger
from settings import settings
from dotenv import load_dotenv

mode = settings.mode

load_dotenv('.env')

if mode == 'celery':
    from worker import app
    logger.info('Starting celery')
    app.worker_main([
        'worker',
        f'--concurrency={settings.celery_worker_concurrency}'
    ])

if mode == 'fastapi':
    import uvicorn

    from fastapi_api import app

    logger.info('Starting fastapi')
    uvicorn.run(app, host=settings.fastapi_host, port=settings.fastapi_port)
