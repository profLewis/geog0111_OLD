# Welcome to geog0111: Scientific Computing 
UCL Geography: Level 7 course, Scientific Computing

![](https://raw.github.com/profLewis/geogg122/master/images/ucl_logo.png)

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

### Python version

These notes assume you are using python version 3.7

To verify that the current environment uses the new Python version, in your Terminal window or an Anaconda Prompt, run:

`python --version`

If this doesn't show 3.7.* then you may need to update your environment and/or install a new version of python.

#### Installing a different version of Python

To install a different version of Python without overwriting the current version, create a new environment and install the second Python version into it:

Create the new environment:

1.  To create the new environment for Python 3.7, in your Terminal window or an Anaconda Prompt, run:

    `conda create -n py37 python=3.7 anaconda`

    NOTE: Replace py37 with the name of the environment you want to create. anaconda is the metapackage that includes all of the Python packages comprising the Anaconda distribution. python=3.7 is the package and version you want to install in this new environment. This could be any package, such as numpy=1.7, or multiple packages.
    
    To create the new environment for Python 2.7, in your Terminal window or an Anaconda Prompt, run:
    
    `conda create -n py37 python=3.7 anaconda`
    
2.  [Activate the new environment.](https://conda.io/docs/user-guide/tasks/manage-environments.html#activate-env)

3.   Verify that the new environment is your [current environment.](https://conda.io/docs/user-guide/tasks/manage-environments.html#determine-current-env)

      To verify that the current environment uses the new Python version, in your Terminal window or an Anaconda Prompt, run:

    python --version

### Structure of the Course

[Course notes](index.ipynb)  
