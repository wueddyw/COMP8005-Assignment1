# COMP 8005 – Distributed Password Cracking System

**Course:** COMP 8005  
**Program:** BSc Applied Computer Science  
**Term:** January 2026  


## Overview

This project implements a distributed password cracking system using a
controller/worker architecture on UNIX systems.

The system consists of exactly:
- One controller process
- One single-threaded worker process running on a separate host

The design intentionally avoids parallelism in order to measure and analyze the
overheads introduced by distributed execution, including parsing, network
communication, remote execution, and result handling.



## Supported Hashing Algorithms

The system supports the following UNIX password hashing formats:

| Algorithm        | Shadow Prefix |
|------------------|---------------|
| MD5-crypt        | `$1$`         |
| SHA256-crypt     | `$5$`         |
| SHA512-crypt     | `$6$`         |
| bcrypt           | `$2a$`, `$2b$`, `$2y$` |
| yescrypt         | `$y$`         |


## System Architecture

### Controller
The controller is responsible for:
- Parsing the shadow file to extract the target hash
- Detecting the hashing algorithm
- Accepting a single worker registration
- Dispatching the cracking job
- Receiving results from the worker
- Recording timing measurements and final outcomes

### Worker
The worker is responsible for:
- Registering with the controller
- Receiving a cracking job
- Performing password cracking sequentially
- Returning results and timing data

The worker is strictly single-threaded and does not spawn additional threads or processes.



## Password Search Parameters

All experiments use:
- Password length: **3 characters**
- Character set size: **79 characters**
- Exhaustive sequential search of the full keyspace

No partitioning or parallel execution is performed.



## Communication Model

- TCP socket communication
- Explicit message framing
- Structured job and result messages

Job messages include the target hash, search parameters, and dispatch timestamp.
Result messages include cracking outcomes and worker-side timestamps.


## Performance Measurement

All timing measurements are collected using a monotonic high-resolution clock
(`time.perf_counter_ns`) and reported in milliseconds.

The following metrics are recorded:
- Controller-side parsing time
- Job dispatch latency (controller → worker)
- Worker cracking time
- Result return latency (worker → controller)
- Total end-to-end runtime

Multiple trials are executed for each hashing algorithm and summarized using
basic statistics.


## Implementation Notes

- Language: Python 3.13
- Hash verification:
  - `passlib` for MD5-crypt, SHA256-crypt, SHA512-crypt, and bcrypt
  - `crypt-r` for yescrypt support (required due to removal of `crypt` in Python 3.13)
- All password cracking is performed sequentially on the worker


## Usage

### Controller
```bash
python controller.py -f shadow.txt -u <username> -p <port>
### Controller


## Dependencies

The project requires Python 3.13 and the following packages:

- passlib
- bcrypt (version 4.3.0)
- crypt-r

Dependencies can be installed using:

```bash
pip install -r requirements.txt

