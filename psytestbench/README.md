### psytestbench organization

See the `examples` package for some sample use of the library.  I've also stuck my lab setup in examples.mylab and re-use that in a few of the samples--you might want to change the device IDs in there.

The

    *  ds1000z (Rigol DSO1000/MSO1000 oscilloscopes)
    *  spd3303x (Siglent power supplies)
    *  ut880x  (Unitrend UT8000 multimeters)
    *  utg9xx  (Unitrend signal generators)

packages are actual implementation classes, which each have a top-level `Instrument` class for their given instrument type.

The `lab` package is a base class for containers that give handy access to all available instruments (see `examples.mylab` for use).

The rest is support, with the core of base classes and abstractions in the `psytb` package.

