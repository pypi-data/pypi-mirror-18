#!/usr/bin/env python
#    This file is part of pyrsp

#    pyrsp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pyrsp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pyrsp  If not, see <http://www.gnu.org/licenses/>.

# (C) 2014 by Stefan Marsiske, <s@ctrlc.hu>

import os, time, sys, struct, socket
activate_this = os.path.dirname(__file__)+'/../env/bin/activate_this.py'
if os.path.exists(activate_this):
    execfile(activate_this, dict(__file__=activate_this))

import serial
from pyrsp.utils import hexdump, pack, unpack, unhex, switch_endian, split_by_n
from pyrsp.elf import ELF
from binascii import hexlify

def Debugger(*args, **kwargs):
    if os.path.exists(args[0]):
        return BlackMagic(*args,**kwargs)
    try:
        int(args[0])
    except:
        print "cannot access", args[0]
        sys.exit(0)
    return STlink2(*args, **kwargs)

class BlackMagic(object):
    def __init__(self, port):
        self.__dict__['port'] = serial.Serial(port, 115200, timeout=1)

    def setup(self, rsp):
        rsp.send('qRcmd,737764705f7363616e')
        pkt=rsp.readpkt()
        while pkt!='OK':
            if pkt[0]!='O':
                raise ValueError('not O: %s' % pkt)
            if rsp.verbose:
                print unhex(pkt[1:-1])
            pkt=rsp.readpkt()
        rsp.fetchOK('vAttach;1','T05')

    def write(self, data):
        return self.port.write(data)

    def read(self, size=1):
        return self.port.read(size)

    def close(self, rsp):
        rsp.fetchOK('D')
        self.port.close()

class STlink2(object):
    def __init__(self, port):
        self.__dict__['port'] = socket.socket( socket.AF_INET,socket.SOCK_STREAM)
        self.port.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port.settimeout(1)
        self.port.connect(('localhost',int(port)))

    def setup(self, rsp):
        pass

    def write(self, data):
        i = 0
        while(i<len(data)):
            i += self.port.send(data[i:])
        return i

    def read(self):
        try:
            return self.port.recv(1)
        except:
            return ''

    def close(self):
        self.port.close()

class RSP(object):
    def __init__(self, port, elffile=None, verbose=False):
        """ read the elf file if given by elffile, connects to the
            debugging device specified by port, and initializes itself.
        """
        self.registers = self.arch['regs']
        self.__dict__['br'] = {}
        self.__dict__['verbose'] = verbose
        # open serial connection
        self.__dict__['port'] = Debugger(port) #serial.Serial(port, 115200, timeout=1)
        # parse elf for symbol table, entry point and work area
        self.__dict__['elf'] = ELF(elffile) if elffile else None
        if verbose and self.elf:
            print "work area: 0x%x" % self.elf.workarea
            print "entry: 0x%x" % self.elf.entry

        # check for signal from running target
        tmp = self.readpkt(timeout=1)
        if tmp: print 'helo', tmp

        self.port.write(pack('+'))

        tmp = self.readpkt(timeout=1)
        if tmp: print 'helo', tmp

        self.send('qSupported')
        #self.port.write(pack('qSupported:multiprocess+;qRelocInsn+'))
        feats = self.readpkt()
        if feats:
            self.feats = dict((ass.split('=') if '=' in ass else (ass,None) for ass in feats.split(';')))

        # attach
        self.connect()

    def connect(self):
        pass

    def send(self, data, retries=50):
        """ sends data via the RSP protocol to the device """
        self.port.write(pack(data))
        res = None
        while not res:
            res = self.port.read()
        discards = []
        while res!='+' and retries>0:
            discards.append(res)
            retries-=1
            res = self.port.read()
        if len(discards)>0 and self.verbose: print 'send discards', discards
        if retries==0:
            raise ValueError("retry fail")
        #print 'sent', data

    def readpkt(self, timeout=0):
        """ blocks until it reads an RSP packet, and returns it's
            data"""
        c=None
        discards=[]
        if timeout>0:
            start = time.time()
        while(c!='$'):
            if c: discards.append(c)
            c=self.port.read()
            if timeout>0 and start+timeout < time.time():
                return
        if len(discards)>0 and self.verbose: print 'discards', discards
        res=[c]

        while True:
            res.append(self.port.read())
            if res[-1]=='#' and res[-2]!="'":
                res.append(self.port.read())
                res.append(self.port.read())
                try:
                    res=unpack(''.join(res))
                except:
                    self.port.write('-')
                    res=[]
                    continue
                self.port.write('+')
                #print "read", res
                return res

    def store(self, data, addr=None):
        """ stores data at addr if given otherwise at beginning of
            .text segment aka self.elf.workarea"""
        if addr==None:
            addr=self.elf.workarea
        for pkt in split_by_n(hexlify(data), int(self.feats['PacketSize'],16) - 20):
            pktlen = len(pkt)/2
            self.fetchOK('M%x,%x:%s' % (addr, pktlen, pkt))
            addr+=pktlen

    def __getslice__(self, i, j):
        return self.dump(j-i,i)

    def __setitem__(self, i,val):
        self.store(val,i)

    def _get_feats(self):
        self.port.write(pack('+'))

        tmp = self.readpkt(timeout=1)
        if tmp: print 'helo', tmp

        self.send('qSupported')
        feats = self.readpkt()
        if feats:
            self.feats = dict((ass.split('=') if '=' in ass else (ass,None) for ass in feats.split(';')))

    def __getattr__(self, name):
        if name not in self.__dict__ or not self.__dict__[name]:
            if name in self.regs.keys():
                return self.regs[name]
        if name in self.__dict__.keys():
            return self.__dict__[name]
        else:
            if name=='feats':
                self._get_feats()
                return self.__dict__[name]
            raise AttributeError, name

    def dump(self, size, addr = None):
        """ dumps data from addr if given otherwise at beginning of
            .text segment aka self.elf.workarea"""
        if addr==None:
            addr=self.elf.workarea
        rd = []
        i=0
        bsize = int(self.feats['PacketSize'], 16) / 2
        while(i<size):
            bsize = bsize if i+bsize<size else size - i
            #print 'm%x,%x' % (addr+i, bsize)
            self.send('m%x,%x' % (addr+i, bsize))
            pkt=self.readpkt()
            rd.append(unhex(pkt))
            i+=bsize
            #print i, size, 'pkt', pkt
        return ''.join(rd)

    def fetch(self,data):
        """ sends data and returns reply """
        self.send(data)
        return self.readpkt()

    def fetchOK(self,data,ok='OK'):
        """ sends data and expects success """
        res = self.fetch(data)
        if res!=ok: raise ValueError(res)

    def set_reg(self, reg, val):
        """ sets value of register reg to val on device """
        if isinstance(val, str):
            self.regs[reg]=val
        if isinstance(val, int):
            self.regs[reg]='%x' % val
        self.fetchOK("G%s" % ''.join([switch_endian(self.regs[r]) for r in self.registers if r in self.regs]))

    def refresh_regs(self):
        """ loads and caches values of the registers on the device """
        self.send('g')
        if self.arch['endian']:
            self.regs=dict(zip(self.registers,(switch_endian(reg) for reg in split_by_n(self.readpkt(),self.arch['bitsize']>>2))))
        else:
            self.regs=dict(zip(self.registers,split_by_n(self.readpkt(),self.arch['bitsize']>>2)))

    def dump_regs(self):
        """ refreshes and dumps registers via stdout """
        self.refresh_regs()
        print ' '.join(["%s:%s" % (r, self.regs.get(r)) for r in self.registers])

    prev_regs={}
    def lazy_dump_regs(self):
        """ refreshes and dumps registers via stdout """
        self.refresh_regs()
        print '[r]', ' '.join(["%s:%s" % (r, self.regs.get(r)) for r in self.registers if self.regs.get(r)!=self.prev_regs.get(r)])
        self.prev_regs=self.regs

    def get_thread_info(self):
        tid = None
        tmp = self.fetch('qC')
        if tmp.startswith("QC"):
            tid=tmp[2:].strip()
        extra = unhex(self.fetch('qThreadExtraInfo,%s' % tid))
        tids = []
        tmp = self.fetch('qfThreadInfo')
        while tmp != 'l':
            if not tmp.startswith('m'):
                raise ValueError('invalid qThreadInfo response')
            tids.extend(tmp[1:].split(','))
            tmp = self.fetch('qsThreadInfo')
        return (tid, extra, tids)

    def run(self, start=None):
        """ sets pc to start if given or to entry address from elf header,
            passes control to the device and handles breakpoints
        """
        if not start:
            entry = "%08x" % self.elf.entry
        else:
            entry = "%08x" % (self.elf.symbols[start] & ~1)
        if self.verbose: print "set new pc: @test (0x%s)" % entry,
        self.set_reg('pc', entry)
        if self.verbose: print 'OK'

        if self.verbose: print "continuing"
        sig = self.fetch('c')
        while sig in ['T05', 'S05']:
            self.handle_br()
            sig = self.fetch('c')

        if sig!='T0B': print 'strange signal', sig
        if hasattr(self, 'checkfault'):
            self.checkfault()
        else:
            src_line = self.get_src_line(int(self.regs['pc'],16 - 1))
            if src_line:
                print "0 %s:%s %s" % (src_line['file'], src_line['lineno'], src_line['line'])
            else:
                print 'pc', self.regs['pc']
            src_line = self.get_src_line(int(self.regs['lr'],16) -3)
            if src_line:
                print "1 %s:%s %s" % (src_line['file'], src_line['lineno'], src_line['line'])
            else:
                print 'lr', self.regs['lr']
            self.dump_regs()

        res = None
        while not res:
            res = self.port.read()
        discards = []
        retries = 20
        while res!='+' and retries>0:
            discards.append(res)
            retries-=1
            res = self.port.read()
        if len(discards)>0 and self.verbose: print 'send discards', discards

        self.port.close(self)
        sys.exit(0)

    def handle_br(self):
        """ dumps register on breakpoint/signal, continues if unknown,
            otherwise it calls the appropriate callback.
        """
        print
        self.dump_regs()
        if not self.regs['pc'] in self.br:
            print "unknown break point passed"
            self.dump_regs()
            return
        if self.verbose:
            print 'breakpoint hit:', self.br[self.regs['pc']]['sym']
        self.br[self.regs['pc']]['cb']()

    def set_br(self, sym, cb, quiet=False):
        """ sets a breakpoint at symbol sym, and install callback cb
            for it
        """
        addr = self.elf.symbols.get(sym)
        if not addr:
            print "unknown symbol: %s, ignoring request to set br" % sym
            return
        addr = "%08x" % (addr & ~1)
        if addr in self.br:
            print "warn: overwriting breakpoint at %s" % sym
            self.br[addr]={'sym': sym,
                           'cb': cb,
                           'old': self.br[addr]['old']}
        else:
            self.br[addr]={'sym': sym,
                           'cb': cb,
                           'old': unhex(self.fetch('m%s,2' % addr))}
        #self.fetch('Z0,%s,2' % addr)
        tmp = self.fetch('X%s,2:\xbe\xbe' % addr)
        if self.verbose and not quiet:
            print "set break: @%s (0x%s)" % (sym, addr), tmp

    def del_br(self, addr, quiet=False):
        """ deletes breakpoint at address addr """
        sym = self.br[addr]['sym']
        #self.fetch('z0,%s,2' % addr)
        if 'old' in self.br[addr]:
            tmp = self.fetch('X%s,2:%s' % (addr, self.br[addr]['old']))
            if self.verbose and not quiet: print "clear breakpoint: @%s (0x%s)" % (sym, addr), tmp
        else:
            tmp = self.fetch('Z0,%s,2' % addr)
            if tmp!= 'OK':
                print "failed to clear break: @%s (0x%s)" % ('FaultHandler', addr), tmp
            elif self.verbose and not quiet:
                print "clear break: @%s (0x%s)" % ('FaultHandler', addr), tmp

        del self.br[addr]

    def finish_cb(self):
        """ final breakpoint, if hit it deletes all breakpoints,
            continues running the cpu, and detaches from the debugging
            device
        """
        # clear all breaks
        for br in self.br.keys()[:]:
            self.del_br(br)
        if self.verbose:
            print "continuing and detaching"
        # leave in running state
        self.send('c')
        sys.exit(0)

    def get_src_line(self, addr):
        """ returns the source-code line associated with address addr
        """
        i = 0
        src_line = None
        while not src_line and i<1023:
            src_line = self.elf.src_map.get("%08x" % (addr - i))
            i+=2
        return src_line

    def step_over_br(self):
        sym = self.br[self.regs['pc']]['sym']
        cb  = self.br[self.regs['pc']]['cb']
        self.del_br(self.regs['pc'], quiet=True)
        sig = self.fetch('s')
        if sig in ['T05', 'T0B']:
            self.set_br(sym, cb, quiet=True)
        else:
            print 'strange signal while stepi over br, abort'
            sys.exit(1)

    def dump_cb(self):
        """ rsp_dump callback, hit if rsp_dump is called. Outputs to
            stdout the source line, and a hexdump of the memory
            pointed by $r0 with a size of $r1 bytes. Then it resumes
            running.
        """
        src_line = self.get_src_line(int(self.regs['lr'],16) - 3)
        if src_line:
            print "%s:%s %s" % (src_line['file'], src_line['lineno'], src_line['line'])

        res_size = int(self.regs['r1'],16)
        if res_size <= 2048: # for sanity
            ptr = int(self.regs['r0'],16)
            res = unhex(self.fetch('m%x,%x' % (ptr, res_size)))
            print hexdump(res, ptr)

        self.step_over_br()

    def load(self, verify):
        """ loads binary belonging to elf to beginning of .text
            segment (alias self.elf.workarea), and if verify is set read
            it back and check if it matches with the uploaded binary.
        """
        if self.verbose: print 'load %s' % self.elf.name
        buf = self.elf.get_bin()
        self.store(buf)

        if verify:
            if self.verbose: print "verify test",
            if not self.dump(len(buf)) == buf:
                raise ValueError("uploaded binary failed to verify")
            if self.verbose: print 'OK'

    def call(self, start=None, finish='rsp_finish', dump='rsp_dump', verify=True):
        """
        1. Loads the '.bin' file given by self.elf into the device
           at the workarea (.text seg) of the device.
        2. Using the '.elf' file it sets a breakpoint on the function
           specified by rsp_finish and rsp_dump,
        3. and starts execution at the function specified by start or elf e_entry.
        4. After the breakpoint of rsp_dump is hit, r1 bytes are dumped
           from the buffer pointed to by r0.
        5. After the breakpoint of rsp_finish is hit, it removes all
           break points, and detaches
        """

        self.refresh_regs()
        self.load(verify)
        self.set_br(finish, self.finish_cb)
        self.set_br('rsp_detach', self.finish_cb)
        self.set_br(dump, self.dump_cb)
        self.run(start)

    def test(self):
        # show current regs
        self.dump_regs()

        # test write
        self.fetchOK('X%08x,0' % self.elf.workarea)

        # reset workspace area
        self.store('\x00' * 2048)

        # verify workspace area empty
        if self.dump(2048) != '\x00' * 2048:
            raise ValueError('cannot erase work area')

from cortexhwregs import *
class CortexM3(RSP):
    def __init__(self, *args,**kwargs):

        self.arch = {'regs': ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8",
                              "r9", "r10", "r11", "r12", "sp", "lr", "pc",
                              "xpsr", "msp", "psp", "special"],
                     'endian': True,
                     'bitsize': 32}
        super(CortexM3,self).__init__(*args, **kwargs)

    def get_thread_info(self):
        return

    def getreg(self,size,ptr):
        tmp = self.fetch('m%x,%x' % (ptr, size))
        return unhex(switch_endian(tmp))

    def printreg(self, reg):
        return [n if type(v)==bool and v==True else (n,v if n!='ADDR' else hex(v<<5)) for n,v in reg.items() if v]

    def dump_mpu(self):
        print 'mpu_cr', self.printreg(mpu_cr.parse(self.getreg(4, MPU_CR)))
        for region in xrange(8):
            self.store(struct.pack("<I", region), MPU_RNR)
            print region,
            print self.printreg(mpu_rbar.parse(self.getreg(4, MPU_RBAR))),
            print self.printreg(mpu_rasr.parse(self.getreg(4, MPU_RASR)))

    def checkfault(self):
        # impl check, only dumps now.
        #sig = self.fetch('s')
        #print 'sig', sig
        self.dump_mpu()
        print 'hfsr=', self.printreg(scb_hfsr.parse(self.getreg(4, SCB_HFSR)))
        print 'icsr=', self.printreg(scb_icsr.parse(self.getreg(4, SCB_ICSR)))
        print 'shcsr=', self.printreg(scb_shcsr.parse(self.getreg(4, SCB_SHCSR)))
        print 'cfsr=', self.printreg(scb_cfsr.parse(self.getreg(4, SCB_CFSR)))
        print 'MMFAR=', hex(struct.unpack(">I", self.getreg(4, SCB_MMFAR))[0])
        print 'BFAR=', hex(struct.unpack(">I", self.getreg(4, SCB_BFAR))[0])
        print
        src_line = self.get_src_line(struct.unpack(">I", self.getreg(4, int(self.regs['sp'],16) + 24))[0])
        if src_line:
            print "%s:%s %s" % (src_line['file'], src_line['lineno'], src_line['line'])
        else:
            print 'sp', format(struct.unpack(">I", self.getreg(4, int(self.regs['sp'],16) + 24))[0], '08x')

        self.port.close(self)
        sys.exit(0)

    def connect(self):
        """ attaches to blackmagic jtag debugger in swd mode """
        # ignore redundant stuff
        tmp = self.readpkt(timeout=1)
        while(tmp):
            tmp = self.readpkt(timeout=1)
        # enable extended mode
        self.fetchOK('!')

        # setup registers TODO
        # registers should be parsed from the output of, see target.xml
        #print self.fetch('qXfer:features:read:target.xml:0,3fb')
        #print self.fetch('Xfer:features:read:target.xml:3cf,3fb')
        #print self.fetch('qXfer:memory-map:read::0,3fb')
        #print self.fetch('qXfer:memory-map:read::364,3fb')

        self.port.setup(self)

        addr=struct.unpack(">I", self.getreg(4, 0x0800000c))[0] - 1
        self.br[format(addr, '08x')]={'sym': "FaultHandler",
                             'cb': self.checkfault}
        tmp = self.fetch('Z1,%s,2' % format(addr, 'x'))
        if tmp== 'OK':
            print "set break: @%s (0x%s)" % ('FaultHandler', format(addr, 'x')), tmp
            return

        # vector_catch enable hard int bus stat chk nocp mm reset
        self.send('qRcmd,766563746f725f636174636820656e61626c65206861726420696e742062757320737461742063686b206e6f6370206d6d207265736574')
        pkt=self.readpkt()
        while pkt!='OK':
            if pkt[0]!='O':
                raise ValueError('not O: %s' % pkt)
            if self.verbose:
                print unhex(pkt[1:-1])
            pkt=self.readpkt()

class AMD64(RSP):
    def __init__(self, *args,**kwargs):
        self.arch = {'regs': ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
                              "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",
                              "rip", "eflags", "cs", "ss", "ds", "es", "fs", "gs",
                              "st0", "st1", "st2", "st3", "st4", "st5", "st6", "st7",
                              "fctrl", "fstat", "ftag", "fiseg", "fioff", "foseg", "fooff", "fop",
                              "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7",
                              "xmm8", "xmm9", "xmm10", "xmm11", "xmm12", "xmm13", "xmm14", "xmm15",
                              "mxcsr",],
                     'endian': False,
                     'bitsize': 64}
        super(AMD64,self).__init__(*args, **kwargs)

class i386(RSP):
    # TODO gdb sends qSupported:multiprocess+;xmlRegisters=i386;qRelocInsn+
    def __init__(self, *args,**kwargs):
        self.arch = {'regs': ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi",
                             "eip", "eflags", "cs", "ss", "ds", "es", "fs", "gs",
                             "st0", "st1", "st2", "st3", "st4", "st5", "st6", "st7",
                             "fctrl", "fstat", "ftag", "fiseg", "fioff", "foseg", "fooff", "fop",
                             "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7",
                             "mxcsr"],
                    'endian': False,
                    'bitsize': 32}
        super(i386,self).__init__(*args, **kwargs)

archmap={'amd64': AMD64, "i386": i386, "cortexm3": CortexM3}

def main():
    # parse arch from cmdline
    arch=i386
    for i, arg in enumerate(sys.argv):
        if arg in archmap:
            arch=archmap[arg]
            del sys.argv[i]
            break
    # argv[1] should be the file to the debugger device, e.g: /dev/ttyACM0
    # argv[2] can be the elf file
    if len(sys.argv)<2:
        print "%s [<%s>] <serial interface> [<elf file>]" % (sys.argv[0],
                                                             '|'.join(archmap.keys()))
        sys.exit(1)

    elffile=sys.argv[2] if len(sys.argv)>2 else None

    rsp = arch(sys.argv[1], elffile, verbose=False)

    if elffile:
        try:
            rsp.call()
        except KeyboardInterrupt:
            import traceback
            traceback.print_exc()

            res = None
            while not res:
                res = rsp.port.read()
            discards = []
            retries = 20
            while res!='+' and retries>0:
                discards.append(res)
                retries-=1
                res = rsp.port.read()
            if len(discards)>0 and rsp.verbose: print 'send discards', discards

            rsp.port.close(rsp)
            sys.exit(1)
    else:
        print hexdump(rsp.dump(2048, 0),0)
        rsp.dump_regs()
        print rsp.get_thread_info()
        rsp.send('c')
    rsp.port.close(rsp)

if __name__ == "__main__":
    main()
