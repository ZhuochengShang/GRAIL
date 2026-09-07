"""Opt-in local multi-process quota admission for a future transport adapter.

No SDK imports or paid calls. Every transport attempt must reserve separately.
Reservations are charged even after failures; active leases require explicit
release, preventing silent over-admission when requests hang. SQLite file must
be shared by all clients of the same provider project/model on one machine.
"""
from dataclasses import dataclass
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import sqlite3
import time
import uuid
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Limits:
    enabled: bool = False
    rpm: int = 0
    input_tpm: int = 0
    rpd: int = 0
    max_inflight: int = 0


class Gate:
    def __init__(self, database, scope, limits):
        if not limits.enabled:
            raise ValueError('Next-protocol quota admission is disabled')
        if not scope or any(type(v) is not int or v <= 0 for v in
                            (limits.rpm, limits.input_tpm, limits.rpd, limits.max_inflight)):
            raise ValueError('Explicit positive project/model limits are required')
        self.path, self.scope, self.limits = Path(database), scope, limits
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, scope TEXT, started REAL, day TEXT, tokens INTEGER, active INTEGER, outcome TEXT)')
            db.execute('CREATE TABLE IF NOT EXISTS cooldown (scope TEXT PRIMARY KEY, until REAL)')
            db.execute('CREATE INDEX IF NOT EXISTS request_window ON requests(scope, started)')
            db.execute('CREATE TABLE IF NOT EXISTS policies (scope TEXT PRIMARY KEY, rpm INTEGER, tpm INTEGER, rpd INTEGER, inflight INTEGER)')
            values = (scope, limits.rpm, limits.input_tpm, limits.rpd, limits.max_inflight)
            db.execute('INSERT OR IGNORE INTO policies VALUES (?,?,?,?,?)', values)
            if db.execute('SELECT * FROM policies WHERE scope=?', (scope,)).fetchone() != values:
                raise ValueError('Conflicting limits for shared scope; migrate policies explicitly')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        try:
            with db:
                yield db
        finally:
            db.close()

    def reserve(self, input_tokens, now=None):
        if type(input_tokens) is not int or input_tokens < 0 or input_tokens > self.limits.input_tpm:
            raise ValueError('Request requires a valid input-token upper bound within the budget')
        now = time.time() if now is None else now
        day = datetime.fromtimestamp(now, ZoneInfo('America/Los_Angeles')).date().isoformat()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            cooldown = db.execute('SELECT until FROM cooldown WHERE scope=?', (self.scope,)).fetchone()
            if cooldown and cooldown[0] > now:
                return {'admitted': False, 'reason': 'shared_cooldown', 'retry_at': cooldown[0]}
            active = db.execute('SELECT count(*) FROM requests WHERE scope=? AND active=1', (self.scope,)).fetchone()[0]
            recent = db.execute('SELECT count(*),coalesce(sum(tokens),0),min(started) FROM requests WHERE scope=? AND started>?', (self.scope, now-60)).fetchone()
            daily = db.execute('SELECT count(*) FROM requests WHERE scope=? AND day=?', (self.scope, day)).fetchone()[0]
            reason = ('inflight' if active >= self.limits.max_inflight else
                      'rpm' if recent[0] >= self.limits.rpm else
                      'input_tpm' if recent[1]+input_tokens > self.limits.input_tpm else
                      'rpd' if daily >= self.limits.rpd else None)
            if reason:
                return {'admitted': False, 'reason': reason}
            request_id = uuid.uuid4().hex
            db.execute('INSERT INTO requests VALUES (?,?,?,?,?,1,NULL)', (request_id, self.scope, now, day, input_tokens))
            return {'admitted': True, 'request_id': request_id}

    def finish(self, request_id, outcome, actual_input_tokens=None):
        if actual_input_tokens is not None and (type(actual_input_tokens) is not int or actual_input_tokens < 0):
            raise ValueError('Invalid actual token usage')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT tokens,active FROM requests WHERE id=? AND scope=?', (request_id,self.scope)).fetchone()
            if row is None:
                raise ValueError('Unknown reservation')
            tokens = max(row[0], actual_input_tokens or 0)
            db.execute('UPDATE requests SET active=0,outcome=?,tokens=? WHERE id=?', (outcome,tokens,request_id))
            return {'input_bound_exceeded': actual_input_tokens is not None and actual_input_tokens > row[0]}

    def cooldown(self, seconds, now=None):
        if seconds < 0:
            raise ValueError('Negative cooldown')
        now = time.time() if now is None else now
        with self.connect() as db:
            db.execute('INSERT INTO cooldown VALUES (?,?) ON CONFLICT(scope) DO UPDATE SET until=max(until,excluded.until)', (self.scope,now+seconds))
