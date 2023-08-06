from os import read, pipe, close, dup, fork, waitpid
from threading import Thread
from queue import Queue, Empty
from sys import stderr
from subprocess import Popen, PIPE, TimeoutExpired
from binascii import unhexlify
from time import sleep

from dnc.utils import has_flag, filtered, net_ns, dup_close, drop_privileges, format_buffer
from dnc import start_pcap_parser, CaptureFlags, MAX_PACKET_SIZE, MAX_WAIT_RUNS


class ConsumerComponent(object):
    """ Base class for a pipeline consumers """
    def __init__(self, ip):
        self.ip = ip

    def consume(self, src, src_port, dst, dst_port, interface, seq, payload):
        raise NotImplementedError("Calling consume on: {}".format(self.__class__.__name__))

    def __call__(self, data):
        src_spec, dst_spec, interface, seq, payload = data.split(' ')
        src, src_port, dst, dst_port = src_spec.split(':') + dst_spec.split(':')
        self.consume(src, src_port, dst, dst_port, interface, seq, payload)


class JsonConsumer(ConsumerComponent):
    """ Returns a buffered list of JSON objects """
    def __init__(self, ip):
        super().__init__(ip)
        self.buffered = []

    def consume(self, src, src_port, dst, dst_port, interface, seq, payload):
        obj = {
            'interface': interface,
            'src': src,
            'src_port': src_port,
            'dst': dst,
            'dst_port': dst_port,
            'payload': payload
        }

        if seq == '-':
            obj['type'] = 'udp'
        else:
            obj['type'] = 'tcp'
            acknum, seqnum = seq.split('-')
            obj['acknum'] = acknum
            obj['seqnum'] = seqnum

        self.buffered.append(obj)


class StdoutConsumer(ConsumerComponent):
    """ Prints the packet information to the stdout """
    def consume(self, src, src_port, dst, dst_port, interface, seq, payload):
        if src == self.ip:
            print('OUT: {}:{} ({})'.format(dst, dst_port, seq))
        elif dst == self.ip:
            print('IN:  {}:{} ({})'.format(src, src_port, seq))
        elif dst == src == '127.0.0.1':
            print('LOCALHOST {}-{} ({})'.format(src_port, dst_port, seq))

        if payload:
            print(format_buffer(unhexlify(payload)))


class ProducerComponent(object):
    """ Base class for a `tcpdump` pipeline component functor """
    def __init__(self, capture, context=None):
        self.capture = capture
        self.pipeline = None
        self.rx = None
        self.child = None
        self.child_parser = None

    def _run_pcap_parser(self, rx_tcpdump, interface):
        rx, tx = pipe()
        # dupe pids for the child process
        tcpdump, out = dup(rx_tcpdump), dup(tx)
        close(tx)
        close(rx_tcpdump)
        pid = fork()
        if pid:
            close(out)
            close(tcpdump)
            self.child_parser = pid
            self.rx = rx
        else:
            # get rid of unnecessary privileges
            drop_privileges()
            # start parsing packets
            start_pcap_parser(tcpdump, out, interface)

    def _init_tcpdump(self, interface, address=None, flags=CaptureFlags.Ingress):
        """ Initialize `tcpdump` and set child process info and the `read` pipe of the process"""
        direction, proto = [], None
        if address:
            proto = "ether"
            if has_flag(flags, CaptureFlags.Ingress):
                direction += ["dst"]
            if has_flag(flags, CaptureFlags.Both):
                direction += ["or"]
            if has_flag(flags, CaptureFlags.Egress):
                direction += ["src"]

        args = filtered(["tcpdump", "-i", interface, "-w-", "-U", proto] + direction + [address])
        rx, tx = pipe()

        # pipes are not inheritable by children processes, so we need
        # to duplicate the tx pipe, then close it
        with dup_close(tx) as (write2,):
            self.child = Popen(args, stdin=PIPE, stdout=write2, stderr=PIPE)

        self._run_pcap_parser(rx, interface)

    def init_tcpdump(self):
        """ Subclasses override this with specific way how to call `_init_tcpdump` """
        raise NotImplementedError()

    def __call__(self):
        """ Starts reading from the `read` pipe as long as the pipeline is running """
        self.init_tcpdump()

        buffered = ''

        while self.pipeline.running:
            # probe the tcpdump process
            try:
                code = self.child.wait(0)
                if code == 1:
                    print('[!] Tcpdump execution **failed**, are you a superuser?', file=stderr)
                return
            except TimeoutExpired:
                pass

            # read data from the pipe
            data = read(self.rx, MAX_PACKET_SIZE)
            if not data:
                continue

            data = data.decode('utf-8')
            packets = data.splitlines()
            if buffered:
                # We already have some data buffered so merge the data with the contents
                # of the first packet and empty the buffer
                packets[0] = buffered + packets[0]
                buffered = ''

            if not data.endswith('\n'):
                # If the data doesn't end with a new line then we're in a middle
                # of a packet, so we put the last element into a buffer and remove it
                # from the packets list
                buffered = packets[-1]
                packets.pop()

            # enqueue each entry
            if self.pipeline.queue:
                for p in packets:
                    self.pipeline.queue.put(p)

        # reap what we have sown
        waitpid(self.child_parser, 0)


class InterfaceProducer(ProducerComponent):
    """ Subclass to capture on a specific interface and address """
    def __init__(self, bridge, mac, capture):
        super().__init__(capture)
        self.bridge = bridge
        self.mac = mac

    def init_tcpdump(self):
        self._init_tcpdump(self.bridge, self.mac, self.capture)


class LoopbackProducer(ProducerComponent):
    """ Subclass to capture on the namespaced local loopback """
    def __init__(self, pid, capture):
        super().__init__(capture)
        self.pid = pid

    def init_tcpdump(self):
        net_ns(self.pid)
        self._init_tcpdump("lo", flags=self.capture)


class PipelineError(Exception):
    pass


class Pipeline(object):
    """ Provides simple interface for running multiple producers and consumers and synchronizing them via queue """
    def __init__(self, **kwargs):
        self.producers = []
        self.queue = Queue()
        self.consumers = []
        self.running = False
        self.context = kwargs

    def add_producer(self, target):
        """ Adds a new producers, an error is thrown if the pipeline is already running """
        if not self.running:
            target.pipeline = self
            self.producers.append(target)
        else:
            raise PipelineError("Pipeline already running")

    def add_consumer(self, target):
        """ Adds a new consumer target """
        self.consumers.append(target)

    def run(self):
        """ Start running the pipeline """
        self.running = True

        threads = []
        for p in self.producers:
            threads.append(Thread(target=p))
            threads[-1].start()

        runs = 0
        while runs < MAX_WAIT_RUNS:
            sleep(1)
            # make sure that the we already have the read pipe
            # of the producer
            if all(p.rx is not None for p in self.producers):
                break
            runs += 1

        if runs != MAX_WAIT_RUNS:
            # tcpdump processes have been started, so we can drop root from
            # the main process as well
            drop_privileges()
        else:
            raise PipelineError("Couldn't attach to tcpdump data producers")

        while any(t.is_alive() for t in threads):
            try:
                data = self.queue.get()
                for c in self.consumers:
                    c(data)
                self.queue.task_done()
            except Empty:
                pass
