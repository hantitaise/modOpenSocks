# Planification des tâches récurrentes
scheduler = BackgroundScheduler()

def task_example():
    logger.info("Tâche récurrente exécutée.")

scheduler.add_job(task_example, "interval", seconds=10)
scheduler.start()
