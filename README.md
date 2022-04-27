*Below are the instructions on how to run this project*

*DISCLAIMER*: Make sure you have all the modules listed below installed

numpy,
argparse,
matplotlib,
copy,
cv2,
os,
pymaxflow (requires Windows Visual Studio C++ tools installed),
networkx  (requires Windows Visual Studio C++ tools installed),

>open command prompt and use command <pip install *module-name*> for getting the above modules

STEP 1: Creating Mask

> Choose the two pictures you would like to blend, and put them in a directory.
> Make sure both of the images are of same dimensions.
> Rename them to 'pic1' & 'pic2'
> Now open command prompt and navigate to the directory containing the 'mask_file' python file. 
> Run the following command "python mask_file -i "directory of the image files"

STEP 2: Selecting the Mask Area

> A window containing the src image appears
> The selection works on a two click basis, click at the two end points of a region,
  one after the other, you want to select 
> After that, click on next/end button and repeat the above step for the second image too
  (thes yellow & blue patches are the dimensions you selected)
> Now click on next/end after finishing.

STEP 3: Graph Cut Output

> Now, On the same command line, 
  Run the following command "python graphcut_file -i "directory of the three image files(src,target,mask)"
> You can notice a file 'output.jpg' has been created in the directory. 

*I have provided my output and mask images for the two tasks that I have performed*
 note: Make sure to rename the input images to 'pic1' & 'pic2' before you execute.  
 
 **The Outputs I got are named as output_A & output_B**

THANK YOU..!
