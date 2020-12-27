import astropy as apy
import datetime


def f_time(scope: apy.Scope):
    time_str = datetime.datetime.now().strftime('%H:%M:%S')
    astro_string = apy.models.String.new('current_time', time_str)
    scope.set('current_time', astro_string)
    
    return scope.format()


def __build__():
    return [
        apy.render(f_time, lib='Time', name='time')
    ]
