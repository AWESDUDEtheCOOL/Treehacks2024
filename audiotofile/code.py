# from scipy.io.wavfile import write
import struct
import sys
from analogio import AnalogIn
import board
import time
import os 

f = open("file1.txt", "a")
    

INTERNAL_MIC_PIN = AnalogIn(board.MIC)
samplerate = 900
amplitude = 250
total_data = 0


# data = 100000* [INTERNAL_MIC_PIN.value / 65536]
# for j in range(100):
#     data = []
#     for i in range(100):
#         data.append(INTERNAL_MIC_PIN.value / 65536)
#         time.sleep(0.0002)s



def float_to_uint8(data_pt, amplitude):
    data_pt *= amplitude
    data_pt = int(data_pt)
    if (data_pt < 0): data_pt += 256
    return data_pt


# normalize and multiply by magnitude
    # print(INTERNAL_MIC_PIN.value / 65536)

def scipy_wavefile_write(filename, rate):
    global total_data
    # if hasattr(filename, 'write'):
    #     fid = filename
    # else:
    fid = open(filename, 'w')

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
        # if ((len(header_data)-4-4) + (4+4+bit_depth*len(data))) > 0xFFFFFFFF:
            # raise ValueError("Data exceeds wave file size limit")

        fid.write(header_data)

        # data chunk
        fid.write(b'data')
        fid.write(bytes(open("file1.txt", "rb").read()))
        fid.write(struct.pack('<I', bit_depth*(total_data)))
        # if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and
                                        # sys.byteorder == 'big'):
        
        size = fid.tell()
        fid.seek(4)
        fid.write(struct.pack('<I', size-8))
    finally:
        if not hasattr(filename, 'write'):
            fid.close()
        else:
            fid.seek(0)
        
        os.remove("file1.txt")

def temp_write(data_new):
    global total_data
    global f
    if (sys.byteorder == 'big'):
        data_new = data_new.byteswap()
        # fid.write(data.ravel().view('b').data)
    f.write(bytes(data_new))
    (total_data) += len(data_new)


# for j in range(5):
#     print(j)
for i in range(100):
    data = []
    for j in range(500):
        data.append(INTERNAL_MIC_PIN.value / 65536)
        time.sleep(0.001)
    temp_write([float_to_uint8(x, amplitude) for x in data])

f.close()

    

scipy_wavefile_write("example.wav", samplerate)