# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function
import numpy as np
import astropy.io.fits as pyfits
import fermipy.utils as utils
import fermipy.wcs_utils as wcs_utils


def make_srcmap(skydir, psf, spatial_model, sigma, npix=500, xpix=0.0, ypix=0.0,
                cdelt=0.01, rebin=1, psf_scale_fn=None):
    """Compute the source map for a given spatial model.

    Parameters
    ----------

    skydir : `~astropy.coordinates.SkyCoord`

    psf : `~fermipy.irfs.PSFModel`

    spatial_model : str
        Spatial model.

    sigma : float
        Spatial size parameter for extended models.
        
    xpix : float
        Source position in pixel coordinates in X dimension.

    ypix : float
        Source position in pixel coordinates in Y dimension.

    rebin : int    
        Factor by which the original map will be oversampled in the
        spatial dimension when computing the model.

    psf_scale_fn : callable        
        Function that evaluates the PSF scaling function.
        Argument is energy in MeV.

    """

    energies = psf.energies
    nebin = len(energies)

    if spatial_model == 'GaussianSource' or spatial_model == 'RadialGaussian':
        k = utils.make_cgauss_kernel(psf, sigma, npix * rebin, cdelt / rebin,
                                     xpix * rebin, ypix * rebin,
                                     psf_scale_fn)
    elif spatial_model == 'DiskSource' or spatial_model == 'RadialDisk':
        k = utils.make_cdisk_kernel(psf, sigma, npix * rebin, cdelt / rebin,
                                    xpix * rebin, ypix * rebin,
                                    psf_scale_fn)
    elif spatial_model == 'PSFSource' or spatial_model == 'PointSource':
        k = utils.make_psf_kernel(psf, npix * rebin, cdelt / rebin,
                                  xpix * rebin, ypix * rebin,
                                  psf_scale_fn)
    else:
        raise Exception('Unrecognized spatial model: %s' % spatial_model)

    if rebin > 1:
        k = utils.rebin_map(k, nebin, npix, rebin)

    k *= psf.exp[:, np.newaxis, np.newaxis] * np.radians(cdelt) ** 2

    return k


def make_cgauss_mapcube(skydir, psf, sigma, outfile, npix=500, cdelt=0.01,
                        rebin=1):
    energies = psf.energies
    nebin = len(energies)

    k = utils.make_cgauss_kernel(psf, sigma, npix * rebin, cdelt / rebin)

    if rebin > 1:
        k = utils.rebin_map(k, nebin, npix, rebin)
    w = wcs_utils.create_wcs(skydir, cdelt=cdelt, crpix=npix / 2. + 0.5, naxis=3)

    w.wcs.crpix[2] = 1
    w.wcs.crval[2] = 10 ** energies[0]
    w.wcs.cdelt[2] = energies[1] - energies[0]
    w.wcs.ctype[2] = 'Energy'

    ecol = pyfits.Column(name='Energy', format='D', array=10 ** energies)
    hdu_energies = pyfits.BinTableHDU.from_columns([ecol], name='ENERGIES')

    hdu_image = pyfits.PrimaryHDU(np.zeros((nebin, npix, npix)),
                                  header=w.to_header())

    hdu_image.data[...] = k

    hdu_image.header['CUNIT3'] = 'MeV'

    hdulist = pyfits.HDUList([hdu_image, hdu_energies])
    hdulist.writeto(outfile, clobber=True)


def make_psf_mapcube(skydir, psf, outfile, npix=500, cdelt=0.01, rebin=1):
    energies = psf.energies
    nebin = len(energies)

    k = utils.make_psf_kernel(psf, npix * rebin, cdelt / rebin)

    if rebin > 1:
        k = utils.rebin_map(k, nebin, npix, rebin)
    w = wcs_utils.create_wcs(skydir, cdelt=cdelt, crpix=npix / 2. + 0.5, naxis=3)

    w.wcs.crpix[2] = 1
    w.wcs.crval[2] = 10 ** energies[0]
    w.wcs.cdelt[2] = energies[1] - energies[0]
    w.wcs.ctype[2] = 'Energy'

    ecol = pyfits.Column(name='Energy', format='D', array=10 ** energies)
    hdu_energies = pyfits.BinTableHDU.from_columns([ecol], name='ENERGIES')

    hdu_image = pyfits.PrimaryHDU(np.zeros((nebin, npix, npix)),
                                  header=w.to_header())

    hdu_image.data[...] = k

    hdu_image.header['CUNIT3'] = 'MeV'

    hdulist = pyfits.HDUList([hdu_image, hdu_energies])
    hdulist.writeto(outfile, clobber=True)


def make_gaussian_spatial_map(skydir, sigma, outfile, cdelt=None, npix=None):

    if cdelt is None:
        cdelt = sigma/10.
    
    if npix is None:
        npix = int(np.ceil((6.0*(sigma+cdelt))/cdelt))
    
    w = wcs_utils.create_wcs(skydir, cdelt=cdelt, crpix=npix / 2. + 0.5)
    hdu_image = pyfits.PrimaryHDU(np.zeros((npix, npix)),
                                  header=w.to_header())

    hdu_image.data[:, :] = utils.make_gaussian_kernel(sigma, npix=npix, cdelt=cdelt)
    hdulist = pyfits.HDUList([hdu_image])
    hdulist.writeto(outfile, clobber=True)


def make_disk_spatial_map(skydir, radius, outfile, cdelt=None, npix=None):

    if cdelt is None:
        cdelt = radius/10.
    
    if npix is None:
        npix = int(np.ceil((2.0*(radius+cdelt))/cdelt))
        
    w = wcs_utils.create_wcs(skydir, cdelt=cdelt, crpix=npix / 2. + 0.5)
    hdu_image = pyfits.PrimaryHDU(np.zeros((npix, npix)),
                                  header=w.to_header())

    hdu_image.data[:, :] = utils.make_disk_kernel(radius, npix=npix, cdelt=cdelt)
    hdulist = pyfits.HDUList([hdu_image])
    hdulist.writeto(outfile, clobber=True)


def delete_source_map(srcmap_file, names, logger=None):
    """Delete a map from a binned analysis source map file if it exists.

    Parameters
    ----------
    srcmap_file : str
       Path to the source map file.

    names : list
       List of HDU keys of source maps to be deleted.

    """
    hdulist = pyfits.open(srcmap_file)
    hdunames = [hdu.name.upper() for hdu in hdulist]

    if not isinstance(names,list):
        names = [names]

    for name in names:        
        if not name.upper() in hdunames:
            continue
        del hdulist[name.upper()]

    hdulist.writeto(srcmap_file, clobber=True)


def update_source_maps(srcmap_file, srcmaps, logger=None):
    hdulist = pyfits.open(srcmap_file)
    hdunames = [hdu.name.upper() for hdu in hdulist]

    for name, data in srcmaps.items():

        if not name.upper() in hdunames:

            for hdu in hdulist[1:]:
                if hdu.header['XTENSION'] == 'IMAGE':
                    break

            newhdu = pyfits.ImageHDU(data, hdu.header, name=name)
            newhdu.header['EXTNAME'] = name
            hdulist.append(newhdu)

        if logger is not None:
            logger.debug('Updating source map for %s' % name)

        hdulist[name].data[...] = data

    hdulist.writeto(srcmap_file, clobber=True)
