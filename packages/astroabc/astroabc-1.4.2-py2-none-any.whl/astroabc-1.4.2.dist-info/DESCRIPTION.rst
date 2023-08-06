Approximate Bayesian computation (ABC) and so 
called "likelihood free" Markov chain Monte Carlo 
techniques are popular methods for tackling parameter 
inference in scenarios where the likelihood is intractable or unknown. 
These methods are called likelihood free as they are free from 
the usual assumptions about the form of the likelihood e.g. Gaussian, 
as ABC aims to simulate samples from the parameter posterior distribution directly.
``astroABC`` is a python package that implements  
an Approximate Bayesian Computation Sequential Monte Carlo (ABC SMC) sampler 
as a python class. It is extremely flexible and applicable to a large suite of problems. 
``astroABC`` requires ``NumPy``,``SciPy`` and ``sklearn``. ``mpi4py`` and ``multiprocessing`` are optional.


