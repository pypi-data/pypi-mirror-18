/*
 * Python object definition of the items sequence and iterator
 *
 * Copyright (C) 2008-2016, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#if !defined( _PYOLECF_ITEMS_H )
#define _PYOLECF_ITEMS_H

#include <common.h>
#include <types.h>

#include "pyolecf_item.h"
#include "pyolecf_libolecf.h"
#include "pyolecf_python.h"

#if defined( __cplusplus )
extern "C" {
#endif

typedef struct pyolecf_items pyolecf_items_t;

struct pyolecf_items
{
	/* Python object initialization
	 */
	PyObject_HEAD

	/* The pyolecf item object
	 */
	pyolecf_item_t *item_object;

	/* The get sub item by index callback function
	 */
	PyObject* (*get_sub_item_by_index)(
	             pyolecf_item_t *item_object,
	             int sub_item_index );

	/* The (current) sub item index
	 */
	int sub_item_index;

	/* The number of sub items
	 */
	int number_of_sub_items;
};

extern PyTypeObject pyolecf_items_type_object;

PyObject *pyolecf_items_new(
           pyolecf_item_t *item_object,
           PyObject* (*get_sub_item_by_index)(
                        pyolecf_item_t *item_object,
                        int sub_item_index ),
           int number_of_sub_items );

int pyolecf_items_init(
     pyolecf_items_t *pyolecf_items );

void pyolecf_items_free(
      pyolecf_items_t *pyolecf_items );

Py_ssize_t pyolecf_items_len(
            pyolecf_items_t *pyolecf_items );

PyObject *pyolecf_items_getitem(
           pyolecf_items_t *pyolecf_items,
           Py_ssize_t item_index );

PyObject *pyolecf_items_iter(
           pyolecf_items_t *pyolecf_items );

PyObject *pyolecf_items_iternext(
           pyolecf_items_t *pyolecf_items );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _PYOLECF_ITEMS_H ) */

