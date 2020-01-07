class NGram:
    def __init__(self, order):
        self.order = order
        self.buffer = []

    def add(self, element):
        tmp = None
        if not element:
            return tmp

        if len(self.buffer) == self.order * 2:
            tmp = self.buffer.pop(0)

        if type(element) == list:
            self.buffer.append(element)
        else:
            self.buffer.append([element, 1])

        self.analyse()
        return tmp

    def analyse(self):
        tmp = [c[0] for c in self.buffer]
        if tmp[0:self.order] == tmp[self.order:]:
            for i in range(self.order):
                self.buffer[i][1] += self.buffer[i+self.order][1]
            self.buffer = self.buffer[0:self.order]

class Compressor:
    def __init__(self, level):
        self.level  = level
        self.ngrams = [ NGram(i) for i in range(1,level+1) ]
        self.final  = []

    def add(self, element):
        head, tail = (self.ngrams[0], self.ngrams[1:])
        out = head.add(element)

        for t in tail:
            out = t.add(out)

        if out:
            self.final.append(out)

    def flush(self):
        for i in range(len(self.ngrams)):
            current_buffer = self.ngrams[i].buffer
            for out in current_buffer:
                for u in range(i+1, len(self.ngrams)):
                    out = self.ngrams[u].add(out)
                if out:
                    self.final.append(out)

if __name__ == '__main__':
    import logging
    LOGGING_FORMAT = '[%(levelname)s] [%(asctime)s] %(funcName)s(): %(message)s'
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
    logger = logging.getLogger()

    t0 = [ 
        '0', '1', '2', '2', '2', '2', \
        '0', '1', '2', '2', '2', '2'
    ]
    comp = Compressor(5)

    logger.info('[+] Original buffer: {}'.format(t0))

    for c in t0:
        comp.add(c)
    comp.flush()

    logger.info('[+] Compressed list: {}'.format(comp.final))
    size_before = len(t0)
    size_after = len(comp.final)
    logger.info('[+] Compression rate: {:.2f}%'.format(100.0 - (size_after * 100 / size_before)))
