Instructions for running "WormSim" software on a Linux system.

Installation guide:

1) Copy "WormSimPackage.zip" to the location of your choice. However, there must be NO SPACES ANYWHERE IN THE PATH for this directory!

2) Extract "WormSimPackage.zip"

3) Make sure the current working directory is "WormSim".

4) Enter the command "idaInstallDir=`pwd`/Sundials".

5) Enter the command "cd sundials-2.3.0".

6) Enter the command "./configure CC=g++ --prefix=$idaInstallDir --disable-mpi --disable-fcmix".

7) Look carefully at the resulting output and check for any error messages (there shouldn't be any...). Fix and repeat steps 7 and 8 if necessary.

8) Enter the command "make".

9) Look carefully at the resulting output and check for any error messages (there shouldn't be any...). Fix and repeat steps 7 to 10 if necessary.

10) Enter the command "make install".

11) Look carefully at the resulting output and check for any error messages (there shouldn't be any...). Fix and repeat steps 7 to 12 if necessary.

12) You should now be able to proceed to running the simulator.

Useage guide:

1) The whole integrated model is in "worm.cc". Edit this to change any aspects of the model e.g. different environments (water -> intermediate -> agar, with and without objects).

2) To compile the program, make sure you're in the "Model" directory.

3) Enter the command "make".

4) Check the resulting output for errors (some warnings are unfortunately inevitable, but they shouldn't be a problem), fix and re-run "make" if necessary.

5) Enter the command "./program" and wait for it to complete.

6) "program" will generate a file called "simdata.csv", and possibly also "objects.csv" (if objects are being used).

7) Open the appropriate viewer program, found in "WormSim/MatlabSupport/", in Matlab. If you don't have access to matlab, it should be possible to reproduce this viewer in another language by examining the code and translating it as appropriate.

8) Run the viewer to visualize the model behaviour.


