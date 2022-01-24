#!/usr/bin/env python3
#
############################################################################
#
# MODULE:      v.divide.training_validation
# AUTHOR(S):   Anika Bettge
#
# PURPOSE:     Divides data into training and validation data
# COPYRIGHT:   (C) 2019 by Hajar Benelcadi and Anika Bettge, mundialis
#
#              This program is free software under the GNU General Public
#              License (>=v2). Read the file COPYING that comes with GRASS
#              for details.
#
#############################################################################
# %module
# % description: divides data into training and validation data.
# % keyword: vector
# % keyword: sampling
# % keyword: statistics
# % keyword: random
# % keyword: stratified random sampling
# %end

# %option G_OPT_V_INPUT
# %end

# %option G_OPT_DB_COLUMN
# % description: Name of column with class information
# %end

# %option G_OPT_V_OUTPUT
# % key: training
# %end

# %option G_OPT_V_OUTPUT
# % key: validation
# %end

# %option
# % key: training_percent
# % type: integer
# % required: no
# % description: Percent of data which should be selected as training data
# % answer: 30
# %end

import grass.script as grass
import os
import random
import atexit

newcol = None


def cleanup():
    grass.message(_("Cleaning up..."))
    if newcol:
        columns_existing = grass.vector_columns(options["input"]).keys()
        if newcol in columns_existing:
            grass.run_command(
                "v.db.dropcolumn", map=options["input"], columns=newcol
            )


def extract_data(input, output, cats, value):
    if len(cats) > 20000:
        newcol = "train_val_%s" % (os.getpid())
        columns_existing = grass.vector_columns(options["input"]).keys()
        if newcol not in columns_existing:
            grass.run_command(
                "v.db.addcolumn", map=input, columns="%s INTEGER" % (newcol)
            )
        n = 500
        for i in range(0, len(cats), n):
            cats_list = cats[i:i + n]
            grass.run_command(
                "v.db.update",
                where="cat IN (%s)" % (",".join(cats_list)),
                map=input,
                column=newcol,
                value=value,
                quiet=True,
            )
            grass.percent(i + n, len(cats), 1)
        grass.run_command(
            "v.extract",
            input=input,
            output=output,
            where="%s='%d'" % (newcol, value),
        )
    else:
        grass.run_command(
            "v.extract", input=input, cats=",".join(cats), output=output
        )


def main():
    global newcol

    input = options["input"]
    column = options["column"]
    training = options["training"]
    validation = options["validation"]
    training_percent = options["training_percent"]

    # get classes
    grass.message("Getting classes...")
    classes = grass.parse_command(
        "v.db.select", map=input, column=column, flags="c"
    )

    grass.message("Selecting points for each class...")
    training_cats = []
    validation_cats = []
    for cl in classes:
        where_str = "%s = '%s'" % (column, cl)
        classI = grass.parse_command(
            "v.db.select", map=input, columns="cat", flags="c", where=where_str
        )
        cats_classI = [x for x in classI]
        random.shuffle(cats_classI)
        num_classI = len(cats_classI)
        num_trainingdata = round(int(training_percent) / 100.0 * num_classI)
        cats_tr = cats_classI[:num_trainingdata]
        cats_val = cats_classI[num_trainingdata:]
        training_cats.extend(cats_tr)
        validation_cats.extend(cats_val)

    grass.message(_("Extracting training points..."))
    extract_data(input, training, training_cats, 1)
    grass.message(_("Extracting validation points..."))
    extract_data(input, validation, validation_cats, 2)

    grass.message("Divided data into <%s> and <%s>" % (training, validation))


if __name__ == "__main__":
    options, flags = grass.parser()
    atexit.register(cleanup)
    main()
