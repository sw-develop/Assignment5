import logging
import time
import functools


def retry(total_try_cnt=5, sleep_in_sec=5, retryable_exceptions=(), log=logging.getLogger()):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            for cnt in range(total_try_cnt):
                log.info(f"[{func.__name__}] trying [{cnt+1}/{total_try_cnt}]")

                try:
                    result = func(*args, **kwargs)
                    if result:
                        return result

                except retryable_exceptions as e:
                    log.warning(f'[{func.__name__}] {e} {type(e)}')
                
                except Exception as e:
                    log.warning(f'[{func.__name__}] {e} {type(e)}')

                time.sleep(sleep_in_sec)

            log.error(f"[{func.__name__}] finally has been failed")
        return wrapper
    return decorator