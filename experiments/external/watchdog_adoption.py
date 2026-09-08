"""Observe surviving jobs after supervisor death; never signal adopted processes."""
from __future__ import annotations

import subprocess


def process_table():
    proc = subprocess.run(['ps', '-axo', 'pid,ppid,lstart,etime,state,command'],
                          text=True, capture_output=True, check=True)
    rows = {}
    for line in proc.stdout.splitlines()[1:]:
        fields = line.split(None, 9)
        if len(fields) == 10:
            pid, ppid, *rest = fields
            rows[int(pid)] = {'pid': int(pid), 'ppid': int(ppid),
                'started': ' '.join(rest[:5]), 'state': rest[6], 'command': rest[7]}
    return rows


def identity(row):
    return {k: row[k] for k in ('pid', 'started', 'command')}


class AdoptedProcess:
    """Popen-like observer. Unknown exit is failure, never fabricated success.

    Descendants are tracked even when they create separate sessions. Persist
    identities each poll so another supervisor crash cannot release live work.
    An unreadable process table raises rather than authorizing duplicate work.
    """
    adopted = True

    def __init__(self, pid, tracked):
        self.pid, self.tracked, self.returncode = pid, tracked, None

    def poll(self):
        table = process_table()
        live = {pid for pid, row in table.items() if not row['state'].startswith('Z')
                and identity(row) in self.tracked}
        while True:
            descendants = {pid for pid, row in table.items() if row['ppid'] in live
                           and not row['state'].startswith('Z')}
            if descendants <= live:
                break
            live |= descendants
        self.tracked = [identity(table[pid]) for pid in sorted(live)]
        self.returncode = None if live else 255
        return self.returncode


def adopt(row, command):
    pid = row.get('pid')
    if not pid:
        return None
    tracked = row.get('adopted_processes', [])
    if not tracked:
        current = process_table().get(pid)
        if current is None or current['state'].startswith('Z'):
            return None
        if current['command'] != ' '.join(command):
            raise RuntimeError(f'PID {pid} identity differs from saved job; inspect before resuming')
        tracked = [identity(current)]
    proc = AdoptedProcess(pid, tracked)
    return proc if proc.poll() is None else None
