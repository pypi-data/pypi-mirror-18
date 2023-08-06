"""Main python-htop module."""
import psutil


class HTop(object):
    """Class structure for python htop-like program."""
    @staticmethod
    def _sizeof_fmt(num, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    @classmethod
    def get_ram_stat(cls):
        """Return total and used RAM of the system."""
        mem_stat = psutil.virtual_memory()
        return {'info': 'Memory statistic',
                'total': '{0}'.format(cls._sizeof_fmt(mem_stat.total)),
                'info': 'Memory statistic',
                'used': '{0}'.format(cls._sizeof_fmt(mem_stat.used)),
                }

    @classmethod
    def get_cpu_stat(cls):
        """Return percentage usage pre cpu."""
        cpu_dict = {'info': 'CPU'}
        psutil.cpu_percent(interval=1)
        for index, x in enumerate(psutil.cpu_percent(percpu=True)):
            cpu = 'cpu #{0}'.format(index)
            used = 'used {0}%'.format(x)
            cpu_dict.update({cpu:used})
        return cpu_dict

    @classmethod
    def get_hdd_stat(cls):
        """Return mount point occupation."""
        hdd_dict = {'info': 'HDD'}
        for partition in psutil.disk_partitions():
            mount_point = partition.mountpoint
            dsk_usg = psutil.disk_usage(mount_point)
            hdd_dict.update({mount_point: {'total': cls._sizeof_fmt(dsk_usg.total),
                                          'used':cls._sizeof_fmt(dsk_usg.used)}})
        return hdd_dict

    @classmethod
    def print_all_statistic(cls):
        """General output of the information."""
        methods = [method for method in dir(cls) if method.endswith('stat')]
        for method in methods:
            print '\n'
            stat_item = getattr(cls, method)()
            for key, value in stat_item.iteritems():
                print key, value


if __name__ == '__main__':
        HTop.print_all_statistic()
