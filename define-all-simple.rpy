init python early:

    ###
    #Purpose: defines any images found within a specific folder.
    #Parameters:
    #  imageFolder: folder in which to search for images to define
    #  excludeFirstXFolders: number of initial folders to exclude from the definition path
    #  flip: whether or not to also create a flipped version of the image
    ###

    def define_images(imageFolder, excludeFirstXFolders=0, flip=True):
            for path in renpy.list_files():
                if path.startswith(imageFolder + "/"):
                    path_list = path.split("/")
                    path_list[-1] = os.path.splitext(path_list[-1])[0]
                    path_list = tuple(path_list[excludeFirstXFolders:])
                    renpy.image(path_list, path)
                    if flip:
                        renpy.image(path_list + ("flip", ), im.Flip(path, horizontal=True))

    ###
    #Usage:
    #
    #define_images('sprites/', 1)
    #This statement tells the function that there's a 'sprites' folder within the Renpy game's "game" folder.
    #The "1" tells the script to ignore the word 'sprites' when defining images.
    #
    #For example, let's say we have a folder game/sprites/sara/. In there we have a folder called "uniform",
    #and in that folder we have an image "happy.png", which is a smiling sprite wearing a school uniform.
    #After running define_images('sprites/', 1), we'd be able to call the sprite with:
    #show sara uniform happy
    #and also the flipped version with:
    #show sara uniform happy flip
    #
    #Another example: let's say we wanted to define some backgrounds as well.
    #We have a folder game/bg/, and in it there's the image "school.png".
    #We could use the function:
    #define_images('bg/', 0, False)
    #after which we'd be able to call the image with
    #scene bg school
    #Because excludeFirstXFolders was set to 0, the "bg" part of the name wasn't removed.
    #Also, since flip was set to false, there's no flipped version available.
    ###
