# -----------------------------------------------------------------
# $Revision: 1.15 $
# $Date: 2006/07/27 22:20:57 $
# -----------------------------------------------------------------
# Programmer(s): Radu Serban and Aaron Collier @ LLNL
# -----------------------------------------------------------------
# Copyright (c) 2002, The Regents of the University of California.
# Produced at the Lawrence Livermore National Laboratory.
# All rights reserved.
# For details, see the LICENSE file.
# -----------------------------------------------------------------
# Main Makefile for SUNDIALS suite
#
# Makefile.  Generated from Makefile.in by configure.
# -----------------------------------------------------------------

SHELL = /bin/sh



srcdir       = .
abs_builddir = /home/cserv2_a/soc_staff/scsjhb/Programming/TestingCodeForPaper/WormSim/sundials-2.3.0
prefix       = /home/cserv2_a/soc_staff/scsjhb/Programming/TestingCodeForPaper/WormSim/Sundials
exec_prefix  = ${prefix}
includedir   = ${prefix}/include
libdir       = ${exec_prefix}/lib

SLV_MODULES  = src/sundials src/nvec_ser src/cvode src/cvodes src/ida src/kinsol
EXS_MODULES  = 

ALL_MODULES  = src/sundials src/nvec_ser src/cvode src/cvodes src/ida src/kinsol 

EXS_INSTDIR  = 

# -----------------------------------------------------------------

all:
	@for i in ${ALL_MODULES} ; do       \
	   if test -d $${i} ; then          \
	     echo "----------------------"; \
	     echo "Make $${i}..." ;         \
	     echo "----------------------"; \
	     cd $${i} ;                     \
	     ${MAKE} ;                      \
	     cd ${abs_builddir} ;           \
	     echo "" ;                      \
	   fi ;                             \
	 done

install:
	@for i in ${SLV_MODULES} ; do                                         \
	   if test -d $${i} ; then                                            \
	     echo "----------------------";                                   \
	     echo "Install $${i}..." ;                                        \
	     echo "----------------------";                                   \
	     cd $${i} ;                                                       \
	     ${MAKE} install ;                                                \
	     cd ${abs_builddir} ;                                             \
	     echo "" ;                                                        \
	   fi ;                                                               \
	 done
	@if test "X${EXS_MODULES}" = "X" ; then                               \
	   : ;                                                                \
	 else                                                                 \
	   if test "X${EXS_INSTDIR}" = "Xno"; then                            \
	     echo "" ;                                                        \
	     echo "" ;                                                        \
	     echo "Examples were built but installation was disabled." ;      \
	     echo "" ;                                                        \
	     echo "" ;                                                        \
	   else                                                               \
	     for i in ${EXS_MODULES} ; do                                     \
	       echo "----------------------";                                 \
	       echo "Install $${i}..." ;                                      \
	       echo "----------------------";                                 \
	       cd $${i} ;                                                     \
	       ${MAKE} install ;                                              \
	       cd ${abs_builddir} ;                                           \
	       echo "" ;                                                      \
	     done ;                                                           \
	   fi ;                                                               \
	 fi

clean:
	@for i in ${ALL_MODULES} ; do \
	   if test -d $${i} ; then    \
	     cd $${i} ;               \
	     ${MAKE} clean ;          \
	     cd ${abs_builddir} ;     \
	   fi ;                       \
	 done

uninstall:
	@for i in ${ALL_MODULES} ; do \
	   if test -d $${i} ; then    \
	     cd $${i} ;               \
	     ${MAKE} uninstall ;      \
	     cd ${abs_builddir} ;     \
	   fi ;                       \
	 done

# ---------------------------------------------------------------------

distclean:
	@for i in ${ALL_MODULES} ; do  \
	   if test -d $${i} ; then     \
	     cd $${i};                 \
	     ${MAKE} distclean;        \
	     cd ${abs_builddir} ;      \
	   fi ;                        \
	 done
	rm -f config.log
	rm -f config.status
	rm -f config.cache
	rm -f config.h
	rm -f libtool
	rm -f sundials-config
	rm -f src/sundials/sundials_config.h
	rm -f examples/fortran_update.sh
	rm -f Makefile
