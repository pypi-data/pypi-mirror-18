#! /usr/bin/env python
import sys


def human_time(seconds):
    if not seconds:
        seconds = 0
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d" % (m, s) if h == 0 else "%d:%02d:%02d" % (h, m, s)


def push_in_range(val, minimum, maximum):
    if val < minimum:
        return minimum
    elif val > maximum:
        return maximum
    else:
        return val


def print_progress(iteration, total, time=0, mdet=None, prefix='', suffix='', decimals=1, bar_length=100):
    format_str = "{0:." + str(decimals) + "f}"
    percents = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '=' * filled_length + ' ' * (bar_length - filled_length)
    if mdet is None:
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))
    else:
        sys.stdout.write('\r%s |%s| %s%s %s %s=%s-%s [%shz][%sch][%sbytes/sample]' %
                         (prefix, bar, percents, '%', suffix,
                          human_time(time), human_time(mdet.duration_seconds), human_time(mdet.duration_seconds - time),
                          mdet.frame_rate, mdet.no_channels, mdet.frame_width))
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

