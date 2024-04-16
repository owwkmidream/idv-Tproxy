import asyncio
import logging
import signal
import sys

from mitmproxy import options
from mitmproxy.tools import cmdline
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.utils import arg_check
from mitmproxy.utils import debug


def run(args=None, callback=None) -> DumpMaster:
    arguments = [*args]

    async def main() -> DumpMaster:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("tornado").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("hpack").setLevel(logging.WARNING)
        logging.getLogger("quic").setLevel(
            logging.WARNING
        )  # aioquic uses a different prefix...
        debug.register_info_dumpers()

        opts = options.Options()
        the_master = DumpMaster(opts, with_termlog=False, with_dumper=False)
        callback(the_master)
        parser = cmdline.mitmdump(opts)

        try:
            args = parser.parse_args(arguments)
        except SystemExit:
            arg_check.check()
            sys.exit(1)

        adict = {
            key: val for key, val in vars(args).items() if key in opts and val is not None
        }
        opts.update(**adict)

        loop = asyncio.get_running_loop()

        def _sigint(*_):
            loop.call_soon_threadsafe(
                getattr(the_master, "prompt_for_exit", the_master.shutdown)
            )

        def _sigterm(*_):
            loop.call_soon_threadsafe(the_master.shutdown)

        signal.signal(signal.SIGINT, _sigint)
        signal.signal(signal.SIGTERM, _sigterm)

        await the_master.run()
        return the_master

    return asyncio.run(main())
