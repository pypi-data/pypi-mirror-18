 Summary
        -------
        
        This package provides tools for the analysis of raw nanopore sequencing
        data, including correction of basecalls and visualization.
        
        Installation
        ------------
        
        Install nanoraw via pip
        
        ::
        
            pip install nanoraw
        
        Install bleeding edge via github
        
        ::
        
            pip install git+https://github.com/marcus1487/nanoraw.git
        
        Usage
        -----
        
        ::
        
            nanoraw -h
            nanoraw [command] [options]
        
        
        Main Comand (Must be run before any other commands):
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        -   genome\_resquiggle             Re-annotate raw signal with genomic aignement of existing basecalls.
        
        Genome Anchored Plotting Commands:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        -   plot\_max\_coverage             Plot signal in regions with the maximum coverage.
        -   plot\_genome\_location          Plot signal at defined genomic locations.
        -   plot\_kmer\_centered            Plot signal at regions centered on a specific kmer.
        -   plot\_max\_difference           Plot signal where signal differs the most between two groups.
        -   plot\_most\_significant         Plot signal where signal differs the most significantly between two groups.
        -   plot\_kmer\_with\_stats         Plot signal from several regions and test statistics centered on a k-mer of interst.
        
        Sequencing Time Anchored Plotting Command:
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        -   plot\_correction               Plot segmentation before and after correction.
        -   plot\_multi\_correction        Plot multiple raw signals anchored by genomic location.
        
        Other Plotting Command:
        ^^^^^^^^^^^^^^^^^^^^^^^
        
        -   plot\_kmer                     Plot signal quantiles acorss kmers.
        -   cluster\_signif                Clustering traces at bases with significant differences.
        
        Auxiliary Command:
        ^^^^^^^^^^^^^^^^^^
        
        -  write\_most\_significant       Write sequence where signal differs the most significantly between two groups.
        -  write\_wiggle                  Write wiggle file of genome coverage from genome_resquiggle mappings.
        
            Get additional help for subcommands with ``nanoraw [command] -h``
        
        Requirements
        ------------
        
        -  HDF5 (http://micro.stanford.edu/wiki/Install_HDF5#Install)
        -  graphmap (https://github.com/isovic/graphmap)
        
        python Requirements:
        ^^^^^^^^^^^^^^^^^^^^
        
        -  numpy
        -  scipy
        -  h5py
        -  rpy2
        
        Optional python Package:
        ^^^^^^^^^^^
        
        -  Biopython (for robust FASTA parsing, but a simple parser is provided)
        
        Optional R Packages (install with `install.packages([package_name])` from an R prompt):
        ^^^^^^^^^^^
        
        -  changepoint (for using R's changepoint package for re-segmentation)
        -  ggplot2 (required for all plotting subcommands)
        -  cowplot (required for plot_kmer_with_stats subcommand)
        
        Legal
        -----
        
        nanoraw v.1 Copyright (c) 2016, The Regents of the University of
        California, through Lawrence Berkeley National Laboratory (subject to
        receipt of any required approvals from the U.S. Dept. of Energy). All
        rights reserved.
        
        If you have questions about your rights to use or distribute this
        software, please contact Berkeley Lab's Innovation and Partnerships
        department at IPO@lbl.gov referring to " nanoraw v.1 (2016-199)."
        
        NOTICE. This software was developed under funding from the U.S.
        Department of Energy. As such, the U.S. Government has been granted for
        itself and others acting on its behalf a paid-up, nonexclusive,
        irrevocable, worldwide license in the Software to reproduce, prepare
        derivative works, and perform publicly and display publicly. Beginning
        five (5) years after the date permission to assert copyright is obtained
        from the U.S. Department of Energy, and subject to any subsequent five
        (5) year renewals, the U.S. Government is granted for itself and others
        acting on its behalf a paid-up, nonexclusive, irrevocable, worldwide
        license in the Software to reproduce, prepare derivative works,
        distribute copies to the public, perform publicly and display publicly,
        and to permit others to do so.
        
