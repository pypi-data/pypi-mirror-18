from __future__ import print_function

import sys
import xml.sax
import json

from cpe import CPE

def emit_mismatch(**kwargs):
    out = {}
    for k, v in kwargs.items():
        out[k] = {}
        out[k]['value'] = v.cpe_str
        out[k]['fs'] = v.as_fs()
        out[k]['uri'] = v.as_uri_2_3()
        out[k]['wfn'] = v.as_wfn()
    print(json.dumps(out))


class ABContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if name == "cpe-item":
            value = attrs.getValue("name")
            try:
                self.current_cpe_uri = CPE(value)
            except Exception as err:
                print(err, value)
        elif name == "cpe-23:cpe23-item":
            value = attrs.getValue("name")
            try:
                self.current_cpe_fs = CPE(value)
            except Exception as err:
                print(err, value)
            if self.current_cpe_uri is not None and \
               self.current_cpe_fs is not None:
                if self.current_cpe_fs != self.current_cpe_uri:
                    emit_mismatch(a=self.current_cpe_uri, b=self.current_cpe_fs)


def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, ABContentHandler())


if __name__ == "__main__":
    main(sys.argv[1])
