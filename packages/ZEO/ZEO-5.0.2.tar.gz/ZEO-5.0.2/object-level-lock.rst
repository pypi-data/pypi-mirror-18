==============================
Status of object-level locking
==============================

TL;DR: initial performance tests are disappointing. :(

I'm not done.  Two big pieces that are done:

- A branch of FileStorage that allows multiple transactions to be in
  flight at once.  It does no locking to assure that they don't
  conflict, but delegates that it it's caller.  Each transaction gets
  it's own buffer.  Because the transaction id and actual position in
  the file isn't known when a buffer is created, a lot more work has
  to be done when finally committing the buffer to the file than is
  done now.  Also, because the buffers are committed to the file in
  tpc_finish, rather than in tpc_vote, there's a greater chance of
  failure in the last stage of 2-phase commit due to running out of
  disk space.

- A ZEO storage server lock manager that manages locks by
  object id. When a transaction wants to lock, it gets locks for all
  of it's objects.

I've also made some other changes to the ZEO storage to integrate
these.  These changes are likely correct, but not all tests
pass. (Although many do.)  I decided to do some performance tests to
see what benefit we got if any, before doing more work.

How I tested
============

I used a zodbshootout-like, but ZEO specific, script:

https://gist.github.com/jimfulton/2ae9ec911059888e4d61103baf7e7aa2

This script is evolving over time, and I want to use it with both ZEO
4 and 5, which is why it's just a gist for now.


First stab: running test on my Mac. :)
======================================

It turns out that the extra Python code to manage object-level locks
and to manage the new FileStorage transaction buffers made
object-level locking significantly slower.  :(  Thanks Python.

According to profiling data, a fair chunk of time was spent opening
and closing the temporary files used for FileStorage transaction
buffers.  This could probably be mitigated by pooling and reusing the
temporary files.  For the remainder of the tests, I changed the
file-storage temporary buffers to use ``io.BytesIO`` objects rather
than temporary files, as I didn't want the results to be biased by
that detail.

I also wondered if I might have some sort of process starvation issue
running on my (quad core) Mac with various applications running.

Second stab: running on an EC2 m4.10xlarge
==========================================

This machine has 40 cores and is EBS backed.  The first thing I
noticed was that everything ran much slower on this box.  Pretty
quickly I realized that a lot of time was spend fsyncing. Even though
this machine's disks are SSDs, they're EBS and thus network disks. :/

For the remainder of the tests, I disabled fsyncing, again, because I
didn't want that to be a distraction.

Again, object-level locks were much slower.  It's was fairly easy to
peg the storage server's CPU (just one because the GIL).  This was
depressing. :)

Multi-threaded acceptor :(
--------------------------

In flailing, I decided to try using the multi-threaded server.  This
made things much slower for more than 4 clients. :( The performance is
similar to ZEO4.

I was able to mitigate the slowness a bit with uvloop, but it's still
much slower using the multi-threaded server.

If you are'nt going to have users actually authenticate with
certificates, then I suggest changing ZeroDB to drop certificate
authentication support and use the single-threaded server.

If you *really* want to support authenticating with certs, then I
think we need to look into extending SSLK contexts to allow them to be
modified in place. This should be possible in C.

I stopped to ponder :)
======================

It was the end of the day. I decided to stop and mull things a bit.

I considered that the main benefit of object-level locks is to avoid
serializing waiting for clients to respond to vote results and call
tpc_finish.

To review: ZEO 4 doesn't get the global lock at the beginning of a
transaction. It gets it at vote time.  When it gets the lock, it
executes the first phase of 2-phase commit on the underlying storage
and returns the vote result.  The global lock is held while the commit
executes on the underlying storage, plus the time it takes the client
to respond to the vote result.  In tests on the same machine, it takes
very little time for the client to respond, and network latency is
practically nil and the client itself calls tpc_finish immediately.

On the m4.10xlarge I'm using for testing, ping times to another
machine in the same VPC are ~.4ms, but pings of the loopback interface
are about .02ms, or 20 times faster.

For database as a service, network latencies are likely to be much
worse.  For example, ping times from my home in Manassas to the AWS
US-Eastern region, about 30 miles away, are ~20ms.

Third Stab, testing from my home to am m4.xlarge in EC2
=======================================================

This is similar to the sort of situation one might encounter with
database as a service.  Unfortunately, I was limited by my upload
speed, which is around 1MBps, or less.

Here are some results, first, without object level locks:

Times per operation in microseconds (o=999, t=3, c=1)
           op          min         mean       median          max
          add        54542
       update        37346
Times per operation in microseconds (o=999, t=3, c=2)
           op          min         mean       median          max
          add        58374        58386        58374        58397
       update        41087        41094        41101        41101
Times per operation in microseconds (o=999, t=3, c=4)
           op          min         mean       median          max
          add        73374        76554        76299        78991
       update        48818        62618        53405        88154
Times per operation in microseconds (o=999, t=3, c=8)
           op          min         mean       median          max
          add        76706       118757       166185       166185
       update        51508       103034       157476       157476
Times per operation in microseconds (o=999, t=3, c=16)
           op          min         mean       median          max
          add        78970       204731       177936       335452
       update        56742       190900       190641       326105
Times per operation in microseconds (o=999, t=3, c=32)
           op          min         mean       median          max
          add        76734       394857       558555       719873
       update        64355       376589       532705       693523

Note that in the headers above: ``o`` is roughly the object size in bytes,
``t`` is the number of objects in a transaction, and ``c`` is the
number of concurrent clients.  The ``add`` rows have times for
transactions that add objects. The ``update`` rows have times for
transactions that update the objects just added.

1000 repetitions are used for each test.  As you can see, the
performance degrades starting at around 4 concurrent transactions.

Note that the times are very long. owing t the large network latency.

Here are data for a server that uses object level locks:

Times per operation in microseconds (o=999, t=3, c=1)
           op          min         mean       median          max
          add        53784
       update        37235
Times per operation in microseconds (o=999, t=3, c=2)
           op          min         mean       median          max
          add        56812        56895        56978        56978
       update        38858        38890        38858        38922
Times per operation in microseconds (o=999, t=3, c=4)
           op          min         mean       median          max
          add        63383        63886        63383        64367
       update        42428        42830        42428        43402
Times per operation in microseconds (o=999, t=3, c=8)
           op          min         mean       median          max
          add        67187        68413        69152        69558
       update        46526        47193        47784        47931
Times per operation in microseconds (o=999, t=3, c=16)
           op          min         mean       median          max
          add       112624       113544       114932       114932
       update       103852       104366       105018       105018
Times per operation in microseconds (o=999, t=3, c=32)
           op          min         mean       median          max
          add       270882       280825       274562       285359
       update       230653       242243       240713       257380

Object-level locking provided a noticeable (but not stunning) win for
concurrencies of 4, 8, and 16, but the advantage was starting to
decrease at a concurrency of 16 and was much less at a concurrency
of 32.  I'm pretty sure this was due to bandwidth from my home
becoming the limiting factor.

Assuming that latency for database as a service clients is similar,
object-level locks might be fairly advantageous.

Fourth stab: in-cluster test.
=============================

For this test, I created an i2.xlarge instance to use as a storage
server to get better IO speed. I used it's local disk rather than EBS
for the storage data.

I used the m4.10xlarge as the client to assure that clients weren't
starving one another.

The ping times between the client and the server are ~.4ms, about 50x
faster than from my home.  One issue with using a single client
machine is that I might have saturated the connection between the
client and server.  When I did somewhat similar testing a few years
ago, I ran clients on multiple EC2 machines. Obviously, orchestrating
that is more complicated.

Without object-level locks:

Times per operation in microseconds (o=999, t=3, c=1)
           op          min         mean       median          max
          add         5867
       update         4800
Times per operation in microseconds (o=999, t=3, c=2)
           op          min         mean       median          max
          add         5776         5777         5776         5778
       update         4863         4867         4863         4871
Times per operation in microseconds (o=999, t=3, c=4)
           op          min         mean       median          max
          add         6718         6734         6748         6748
       update         5894         5900         5896         5908
Times per operation in microseconds (o=999, t=3, c=8)
           op          min         mean       median          max
          add         7916        11215         7916        15178
       update         7006        10687         7006        15324
Times per operation in microseconds (o=999, t=3, c=16)
           op          min         mean       median          max
          add         9578        22702        34650        35616
       update         8069        21157        20549        34220
Times per operation in microseconds (o=999, t=3, c=32)
           op          min         mean       median          max
          add        10940        54382        78942        94904
       update         9117        52074        46486        92650
Times per operation in microseconds (o=999, t=3, c=64)
           op          min         mean       median          max
          add        15051       158512       127817       294296
       update        10933       159925       128806       293377

With object-level locks:

Times per operation in microseconds (o=999, t=3, c=1)
           op          min         mean       median          max
          add         5964
       update         4965
Times per operation in microseconds (o=999, t=3, c=2)
           op          min         mean       median          max
          add         5888         5912         5937         5937
       update         5033         5035         5037         5037
Times per operation in microseconds (o=999, t=3, c=4)
           op          min         mean       median          max
          add         6637         6690         6665         6761
       update         5656         5701         5698         5728
Times per operation in microseconds (o=999, t=3, c=8)
           op          min         mean       median          max
          add        11819        11965        11903        12176
       update         9381         9717         9719         9808
Times per operation in microseconds (o=999, t=3, c=16)
           op          min         mean       median          max
          add        17628        20746        19320        22360
       update        15303        17996        18156        19478
Times per operation in microseconds (o=999, t=3, c=32)
           op          min         mean       median          max
          add        54045        57384        54090        60694
       update        49044        51286        51794        54496
Times per operation in microseconds (o=999, t=3, c=64)
           op          min         mean       median          max
          add       171574       173295       171819       181187
       update       162063       163335       162215       169989

Here we see little or no benefit in using object-level locks. (There
might be a slight benefit to median times, but that breaks down at a
concurrency of 64.)  The benefit of not serializing client handling of
vote results is outweighed by the overhead of the additional
computations.

fsync *not* considered harmful on fast disks :)
-----------------------------------------------

I did some of these tests with fsync enabled and verified that doing
so has minimal effect on performance on a machine with fast disks. It's
good to pay attention to disk speed.  I suppose a good test of disk
configuration is to do one of these tests with fsync enabled and with
fsync disabled and verify that the times are roughly the same.

OTOH, if the server wasn't so slow, it's likely that disk bottlenecks
would be a greater issue.

Summary
=======

The benefits of object-level locks aren't compelling at this point,
unless you think customers will have poor latency in their
connections.

The slowness of the Python code prevents the benefits of object-level
locks from being realized unless network latencies are poor.  The
server-process was using about 100% CPU at a concurrency of around 8.

It's likely that the server Python code could be speeded somewhat.  A
lot of the code was over abstracted years ago by another developer.
And it's possible I screwed something up. <shrug>

I think a non-Python server implementation will be needed to realize
benefits of object-level locks.

If you want to move forward with them, the remaining work:

- Create a FileStorage subclass that supports object-level locking, so
  as not to penalize applications that don't benefit from object-level
  locks.  This is mostly a refactoring of what I already have. WAG a
  day or 2.

- Finish the server implementation, including getting tests to pass.
  This includes the server conditionally using object-level locks
  depending on the server it's configured to use. WAG 2-3 days.

- Do some optimizations, like pooling temporary files and
  de-abstracting some of the code that reads and writes file-storage
  files.

When you've had a chance to digest this, we should discuss next steps.

