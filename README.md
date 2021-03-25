spiral-target-remote
====================

SPIRAL profiler framework for forwarding requests to remote machines.

Use the `-f/--forward` option for `spiralprofiler` or `opts.target.remote`
to tell the profiler to forward the request.  You must also explicitly
set the name for the target on the remote machine with the `-t/--target` option
or with `opts.target.name`.

This version only supports requests sent from a Windows system to a Linux system, and
it uses basic username/password authentication.

Installation
------------

Clone this repository into the profiler/targets subdirectory of your SPIRAL
installation tree and rename it to "remote". From the SPIRAL root directory:

```
cd profiler/targets
git clone https://github.com/spiral-software/spiral-target-remote.git remote
```

The request forwarder requires the [paramiko](https://pypi.org/project/paramiko/) Python 
module, which supports SSH2.  Install it with:

```
pip install paramiko
```


Configuration and Use
---------------------

The SPIRAL profiler, when invoked with the `--forward <nickname>` option, looks for
a `<nickname>` subdirectory under `profiler/targets/remote` and calls the `forward`
script in that subdirectory.  The configuration for each remote machine is in its
corresponding subdirectory.

### Local Machine

1. Create a subdirectory under `profiler/targets/remote` with a unique
nickname for the remote machine.

2. Copy `profiler/targets/remote/forward.cmd` to the new subdiretory.

3. Edit the new copy of `forward.cmd` with the hostname and login info
for the remote machine.


### Remote Machine

1. Install SPIRAL and make sure it locally runs any profiler targets you
will be using.

2. Add the full path to `profiler/bin` to the `PATH` variable in your `.profile`.


Example
-------

For this example, the nickname for the remote machine is "testbox".  Note that the remote machine name and 
remote target are set in the SPIRAL options before calling the profiler.  The `forward.cmd` script
for `testbox`, edited with the remote address and login info, is in `profiler/targets/remote/testbox`.

```
opts := SpiralDefaults;
opts.target.forward := "testbox";
opts.target.name := "linux-x86";
t := DFT(32, -1);
rt := RandomRuleTree(t, opts);
s := SumsRuleTree(rt, opts);
c := CodeSums(s, opts);
CMeasure(c, opts);
```


