# zstandard package.
import zstd

from ._base import BaseCodec


class ZstdCodec(BaseCodec):

    Compressor = zstd.ZstdCompressor
    Decompressor = zstd.ZstdDecompressor

    def __init__(self, level=3, **kwargs):
        super(ZstdCodec, self).__init__(**kwargs)
        self.level = level

    def encode(self, data):
        compressor = self.Compressor(level=self.level)
        return compressor.compress(data)

    def decode(self, data):
        decompressor = self.Decompressor()
        return decompressor.decompress(data)
