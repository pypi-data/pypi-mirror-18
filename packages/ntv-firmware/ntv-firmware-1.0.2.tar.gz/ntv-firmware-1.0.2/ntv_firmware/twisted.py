from __future__ import absolute_import
import sys
import serial
from serial.tools import list_ports
import glob
from time import sleep
from twisted.internet import reactor, defer


def locate_firmware(
    baudrate = 57600,
    firmware_id = None,
    firmware_version = None,
    firmware_uid = None,
    outstream = sys.stdout,
    silent = False,
    delay = 1,
    max_attempts = 0
    ):
    """

    Parameters
    ---
        baudrate (int):             Baudrate to open COM port at
        firmware_id (string):       Firmware identifier to search for
        firmware_version (string):  Firmware version to search for
        firmware_uid (string):      Firmware instance UID to search for
        outstream (file):           Output stream for logging. Defaults to stdout
        silent (boolean):           Don't output anything to outstream
        delay (int):                Seconds to delay between iterations
        max_attempts (int):         Number of iterations to search for. Defaults
                                    to `0` (infinite)

    Returns
    -------
    Deferred
        Deferred object that resolves once the port has been found
    """
    d = defer.Deferred()
    attempts = 0

    # outstream = sys.stdout if outstream is None else outstream
    def log (msg, *args):
        if not silent:
            outstream.write( msg.format(*args) )


    def search():
        ## Platform-dependant port enumeration
        log("[NTV-Firmware] Enumerating COM ports... ")
        ports = list_ports.comports()
        # if sys.platform.startswith('win'):
        #     ports = ['COM%s' % (i + 1) for i in range(256)]
        # elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        #     # this excludes your current terminal "/dev/tty"
        #     ports = glob.glob('/dev/ttyACM[0-9]*')
        # elif sys.platform.startswith('darwin'):
        #     ports = glob.glob('/dev/tty.usbmodem[0-9]*')
        # else:
        #     raise EnvironmentError('Unsupported platform')
        log("{} found\n", len(ports))

        for port in ports:
            try:
                log("[NTV-Firmware] - Checking {}... ", port.device)
                with serial.Serial(port.device, baudrate, timeout=1) as sp:
                    sleep(1)
                    numBytes = sp.inWaiting()
                    sp.read(9999)
                    sp.reset_input_buffer()
                    sp.write("IDENTIFY\n")

                    replied = False
                    tries = 0
                    id = None
                    while not replied:
                        id = sp.readline()
                        if len(id) == 0:
                            tries += 1
                            if tries > 6:
                                id = ''
                                replied = True
                        else:
                            replied = True


                    if id == "":
                        log("NOT_NTV_FIRMWARE\n")
                        continue
                    _,f_uid,f_id,f_version = id.strip().split(":")

                    if firmware_id is not None and firmware_id != f_id:
                        log("INVALID_FIRMWARE\n")
                        continue
                    if firmware_version is not None and firmware_version != f_version:
                        log("INVALID_FIRMWARE_VERSION")
                        continue
                    if firmware_uid is not None and firmware_uid != f_uid:
                        log("INVALID_UID\n")
                        continue

                    log("SUCCESS\n")
                    return port.device

            except Exception as e:
                if hasattr(e,'errno') and e.errno == 16:
                    log("DEVICE_BUSY\n")
                else:
                    print e
                    log("NOT_NTV_FIRMWARE\n")

        return None


    def deferred_search( attempts = 0, max_attempts = 0):
        try:
            found_port = search()
            attempts += 1
            if found_port is None:
                if max_attempts > 0 and attempts >= max_attempts:
                    d.errback()
                else:
                    reactor.callLater(delay, deferred_search, attempts=attempts, max_attempts=max_attempts)

            else:
                d.callback(found_port)
        except Exception as err:
            d.errback(err)


    reactor.callLater(0, deferred_search, max_attempts=max_attempts )
    return d
