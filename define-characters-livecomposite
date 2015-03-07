###
#In this script, there's a set format in which images should be stored.
#This script is specifically designed for characters, and the images themselves
#are expected to be in a specific format.
#
#Images should be exported to multiple different layers.
#eg. A layer for the base sprite, one for the outfit, one for the pose, one for the expression.
#There's a bit of leeway here. At a minimum, you could have a base sprite with expressions.
#
#The structure is as follows:
#-A directory for sprites
#-Separate character directories within that directory
#
#After that, the format can shift a bit. For example, a very basic character could include:
#-A base.png file (the sprite itself) in the character directory
#-An "expressions" folder within the character directory
#-Multiple expression files within the "expressions" folder.
#
#Another possible format would be:
#-A poses folder, containing a folder for each pose
#-Within each of those folders, a "pose.png" file for the base sprite, and other images (eg. uniform.png)
#   for each outfit
#-Once again, an expressions folder containing each expression
###

def define_image(size, path_tuple, argList):
        path_tuple = tuple(entry for entry in path_tuple if entry is not None)
        args = []
        for i in xrange(1, len(argList), 2):
            if argList[i] is not None:
                args.extend([(0, 0), argList[i]])
        renpy.image(path_tuple, LiveComposite(size, *args))
        #if 'lucas' in path_tuple:
        #    print 'Defining image', path_tuple, 'from', tuple(args)

        flipArr = args
        for i in xrange(1, len(args), 2):
            flipArr[i] = im.Flip(args[i], horizontal=True)
        plist = list(path_tuple)
        plist.insert(1, 'flip') #flip after char name. eg. sara flip arms_crossed etc.
        renpy.image(tuple(plist), LiveComposite(size, *flipArr))

def define_characters(characterImageFolder, size=(370, 512), flip=True):
        characters = {}

        for path in renpy.list_files():
            if path.startswith(characterImageFolder):
              path_list = path.split("/")

              if path.startswith(characterImageFolder + path_list[-4] + "/poses/"):
                    if path_list[-4] not in characters:
                      characters[path_list[-4]] = {'expressions': {}, 'poses': {}, 'outfits': {}, 'outfits_extra': {}} #New character
                    if path_list[-2] not in characters[path_list[-4]]['poses']:
                      characters[path_list[-4]]['poses'][path_list[-2]] = {} #New pose
                    splitVal = os.path.splitext(path_list[-1])[0]
                    if splitVal not in characters[path_list[-4]]['poses'][path_list[-2]]:
                      if splitVal != 'pose': #Ignore pose.png
                        characters[path_list[-4]]['poses'][path_list[-2]][splitVal] = path #New outfit
              elif path == characterImageFolder + path_list[-2] + '/base.png':
                #print 'found base for', path_list[-2], 'at', path
                if path_list[-2] not in characters:
                  characters[path_list[-2]] = {'expressions': {}, 'poses': {}, 'outfits': {}, 'outfits_extra': {}} #New character
                characters[path_list[-2]]['base'] = path
                #print characters[path_list[-2]]
              else:
                for val in ['outfits', 'poses', 'expressions', 'outfits_extra']:
                  if path.startswith(characterImageFolder + path_list[-3] + "/" + val + "/") and path_list[-2] == val:
                    if path_list[-3] not in characters:
                      characters[path_list[-3]] = {'expressions': {}, 'poses': {}, 'outfits': {}, 'outfits_extra': {}}
                    splitVal = os.path.splitext(path_list[-1])[0]
                    if splitVal not in characters[path_list[-3]][path_list[-2]]:
                      characters[path_list[-3]][path_list[-2]][splitVal] = path
                    break

        #print characters
        for cKey in characters:
            character = characters[cKey]
            if 'outfits' in character: #Standard directory structure
              for oKey in character['outfits']:
                outfit = character['outfits'][oKey]
                for pKey in character['poses']:
                    pose = character['poses'][pKey]
                    define_extra(size, character, pose, outfit, cKey, oKey, pKey)
            if 'poses' in character: #Pose-specific outfits
              for pKey in character['poses']:
                pose = character['poses'][pKey]
                if isinstance(pose, dict):
                  posePath = characterImageFolder + cKey + '/poses/' + pKey + '/' + 'pose.png'
                  for oKey in pose:
                    outfit = pose[oKey]
                    define_extra(size, character, posePath, outfit, cKey, oKey, pKey)
                else:
                    define_extra(size, character, pose, None, cKey, None, pKey)
            elif 'outfits' not in character and 'expressions' in character:
                #Base sprite contains pose and outfit
                define_extra(size, character, None, None, cKey, None, None)

def define_extra(size, character, pose, outfit, cKey, oKey, pKey):
        for eKey in character['expressions']:
            expression = character['expressions'][eKey]
            nameList = tuple([cKey, oKey, pKey, eKey])
            args = [(0, 0), pose, (0, 0), outfit, (0, 0), expression]

            if 'base' in character:
                args = [(0, 0), character['base']] + args
            define_image(size, nameList, args)
            for oeKey in character['outfits_extra']:
                outfit_extra = character['outfits_extra'][oeKey]
                #print outfit_extra
                nameList = tuple([cKey, oKey, oeKey, pKey, eKey])
                define_image(size, nameList, args + [(0, 0), outfit_extra])

###
#Example usage:
#
#Directories:
#/game/sprites/
#              sara/
#                   expressions/
#                               happy.png
#                   poses/arms_crossed/
#                                      pose.png
#                                      uniform.png
#                   base.png
#
#If we then ran:
#define_characters("sprites/")
#we would be able to call:
#show sara uniform arms_crossed happy
#and
#show sara flip uniform arms_crossed happy
#
#I could also add the directory and image:
#/game/sprites/sara/outfits_extra/apron.png
#After which I could call:
#show sara uniform apron arms_crossed happy
#
#What happens is, the images found in the path are combined using LiveComposite, and the definition is defined
#based on the path to the image.
#So, for example, base.png is on the bottom, then the uniform is added to it, then the pose, then the expression.
#The result is a complete sprite created dynamically.
###






