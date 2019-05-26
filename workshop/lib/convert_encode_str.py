#!/usr/bin/env python3


CODING_STYLES = ["ASCII", "shift-jis", "utf-8", "cp932"]


class AdminEncoding(object):
    def __init__(self, before_code="shift-jis",
                 after_encode="utf-8"):
        if before_code not in CODING_STYLES:
            emes = "before_code doesn't include {}:"
            emes = emes.format(CODING_STYLES)
            raise TypeError(emes)
        if after_encode not in CODING_STYLES:
            emes = "after_encode doesn't include {}:"
            emes = emes.format(CODING_STYLES)
            raise TypeError(emes)
        self.before_code = before_code
        self.after_encode = after_encode

    def convert_strdata(self, strdata):
        if type(strdata) != str:
            raise TypeError("")
        byte_data = strdata.encode(self.before_code)
        str_data_converted = byte_data.decode(self.after_encode)
        return str_data_converted

    def __call__(self, line):
        return self.convert_strdata(line)

    def file_convert(self, before_file, after_file):
        with open(before_file, "r",
                  encoding=self.before_code) as read:
            strdata = read.read()
        byte_data = strdata.decode()
        new_decode_data = byte_data.decode(self.after_encode)
        with open(after_file, "w") as write:
            write.write(new_decode_data)

    def _gene_encode_decode_pipe(self, before_file, after_file):
        self.tmp_read_pipe = open(before_file, "r")
        self.tmp_write_pipe = open(after_file, "w")
        for line in self.tmp_read_pipe:
            wline = self.convert_strdata(line)
            self.tmp_write_pipe.write(wline)
            yield

    def set_encode_decode_pipe(self, before_file, after_file):
        self.endecode_pipe = self._gene_encode_decode_pipe(
                                                    before_file,
                                                    after_file)

    def cosume_pipe(self):
        list(self.endecode_pipe)
