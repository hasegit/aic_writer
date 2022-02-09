import aic_writer


def lambda_handler(event, _):

    aic_writer.update_db()
