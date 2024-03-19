:class:`EulerIntegrator`: Euler characteristic integration
==========================================================

.. currentmodule:: simplicial

.. autoclass:: EulerIntegrator

For more details see Curry *et alia* :cite:`EulerCalculus`. See
Baryshnikov and Ghrist :cite:`BaryshnikovGhristEulerIntegrals` for a
detailed application.

There is a single top-level method.

.. automethod:: EulerIntegrator.integrate

To implement this we need to be able to generate level sets extracted
from the complex by way of the metric.

.. automethod:: EulerIntegrator.levelSet
