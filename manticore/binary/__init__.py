''' Common binary formats interface
Ideally you should be able to do something like

        from binary import Binary
        binary = Binary(filename)
        assert cpu.machine == binary.arch, "Not matching cpu"
        logger.info("Loading %s as a %s elf"%(filename, binary.arch))
        for mm in binary.maps():
            cpu.mem.mmapFile( mm )
        for th in binary.threads():
            setup(th)

But there are difference between format that makes it difficult to find a simple
and common API.  interpreters? linkers? linked DLLs?

'''

from manticore.binary import Binary
from manticore.binary.binary import Binary, CGCElf, Elf


if __name__ == '__main__':
    import sys
    print(list(Binary(sys.argv[1]).threads()))
    print(list(Binary(sys.argv[1]).maps()))
