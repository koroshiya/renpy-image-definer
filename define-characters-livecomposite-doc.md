<h3>Format</h3>
<pre>
This script assumes you have a folder for characters, and each character has their own folder.
Inside of a character's folder are three more folders: outfits, poses, expressions.
Each of those folders has a bunch of images.

eg.
characters/sara/poses/arms_crossed.png
characters/sara/poses/casual.png
characters/sara/outfits/school_uniform.png
characters/sara/expressions/sad.png
characters/sara/expressions/happy.png

In this example, we'd call the function

define_characters("characters/")

which would create and define the images:
-sara arms_crossed school_uniform sad
-sara arms_crossed school_uniform happy
-sara casual school_uniform sad
-sara casual school_uniform happy

Images should all be the same size.
In the above example, happy.png, school_uniform.png, etc. are all 370x512px in size.
Since they're transparent PNGs, these files can overlap just fine, and the individual sizes are small.
If you're saving character sprites as PSD files, just toggle the layers on one at a time when saving 
and you'll already have the right size, spacing, etc.

However, the above only works if all poses use the same outfits.
In this example, we assume outfits change with their poses.

Running the script with the images:
/characters/sara/poses/arms_crossed/pose.png
/characters/sara/poses/arms_crossed/school_uniform.png
/characters/sara/poses/casual/pose.png
/characters/sara/poses/casual/school_uniform.png
/characters/sara/expressions/happy.png
would result in:
-sara arms_crossed school_uniform happy
-sara casual school_uniform happy

This approach assumes that outfits change to match the body movement of a pose, but expressions remain the same.
If you wanted to have expressions change with the pose as well (eg. the character moves their head), then you would follow the same procedure as with the outfits.

</pre>
<h3>How it works</h3>
<pre>
Simply put, we tell the script where to find and how to group a bunch of images, then we smush them together.
ie. We get sara's pose, put the uniform on top of that, slap an expression onto her face, 
and as a result we have a normal character sprite.

To go into more detail,
in the above, we tell the script to check the folder "characters" for character sprites.
The script finds the "sara" folder in there and thus assumes that she's a character.
Within the sara folder the script finds "outfits", "expressions" and "poses", searching each of those folders.
Once it's done searching, the script has a dictionary of characters, poses, etc. It looks a little like this:

characters: {
  'sara': {
    'poses': {
      'arms_crossed': 'characters/sara/poses/arms_crossed.png',
      'arms_crossed': 'characters/sara/poses/casual.png'
    },
    'outfits': {
      'school_uniform': 'characters/sara/outfits/school_uniform.png'
    },
    'expressions': {
      'sad': 'characters/sara/expressions/sad.png',
      'happy': 'characters/sara/expressions/happy.png'
    }
  }
}

Now that the script knows where each of sara's outfits & such are located, it can start building & defining her sprites.
At this point the script loops over each character and their outfits, poses, etc. creating them as it goes.
Then, we at last reach the LiveComposite method, which pushes the images all together.
</pre>
