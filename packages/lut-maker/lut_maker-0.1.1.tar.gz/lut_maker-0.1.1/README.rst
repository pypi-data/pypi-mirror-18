.. image:: https://travis-ci.org/faymontage/lut-maker.svg?branch=master
    :target: https://travis-ci.org/faymontage/lut-maker

.. image:: https://raw.githubusercontent.com/faymontage/lut-maker/master/readme_images/header.jpg
  :width: 100%

===========
Description
===========

lut_maker is a Python CLI tool for generating 3D RGB color look-up tables (LUTs).
Such a table can capture the 'look' of anything that alters color, such as a set
of Photoshop adjustments, or a particular analog film. The LUT can then be used
as a 'filter' in tools such as Adobe Photoshop, Adobe Premiere, or OpenGL.
Think of it like an Instagram filter.

This tool is currently crazy alpha, and is missing a lot of the fancy stuff
needed in a pro workflow.

Python >3.4 only at the moment.


===========
Basic Usage
===========

Install the CLI tool from PyPi:

.. code:: bash

  pip install lut_maker


Step 1: Generate measurement assets
-----------------------------------

Navigate to the directory where you want the measurement assets to be created, and then issue the :code:`lut_maker new` command (the defaults are sensible).

.. code:: bash

  mkdir my-lut
  cd my-lut
  lut_maker new

Step 2: Modify measurement colors
---------------------------------

Modify the resulting :code:`lut_measurement_0.png` file to change the colors. Just
keep in mind to only make adjustments that are applied to every pixel equally, such
as curves, levels, saturation, contrast, brightness. Position-dependent effects
such as blurs, clarity, 'local contrast' etc. are not valid.

In this example, I'll expose :code:`lut_measurement_0.png` onto polaroid film
and then scan, align, and save it back into the same file.


Step 3: Compute LUT
-------------------

When you are happy with your color modifications, in the same directory run:

.. code:: bash

  lut_maker compute

That's it! The newly created lut.* files are ready for use. A few guides:

- `How Do I Apply 3D LUTs in Adobe Photoshop? <https://lutify.me/knowledge-base/how-do-i-apply-3d-luts-in-adobe-photoshop/>`_
- `Using Lookup Tables to Accelerate Color Transformations (GPU) <http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter24.html>`_

Here is a LUT based on Impossible Project Color polaroid film, applied to an image in Photoshop:

.. image:: https://raw.githubusercontent.com/faymontage/lut-maker/master/readme_images/photo_application.jpg
  :width: 100%


===============
Options & Notes
===============

The generation step generates a uniform 3D lattice filling the entire linear 8bpc RGB space.
In many cases it is impractical to sample/transport/store every location (256^3 = 16777216 samples).
A common standard is to sample only 17 locations along each color axis, and then later interpolate
between them. You should only need to use more than the default 17 if the modifications you make
are extreme or discontinuous.

Using the default settings will generate 3 files:

- lut_alignment_guide.png - transparent overlay that shows the sampling locations, to help you align an analog photo/scan
- lut_measurement_0.png - the palette image to be modified
- lut_metadata.json - metadata about the LUT, used by later steps

The defaults are sensible for most cases, but the :code:`lut_maker new` command
has the following options::

    --name TEXT           Name of LUT to generate
    --lut-size INTEGER    Size of each dimension in 3D LUT
    --image-size INTEGER  Width & height of square output image in pixels
    --stack INTEGER       Number of unique measurement palettes to output
    --data-dir TEXT       Location for LUT files

If you will be modifying the measurement assets using an analog technique, it will
probably susceptible to imperfections from dust, vignetting, chromatic abberrations
scratches etc. To help combat these, increase the :code:`--stack` setting from the
default of 1. This will output multiple measurement images, each with the positions
of the colors randomized. During the compute phase, it will average the results from
each image together to create the final LUT.
