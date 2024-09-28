# Kerberos Simulation Example

This project simulates a simplified version of the Kerberos authentication protocol using Python. It demonstrates the interaction between a Key Distribution Center (KDC), a client, and a service, showcasing how tickets are issued and verified.

## Overview

Kerberos is a network authentication protocol designed to provide secure authentication for users and services. This simulation includes:

- **KDC**: Issues Ticket-Granting Tickets (TGT) and Service Tickets.
- **Client**: Requests TGT and Service Tickets.
- **Service**: Verifies Service Tickets and grants access.

## Requirements

- Python 3.x
- `pycryptodome` library for cryptographic functions

You can install the required library using pip:

```bash
pip install pycryptodome
```

## Usage

To run the simulation, execute the following command:

```bash
python main.py
```

This will simulate the Kerberos flow, where a client requests a TGT, then requests a Service Ticket, and finally, the service verifies the ticket.

## Code Structure

- `main.py`: Contains the implementation of the KDC, Client, and Service classes, along with the simulation function.

### Key Classes

- **KDC**: Manages ticket issuance and encryption/decryption.
- **Client**: Represents the user requesting access to a service.
- **Service**: Represents the service that verifies tickets.

```

```
