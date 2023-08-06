import asyncio
import logging
import struct

import serial_asyncio

from . import exceptions

try:
    from asyncio import ensure_future
except ImportError:
    # Python 3.4.3 and earlier has this as async
    # pylint: disable=unused-import
    from asyncio import async
    ensure_future = async

# Exports.
__all__ = [
    'EmonPiSensors'
]

logger = logging.getLogger(__name__)


class EmonPiSensors(object):
    """
    EmonPi sensors.
    """

    # Message field decoders.
    message_field_decoders = [
        {'name': 'power_ct1', 'format': 'h', 'scale': 1.0},
        {'name': 'power_ct2', 'format': 'h', 'scale': 1.0},
        {'format': 'h'},  # Ignored (power_ct1 + power_ct2).
        {'name': 'v_rms', 'format': 'h', 'scale': 0.01},
        {'name': 'temperature_1', 'format': 'h', 'scale': 0.1},
        {'name': 'temperature_2', 'format': 'h', 'scale': 0.1},
        {'name': 'temperature_3', 'format': 'h', 'scale': 0.1},
        {'name': 'temperature_4', 'format': 'h', 'scale': 0.1},
        {'name': 'temperature_5', 'format': 'h', 'scale': 0.1},
        {'name': 'temperature_6', 'format': 'h', 'scale': 0.1},
        {'name': 'pulse_count', 'format': 'L', 'scale': 1.0},
    ]

    def __init__(self, serial_port, loop=None):
        """
        Constructs the sensors object.

        :param serial_port: Serial port where the emonPi is connected to
        :param loop: Optional event loop to use
        """

        if loop is None:
            loop = asyncio.get_event_loop()

        self._loop = loop
        self._port = serial_port
        self._reader = None
        self._writer = None

        # Handlers.
        self._handler_sensors_update = None

    @property
    def handler_sensors_update(self):
        return self._handler_sensors_update

    @handler_sensors_update.setter
    def handler_sensors_update(self, value):
        self._handler_sensors_update = value

    def connect(self):
        """
        Establishes a connection with the emonPi module.
        """

        if self._reader or self._writer:
            raise exceptions.SensorsError('Already connected')

        ensure_future(self._connect(), loop=self._loop)

    @asyncio.coroutine
    def _connect(self):
        self._reader, self._writer = yield from serial_asyncio.open_serial_connection(
            loop=self._loop, url=self._port, baudrate=38400)

        # Spawn coroutine for handling protocol messages.
        ensure_future(self._handle_messages(), loop=self._loop)

    @asyncio.coroutine
    def _handle_messages(self):
        """
        Incoming message handler.
        """

        while not self._reader.at_eof():
            line = yield from self._reader.readline()
            line = line.strip().decode().split()
            if not line or line[0] != 'OK':
                continue
            line = line[2:]

            if self._handler_sensors_update is None:
                continue

            index = 0
            message = {}
            try:
                for decoder in self.message_field_decoders:
                    size = struct.calcsize(decoder['format'])
                    data = bytes([int(x) for x in line[index:index + size]])
                    value = struct.unpack(decoder['format'], data)[0] * decoder.get('scale', 1.0)
                    index += size

                    if 'name' not in decoder:
                        continue

                    message[decoder['name']] = value
            except ValueError:
                logger.error("Malformed message from emonPi.")
                continue

            self._handler_sensors_update(message)

    def close(self):
        """
        Closes the connection with the emonPi module.
        """

        if not self._writer:
            raise exceptions.SensorsError('Not connected')

        self._writer.transport.close()
