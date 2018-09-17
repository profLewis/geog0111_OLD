# Welcome to geog0111: Scientific Computing 
UCL Geography: Level 7 course, Scientific Computing

![](images/ucl_logo.png)

[Go to Binder version](https://mybinder.org/v2/gh/profLewis/geog0111.git/master)

## Course information

### Course Convenor

[Prof P. Lewis](http://www.geog.ucl.ac.uk/~plewis)

N.B. 2018-19 Course Convenors: Dr Qingling Wu and Dr. Jose Gomez-Dans

### Course and Contributing Staff

[Prof Philip Lewis](http://www.geog.ucl.ac.uk/~plewis)  

[Dr. Jose Gomez-Dans](http://www.geog.ucl.ac.uk/about-the-department/people/research-staff/research-staff/jose-gomez-dans/)

[Dr Qingling Wu](http://www.geog.ucl.ac.uk/about-the-department/people/research-staff/research-staff/qingling-wu/)

[Mr Feng Yin](https://www.geog.ucl.ac.uk/people/research-staff/feng-yin)


### Purpose of this course

This course, geog0111 Scientific Computing, is a term 1 MSc module worth 15 credits (25% of the term 1 credits) that aims to:

* impart an understanding of scientific computing
* give students a grounding in the basic principles of algorithm development and program construction
* to introduce principles of computer-based image analysis and model development

It is open to students from a number of MSc courses run by the Department of Geography UCL, but the material should be of wider value to others wishing to make use of scientific computing. 

The module will cover:

* Computing in Python
* Computing for image analysis
* Computing for environmental modelling
* Data visualisation for scientific applications

### Learning Outcomes

At the end of the module, students should:

* have an understanding of the Python programmibng language and experience of its use
* have an understanding of algorithm development and be able to use widely used scientific computing software to manipulate datasets and accomplish analytical tasks
* have an understanding of the technical issues specific to image-based analysis, model implementation and scientific visualisation

### Timetable

The course takes place over 10 weeks in term 1, in the Geography Department Unix Computing Lab (PB110) in the [Pearson Building](http://www.ucl.ac.uk/estates/roombooking/building-location/?id=003), UCL. 

Classes take place from the second week of term to the final week of term, other than Reading week. See UCL [term dates](http://www.ucl.ac.uk/staff/term-dates) for further information.

The timetable is available on the UCL Academic Calendar

### Assessment

Assessment is through two pieces of coursework, submitted in both paper form and electronically via Moodle. 

See the [Moodle page](https://moodle-1819.ucl.ac.uk/course/view.php?id=2796) for more details.

### Useful links

[Course Moodle page](https://moodle-1819.ucl.ac.uk/course/view.php?id=2796)  

### Using Python

[Python](http://www.python.org/) is a high level programming language that is freely available, relatively easy to learn and portable across different computing systems. In Python, you can rapidly develop solutions for the sorts of problems you might need to solve in your MSc courses and in the world beyond. Code written in Python is also easy to maintain, is (or should be) self-documented, and can easily be linked to code written in other languages.

Relevant features include: 

- it is automatically compiled and executed 
- code is portable provided you have the appropriate Python modules. 
- for compute intensive tasks, you can easily make calls to methods written in (faster) lower-level languages such as C or FORTRAN 
- there is an active user and development community, which means that new capabilities appear over time and there are many existing extensions and enhancements easily available to you.

For further background on Python, look over the material on [Advanced Scientific Programming in Python](https://python.g-node.org/wiki/schedule) or [python.org](http://www.python.org/) web sites.

For this course, we suggest you use the [anaconda](https://store.continuum.io/cshop/anaconda/) Python distribution (this is what is installed in the unix lab computers), though you are free to use whichever version of it you like on your own computers.

If you are intending to use these notes on your opwn computer, you will need a relatively comprehensive installation of Python (such as that from [anaconda](https://store.continuum.io/cshop/anaconda/)), and will also need [GDAL](http://www.gdal.org/) installed for some of the work. You may also find it of value to have [git](http://git-scm.com/) installed.

We are assuming that you are new to computing in this course. We will not explicitly go through unix (operating system) notes, but you should make yourself familiar with the basic concepts. 

### Using the course notes

We will generally use the `ipython` interpreter for running interactive Python programs.

You will probably want to run each session and store scripts in your `Data` (or `DATA`) directory.

If you are taking this course at UCL, the notes should already have been downloaded to your `DATA` directory.

If so, then:

```
berlin% cd ~/DATA/geog0111
berlin% git reset --hard HEAD
berlin% git pull
```

will update the notes (for any changes I make over the sessions).

If you need to download the notes and want to run the session directly in the notebook, you will need to download the course material from [github](https://github.com/profLewis/geog0111) and run the notebook with e.g.:

```
berlin% cd ~/DATA
berlin% git clone https://github.com/profLewis/geog0111.git
```

to obtain the notes. 

You should next check that you are using the version of Python that we intend:

```
berlin% which ipython
/opt/anaconda/bin/ipython
```

If this isn't the version of Python that you are picking up (note the use of the unix command `which` here), then you can either just type the full path name:

```
berlin% /opt/anaconda/bin/ipython  
```

in place of where it says `ipython` in these notes, or modify your shell initialisation file (`~/.bashrc` if you are using `bash` or `~/.cshrc` for `tcsh` or `csh`) to include `/opt/anaconda/bin` early on in the `PATH`. For running notebooks, we use `jupyter` rather than `ipython`.

To go to the directory for the first session:  

`berlin% cd ~/Data/geogg122`  
`berlin% jupyter notebook Chapter1_Python_intro.ipynb`  

You quit an `jupyter` notebook session with `^C` (`Control C`).

To exectute ('run') blocks of Python code in the notebook, use `^<return>` (`SHIFT` and `RETURN` keys together).

Alternatively, just run `ipython`:  
```
berlin% cd ~/DATA/geog0111
berlin% ipython
```

and type your own commands in at the prompt, following the class or the material on the webpages.


### Course Notes

[Course notes](index.ipynb)  


### Help

[Connections to the lab](Connection.ipynb)

[Installation issues](Issues.ipynb)
