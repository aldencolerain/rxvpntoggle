from subprocess import call, check_output
from .settings import settings


def up():
    return call(f'pkexec wg-quick up {settings.values.get("interface")}', shell=True)

def down():
    return call(f'pkexec wg-quick down {settings.values.get("interface")}', shell=True)

# down, disconnected, connected, localized
def status():
    interface = settings.values.get('interface')
    expected = settings.values.get('expected')
    external = settings.values.get('external')
    internal = settings.values.get('internal')

    assert interface, 'Expected interface to be configured'
    assert expected, 'Expected interface to be configured'

    if call(f'ip link show | grep {interface}', shell=True) != 0:
        return 'down'
    ip = check_output('dig +short myip.opendns.com @resolver1.opendns.com', shell=True).decode("utf-8").strip()
    if ip != expected:
        return 'disconnected'
    if call(f'ping -c 1 {external}', shell=True) != 0:
        return 'disconnected'
    if not internal:
        return 'connected'
    if call(f'ping -c 1 {internal}', shell=True) != 0:
        return 'connected'
    return 'localized'
