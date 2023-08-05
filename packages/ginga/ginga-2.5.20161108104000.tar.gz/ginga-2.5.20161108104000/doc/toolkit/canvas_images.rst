================================
How Ginga maps an image to color
================================

The process of mapping an image to color in Ginga involves three
steps:

1) setting the *cut levels*, which scales all values in the image to a
   specified range,
2) a *color distribution algorithm*, which distributes values within
   that range to indexes into a color map table, and 
3) an *intensity map* and *color map*, which are applied to these
   indexes to map the final values to RGB pixels. 

