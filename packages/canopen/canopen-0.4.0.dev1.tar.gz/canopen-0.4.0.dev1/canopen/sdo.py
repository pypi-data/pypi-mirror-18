import collections
import struct
import logging
import threading

from . import objectdictionary
from . import common


logger = logging.getLogger(__name__)


# Command, index, subindex
SDO_STRUCT = struct.Struct("<BHB")


REQUEST_SEGMENT_DOWNLOAD = 0 << 5
REQUEST_DOWNLOAD = 1 << 5
REQUEST_UPLOAD = 2 << 5
REQUEST_SEGMENT_UPLOAD = 3 << 5

RESPONSE_SEGMENT_UPLOAD = 0 << 5
RESPONSE_SEGMENT_DOWNLOAD = 1 << 5
RESPONSE_UPLOAD = 2 << 5
RESPONSE_DOWNLOAD = 3 << 5
RESPONSE_ABORTED = 4 << 5

EXPEDITED = 0x2
SIZE_SPECIFIED = 0x1


class SdoClient(collections.Mapping):
    """Handles communication with an SDO server."""

    def __init__(self, node_id, od):
        #: Node ID
        self.id = node_id
        self.network = None
        self.od = od
        self.response = None
        self.response_received = threading.Condition()

    def on_response(self, can_id, data, timestamp):
        with self.response_received:
            self.response = data
            self.response_received.notify_all()

    def send_request(self, sdo_request):
        retires_left = 5
        while retires_left:
            # Wait for node to respond
            with self.response_received:
                self.response = None
                self.network.send_message(0x600 + self.id, sdo_request)
                self.response_received.wait(0.5)

            if self.response is None:
                retires_left -= 1
            else:
                retires_left = 0

        if self.response is None:
            raise SdoCommunicationError("No SDO response received")
        elif self.response[0] == RESPONSE_ABORTED:
            abort_code, = struct.unpack("<L", self.response[4:8])
            raise SdoAbortedError(abort_code)
        else:
            return self.response

    def upload(self, index, subindex):
        """May be called to manually make a read operation.

        :param int index:
            Index of object to read.
        :param int subindex:
            Sub-index of object to read.

        :return: A data object.
        :rtype: bytearray

        :raises canopen.SdoCommunicationError:
            On unexpected response or timeout.
        :raises canopen.SdoAbortedError:
            When node responds with an error.
        """
        request = SDO_STRUCT.pack(REQUEST_UPLOAD, index, subindex)
        request += b"\x00\x00\x00\x00"
        response = self.send_request(request)
        res_command, res_index, res_subindex = SDO_STRUCT.unpack(response[0:4])
        res_data = response[4:]

        if res_command & 0xE0 != RESPONSE_UPLOAD:
            raise SdoCommunicationError("Unexpected response")

        # Check that the message is for us
        if res_index != index or res_subindex != subindex:
            raise SdoCommunicationError((
                "Node returned a value for 0x{:X}:{:d} instead, "
                "maybe there is another SDO master communicating "
                "on the same SDO channel?").format(res_index, res_subindex))

        expedited = res_command & EXPEDITED
        size_specified = res_command & SIZE_SPECIFIED

        length = None

        if expedited and size_specified:
            # Expedited upload
            length = 4 - ((res_command >> 2) & 0x3)
        elif not expedited:
            # Segmented upload
            if size_specified:
                length, = struct.unpack("<L", res_data)

            request = bytearray(8)
            request[0] = REQUEST_SEGMENT_UPLOAD
            res_data = bytearray()
            while True:
                response = self.send_request(request)
                if response[0] & 0xE0 != RESPONSE_SEGMENT_UPLOAD:
                    raise SdoCommunicationError("Unexpected response")
                last_byte = 8 - ((response[0] >> 1) & 0x7)
                res_data.extend(response[1:last_byte])
                if response[0] & 0x1:
                    break
                request[0] ^= 0x10

        if length is not None and len(res_data) != length:
            res_data = res_data[:length]
        return res_data

    def download(self, index, subindex, data):
        """May be called to manually make a write operation.

        :param int index:
            Index of object to write.
        :param int subindex:
            Sub-index of object to write.
        :param bytes data:
            Data to be written.

        :raises canopen.SdoCommunicationError:
            On unexpected response or timeout.
        :raises canopen.SdoAbortedError:
            When node responds with an error.
        """
        length = len(data)
        command = REQUEST_DOWNLOAD | SIZE_SPECIFIED

        if length <= 4:
            # Expedited download
            command |= EXPEDITED
            command |= (4 - length) << 2
            request = SDO_STRUCT.pack(command, index, subindex)
            request += data.ljust(4, b"\x00")
            response = self.send_request(request)
            if response[0] != RESPONSE_DOWNLOAD:
                raise SdoCommunicationError("Unexpected response")
        else:
            # Segmented download
            request = SDO_STRUCT.pack(command, index, subindex)
            request += struct.pack("<L", length)
            response = self.send_request(request)
            if response[0] != RESPONSE_DOWNLOAD:
                raise SdoCommunicationError("Unexpected response")

            request = bytearray(8)
            request[0] = REQUEST_SEGMENT_DOWNLOAD
            for pos in range(0, length, 7):
                request[1:8] = data[pos:pos + 7]
                if pos + 7 >= length:
                    # No more data after this message
                    request[0] |= 1
                # Specify number of bytes in that do not contain segment data
                request[0] |= (8 - len(request)) << 1
                response = self.send_request(request.ljust(8, b'\x00'))
                # Toggle bit for next request
                request[0] ^= 0x10
                if response[0] & 0xE0 != RESPONSE_SEGMENT_DOWNLOAD:
                    raise SdoCommunicationError("Unexpected response")

    def __getitem__(self, index):
        entry = self.od[index]
        if isinstance(entry, objectdictionary.Variable):
            return Variable(self, entry)
        elif isinstance(entry, objectdictionary.Array):
            return Array(self, entry)
        elif isinstance(entry, objectdictionary.Record):
            return Record(self, entry)

    def __iter__(self):
        return iter(self.od)

    def __len__(self):
        return len(self.od)

    def __contains__(self, key):
        return key in self.od


class Record(collections.Mapping):

    def __init__(self, sdo_node, od):
        self.sdo_node = sdo_node
        self.od = od

    def __getitem__(self, subindex):
        return Variable(self.sdo_node, self.od[subindex])

    def __iter__(self):
        return iter(self.od)

    def __len__(self):
        return len(self.od)

    def __contains__(self, subindex):
        return subindex in self.od


class Array(collections.Mapping):

    def __init__(self, sdo_node, od):
        self.sdo_node = sdo_node
        self.od = od

    def __getitem__(self, subindex):
        return Variable(self.sdo_node, self.od[subindex])

    def __iter__(self):
        return iter(range(1, len(self) + 1))

    def __len__(self):
        return self[0].raw

    def __contains__(self, subindex):
        return 0 <= subindex <= len(self)


class Variable(common.Variable):
    """Access object dictionary variable values using SDO protocol."""

    def __init__(self, sdo_node, od):
        self.sdo_node = sdo_node
        common.Variable.__init__(self, od)

    def get_data(self):
        return self.sdo_node.upload(self.od.index, self.od.subindex)

    def set_data(self, data):
        self.sdo_node.download(self.od.index, self.od.subindex, data)


class SdoError(Exception):
    pass


class SdoAbortedError(SdoError):
    """SDO abort exception."""

    CODES = {
        0x05030000: "SDO toggle bit error",
        0x05040000: "Timeout of transfer communication detected",
        0x05040001: "Unknown SDO command specified",
        0x05040003: "Invalid sequence number",
        0x06010000: "Unsupported access to an object",
        0x06010001: "Attempt to read a write only object",
        0x06010002: "Attempt to write a read only object",
        0x06020000: "Object does not exist",
        0x06040042: "PDO length exceeded",
        0x06060000: "Access failed due to a hardware error",
        0x06070010: "Data type and length code do not match",
        0x06090011: "Subindex does not exist",
        0x06090030: "Value range of parameter exceeded",
        0x060A0023: "Resource not available",
        0x08000000: "General error",
        0x08000021: ("Data can not be transferred or stored to the application "
                     "because of local control"),
        0x08000022: ("Data can not be transferred or stored to the application "
                     "because of the present device state")
    }

    def __init__(self, code):
        #: Abort code
        self.code = code

    def __str__(self):
        text = "Code 0x{:08X}".format(self.code)
        if self.code in self.CODES:
            text = text + ", " + self.CODES[self.code]
        return text


class SdoCommunicationError(SdoError):
    """No or unexpected response from slave."""
