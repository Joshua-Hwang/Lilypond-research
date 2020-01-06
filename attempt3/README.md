# Attempt 3
This attempt will cut out some of the extensions we've added previously.
Though we're still going to use the same \*.lp file format we're going to
assume that all births will happen at time 0 instead of random times.

We will implement the algorithm defined by Heveling & Last (2005).
We will attempt to measure the speed of this algorithm empirically since
the worst case is n^2 but it apparently works for better than this.

We're going to be using Python and just checking the number of global steps
it takes to evaluate a "natural" system.
