# from scipy.io.wavfile import write
import struct
import numpy as np
import sys

# print(INTERNAL_MIC_PIN.value / 65536)

samplerate = 400; fs = 300
t = np.linspace(0., 1., samplerate)
amplitude = 40
data = np.sin(2. * np.pi * fs * t)
def float_to_uint8(data_pt, amplitude):
    data_pt *= amplitude
    data_pt = int(data_pt)
    if (data_pt < 0): data_pt += 256
    return data_pt
data_new = [float_to_uint8(x, amplitude) for x in data]


# normalize and multiply by magnitude
    # print(INTERNAL_MIC_PIN.value / 65536)

def scipy_wavefile_write(filename, rate, data):
    if hasattr(filename, 'write'):
        fid = filename
    else:
        fid = open(filename, 'wb')

    fs = rate

    try:
        dkind = 'i'

        header_data = b''

        header_data += b'RIFF'
        header_data += b'\x00\x00\x00\x00'
        header_data += b'WAVE'

        # fmt chunk
        header_data += b'fmt '
        format_tag = 0x0001
        channels = 1
        
        bit_depth = 8
        bytes_per_second = fs*(bit_depth // 8)*channels
        block_align = channels * (bit_depth // 8)

        fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, fs,
                                    bytes_per_second, block_align, bit_depth)
        if not (dkind == 'i' or dkind == 'u'):
            # add cbSize field for non-PCM files
            fmt_chunk_data += b'\x00\x00'

        header_data += struct.pack('<I', len(fmt_chunk_data))
        header_data += fmt_chunk_data

        # fact chunk (non-PCM files)
        if not (dkind == 'i' or dkind == 'u'):
            header_data += b'fact'
            header_data += struct.pack('<II', 4, data.shape[0])

        # check data size (needs to be immediately before the data chunk)
        if ((len(header_data)-4-4) + (4+4+bit_depth*len(data))) > 0xFFFFFFFF:
            raise ValueError("Data exceeds wave file size limit")

        fid.write(header_data)

        # data chunk
        fid.write(b'data')
        fid.write(struct.pack('<I', bit_depth*len(data)))
        # if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and
                                        # sys.byteorder == 'big'):
        if (sys.byteorder == 'big'):
            data = data.byteswap()
        # fid.write(data.ravel().view('b').data)
        fid.write(bytes(data))

        # Determine file size and place it in correct
        #  position at start of the file.
        size = fid.tell()
        fid.seek(4)
        fid.write(struct.pack('<I', size-8))

    finally:
        if not hasattr(filename, 'write'):
            fid.close()
        else:
            fid.seek(0)

scipy_wavefile_write("example.wav", samplerate, data_new)
