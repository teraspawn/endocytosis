#! /bin/bash

convert -delay 20 -dispose Previous -alpha opaque -size 10000 ./output/???0.eps ./output/animation.gif
