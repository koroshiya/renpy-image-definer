# Renpy Image Definer
Automates the definition of character sprites, backgrounds, and any other images used in a Renpy game

These scripts help to automate the process of defining images to be used within a Renpy game.
The idea is that manually defining every single image to be used in a game is only worth it if
the game is relatively short or low on images.
When you consider a game with dozens of characters, each one of whom has several outfits, poses and expressions,
the number of image definitions skyrockets, making it harder to keep track and time-consuming to do.

These scripts instead allow you to automatically define images based on a directory structure, so defining
a new image is as simple as copying it into the right folder.
If you have a folder called "backgrounds" in your "game" folder, using this script you could simply copy and
paste any new background images into that folder, and it would automatically be defined.

In the case of define-characters-livecomposite.py, we can go even further than that.
When creating character sprites, different variations of the same image quickly add up, resulting
in a large number of images of a decent size.
For example, if you have 1 character with 3 outfits, 5 poses and 10 expressions, that's 150 sprites for one character.
By using this script, not only can you avoid defining every variation, you can also cut down on the total number of
images, and wind up with far smaller files.

<h3>Example of basic automatic definition</h3>

At its simplest, you only need to point the function defined in a script to a directory and let it go from there.
Taking define-all-simple.py as an example, let's say we have a "bg" folder containing your project's backgrounds.
To define all of the images within that folder, you would run:

define_images('bg/', 0, False)

This tells the script to search the "bg" folder for any images, and to define each one.
For example, if we had an image called "school.png" in that folder, the script would define an image called:
bg school
Which you would then call with:
scene bg school

If you wanted to exclude the "bg" from the statement, you would simply change the "0" in the function to "1",
thus telling the script to exclude the first word in the statement. So

define_images('bg/', 1, False)

would allow us to display the image with:
scene school

<h3>Example of LiveComposite character defining</h3>

As mentioned before, when it comes to character sprites, these scripts can go a bit further in assisting you.
Since character sprites are generally composed of multiple layers (base, outfit, pose, expression), and since
many of those layers are common across different sprites of the same character, it's best to automate the
creation and definition of these images.

For this example, let's say I have an image called sara.psd.
The image is 370x512 in size.
The layers are:
-A base layer (the "naked" sprite with no decorations)
-Outfits
-Outfit extras (something to go on top of the outfit, eg. an apron over the outfit)
-Poses
-Expressions

Using the numbers from earlier, let's say she has 3 outfits, 5 poses, 10 expressions.
Exporting each variation would yield 150 images in total. At 370x512, each one of those images,
as a full-quality PNG-24 file, would be at least 100KB, leaving us with 15MB of images.

Rather than combining and exporting each individual sprite, what we should instead do is export the base
and each outfit, pose and expression separately, then let the script combine them.
This way we only need to export 19 images, rather than 150, and each image would be significantly smaller.
Even if they somehow were still 100KB each, we'd have already reduced the total from 15MB to 1.9MB,
and saved ourselves the hassle of exporting an excessive number of images.

To achieve this, I might have a 'sprites' directory within my game's 'game' folder.
Within that directory I'd have a folder called 'sara', and within that I'd have folders called 'expressions',
'outfits_extra' and 'poses'.
The structure would look like this:
/game/sprites/
              sara/
                   expressions/
                               happy.png
                               sad.png
                   poses/arms_crossed/
                                      pose.png
                                      uniform.png
                                      dress.png
                   outfits_extra/
                                 apron.png
                   base.png

If we then ran
define_characters("sprites/")
we would be able to call statements such as:
show sara uniform arms_crossed happy
show sara uniform apron arms_crossed happy
show sara uniform apron arms_crossed sad
show sara flip uniform arms_crossed happy
and so on.
