# SharedArray python/numpy extension

This is a simple python extension that lets you share numpy arrays
with other processes on the same computer. It uses either shared files
or POSIX shared memory as data stores and therefore should work on
most operating systems.

## Example

Here's a simple example to give an idea of how it works. This example
does everything from a single python interpreter for the sake of
clarity, but the real point is to share arrays between python
interpreters.

	import numpy as np
	import SharedArray as sa

	# Create an array in shared memory
	a = sa.create("shm://test", 10)

	# Attach it as a different array. This can be done from another
	# python interpreter as long as it runs on the same computer.
	b = sa.attach("shm://test")

	# See how they are actually sharing the same memory block
	a[0] = 42
	print(b[0])

	# Destroying a does not affect b.
	del a
	print(b[0])

	# See how "test" is still present in shared memory even though we
	# destroyed the array a.
	sa.list()

	# Now destroy the array "test" from memory.
	sa.delete("test")

	# The array b is not affected, but once you destroy it then the
	# data are lost.
	print(b[0])

## Functions

### `SharedArray.create(name, shape, dtype=float)`

This function creates an array identified by `name`, which can use the
`file://` prefix to indicate that the data backend will be a file, or
`shm://` to indicate that the data backend shall be a POSIX shared
memory object. For backward compatibility `shm://` is assumed when no
prefix is given. The `shape` and `dtype` arguments are the same as the
numpy function `numpy.zeros()` and the returned array is indeed
initialized to zero.

The contents of the array will not be deleted when this array is
destroyed, either implicitly or explicitly by calling `del`, it will
simply be detached from the current process.  To delete a shared array
and therefore reclaim system resources use the `SharedArray.delete()`
function.

### `SharedArray.attach(name)`

This function attaches the previously created array identified by
`name`, which can use the `file://` prefix to indicate that the array
is stored as a file, or `shm://` to indicate that the array is stored
as a POSIX shared memory object. For backward compatibility `shm://`
is assumed when no prefix is given

The contents of the array will not be deleted when this array is
destroyed, either implicitly or explicitly by calling `del`, it will
simply be detached from the current process.  To delete a shared array
and therefore reclaim system resources use the `SharedArray.delete()`
function.

### `SharedArray.delete(name)`

This function destroys the previously created array identified by
`name`, which can use the `file://` prefix to indicate that the array
is stored as a file, or `shm://` to indicate that the array is stored
as a POSIX shared memory object. For backward compatibility `shm://`
is assumed when no prefix is given

After calling `delete`, the array will not be attachable anymore, but
existing attachments will remain valid until they are themselves
destroyed.

### `SharedArray.list()`

This function returns a list of previously created arrays stored as
POSIX SHM objects, along with their name, data type and dimensions.
At the moment this function only works on Linux because it accesses
files exposed under `/dev/shm`.  There doesn't seem to be a portable
method of doing that.

### `SharedArray.msync(array, flags)`

This function is a wrapper around `msync(2)` and is only useful when
using file-backed arrays (i.e. not POSIX shared memory). msync(2)
flushes the mapped memory region back to the filesystem. The `flags`
are exported as constants in the module definition (see below) and are
a 1:1 map of the `msync(2)` flags, please refer to the manual page of
`msync(2)` for details.

### `SharedArray.mlock(array)`

This function is a wrapper around `mlock(2)`: lock the memory map into
RAM, preventing that memory from being paged to the swap area.

### `SharedArray.munlock(array)`

This function is a wrapper around `munlock(2)`: unlock the memory map,
allowing that memory to be paged to the swap area.

## Constants

### `SharedArray.MS_ASYNC`

Flag for `SharedArray.msync()`. Specifies that an update be scheduled,
but the call returns immediately.

### `SharedArray.MS_SYNC`

Flag for `SharedArray.msync()`. Requests an update and waits for it to
complete.

### `SharedArray.MS_INVALIDATE`

Flag for `SharedArray.msync()`. Asks to invalidate other mappings of
the same file (so that they can be updated with the fresh values just
written).

## Requirements

* Python 2.7 or 3+
* Numpy 1.8
* Posix shared memory interface

SharedArray uses the posix shm interface (`shm_open` and `shm_unlink`)
and so should work on most operating systems that follow the posix
standards (Linux, *BSD, etc.).

## FAQ

### On Linux, I get segfaults when working with very large arrays.

A few people have reported segfaults with very large arrays using
POSIX shared memory. This is not a bug in SharedArray but rather an
indication that the system ran out of POSIX shared memory. On Linux a
`tmpfs` virtual filesystem is used to provide POSIX shared memory, and
by default it is given only about 20% of the total available memory,
depending on the distribution. That amount can be changed by
re-mounting the `tmpfs` filesystem with the `size=100%` option:

	sudo mount -o remount,size=100% /run/shm

Also you can make the change permanent, on next boot, by setting
`SHM_SIZE=100%` in `/etc/defaults/tmpfs` on recent Debian
installations.

### I can't attach old (pre 0.4) arrays anymore.

Since version 0.4 all arrays are now page aligned in memory, to be
used with SIMD instructions (e.g. fftw library). As a side effect,
arrays created with a previous version of SharedArray aren't
compatible with the new version (the location of the metadata
changed). Save your work before upgrading.

## Installation

The extension uses the `distutils` python package that should be
familiar to most python users. To test the extension directly from the
source tree, without installing, type:

	python setup.py build_ext --inplace

To build and install the extension system-wide, type:

	python setup.py build
	sudo python setup.py install

## Contact

For updates and the browse the code, the canonical repository is:
<https://parad0x.org/git/python/shared-array/>

Packages are also available on PyPi at:
<https://pypi.python.org/pypi/SharedArray>

For bug reports, feature requests, suggestions, patches and everything
else related to SharedArray, please contact the maintainer at:
<mat@parad0x.org>.
