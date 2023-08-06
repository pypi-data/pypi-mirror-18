import time
import sys

number_of_runs = 5
retry_break = 2


def run():  # pragma: no cover
    """
    run the daemon indefinitely
    """
    print('daemon started')
    for n in range(1, number_of_runs + 1, 1):
        try:
            while True:
                run_daemon()
        except (KeyboardInterrupt, SystemExit):
            print('daemon stopped')
            break
        except (ValueError, AttributeError) as e:
            if n == number_of_runs:
                print('daemon stopped')
                raise e
            time.sleep(retry_break)


def run_daemon():
    print 'test'
    raise ValueError('Er ging iets mis')


def run_daemon2():
    print 'test'
    raise sys.exit()


run()