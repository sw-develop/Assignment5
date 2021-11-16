import logging
import sys

from linetimer       import CodeTimer

from research.batch import batch_task
from utils           import retry


logger = logging.getLogger('batch')


@retry(total_try_cnt=5, sleep_in_sec=5, retryable_exceptions=(OSError, ValueError), log=logger)
def start_batch():
    func_name = sys._getframe().f_code.co_name

    ct = CodeTimer(unit='s')

    with ct:
        batch_task()

    logger.info(f"[{func_name}] Success batch job [took:{ct.took:.2f}{ct.unit}]")
    return True
