#include "pixmap.h"

/** ---------------------------------------------------------------------------
 * Retrieve dimensions of python image
 */

void
get_dimensions(PyArrayObject *image, int *ndim, int size[3]) {

    int idim, jdim;
    
    *ndim = PyArray_NDIM(image);
    npy_intp *psize = PyArray_DIMS(image);
    
    /* Put dimensions in xyz order */  

    idim = *ndim;
    jdim = 0;
    while(idim > 0) {
        size[jdim++] = psize[--idim];
    }
    
    while (jdim < 4) {
        size[jdim++] = 0;
    }
    
    return;
}

/** ---------------------------------------------------------------------------
 * Pixel map array accessor
 * 
 * pixmap:   structure containing pixel map and dimensions
 * xpix:     the x coordinate of the pixel
 * ypix:     the y coordinate of the pixel
 * zpix      the z coordinate of the pixel
 */

double*
get_pixmap(PyArrayObject *pixmap, int xpix, int ypix, int zpix) {
    double *pixptr;

    switch (PyArray_NDIM(pixmap)) {
    case 2:
        pixptr = PyArray_GETPTR1(pixmap, xpix);
        break;
    case 3:
        pixptr = PyArray_GETPTR2(pixmap, ypix, xpix);
        break;
    case 4:
        pixptr = PyArray_GETPTR3(pixmap, zpix, ypix, xpix);
        break;
    default:
        pixptr = (double *) 0;
    }

    return pixptr;
}

/** ---------------------------------------------------------------------------
 * Retrieve dimensions of python array
 */

void
get_pixmap_size(PyArrayObject *pixmap, int *ndim, int size[3]) {

    int idim, jdim;
    
    *ndim = PyArray_NDIM(pixmap);
    npy_intp *psize = PyArray_DIMS(pixmap);
    
    /* Drop last dimension of pixmap */
    *ndim -= 1;
    
    /* Put dimensions in xyz order */  

    idim = *ndim;
    jdim = 0;
    while(idim > 0) {
        size[jdim++] = psize[--idim];
    }
    
    while (jdim < 3) {
        size[jdim++] = 0;
    }
    
    return;
}

/** ---------------------------------------------------------------------------
 * Image array accessor TODO: move elsewhere
 * 
 * image:   image map and dimensions
 * xpix:     the x coordinate of the pixel
 * ypix:     the y coordinate of the pixel
 * zpix      the z coordinate of the pixel
 */

float
get_pixel(PyArrayObject *image, int xpix, int ypix, int zpix) {
    float value;

    switch (PyArray_NDIM(image)) {
    case 1:
        value = *(float*) PyArray_GETPTR1(image, xpix);
        break;
    case 2:
        value = *(float*) PyArray_GETPTR2(image, ypix, xpix);
        break;
    case 3:
        value = *(float*) PyArray_GETPTR3(image, zpix, ypix, xpix);
        break;
    default:
        value = 0.0;
    }

    return value;
}

/** ---------------------------------------------------------------------------
 * Set pixel in an image TODO: move elsewhere
 * image:     image to be modified (not pixmap)
 * xpix:     the x coordinate of the pixel
 * ypix:     the y coordinate of the pixel
 * zpix      the z coordinate of the pixel
 */

void
set_pixel(PyArrayObject *image, int xpix, int ypix, int zpix, double value) {  

    switch (PyArray_NDIM(image)) {
    case 1:
        *(float*) PyArray_GETPTR1(image, xpix) = value;
        break;
    case 2:
        *(float*) PyArray_GETPTR2(image, ypix, xpix) = value;
        break;
    case 3:
        *(float*) PyArray_GETPTR3(image, zpix, ypix, xpix) = value;
        break;
    }

    return;
}
