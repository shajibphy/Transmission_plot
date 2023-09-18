# Transmission_plot

The algorithm should work in a way so that:
1) Load dark, light and Measurement image
2) Do the radiometric correction.
3) Do the image splitting in the corrected iamge based on the high intensity region.
4) Now, make the transmission of each pixel of light iamge as 1 and each pixel of dark image as 0 corresponding to the corrected image. Plot transmission curve for the splitted region which should range from 0 to 1 along the Y axis.
5) In this code the plots are not coming as expected. The broadband region(first region) has almost 1 transmittence which should be less than 1 and the third region also touching 1 which should be less than 1 also.
6) The code should be simplified and modified
