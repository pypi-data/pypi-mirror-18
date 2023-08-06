import datetime
import os

import psutil


def get_progress_bar(percentage):
    dashes = '|' * int(percentage / 10 * 5)
    spaces = ' ' * (50 - len(dashes))
    return dashes, spaces


def show():
    for i, cpu_load in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
        dashes, spaces = get_progress_bar(cpu_load)
        print 'CPU{0} [{1}{2}] {3}%'.format(i, dashes, spaces, cpu_load)

    virtual_memory = psutil.virtual_memory()
    dashes, spaces = get_progress_bar(virtual_memory.percent)
    used = virtual_memory.used / 1048576  # make MB
    total = virtual_memory.total / 1048576  # make MB
    print 'Mem  [{0}{1}] {2}% {3}/{4}MB'.format(dashes, spaces, virtual_memory.percent, used, total)

    swap_memory = psutil.swap_memory()
    dashes, spaces = get_progress_bar(swap_memory.percent)
    used = swap_memory.used / 1048576  # make MB
    total = swap_memory.total / 1048576  # make MB
    print 'Swp  [{0}{1}] {2}% {3}/{4}MB'.format(dashes, spaces, swap_memory.percent, used, total)

    tasks = []
    tasks_status = {}
    for p in psutil.process_iter():
        p_key = p.status()
        try:
            tasks_status[p_key] += 1
        except KeyError:
            tasks_status[p_key] = 1
        tasks.append(p)

    st = []
    for x, y in tasks_status.items():
        if y:
            st.append("%s=%s" % (x, y))
    st.sort(key=lambda x: x[:3] in ('run', 'sle'), reverse=1)
    print 'Tasks: {0} ({1})'.format(len(tasks), ', '.join(st))

    av1, av2, av3 = os.getloadavg()
    print 'Load average: {0} {1} {2}'.format(av1, av2, av3)

    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    print 'Uptime: {0}'.format(str(uptime).split('.')[0])


if __name__ == '__main__':
    show()
