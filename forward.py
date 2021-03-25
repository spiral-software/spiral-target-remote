
import paramiko as pmk
import argparse
import os
import sys

parser = argparse.ArgumentParser(prog='forwarder')

parser.add_argument('-r', '--request', dest='request', default=None)
parser.add_argument('-t', '--target',  dest='target',  default=None)
parser.add_argument('-H', '--hostname', dest='hostname', default=None)
parser.add_argument('-u', '--username', dest='username', default=None)
parser.add_argument('-p', '--password', dest='password', default=None)

args = vars(parser.parse_args(sys.argv[1:]))

log = open('trace.txt', 'w')
log.write(' '.join(sys.argv) + '\n')

request = args.get('request', None)
target  = args.get('target', None)

hostname = args.get('hostname', 'hostname')
username = args.get('username', 'username')
password = args.get('password', 'password')

profcmd = 'spiralprofiler -d .'
if request:
    profcmd = profcmd + ' -r ' + request
    
if target:
    profcmd = profcmd + ' -t ' + target
    
log.write(profcmd + '\n')

tdir = 'proftmp' + str(os.getpid())

cmd1 = 'rm -rf ' + tdir + '; mkdir ' + tdir
cmd2 = '. ~/.profile; cd ' + tdir + '; ' + profcmd
cmd3 = 'rm -rf ' + tdir

sshclient = pmk.SSHClient()
sshclient.load_system_host_keys()
sshclient.set_missing_host_key_policy(pmk.WarningPolicy)
sshclient.connect(hostname, username=username, password=password)

sftpclient = pmk.SFTPClient.from_transport(sshclient.get_transport())

out = open('out.txt', 'w')
err = open('err.txt', 'w')

stdin, stdout, stderr = sshclient.exec_command(cmd1)

out.write(stdout.read().decode('utf-8'))
err.write(stderr.read().decode('utf-8'))

sftpclient.put('testcode.c', tdir + '/testcode.c')
sftpclient.put('testcode.h', tdir + '/testcode.h')

stdin, stdout, stderr = sshclient.exec_command(cmd2)

out.write(stdout.read().decode('utf-8'))
err.write(stderr.read().decode('utf-8'))

retfile = request + '.txt'

try:
    sftpclient.get(tdir + '/' + retfile, retfile)
except:
    pass

stdin, stdout, stderr = sshclient.exec_command(cmd3)

out.write(stdout.read().decode('utf-8'))
err.write(stderr.read().decode('utf-8'))

out.close()
err.close()
log.close()

sshclient.close()

