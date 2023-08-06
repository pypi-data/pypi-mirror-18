Dunshire is a `CVXOPT <http://cvxopt.org/>`_-based library for solving
linear (cone) games. The notion of a symmetric linear (cone) game was
introduced by Gowda and Ravindran in *On the game-theoretic value of a
linear transformation relative to a self-dual cone*. I've extended
their results to asymmetric cones and two interior points in my
thesis, which does not exist yet.

The main idea can be gleaned from Gowda and Ravindran, however.
Additional details and our problem formulation can be found in the
full Dunshire documentation. The state-of-the-art is that only
symmetric games can be solved efficiently, and thus the linear games
supported by Dunshire are a compromise between the two: the cones are
symmetric, but the players get to choose two interior points.

Only the nonnegative orthant and the ice-cream cone are supported at
the moment. The symmetric positive-semidefinite cone is coming soon.
