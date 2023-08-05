

.. _sphx_glr_auto_examples_plot_fitting_dists.py:


=====================
Fitting Distributions
=====================

Histograms, PDF fits, Kernel Density.



.. code-block:: python


    # Author: Moritz Lotze <mlotze@km3net.de>
    # License: BSD-3

    import matplotlib.pyplot as plt
    import numpy as np
    import statsmodels.api as sm

    from astropy.stats import knuth_bin_width
    from scipy.stats import norm
    from sklearn.mixture import GaussianMixture
    from sklearn.grid_search import GridSearchCV
    from sklearn.neighbors import KernelDensity

    import km3pipe.style
    km3pipe.style.use('default')







First generate some pseudodata: A bimodal gaussian, + noise.



.. code-block:: python


    N = 100
    bmg = np.concatenate((np.random.normal(15, 1, 0.3 * N),
                          np.random.normal(20, 1, 0.7 * N)))
    noise_bmg = 0.5
    data = np.random.normal(bmg, noise_bmg)[:, np.newaxis]

    # make X axis for plots
    x = np.linspace(5, 35, N+1)







Histograms (nonparametric)
--------------------------

The simplest nonparametric density estimation tool is the Histogram.
Choosing the binning manually can be tedious, however:

15 bins, spaced from ``data.min()`` to ``data.max()``.



.. code-block:: python


    plt.hist(data, bins=15, alpha=.5, normed=True)





.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_001.png
    :align: center




Auto Binning (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use builtin (numpy's) heuristics to figure out best binning.



.. code-block:: python


    plt.hist(data, bins='auto', alpha=.5, normed=True)




.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_002.png
    :align: center




Knuth’s rule:
^^^^^^^^^^^^^

A fixed-width, Bayesian approach to determining the optimal bin
width of a histogram.



.. code-block:: python


    width, knuth_binlims = knuth_bin_width(data=data[:, 0], return_bins=True)

    plt.hist(data, bins=knuth_binlims, alpha=.5, normed=True)





.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_003.png
    :align: center




Bayesian Blocks
^^^^^^^^^^^^^^^

TODO: Compute optimal segmentation of data with Scargle’s Bayesian Blocks.
Produces bins of uneven width.


Fit Distribution via Maximum Likelihood
---------------------------------------

If we have a hypothesis what the distribution looks like (e.g. gaussian), and want to fit its parameters.

The nice thing is, you can define your own PDFs in scipy and fit it.
Or take one from the dozens of pre-defined ones.

However, there is no *bimodal* gaussian implemented in scipy yet :/
In this case, either define it yourself, or use a GMM (below)



.. code-block:: python


    mu, sig = norm.fit(data)

    plt.fill(x, norm(mu, sig).pdf(x), alpha=.5, label='Fitted')
    plt.legend()
    print('Unimodal Gaussian Fit:  Mean {:.4}, stdev {:.4}'.format(mu, sig))
    plt.hist(data, bins='auto', alpha=.3, normed=True)




.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_004.png
    :align: center


.. rst-class:: sphx-glr-script-out

 Out::

    Unimodal Gaussian Fit:  Mean 18.53, stdev 2.48


As expected, the result is rather silly, since we are only fitting *one*
of the two gaussians.


Fit Gaussian Mixture Model (GMM)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming the data is the sum of one or more gaussians.
Easily handles multidimensional case as well.



.. code-block:: python


    gmm = GaussianMixture(n_components=2, covariance_type='spherical')
    gmm.fit(data)

    mu1 = gmm.means_[0, 0]
    mu2 = gmm.means_[1, 0]
    sig1, sig2 = gmm.covariances_
    wgt1, wgt2 = gmm.weights_
    print('''Fit:
          1: Mean {:.4}, stdev {:.4}, weight {:.4}
          2: Mean {:.4}, stdev {:.4}, weight {:.4}
    '''.format(mu1, sig1, wgt1, mu2, sig2, wgt2))

    plt.hist(data, bins='auto', alpha=.3, normed=True)
    plt.vlines((mu1, mu2), ymin=0, ymax=0.35, label='Fitted Means')
    plt.legend()
    plt.title('Gaussian Mixture Model')




.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_005.png
    :align: center


.. rst-class:: sphx-glr-script-out

 Out::

    Fit:
          1: Mean 15.56, stdev 1.759, weight 0.347
          2: Mean 20.1, stdev 1.32, weight 0.653


Kernel Density: (non-parametric)
--------------------------------

If we have no strong assumptions about the underlying pdf.

"Smooth out" each event with a kernel (e.g. gaussian) of
a certain bandwidth, then add together all these mini-functions.

The "bandwidth" (width of the kernel function) depends on the data, and
can be estimated using cross-validation + maximum likelihood


in Statsmodels



.. code-block:: python


    dens = sm.nonparametric.KDEUnivariate(data)
    dens.fit()

    kde_sm = dens.evaluate(x)
    plt.fill(x, kde_sm, alpha=.5, label='KDE')
    plt.hist(data, bins='auto', alpha=.3, normed=True)




.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_006.png
    :align: center




in scikit-learn



.. code-block:: python


    params = {'bandwidth': np.logspace(-2, 2, 50)}
    grid = GridSearchCV(KernelDensity(), params)
    grid.fit(data)

    print("best bandwidth: {0}".format(grid.best_estimator_.bandwidth))

    # use the best estimator to compute the kernel density estimate
    kde_best = grid.best_estimator_
    kde_sk = np.exp(
        kde_best.score_samples(x[:, np.newaxis])
    )
    plt.fill(x, kde_sk, alpha=.5, label='KDE')
    plt.hist(data, bins='auto', alpha=.3, normed=True)





.. image:: /auto_examples/images/sphx_glr_plot_fitting_dists_007.png
    :align: center


.. rst-class:: sphx-glr-script-out

 Out::

    best bandwidth: 3.3932217718953264


References
----------

- B.W. Silverman, “Density Estimation for Statistics and Data Analysis”
- Hastie, Tibshirani and Friedman, “The Elements of Statistical Learning: Data Mining, Inference, and Prediction”, Springer (2009)
- Liu, R., Yang, L. “Kernel estimation of multivariate cumulative distribution function.” Journal of Nonparametric Statistics (2008)
- Scargle, J., et al. "Studies in astronomical time series analysis. vi. Bayesian Block Representations." The Astrophysical Journal 764.2 (2013)


**Total running time of the script:**
(0 minutes 0.894 seconds)



.. container:: sphx-glr-download

    **Download Python source code:** :download:`plot_fitting_dists.py <plot_fitting_dists.py>`


.. container:: sphx-glr-download

    **Download IPython notebook:** :download:`plot_fitting_dists.ipynb <plot_fitting_dists.ipynb>`

.. rst-class:: sphx-glr-signature

    `Generated by Sphinx-Gallery <http://sphinx-gallery.readthedocs.io>`_
