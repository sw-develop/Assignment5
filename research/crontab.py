import logging
import sys

from linetimer       import CodeTimer

from research.models import ResearchInformation 
from utils           import retry


logger = logging.getLogger('batch')

def test_func():
    for i in range(10000000):
        pass

@retry(total_try_cnt=5, sleep_in_sec=5, retryable_exceptions=(OSError, ValueError), log=logger)
def start_batch():
    func_name = sys._getframe().f_code.co_name

    ct = CodeTimer(unit='s')

    with ct:
        test_func()

    logger.info(f"[{func_name}] Success batch job [took:{ct.took:.2f}{ct.unit}]")
    return True
