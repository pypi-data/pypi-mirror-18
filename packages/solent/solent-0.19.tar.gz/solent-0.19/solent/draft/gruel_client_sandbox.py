#!/usr/bin/env python3
#
# gruel_client_sandbox
#
# // brief
# Draft terminal that can speak to a solent server. This is interesting
# because it shows use of the terminal in a nearcast context, as well as
# acting as a demonstration of a gruel client.
#
# // license
# Copyright 2016, Free Software Foundation.
#
# This file is part of Solent.
#
# Solent is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Solent is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Solent. If not, see <http://www.gnu.org/licenses/>.

from solent import SolentQuitException
from solent.eng import engine_new
from solent.eng import nearcast_schema_new
from solent.eng import nc_snoop_new
from solent.eng import orb_new
from solent.gruel import gruel_press_new
from solent.gruel import gruel_puff_new
from solent.gruel import gruel_schema_new
from solent.gruel import spin_gruel_client_new
from solent.log import init_logging
from solent.log import log
from solent.term import e_colpair
from solent.term import cgrid_new
from solent.util import line_finder_new

from collections import deque
from collections import OrderedDict as od
import random
import time
import traceback

# want this to work for people who do not have pygame installed
try:
    from solent.winterm import window_console_end as console_end
    from solent.winterm import window_console_start as console_start
except:
    from solent.term import curses_console_end as console_end
    from solent.term import curses_console_start as console_start

LCONSOLE_ADDR = '127.0.0.1'
LCONSOLE_PORT = 4091

TERM_LINK_ADDR = '127.0.0.1'
TERM_LINK_PORT = 4100

TAP_ADDR = '127.0.0.1'
TAP_PORT = 4101

EVENT_ADDR = '127.0.0.1'
EVENT_PORT = 4102

I_NEARCAST_SCHEMA = '''
    i message h
    i field h

    message def_console
        field console
    
    message gruel_connect
        field server_ip
        field server_port
        field password

    message keystroke
        field k

    message plot
        field drop
        field rest
        field c
        field colour
'''

class CogGruelClient:
    def __init__(self, cog_h, orb, engine):
        self.cog_h = cog_h
        self.orb = orb
        self.engine = engine
        #
        self.gruel_schema = gruel_schema_new()
        self.gruel_press = gruel_press_new(
            gruel_schema=self.gruel_schema,
            mtu=engine.mtu)
        self.gruel_puff = gruel_puff_new(
            gruel_schema=self.gruel_schema,
            mtu=engine.mtu)
        self.spin_gruel_client = spin_gruel_client_new(
            engine=engine,
            gruel_press=self.gruel_press,
            gruel_puff=self.gruel_puff)
    def close(self):
        self.engine.close_tcp_server(self.server_sid)
    def at_turn(self, activity):
        "Returns a boolean which is True only if there was activity."
        self.spin_gruel_client.at_turn(
            activity=activity)
    #
    def on_send_something(self, text):
        pass
    #
    def engine_on_tcp_connect(self, cs_tcp_connect):
        engine = cs_tcp_connect.engine
        client_sid = cs_tcp_connect.client_sid
        addr = cs_tcp_connect.addr
        port = cs_tcp_connect.port
        #
        log("connect/%s/%s/%s/%s"%(
            self.cog_h,
            client_sid,
            addr,
            port))
        engine.send(
            sid=client_sid,
            data='')
    def engine_on_tcp_condrop(self, cs_tcp_condrop):
        engine = cs_tcp_condrop.engine
        client_sid = cs_tcp_condrop.client_sid
        message = cs_tcp_condrop.message
        #
        log("condrop/%s/%s/%s"%(self.cog_h, client_sid, message))
        while self.q_received:
            self.q_received.pop()
    def engine_on_tcp_recv(self, cs_tcp_recv):
        engine = cs_tcp_recv.engine
        client_sid = cs_tcp_recv.client_sid
        data = cs_tcp_recv.data
        #
        self.q_received.append(data)
        engine.send(
            sid=client_sid,
            data='q_received %s\n'%len(data))

class CogTerminal:
    def __init__(self, cog_h, orb, engine):
        self.cog_h = cog_h
        self.orb = orb
        self.engine = engine
        #
        self.console = None
        self.cgrid = None
    #
    def at_turn(self, activity):
        k = self.console.async_getc()
        if k not in ('', None):
            activity.mark(
                l=self,
                s='key received')
            self.orb.nearcast(
                cog_h=self.cog_h,
                message_h='keystroke',
                k=k)
    def on_def_console(self, console):
        self.console = console
        self.cgrid = cgrid_new(
            width=console.width,
            height=console.height)
    def on_plot(self, drop, rest, c, colpair):
        self.cgrid.put(
            drop=drop,
            rest=rest,
            s=c,
            cpair=colpair)
        self.console.screen_update(
            cgrid=self.cgrid)

class CogPlotRandomness:
    def __init__(self, cog_h, orb, engine):
        self.cog_h = cog_h
        self.orb = orb
        self.engine = engine
        #
        self.t = time.time()
    def at_turn(self, activity):
        now = time.time()
        if now - 1 > self.t:
            activity.mark(
                l=self,
                s='sending a random char')
            self._send_a_random_char()
            self.t = now
    #
    def _send_a_random_char(self):
        drop = random.choice(range(25))
        rest = random.choice(range(80))
        c = chr(random.choice(range(ord('a'), ord('z')+1)))
        colpair = random.choice([e for e in e_colpair if not e.name.startswith('_')])
        self.orb.nearcast(
            cog_h=self.cog_h,
            message_h='plot',
            drop=drop,
            rest=rest,
            c=c,
            colour=colour)

class CogQuitScanner:
    # Looks out for a particular letter, and tells the app to quit when it
    # sees it.
    def __init__(self, cog_h, orb, engine):
        self.cog_h = cog_h
        self.orb = orb
        self.engine = engine
    def on_keystroke(self, k):
        log('k! %s'%k)
        if k == 'Q':
            raise SolentQuitException()

def wrap_eng(console):
    init_logging()
    engine = engine_new(
        mtu=1500)
    try:
        nearcast_schema = nearcast_schema_new(
            i_nearcast=I_NEARCAST_SCHEMA)
        snoop = nc_snoop_new(
            engine=engine,
            nearcast_schema=nearcast_schema,
            addr=TAP_ADDR,
            port=TAP_PORT)
        orb = engine.init_orb(
            nearcast_schema=nearcast_schema,
            snoop=snoop)
        #
        orb.init_cog(CogGruelClient)
        orb.init_cog(CogPlotRandomness)
        orb.init_cog(CogTerminal)
        orb.init_cog(CogQuitScanner)
        #
        orb.nearcast(
            cog_h='prep',
            message_h='def_console',
            console=console)
        #
        engine.event_loop()
    except KeyboardInterrupt:
        pass
    except:
        traceback.print_exc()
    finally:
        engine.close()

def main():
    try:
        console = console_start(
            width=80,
            height=25)
        #
        #
        # event loop
        wrap_eng(
            console=console)
    except SolentQuitException:
        pass
    except:
        traceback.print_exc()
    finally:
        console_end()

if __name__ == '__main__':
    main()

