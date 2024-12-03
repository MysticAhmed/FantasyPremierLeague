import azure.functions as func
import logging
import main  # Make sure this is correctly set up with the main function you want to call

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="update_predictions_timer")
@app.schedule(schedule="0 0 0 * * 1", arg_name="myTimer", run_on_startup=False, use_monitor=True)
def update_predictions_timer(myTimer: func.TimerRequest) -> None:
    logging.info("Timer trigger fired for weekly prediction update.")

    try:
        main.main(myTimer)
        logging.info("Prediction update completed successfully.")
    except Exception as e:
        logging.error(f"Error during prediction update: {str(e)}")
        raise
