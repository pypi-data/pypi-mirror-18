# Knock Business Probes

![CI status](https://codeship.com/projects/73e7a970-966e-0134-0b1c-664c28e74ab1/status?branch=master) 

Welcome to Knock Business SDK source code repository

https://knock.center

Copyright (C) 2013/2014/2015/2016 Laurent Champagnac / Laurent Labatut

# Source code 


* We are pep8 compliant (as far as we can, with some exemptions)
* We use a right margin of 360 characters (please don't talk me about 80 chars)
* SDK code is located inside "./knock"
* Unittests are located inside "./knock_test"
* All test files must begin with `test_`, should implement setUp & tearDown methods
* All tests must adapt to any running directory
* The whole sdk is backed by  [pythonsol lib](https://bitbucket.org/LoloCH/pythonsol)
* The daemon is not using threads but relies on coroutines (gevent greenlets) is use if already loaded before
* We are still bound to python 2.7 (we will move to python 3 later on)
* We are using docstring (:return, :rtype, :param, :type etc..), PyCharm "noinspection", feel free to use them

# Requirements


- Knockdaemon
- An account on [Knock](https://knock.center)

# Install
Knock Probe is available on pypi
```bash
pip install knockprobe
```
# Type of probe
## Gauge
A simple counter, storing a current instant value. Last value provided wins.
Gauges are used in quantity cases. For example, a gauge could be defined by the amount of basket being processed.

## Increment
A simple counter, storing cumulative values and graphing them as delta per second.
Increment is typicaly an recurrent event. For example, an increment could be defined by the number of basket validated.

## Delay
A simple counter, storing execution time and graphing them by execution time interval.
For example, a delay could be defined by the time of execution of external request.

# Samples

## Push a Gauge Probe
You can push a gauge probe one by one without declare first.
```
from knockprobe import Knock

Knock.gauge('gauge_total_amount', 1257,42)
Knock.commit()

```
Or in bulk mode
```
from knockprobe import Knock

Knock.gauge('gauge_total_amount', 1257,42)
Knock.gauge('gauge_shoes_amount', 854,65)
Knock.commit()

```
## Push a Counter Probe
You can push a curent instant value probe one by one without declare first.

```
from knockprobe import Knock

if do_something():
    Knock.increment('counter_do_something', 1)
Knock.commit()
```
Or in bulk mode
```
from knockprobe import Knock

if do_something('step1'):
    Knock.increment('counter_do_something', 1)
if do_something('step2'):
    Knock.increment('counter_do_something', 1)
Knock.commit()
```

## Delay to Count

Delay to count is a special probe. This probe agregate all execution time in a dict of range of time.

```
from knockprobe import Knock

t1 = Knock.start_delay('time_manager_init')
m = my_manager()
Knock.stop_delay(t1)

t2 = Knock.start_delay('time_manager_exec')
m.exec()
Knock.stop_delay(t1)

Knock.commit()
```

# Important information

Knock lib is an singleton. So for performance improvement you can commit through multiple objects.
For non persistent script, a commit is launch at exit.
So it's not possible to un-commit a probe.

--------

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA


