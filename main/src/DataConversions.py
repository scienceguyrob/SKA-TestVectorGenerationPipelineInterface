"""
**************************************************************************

 DataConversions.py

**************************************************************************
 Description:

 Converts data quantities represented in bits/bytes.

**************************************************************************
 Author: Rob Lyon
 Email : robert.lyon@manchester.ac.uk
 web   : www.scienceguyrob.com

**************************************************************************
 License:

 Code made available under the GPLv3 (GNU General Public License), that
 allows you to copy, modify and redistribute the code as you see fit
 (http://www.gnu.org/copyleft/gpl.html). Though a mention to the
 original author using the citation above in derivative works, would be
 very much appreciated.

**************************************************************************
"""


def bitsToBytes(bits):
    """
    Simply converts bits to bytes.

    Parameters
    ----------
    @param bits: the integer bits value to be converted.

    Returns
    ----------
    @return the number of bytes as a float.

    Examples
    ----------
    >>> print bitsToBytes(1)
    >>> 0.125
    >>> print bitsToBytes(8)
    >>> 1
    >>> print bitsToBytes(-1)
    >>> None
    """
    if (type(bits) == int) or (type(bits) == float):

        if bits == 0:
            return 0
        elif bits <= 0.0:
            return 0
        else:
            return float(bits / 8.0)
    else:
        return None


# ******************************

def bytesToBits(byte):
    """
    Simply converts bytes to bits.

    Parameters
    ----------
    @param byte: the int/float bytes value to be converted.

    Returns
    ----------
    @return the number of bits as a float.

    Examples
    ----------
    >>> print bytesToBits(1)
    >>> 8
    >>> print bytesToBits(2)
    >>> 16
    >>> print bytesToBits(-1)
    >>> None
    """
    if (type(byte) == int) or (type(byte) == float):

        if byte == 0:
            return 0
        elif byte <= 0.0:
            return 0
        else:
            return float(byte * 8.0)
    else:
        return None


# ******************************

def isBitUnitValid(units):
    """
    Checks the validity of a user specified bit data format.
    For example, 'kbit' would be valid, but 'Kbit' would not
    be according to SI standards.

    The valid formats should include:

    bit     - a single bit of information.
    kbit    - kilobit, 10^3  = 1000 bits.
    Mbit    - megabit, 10^6  bits.
    Gbit    - gigabit, 10^9  bits.
    Tbit    - terabit, 10^12 bits.
    Pbit    - petabit, 10^15 bits.

    Parameters
    ----------
    @param units: the desired format for the data.

    Returns
    ----------
    True if the format is valid, else False.

    Examples
    ----------
    >>> print isBitUnitValid('bits')
    >>> False
    >>> print isBitUnitValid('bit')
    >>> True
    >>> print isBitUnitValid('kbit')
    >>> True
    >>> print isBitUnitValid('GB')
    >>> False
    """
    if type(units) == str:

        if units == 'bit':
            return True
        elif units == 'kbit':
            return True
        elif units == 'Mbit':
            return True
        elif units == 'Gbit':
            return True
        elif units == 'Tbit':
            return True
        elif units == 'Pbit':
            return True
        else:
            return False
    else:
        return False


# ******************************

def isByteUnitValid(units):
    """
    Checks the validity of a user specified byte data format.
    For example, 'B' would be valid, but 'byte' would not be
    according to SI standards.

    The valid formats should include:

    B       - byte, 8 bits of information.
    kB      - kilobyte, 10^3 bytes (or 8 x 10^3 bits).
    MB      - megabyte, 10^6  bytes (or 8 x 10^6 bits).
    Gb      - gigabyte, 10^9  bytes (or 8 x 10^9 bits).
    TP      - terabyte, 10^12 bytes (or 8 x 10^12 bits).
    PB      - petabyte, 10^15 bytes (or 8 x 10^15 bits).

    Parameters
    ----------
    @param units: the desired format for the data.

    Returns
    ----------
    True if the format is valid, else False.

    Examples
    ----------
    >>> print isByteUnitValid('bytes')
    >>> False
    >>> print isByteUnitValid('B')
    >>> True
    >>> print isByteUnitValid('MB')
    >>> True
    """
    if type(units) == str:

        if units == 'B':
            return True
        elif units == 'kB':
            return True
        elif units == 'MB':
            return True
        elif units == 'GB':
            return True
        elif units == 'TB':
            return True
        elif units == 'PB':
            return True
        else:
            return False
    else:
        return False


# ******************************


def convertFromBit(bits, units='None'):
    """
    Converts an int/float describing a number of bits,
    in a supplied bit format, to bits. For example this
    could involve converting 1 kbit to bits, 1 Mbit to bits
    etc. The unit determines how the data will be output.

    Units can be chosen from the list below:

    bit     - a single bit of information.
    kbit    - kilobit, 10^3  = 1000 bits.
    Mbit    - megabit, 10^6  bits.
    Gbit    - gigabit, 10^9  bits.
    Tbit    - terabit, 10^12 bits.
    Pbit    - petabit, 10^15 bits.

    Conversion examples:

    -------------------------
    |  bits  |    bit unit  |
    -------------------------
    | 1      |   1 bit      |
    | 10^3   |   1 kilobit  |
    | 10^6   |   1 Megabit  |
    | 10^9   |   1 Gigabit  |
    | 10^12  |   1 Terabit  |
    | 10^15  |   1 Petabit  |
    -------------------------

    Conversion ratio:

    1 bit : 0.125 byte

    If the supplied bits value is negative, or not an
    integer/float, None is returned. If an invalid format is supplied,
    None is returned. Else the converted value is returned.

    Parameters
    ----------
    @param bits: the integer/float bit value to be converted.
    @param units: the desired format for the data.

    Returns
    ----------
    @return the number of converted bits as a float.

    Examples
    ----------
    >>> print convertFromBit(1,format='bit')
    >>> 1.0
    >>> print convertFromBit(1,format='kbit')
    >>> 1000.0
    >>> print convertFromBit(1,format='Mbit')
    >>> 1000000.0
    """
    if (type(bits) == int or type(bits) == float) and type(units) == str:
        if isBitUnitValid(units):
            if bits == 0:
                return 0
            elif bits < 0:
                return None
            elif bits > 0:
                if units == 'bit':
                    return bits
                elif units == 'kbit':
                    return float(bits) / pow(10, 3)
                elif units == 'Mbit':
                    return float(bits) / pow(10, 6)
                elif units == 'Gbit':
                    return float(bits) / pow(10, 9)
                elif units == 'Tbit':
                    return float(bits) / pow(10, 12)
                elif str(units) == 'Pbit':
                    return float(bits) / pow(10, 15)
                else:
                    return None
        else:
            return None
    else:
        return None


# ******************************

def convertToBit(nonbits, units='None'):
    """
    Converts an int/float describing a number of bits,
    to a desired bit format. For example this could
    involve converting 1000 bits to 1 kbit, 0.001 Mbit etc.
    The unit determines how the data will be output.

    Units can be chosen from the list below:

    bit     - a single bit of information.
    kbit    - kilobit, 10^3  = 1000 bits.
    Mbit    - megabit, 10^6  bits.
    Gbit    - gigabit, 10^9  bits.
    Tbit    - terabit, 10^12 bits.
    Pbit    - petabit, 10^15 bits.

    to bits. For example, 1 Kbit would be converted to
    1000 bits.

    Conversion examples:

    -------------------------
    |  bits  |    bit unit  |
    -------------------------
    | 1      |   1 bit      |
    | 10^3   |   1 kilobit  |
    | 10^6   |   1 Megabit  |
    | 10^9   |   1 Gigabit  |
    | 10^12  |   1 Terabit  |
    | 10^15  |   1 Petabit  |
    -------------------------

    Conversion ratio:

    1 bit : 0.125 byte

    If the supplied non bits value is negative, or not an
    integer/float, None is returned. If an invalid format is supplied,
    None is returned. Else the converted value is returned.

    Parameters
    ----------
    @param nonbits: the integer/float value to be converted.
    @param units: the current format of the data.

    Returns
    ----------
    @return the number of converted bits as a float.

    Examples
    ----------
    >>> print convertToBit(1,format='bit')
    >>> 1
    >>> print convertToBit(1000,format='kbit')
    >>> 1.0
    >>> print convertToBit(1000,format='Mbit')
    >>> 0.001
    """
    if (type(nonbits) == int or type(nonbits) == float) and type(units) == str:
        if isBitUnitValid(units):
            if nonbits == 0:
                return 0
            elif nonbits < 0:
                return None
            elif nonbits > 0:
                if units == 'bit':
                    return nonbits
                elif units == 'kbit':
                    return float(nonbits) * pow(10, 3)
                elif units == 'Mbit':
                    return float(nonbits) * pow(10, 6)
                elif units == 'Gbit':
                    return float(nonbits) * pow(10, 9)
                elif units == 'Tbit':
                    return float(nonbits) * pow(10, 12)
                elif str(units) == 'Pbit':
                    return float(nonbits) * pow(10, 15)
                else:
                    return None
        else:
            return None
    else:
        return None


# ******************************


def convertByteToBit(byte, units='None'):
    """
    Converts an int/float describing a number of bytes,
    to a bit value. This function does the conversion
    according to a user specified unit which describes
    what the input data is (i.e. kb, MB, GB etc). The unit
    determines how the data will be output. Units can be
    chosen from the list below:

    B    - bytes.
    kB   - kilobyte.
    MB   - megabyte.
    GB   - gigabyte.
    TB   - terabyte.
    PB   - petabyte.

    Conversion examples:

    ------------------------------------------------------------
    |  bits  |    bit unit  |     Bytes unit    |     Bytes    |
    ------------------------------------------------------------
    | 1      |   1 bit      | 1 B   (byte)      |     0.125    |
    | 10^3   |   1 kilobit  | 1 kB  (kilobyte)  | 1.25 x 10^2  |
    | 10^6   |   1 Megabit  | 1 MB  (megabyte)  | 1.25 x 10^5  |
    | 10^9   |   1 Gigabit  | 1 GB  (gigabyte)  | 1.25 x 10^8  |
    | 10^12  |   1 Terabit  | 1 TB  (terabyte)  | 1.25 x 10^11 |
    | 10^15  |   1 Petabit  | 1 PB  (petabyte)  | 1.25 x 10^14 |
    ------------------------------------------------------------

    Conversion ratio:

    1 bit : 0.125 byte

    If the supplied bits value is negative, or not an
    integer/float, None is returned. If an invalid format is supplied,
    None is returned. Else the converted value is returned.

    Parameters
    ----------
    @param byte: the integer/float value to be converted.
    @param units: the current format of the data.

    Returns
    ----------
    @return the number of converted bits as a float.

    Examples
    ----------
    >>> print convertByteToBit(1,format='B')
    >>> 8.0
    >>> print convertByteToBit(1,format='kB')
    >>> 8000.0
    """
    if (type(byte) == int or type(byte) == float) and type(units) == str:
        if isByteUnitValid(units):
            if byte == 0:
                return 0
            elif byte < 0:
                return None
            elif byte > 0:
                if units == 'B':
                    return float(byte) * 8
                elif units == 'kB':
                    return (float(byte) * 8) * pow(10, 3)
                elif units == 'MB':
                    return (float(byte) * 8) * pow(10, 6)
                elif units == 'GB':
                    return (float(byte) * 8) * pow(10, 9)
                elif units == 'TB':
                    return (float(byte) * 8) * pow(10, 12)
                elif str(units) == 'PB':
                    return (float(byte) * 8) * pow(10, 15)
                else:
                    return None
        else:
            return None
    else:
        return None


# ******************************

def convertBitToByte(bits, units='None'):
    """
    Converts an int/float describing a number of bits,
    to a byte value. This function does the conversion
    according to a user desired output unit (e.g. kb,
    MB, GB, etc). The unit determines how the data will
    be output. Units can be chosen from the list below:

    B    - bytes.
    kB   - kilobyte.
    MB   - megabyte.
    GB   - gigabyte.
    TB   - terabyte.
    PB   - petabyte.

    Conversion examples:

    ------------------------------------------------------------
    |  bits  |    bit unit  |     Bytes unit    |     Bytes    |
    ------------------------------------------------------------
    | 1      |   1 bit      | 1 B   (byte)      |     0.125    |
    | 10^3   |   1 kilobit  | 1 kB  (kilobyte)  | 1.25 x 10^2  |
    | 10^6   |   1 Megabit  | 1 MB  (megabyte)  | 1.25 x 10^5  |
    | 10^9   |   1 Gigabit  | 1 GB  (gigabyte)  | 1.25 x 10^8  |
    | 10^12  |   1 Terabit  | 1 TB  (terabyte)  | 1.25 x 10^11 |
    | 10^15  |   1 Petabit  | 1 PB  (petabyte)  | 1.25 x 10^14 |
    ------------------------------------------------------------

    Conversion ratio:

    1 bit : 0.125 byte

    If the supplied bits value is negative, or not an
    integer/float, None is returned. If an invalid format is supplied,
    None is returned. Else the converted value is returned.

    Parameters
    ----------
    @param nonbits: the integer/float value to be converted.
    @param units: the current format of the data.

    Returns
    ----------
    @return the number of converted bytes as a float.

    Examples
    ----------
    >>> print convertBitToByte(1,format='B')
    >>> 0.125
    >>> print convertBitToByte(8000,format='kB')
    >>> 1.0
    """
    if (type(bits) == int or type(bits) == float) and type(units) == str:
        if isByteUnitValid(units):
            if bits == 0:
                return 0
            elif bits < 0:
                return None
            elif bits > 0:
                if units == 'B':
                    return float(bits) / 8
                elif units == 'kB':
                    return (float(bits) / 8) / pow(10, 3)
                elif units == 'MB':
                    return (float(bits) / 8) / pow(10, 6)
                elif units == 'GB':
                    return (float(bits) / 8) / pow(10, 9)
                elif units == 'TB':
                    return (float(bits) / 8) / pow(10, 12)
                elif str(units) == 'PB':
                    return (float(bits) / 8) / pow(10, 15)
                else:
                    return None
        else:
            return None
    else:
        return None
