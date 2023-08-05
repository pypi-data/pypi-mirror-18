/*
 * util.c
 *
 * Copyright (C) 2013-2016 Fabian Gieseke <fabian.gieseke@di.ku.dk>
 * License: GPL v2
 *
 */

#include "include/util.h"
#include "include/global.h"

/**
 * Sets default parameters.
 *
 * @param *params Pointer to struct containing the parameters
 */
void set_default_parameters(BRUTE_PARAMETERS *params) {

	params->n_neighbors = 10;
	params->num_threads = 1;
	params->verbosity_level = 1;

}

/**
 * Checks parameters.
 *
 * @param *params Pointer to struct containing the parameters
 */
void check_parameters(BRUTE_PARAMETERS *params) {

	if ((params->n_neighbors < 1) || (params->n_neighbors > 100)) {
		printf("Error: The parameter k must be > 0 and <= 100)\nExiting ...\n");
		exit(1);
	}

}
