from struct import Struct

from pkt.captures import CapturedPacket, NetworkCapture
from ._nicer.structs import DefinedStruct
from ._nicer.times import datetime_from_seconds_and_microseconds, seconds_from_datetime, \
    microseconds_from_datetime

__author__ = 'netanelrevah'


class CapturedPacketHeaderFormat(DefinedStruct):
    LITTLE_ENDIAN_HEADER_STRUCT = Struct('<IIII')
    BIG_ENDIAN_HEADER_STRUCT = Struct('>IIII')

    def __init__(self, seconds=0, microseconds=0, data_length=0, original_length=0):
        self.seconds = seconds
        self.microseconds = microseconds
        self.data_length = data_length
        self.original_length = original_length

    @property
    def capture_time(self):
        return datetime_from_seconds_and_microseconds(self.seconds, self.microseconds)

    def _get_values_tuple(self):
        return (self.seconds,
                self.microseconds,
                self.data_length,
                self.original_length)

    @classmethod
    def init_from_captured_packet(cls, captured_packet):
        seconds = seconds_from_datetime(captured_packet.capture_time)
        microseconds = microseconds_from_datetime(captured_packet.capture_time)
        return cls(seconds, microseconds, len(captured_packet), captured_packet.original_length)

    @classmethod
    def loads(cls, stream, is_big_endian=False):
        header_data = stream.read(cls.size())
        if not header_data or len(header_data) == 0:
            return
        return cls.unpack(header_data, is_big_endian)


class CapturedPacketFormat(object):
    def __init__(self, header=None, data=b''):
        self.data = data
        self.header = header
        if header is None:
            self.header = CapturedPacketHeaderFormat(data_length=len(self.data), original_length=len(self.data))

    @classmethod
    def init_from_captured_packet(cls, captured_packet):
        captured_packet_header = CapturedPacketHeaderFormat.init_from_captured_packet(captured_packet)
        return cls(captured_packet_header, captured_packet.data)

    def to_captured_packet(self):
        return CapturedPacket(self.data, self.header.capture_time, self.header.original_length)

    @classmethod
    def loads(cls, stream, is_big_endian=False):
        captured_packet_header = CapturedPacketHeaderFormat.loads(stream, is_big_endian)
        if captured_packet_header is None:
            return None
        data = stream.read(captured_packet_header.data_length)
        if len(data) != captured_packet_header.data_length:
            raise Exception('Invalid Packet Data Length! Header consist: {} bytes, Data loaded: {} bytes'.format(
                captured_packet_header.data_length, len(data)))
        return cls(captured_packet_header, data)

    def dumps(self, is_big_endian=False):
        return self.header.pack(is_big_endian) + self.data

    def __eq__(self, other):
        return self.data == other.data and self.header == other.header


class PacketCaptureHeaderFormat(DefinedStruct):
    LITTLE_ENDIAN_HEADER_STRUCT = Struct('<IHHiIII')
    BIG_ENDIAN_HEADER_STRUCT = Struct('>IHHiIII')
    MAGIC_VALUE = 0xa1b2c3d4

    @classmethod
    def loads(cls, stream, is_big_endian=False):
        header_data = stream.read(cls.size())
        header_data = b'' if header_data is None else header_data
        return cls.unpack(header_data, is_big_endian)

    def __init__(self, major_version=2, minor_version=4, time_zone_hours=0, max_capture_length_octets=0x40000,
                 link_layer_type=1):
        self.major_version = major_version
        self.minor_version = minor_version
        self.time_zone_hours = time_zone_hours
        self.max_capture_length_octets = max_capture_length_octets
        self.link_layer_type = link_layer_type

    @staticmethod
    def _filter_constants(values):
        return values[1], values[2], values[3], values[5], values[6]

    def _get_values_tuple(self):
        return self.MAGIC_VALUE, self.major_version, self.minor_version, self.time_zone_hours, 0, \
               self.max_capture_length_octets, self.link_layer_type


class PacketCaptureFormatLoader(object):
    MAGIC_VALUES_TO_BIG_ENDIAN = {b'\xa1\xb2\xc3\xd4': False, b'\xa1\xb2\x3c\xd4': False,
                                  b'\xd4\xc3\xb2\xa1': True, b'\xd4\x3c\xb2\xa1': True}

    def __init__(self, stream):
        self.stream = stream
        self._is_big_endian = False
        self._file_header = None

    def _load_file_header(self):
        magic = self.stream.read(4)
        if magic not in self.MAGIC_VALUES_TO_BIG_ENDIAN:
            raise Exception('Stream magic is invalid')
        self._is_big_endian = self.MAGIC_VALUES_TO_BIG_ENDIAN[magic]
        self.stream.seek(-4, 1)

        self._file_header = PacketCaptureHeaderFormat.loads(self.stream, self._is_big_endian)

    def _force_file_header_loading(self):
        if self._file_header is None:
            self._load_file_header()

    @property
    def is_big_endian(self):
        self._force_file_header_loading()
        return self._is_big_endian

    @property
    def file_header(self):
        self._force_file_header_loading()
        return self._file_header

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        self._force_file_header_loading()
        formatted_captured_packet = CapturedPacketFormat.loads(self.stream, self._is_big_endian)
        if formatted_captured_packet is None:
            raise StopIteration()
        return formatted_captured_packet


class PacketCaptureFormatDumper(object):
    def __init__(self, packet_capture, is_big_endian=False):
        self._packet_capture = packet_capture
        self.is_big_endian = is_big_endian
        self._file_header = None
        self._captured_packets_iterator = None

    def _dump_file_header(self):
        self._file_header = self._packet_capture.file_header.pack(self.is_big_endian)

    def _force_file_header_dumping(self):
        if self._file_header is None:
            self._dump_file_header()

    @property
    def file_header(self):
        self._force_file_header_dumping()
        return self._file_header

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        self._force_file_header_dumping()
        if self._captured_packets_iterator is None:
            self._captured_packets_iterator = iter(self._packet_capture.captured_packets)
        return next(self._captured_packets_iterator).dumps(self.is_big_endian)


class PacketCaptureFormat(object):
    def __init__(self, file_header, captured_packets=None, is_big_endian=False):
        self.file_header = file_header
        self.captured_packets = captured_packets if captured_packets is not None else []
        self.is_big_endian = is_big_endian

    @classmethod
    def from_network_capture(cls, network_capture):
        file_header = PacketCaptureHeaderFormat()
        captured_packets = map(CapturedPacketFormat.init_from_captured_packet, network_capture)
        return cls(file_header, list(captured_packets))

    def to_network_capture(self):
        captured_packets = list(map(CapturedPacketFormat.to_captured_packet, self.captured_packets))
        return NetworkCapture(captured_packets, self.file_header.link_layer_type)

    @classmethod
    def loads(cls, stream):
        loader = PacketCaptureFormatLoader(stream)
        return cls(loader.file_header, list(loader), loader.is_big_endian)

    def dumps(self):
        dumper = PacketCaptureFormatDumper(self, self.is_big_endian)
        return dumper.file_header + b''.join(list(dumper))
