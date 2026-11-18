"""Deterministic simulation of course registration at Palm University College.

Run this file to register the morning's students, compare three resource
allocations, and write the tables and graphs.

    python registration.py
    python registration.py --students 20 --officers 1 --computers 2
"""

from registration_sim.__main__ import main

if __name__ == "__main__":
    main()
