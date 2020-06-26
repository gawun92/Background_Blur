
The goal of this project is setting a template in the picture(captured from video) with grayscale.
And blur the background except template; figuring out how to be filmed the template.

First, mannually setting the window and template. The window(blue) is represeting the range
of the template's location changes in all frames (captured from the whole video)
and the template(red) is the target object.

<img src="squares.png" width="500" height="400">

The orange is the template.

<img src="Template_.png" width="50" height="50">



The left side is the image in some period of frames and the right side is the new
representation of image with match_template(). When getting the images from match_template,
it was not necessary to use the whole image so that the window of the image is used.
The highest value (brightest) point is the location of template. and by saving each of 
points in each picture would allow us the location change of template.

<img src="4.png" width="300" height="200"> <img src="1.1.png" width="300" height="200">
<img src="5.png" width="300" height="200"> <img src="5.1.png" width="300" height="200">
<img src="6.png" width="300" height="200"> <img src="6.1.png" width="300" height="200">

Comparing each point to the first start point, visualizing the location change of template.

<img src="graph.png" width="500" height="300">

Based on the information, shifting the each of images and combining them.

<img src="combine.png" width="500" height="300">

Except the template(orange), background has been blurred and the image(shape?) of the template is clear than others.
