import time
from datetime import datetime
from Queue import Queue
from threading import Thread

import pandas as pd
import numpy as np
from nadamq.NadaMq import cPacketParser, PACKET_TYPES


class PacketQueueManager(object):
    '''
    Parse data from an input stream and push each complete packet on a
    :class:`Queue.Queue` according to the type of packet: ``data``, ``ack``, or
    ``stream``.

    Using queues

    Parameters
    ----------
    high_water_mark : int, optional
        Maximum number of packets to store in each packet queue.

        By default, **all packets are kept** (i.e., high-water mark is
        disabled).

        .. note::
            Packets received while a queue is at the :attr:`high_water_mark`
            are discarded.

            **TODO** Add configurable policy to keep either newest or oldest
            packets after :attr:`high_water_mark` is reached.
    '''
    def __init__(self, high_water_mark=None):
        self._packet_parser = cPacketParser()
        packet_types = ['data', 'ack', 'stream']
        self.packet_queues = pd.Series([Queue() for t in packet_types],
                                       index=packet_types)
        self.high_water_mark = high_water_mark

    def parse_available(self, stream):
        '''
        Read and parse available data from :data:`stream`.

        For each complete packet contained in the parsed data (or a packet
        started on previous that is completed), push the packet on a queue
        according to the type of packet: ``data``, ``ack``, or ``stream``.

        Parameters
        ----------
        stream
            Object that **MUST** have a ``read`` method that returns a
            ``str-like`` value.
        '''
        data = stream.read()

        packets = []

        for c in data:
            result = self._packet_parser.parse(np.fromstring(c, dtype='uint8'))
            if result != False:
                packet_str = np.fromstring(result.tostring(), dtype='uint8')
                packets.append((datetime.now(), cPacketParser().parse(packet_str)))
                self._packet_parser.reset()
            elif self._packet_parser.error:
                self._packet_parser.reset()

        for t, p in packets:
            if p.type_ == PACKET_TYPES.DATA and not self.queue_full('data'):
                self.packet_queues['data'].put((t, p))
            elif p.type_ == PACKET_TYPES.ACK and not self.queue_full('ack'):
                self.packet_queues.ack.put((t, p))
            elif ((p.type_ == PACKET_TYPES.STREAM) and
                  (not self.queue_full('stream'))):
                self.packet_queues.stream.put((t, p))

    def queue_full(self, name):
        '''
        Parameters
        ----------
        name : str
            Name of queue.

        Returns
        -------
        bool
            ``True`` if :attr:`high_water_mark` is has been reached for the
            specified packet queue.
        '''
        return ((self.high_water_mark is not None) and
                (self.packet_queues[name].qsize() >= self.high_water_mark))


class SerialStream(object):
    '''
    Wrapper around :class:`serial.Serial` device to provide a parameterless
    :meth:`read` method.

    Parameters
    ----------
    serial_device : serial.Serial
        Serial device to wrap.
    '''
    def __init__(self, serial_device):
        self.serial_device = serial_device

    def read(self):
        '''
        Returns
        -------
        str or bytes
            Available data from serial receiving buffer.
        '''
        return self.serial_device.read(self.serial_device.inWaiting())

    def write(self, str):
        '''
        Parameters
        ----------
        str : str or bytes
            Data to write to serial transmission buffer.
        '''
        self.serial_device.write(str)

    def close(self):
        '''
        Close serial stream.
        '''
        self.serial_device.close()


class FakeStream(object):
    '''
    Stream interface which returns a list of message strings, one message at a
    time, from the :meth:`read` method.

    Useful, for example, for testing the :class:`PacketWatcher` class without a
    serial connection.
    '''
    def __init__(self, messages):
        self.messages = messages

    def read(self):
        if self.messages:
            return self.messages.pop(0)
        else:
            return ''


class PacketWatcher(Thread):
    '''
    Thread task to watch for new packets on a stream.

    Parameters
    ----------
    stream : SerialStream
        Object that **MUST** have a ``read`` method that returns a ``str-like``
        value.
    delay_seconds : float, optional
        Number of seconds to wait between polls of stream.
    high_water_mark : int, optional
        Maximum number of packets to store in each packet queue.

        .. see::
            :class:`PacketQueueManager`
    '''
    def __init__(self, stream, delay_seconds=.01, high_water_mark=None):
        self.message_parser = PacketQueueManager(high_water_mark)
        self.stream = stream
        self.enabled = False
        self._terminated = False
        self.delay_seconds = delay_seconds
        super(PacketWatcher, self).__init__()
        self.daemon = True

    def run(self):
        '''
        Start watching stream.
        '''
        while True:
            if self._terminated:
                break
            elif self.enabled:
                self.parse_available()
            time.sleep(self.delay_seconds)

    def parse_available(self):
        '''
        Parse available data from stream.
        '''
        self.message_parser.parse_available(self.stream)

    @property
    def queues(self):
        return self.message_parser.packet_queues

    def terminate(self):
        '''
        Stop watching task.
        '''
        self._terminated = True
        self.delay_seconds = 0
        self.join()

    def __del__(self):
        '''
        Stop watching task when deleted.
        '''
        self.terminate()
