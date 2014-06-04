octopress_nikola
================

Scripts to migrate from octopress to nikola
octopress_nikola
================

Scripts to migrate from octopress to nikola. The script takes a directory of octopress markdown posts and converts them into RestructuredText posts suitable for `nikola <http:getnikola.com>`_. Usage:
::
   convert.py <path_to_octopress_posts_dir> <path_to_nikola_posts_dir>

The script needs `pandoc <http://johnmacfarlane.net/pandoc/README.html>`_ to be installed since it uses pandoc to do the heavy lifting for conversion to RestructuredText. Currently, octopress img blocks are supported `{% img path alt %}`
