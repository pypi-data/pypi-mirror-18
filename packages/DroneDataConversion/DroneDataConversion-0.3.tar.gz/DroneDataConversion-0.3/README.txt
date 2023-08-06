Description and Purpose:
When flying the Parrot Bebop Quadcopter (and the Bebop 2 Quadcaopter) stores all flight information in a log file. This is a so called pud file and has a json structure.

This pud file includes detailed flight information which is also used by Parrot to store the flights in their cloud (formerly known as ARDrone Academy, Drone Academy) and to perform the flight analysis, such as generating battery plot, speed plot and altitude plot.

This library allows to extract important flight information from the pud file. The data in the pud file (flight log) is processed and can then be used for further flight analysis.

Supported Operating Systems:
The library was written and tested under OS X and Unix. No special libraries or expressions were used which prevent running the library under Windows. But note, it is untested.

Python Interpreter:
This library was written using legacy Python 2.7.10. At the current state it is untested under Python 3 and will most likely run under Python 2.7. only

License:
Copyright 2016, Johannes Kinzig

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.