# Dynamic pages in Petri nets

This repository contains tools to work with dynamic pages in Petri nets.

There is no editor yet, but you can import a pnml-file and augment it with dynamic pages.

## Contents

### /transformation

For the transformation `GrGen` is used. Please see "Installation".

#### /petri_dynamic

Here the transformation from dynamic petri nets to hierarchical petri nets happens.

You can transform something by calling `GrShell paper_buko.grs` or `GrShell paper_feature.grs`.

### /tools

TODO

# Installation

* Install mono `brew install mono`
* Download GrGen from http://GrGen.net
	* add it to your PATH like this: `PATH="/Users/cmai/grgen/engine-net-2/bin:$PATH"`
        * If it works you can run "GrShell"

### Modelchecker:
- download: http://projects.laas.fr/tina/download.php
	- add it to your path
- install lola (http://download.gna.org/service-tech/lola/) or `brew install lola`



