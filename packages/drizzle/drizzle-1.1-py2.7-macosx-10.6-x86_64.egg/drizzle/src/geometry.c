#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <Python.h>
#include <numpy/arrayobject.h>

#include "geometry.h"
#include "pixmap.h"

/** ---------------------------------------------------------------------------
 * Log a message
 *
 * msg: message to write to log file
 */

void
log_message(char msg[]) {
    FILE *fd;
    fd = fopen("/tmp/drizzle.log", "a");
    fprintf(fd, "%s\n", msg);
    fclose(fd);
    
    return;
}

/** ---------------------------------------------------------------------------
 * Add the vertex from the clipped side to the polygon
 *
 * polygon: structure ho;ding the polygon vertices
 * side:    side containing point to be added
 * iside:   which point to add
 */

void
add_vertex(geopoly *polygon, geometry *side, int iside) {
    int idim, npoly;
    
    for (idim = 0; idim < side->ndim; ++idim) {
        polygon->vertex[polygon->npoly][idim] = side->vertex[iside][0][0][idim];
    }
    ++ polygon->npoly;
    
    return;
}

/** ---------------------------------------------------------------------------
 * Center the face by subtracting off the pixel position
 *
 * centered_face: the face after subtraction
 * face:          the face before subtraction
 * position:      the position 
 */

void
center_face(geometry *centered_face, geometry *face, int *position) {
    int i, j, k, idim, ivtx;
    int vertices[4] = {1, 2, 4, 8};
    
    memset(centered_face, 0, sizeof(geometry));
    centered_face->ndim = face->ndim;
    centered_face->odim = face->odim;

    ivtx = vertices[face->odim];
    for (k = 0; k < 2; ++k) {
        for (j = 0; j < 2; ++j) {
            for (i = 0; i < 2; ++i) {
                for (idim = 0; idim < face->ndim; ++idim) {
                    centered_face->vertex[i][j][k][idim] = 
                        face->vertex[i][j][k][idim] - position[idim];
                }

                if (-- ivtx == 0) return;
            }
        }
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Clip a face side to the boundaries of a pixel
 *
 * pixel: The pixel the side is clipped to
 * side:   One side of a pixel face
 *
 * returns true if there is anything left
 */

void
clip_face(geopoly *polygon, geometry *face, int *position) {
    geoindex list;
    geometry centered_face, side;
    int idim, iside, jdim, outside, gap[2], positive[2];
    double delta[2];
    double border[2] = {-0.5, 0.5};
    
    gap[0] = gap[1] = 0;
    center_face(&centered_face, face, position);
    
    new_list(&list, &centered_face, 1);
    while (next_item(&side, &list)) {
        gap[0] = gap[1];
        gap[1] = 0;

        for (idim = 0; idim < face->ndim; ++idim) {
            for (iside = 0; iside < 2; ++ iside) {
                delta[0] = side.vertex[0][0][0][idim] - border[iside];
                delta[1] = side.vertex[1][0][0][idim] - border[iside];
                
                positive[0] = delta[0] > 0.0;
                positive[1] = delta[1] > 0.0;
                
                /* If both deltas have the same sign there is no
                 * baundary crossing
                 */
                if (positive[0] == positive[1]) {

                    /* A diagram will convince that you decide a point is
                     * outside the boundary if the following test is true
                     * Clip the line to the border
                     */
                    if (positive[0] == iside) {
                        side.vertex[0][0][0][idim] = border[iside];
                        side.vertex[1][0][0][idim] = border[iside];
                    }

                } else {
                    /* If ends of the line segment are on opposite sides of the
                     * border, calculate the point of intersection
                     */
                    outside = positive[iside];
                    gap[outside] = 1;
                    for (jdim = 0; jdim < face->ndim; ++jdim) {
                        if (idim == jdim) {
                            side.vertex[outside][0][0][jdim] = border[iside];

                        } else {
                            side.vertex[outside][0][0][jdim] = 
                                (delta[1] * side.vertex[0][0][0][jdim] -
                                 delta[0] * side.vertex[1][0][0][jdim]) /
                                (delta[1] - delta[0]);
                        }
                    }
                }
            }
        }
        
        if (gap[0]) {
            add_vertex(polygon, &side, 0);
        }
        add_vertex(polygon, &side, 1);
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Compute the extent (length, area, or volume) of a geometry object
 */

double
extent_geometry(geometry *object) {
    int idim;
    double extent;
    double a[3], b[3], c[3];
    
    switch (object->ndim) {
    case 0:
        extent = 0.0;
        break;
    
    case 1:
        extent = object->vertex[1][0][0][0] - object->vertex[0][0][0][0];
        break;

    case 2:
        for (idim = 0; idim < 2; ++idim) {
            a[idim] =
                object->vertex[1][0][0][idim] - object->vertex[0][0][0][idim];
            b[idim] =
                object->vertex[0][1][0][idim] - object->vertex[0][0][0][idim];
        }

        extent = 0.5 * (a[0] * b[1] - a[1] * b[0]);
        break;

    case 3:
        for (idim = 0; idim < 3; ++idim) {
            a[idim] =
                object->vertex[1][0][0][idim] - object->vertex[0][0][0][idim];
            b[idim] =
                object->vertex[0][1][0][idim] - object->vertex[0][0][0][idim];
            c[idim] =
                object->vertex[0][0][1][idim] - object->vertex[0][0][0][idim];
        }

        extent = c[0] * (a[1] * b[2] - a[2] * b[1]) -
                 c[1] * (a[0] * b[2] - a[2] * b[0]) +
                 c[2] * (a[0] * b[1] - a[1] * b[0]);
        break;
    }

    return fabs(extent);
}

/** ---------------------------------------------------------------------------
 * Compute the extent (length, area, volume) of a polygon
 */

double
extent_polygon(geopoly *polygon) {
    int ipoly, jpoly;
    double extent = 0.0;
    
    switch (polygon->ndim) {
    case 1:
        if (polygon->npoly > 0) {
            extent = polygon->vertex[1][0] - polygon->vertex[0][0];
        }
        break;

    case 2:
        for (ipoly = 0; ipoly < polygon->npoly; ++ipoly) {
            jpoly = ipoly + 1;
            if (jpoly == polygon->npoly) {
                jpoly = 0;
            }
            
            extent += polygon->vertex[ipoly][0] * polygon->vertex[jpoly][1] -
                      polygon->vertex[ipoly][1] * polygon->vertex[jpoly][0];
        }
        
        extent *= 0.5;
        break;

    case 3:
        for (ipoly = 0; ipoly < polygon->npoly; ++ipoly) {
            jpoly = ipoly + 1;
            if (jpoly == polygon->npoly) {
                jpoly = 0;
            }
            
            extent += (polygon->vertex[ipoly][1] * polygon->vertex[jpoly][2] -
                       polygon->vertex[ipoly][2] * polygon->vertex[jpoly][1]) *
                      polygon->vertex[0][0];
            extent += (polygon->vertex[ipoly][2] * polygon->vertex[jpoly][0] -
                       polygon->vertex[ipoly][0] * polygon->vertex[jpoly][2]) *
                      polygon->vertex[0][1];
            extent += (polygon->vertex[ipoly][0] * polygon->vertex[jpoly][1] -
                       polygon->vertex[ipoly][1] * polygon->vertex[jpoly][0]) *
                      polygon->vertex[0][2];
        }
        
        extent /= 6.0;
        break;
    }
    
    return fabs(extent);
}

/** ---------------------------------------------------------------------------
 * Map a pixel's vertices into the reference frame given by pixmap
 *
 * pixel:    the object representing the pixel
 * pixmap:   an n-dimensional mapping btw the two reference frames
 * position: the position of the object in the starting frame
 */

void
map_pixel(geometry *pixel, PyArrayObject *pixmap, int *position) {
    double value, frac[3];
    int pos[3], dimension[3];
    int i, j, k, idim, ndim, maxpos;
    geometry aligned_pixel;
    
    get_pixmap_size(pixmap, &ndim, dimension);
    pixel_at_pos(&aligned_pixel, ndim, position);
    
    pixel->ndim = aligned_pixel.ndim;
    pixel->odim = aligned_pixel.odim;
    
    for (i = 0; i < 2; ++i) {
        for (j = 0; j < 2; ++j) {
            for (k = 0; k < 2; ++k) {
                for (idim = 0; idim < 3; ++idim) {
                    if (idim < ndim) {
                        maxpos = dimension[idim] - 2;
                        frac[idim] = aligned_pixel.vertex[i][j][k][idim];
                        pos[idim]  = frac[idim];
                        pos[idim]  = (pos[idim] > maxpos) ? maxpos :
                                     (pos[idim] < 0) ? 0 : pos[idim];
                        frac[idim] = frac[idim] - pos[idim];
                
                    } else {
                        pos[idim] = 0;
                        frac[idim] = 0.0;
                    }
                }

                for (idim = 0; idim < ndim; ++idim) {
                    value = 0.0;
                    
                    switch(ndim) {
                    case 1:
                        value += (1.0 - frac[0]) *
                            get_pixmap(pixmap, pos[0], pos[1], pos[2])[idim];
                        value += frac[0] *
                            get_pixmap(pixmap, pos[0]+1, pos[1], pos[2])[idim];
                        break;

                    case 2:
                        value += (1.0 - frac[0]) * (1.0 - frac[1]) * 
                            get_pixmap(pixmap, pos[0], pos[1], pos[2])[idim];
                        value += frac[0] * (1.0 - frac[1]) * 
                            get_pixmap(pixmap, pos[0]+1, pos[1], pos[2])[idim];
                        value += (1.0 - frac[0]) * frac[1] * 
                            get_pixmap(pixmap, pos[0], pos[1]+1, pos[2])[idim];
                        value += frac[0] * frac[1] * 
                            get_pixmap(pixmap, pos[0]+1, pos[1]+1, pos[2])[idim];
                        break;
                    
                    case 3:
                        value +=
                        (1.0 - frac[0]) * (1.0 - frac[1]) * (1.0 - frac[2]) *
                        get_pixmap(pixmap, pos[0], pos[1], pos[2])[idim];
                        value +=
                        frac[0] * (1.0 - frac[1]) * (1.0 - frac[2]) *
                        get_pixmap(pixmap, pos[0]+1, pos[1], pos[2])[idim];
                        value +=
                        (1.0 - frac[0]) * frac[1] * (1.0 - frac[2]) *
                        get_pixmap(pixmap, pos[0], pos[1]+1, pos[2])[idim];
                        value +=
                        frac[0] * frac[1] * (1.0 - frac[2]) *
                        get_pixmap(pixmap, pos[0]+1, pos[1]+1, pos[2])[idim];
                        value +=
                        (1.0 - frac[0]) * (1.0 - frac[1]) * frac[2] *
                        get_pixmap(pixmap, pos[0], pos[1], pos[2]+1)[idim];
                        value +=
                        frac[0] * (1.0 - frac[1]) * frac[2] *
                        get_pixmap(pixmap, pos[0]+1, pos[1], pos[2]+1)[idim];
                        value +=
                        (1.0 - frac[0]) * frac[1] * frac[2] *
                        get_pixmap(pixmap, pos[0], pos[1]+1, pos[2]+1)[idim];
                        value +=
                        frac[0] * frac[1] * frac[2] *
                        get_pixmap(pixmap, pos[0]+1, pos[1]+1, pos[2]+1)[idim];
                        break;
                    }
                    
                    pixel->vertex[i][j][k][idim] = value;
                }
            }
        }
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Create iterator over the vertices of a geometry object
 * 
 * object: the object whose faces or sides are being iterated over
 * ndim:   dimensions of object returned by index
 * 
 */

void
new_list(geoindex *list, geometry *object, int odim) {
    int size[4][4] = {{1, 2, 4, 8}, {0, 1, 4, 0}, {0, 0, 1, 6}, {0, 0, 0, 1}};
    
    list->object = object;
    list->odim = odim;

    if (odim >= 0 && odim < 4) {
        list->index = size[odim][object->odim];
    } else {
        list->index = 0;
    }
    
    if (list->index == 0) {
        list->object = (geometry *) 0;
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Create a new polygon structure
 *
 * polygon: an empty polygon structure
 * pixel: the pixel that the polygon is derived from
 */

void
new_polygon(geopoly *polygon, geometry *object) {

    memset(polygon, 0, sizeof(geopoly));
    polygon->ndim = object->ndim;
    polygon->npoly = 0;

    return;
}

/** ---------------------------------------------------------------------------
 * Copy the next face out of an object
 *
 * item: the returned item from the list
 * list: the iterator over faces of the object
 */

void
next_face(geometry *item, geoindex *list) {

    item->ndim = list->object->ndim;
    item->odim = 2;

    switch (list->index) {
    case 0:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 0);
        vertex_copy(item, 1, 0, 0, list->object, 1, 0, 0);
        vertex_copy(item, 1, 1, 0, list->object, 1, 1, 0);
        vertex_copy(item, 0, 1, 0, list->object, 0, 1, 0);
        break;
    case 1:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 1);
        vertex_copy(item, 1, 0, 0, list->object, 1, 0, 1);
        vertex_copy(item, 1, 1, 0, list->object, 1, 1, 1);
        vertex_copy(item, 0, 1, 0, list->object, 0, 1, 1);
        break;
    case 2:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 0);
        vertex_copy(item, 1, 0, 0, list->object, 1, 0, 0);
        vertex_copy(item, 1, 1, 0, list->object, 1, 0, 1);
        vertex_copy(item, 0, 1, 0, list->object, 0, 0, 1);
        break;
    case 3:
        vertex_copy(item, 0, 0, 0, list->object, 0, 1, 0);
        vertex_copy(item, 1, 0, 0, list->object, 1, 1, 0);
        vertex_copy(item, 1, 1, 0, list->object, 1, 1, 1);
        vertex_copy(item, 0, 1, 0, list->object, 0, 1, 1);
        break;
    case 4:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 0);
        vertex_copy(item, 1, 0, 0, list->object, 0, 1, 0);
        vertex_copy(item, 1, 1, 0, list->object, 0, 1, 1);
        vertex_copy(item, 0, 1, 0, list->object, 0, 0, 1);
        break;
    case 5:
        vertex_copy(item, 0, 0, 0, list->object, 1, 0, 0);
        vertex_copy(item, 1, 0, 0, list->object, 1, 1, 0);
        vertex_copy(item, 1, 1, 0, list->object, 1, 1, 1);
        vertex_copy(item, 0, 1, 0, list->object, 1, 0, 1);
        break;
    }
    
    return;
}

/** ---------------------------------------------------------------------------
 * Return next item of a geometry object
 *
 * item: the returned item from the list
 * list: the iterator over sides of the object
 */

int
next_item(geometry *item, geoindex *list) {

    memset(item, 0, sizeof(geometry));

    if (list->index == 0) {
        return 0;
        
    } else {
        list->index -= 1;
        
        if (list->odim == list->object->odim) {
            next_object(item, list);
    
        } else if (list->odim < list->object->odim) {
            switch (list->odim) {
            case 0:
                next_point(item, list);
                break;
            case 1:
                next_side(item, list);
                break;
            case 2:
                next_face(item, list);
                break;
            }
        }
    }

    return 1;
}

/** ---------------------------------------------------------------------------
 * Copy the object out of a list
 *
 * item: the returned item from the list
 * list: the iterator over the object
 */

void
next_object(geometry *item, geoindex *list) {
    memcpy(item, list->object, sizeof(geometry));
    return;
}

/** ---------------------------------------------------------------------------
 * Copy the next point out of a list
 *
 * item: the returned item from the list
 * list: the iterator over points of an object
 */

void
next_point(geometry *item, geoindex *list) {
    item->ndim = list->object->ndim;
    item->odim = 0;

    switch (list->index) {
    case 0:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 0);
        break;
    case 1:
        vertex_copy(item, 0, 0, 0, list->object, 1, 0, 0);
        break;
    case 2:
        vertex_copy(item, 0, 0, 0, list->object, 0, 1, 0);
        break;
    case 3:
        vertex_copy(item, 0, 0, 0, list->object, 1, 1, 0);
        break;
    case 4:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 1);
        break;
    case 5:
        vertex_copy(item, 0, 0, 0, list->object, 1, 0, 1);
        break;
    case 6:
        vertex_copy(item, 0, 0, 0, list->object, 0, 1, 1);
        break;
    case 7:
        vertex_copy(item, 0, 0, 0, list->object, 1, 1, 1);
        break;
    }
    
    return;
}

/** ---------------------------------------------------------------------------
 * Copy the next side out of a list
 *
 * item: the returned item from the list
 * list: the iterator over sides of the object
 */

void
next_side(geometry *item, geoindex *list) {

    item->ndim = list->object->ndim;
    item->odim = 1;
    
    switch (list->index) {
    case 0:
        vertex_copy(item, 0, 0, 0, list->object, 0, 0, 0);
        vertex_copy(item, 1, 0, 0, list->object, 1, 0, 0);
        break;
    case 1:
        vertex_copy(item, 0, 0, 0, list->object, 1, 0, 0);
        vertex_copy(item, 1, 0, 0, list->object, 1, 1, 0);
        break;
    case 2:
        vertex_copy(item, 0, 0, 0, list->object, 1, 1, 0);
        vertex_copy(item, 1, 0, 0, list->object, 0, 1, 0);
        break;
    case 3:
        vertex_copy(item, 0, 0, 0, list->object, 0, 1, 0);
        vertex_copy(item, 1, 0, 0, list->object, 0, 0, 0);
        break;
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Compute the vertices of the pixel at a position
 *
 * pixel:    the object describing the pixel
 * ndim:     number of dimensions in position
 * position: coordinates of the center of the pixel
 */

void
pixel_at_pos(geometry *pixel, int ndim, int *position) {
    double dh[3];
    int i, j, k, idim, ivtx;
    int vertices[4] = {1, 2, 4, 8};
    
    memset(pixel, 0, sizeof(geometry));
    pixel->ndim = ndim;
    pixel->odim = ndim;

    ivtx = vertices[ndim];
    for (k = 0; k < 2; ++k) {
        dh[2] = 0.5 * (2 * k - 1);

        for (j = 0; j < 2; ++j) {
            dh[1] = 0.5 * (2 * j - 1);
            
            for (i = 0; i < 2; ++i) {
                dh[0] = 0.5 * (2 * i - 1);
                
                for (idim = 0; idim < ndim; ++idim) {
                    pixel->vertex[i][j][k][idim] = 
                            position[idim] + dh[idim];
                }

                if (-- ivtx == 0) return;
            }
        }
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Compute the overlap between two pixels
 *
 * pixel:        the pixel on the output image
 * mapped_pixel: input pixel mapped into output fram
 */

double
pixel_overlap(geometry *pixel, int *position) {

    geoindex list;
    geometry face;
    geopoly  polygon;
    double   extent = 0.0;
    
    new_list(&list, pixel, 2);
    while (next_item(&face, &list)) {
        new_polygon(&polygon, &face);
        clip_face(&polygon, &face, position);
        extent += extent_polygon(&polygon);
    }

    return extent;
}

/** ---------------------------------------------------------------------------
 * Show the contents of a list index

 * buf:   the buffer containing the string representation
 * list:  the list to show
 */

void
show_index(char buf[], int ix, geoindex *list) {
    
    sprintf(&buf[ix], "index = %d\nodim = %d\n", list->index, list->odim);

    ix = strlen(buf);
    if (list->object == (geometry *) 0) {
        sprintf (&buf[ix], "Invalid index\n");
    } else {
        show_pixel(buf, ix, list->object);
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Show the contents of a geometry object
 *
 * buf:   the buffer containing the string representation
 * pixel: the object to show
 */

void
show_pixel(char buf[], int ix, geometry *pixel) {

    int i, j, k, idim, ivtx;
    int vertices[4] = {1, 2, 4, 8};
   
    ivtx = vertices[pixel->odim];

    sprintf(&buf[ix], "ndim = %d\nodim = %d\n", pixel->ndim, pixel->odim);

    for (k = 0; k < 2; ++k) {
        for (j = 0; j < 2; ++j) {    
            for (i = 0;  i < 2; ++i) {
                ix = strlen(buf);
                sprintf(&buf[ix], "(%d,%d,%d) = ", i, j, k);

                for (idim = 0; idim < pixel->ndim; ++idim) {
                    ix = strlen(buf);
                    sprintf(&buf[ix], "%10.3f  ", pixel->vertex[i][j][k][idim]);
                }
                
                ix = strlen(buf);
                sprintf(&buf[ix], "\n");
                if (-- ivtx == 0) return;
            }
        }
    }

    return;
}

/** ---------------------------------------------------------------------------
 * Show the contents of a polygon
 * 
 * buf:   the buffer containing the string representation
 * poly:  the polygon to show
 */

void
show_polygon(char buf[], int ix, geopoly *polygon) {
    int ipoly, idim;

    sprintf(&buf[ix], "ndim = %d\nnpoly = %d\n", polygon->ndim, polygon->npoly);

    for (ipoly = 0; ipoly < polygon->npoly; ++ipoly) {
        ix = strlen(buf);
        sprintf(&buf[ix], "(%d) = ", ipoly);

        for (idim = 0; idim < polygon->ndim; ++idim) {
            ix = strlen(buf);
            sprintf(&buf[ix], "%10.3f  ", polygon->vertex[ipoly][idim]);
        }
                
        ix = strlen(buf);
        sprintf(&buf[ix], "\n");
    }
    
    return;
}

/** ---------------------------------------------------------------------------
 * Copy a single vertex from one geometry structure to another
 */

void
vertex_copy(geometry *output, int i_out, int j_out, int k_out,
            geometry *input, int i_in, int j_in, int k_in) {

    int idim;

    for (idim = 0; idim < input->ndim; ++idim) {
        output->vertex[i_out][j_out][k_out][idim] =
            input->vertex[i_in][j_in][k_in][idim];
    }

    return;
}
