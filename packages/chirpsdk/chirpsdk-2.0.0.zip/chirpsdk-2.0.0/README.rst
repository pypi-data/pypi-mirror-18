Chirp Python SDK
================

The Chirp Python SDK enables the user to create, send and query chirps,
using the Chirp audio protocols.

Requirements
------------

The Chirp SDK supports Python 2 and Python 3.

- `Python 2.6+`_, or `Python 3.5`_.

.. _Python 2.6+: https://docs.python.org/2/
.. _Python 3.5: https://docs.python.org/3/

Usage
-----

For audio playback, the Chirp Python SDK requires PortAudio. To install on Linux:

::

   sudo apt-get install portaudio19-dev

or for MacOS:

::

   brew install portaudio

To install the SDK and its dependencies:

::

   python setup.py install

To create a chirp identifier encapsulating an arbitrary dictionary:

.. code:: python

   import chirpsdk
   
   sdk = chirpsdk.ChirpSDK(YOUR_APP_KEY, YOUR_APP_SECRET)
   chirp = sdk.create_chirp({'key': 'value'})
   print chirp.shortcode

To play this chirp via the inbuilt speaker:

.. code:: python

   chirp.chirp()

To chirp a specific 10-character identifier:

.. code:: python

   chirp = sdk.create_chirp('parrotbill')
   chirp.chirp()
   chirp.save_wav()

To query an existing chirp by its identifier:

.. code:: python

   chirp = sdk.get_chirp('parrotbill')
   print chirp.longcode
   print chirp.data

To retrieve a chirp's numeric and hex representations:

.. code:: python

   chirp = sdk.create_chirp('parrotbill')
   print chirp.encoded
   print chirp.hex

To directly create a chirp from a numeric sequence:

.. code:: python

   chirp = sdk.create_chirp((25, 10, 27, 27, 24, 29, 11, 18, 21, 21))
   print chirp.shortcode
   print chirp.longcode
   print chirp.hex

By default, the SDK will use the Standard Chirp protocol. That is a 10-character identifier from a 5-bit alphabet for a total of 50 bits of data.
You can switch to a different protocol using the `set_protocol()` method:

.. code:: python

   chirpsdk.set_protocol('ultrasonic')

This will set the protocol used by the Chirp SDK to "ultrasonic" which is our standard inaudible protocol. This is formed of 8-character from a 4-bit alphabet and can hold 32 bits of data.
You can learn more about protocols here: http://developers.chirp.io/docs/chirp-protocols

You can also play a Chirp repeatedly in "streaming mode", this is useful for beacons and the Ultrasonic protocol that works better when repeated several times.

.. code:: python

  chirpsdk.start_streaming('parrotbill')

This will play the Chirp "parrotbill" in the background with a 1 second pause between each iteration.
You can set a custom interval with:

.. code:: python

  chirpsdk.streaming_interval = 500

Where the interval is specified in milliseconds. In order to terminate the thread and stop the streaming mode, you can call:

.. code:: python

  chirpsdk.stop_streaming()

Note that if you're using a protocol other than 'standard', the API calls (outside of `encode_message` and `decode_message`) will not work due to incompatibility of the API to the new numeric/hex formats.

Further Information
-------------------

For help, see:

::

   pydoc chirpsdk

----

This file is part of the Chirp Python SDK.
For full information on usage and licensing, see http://chirp.io/

Copyright (c) 2011-2016, Asio Ltd.
All rights reserved.

For commercial usage, commercial licences apply. Please `contact us`_.

For non-commercial projects these files are licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _contact us: contact@chirp.io
