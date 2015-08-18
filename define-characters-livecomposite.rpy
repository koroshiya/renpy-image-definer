init python early:

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

  def define_image(size, side, path_tuple, argList):
      path_tuple = tuple(entry for entry in path_tuple if entry is not None)
      if side:
          path_tuple = ('side', ) + path_tuple
      args = []
      for i in xrange(1, len(argList), 2):
          if argList[i] is not None:
              args.extend([(0, 0), argList[i]])
      renpy.image(path_tuple, LiveComposite(size, *args))

      if not side:

          flipArr = args
          for i in xrange(1, len(args), 2):
              flipArr[i] = im.Flip(args[i], horizontal=True)
          plist = list(path_tuple)
          plist.insert(1, 'flip') #flip after char name. eg. sara flip arms_crossed etc.
          renpy.image(tuple(plist), LiveComposite(size, *flipArr))

  def get_character_indexes():
      return {'expressions': {}, 'poses': {}, 'outfits': {}, 'outfits_extra': {}}

  def define_chars(characterImageFolder, size=(370, 512), flip=True, side=False):
      chars = {}

      for path in renpy.list_files():
          if path.startswith(characterImageFolder):
            pList = path.split("/")

            if len(pList) >= 4 and path.startswith(characterImageFolder + pList[-4] + "/poses/"):
                  if pList[-4] not in chars:
                    chars[pList[-4]] = get_character_indexes() #New character
                  if pList[-2] not in chars[pList[-4]]['poses']:
                    chars[pList[-4]]['poses'][pList[-2]] = {} #New pose
                  splitVal = os.path.splitext(pList[-1])[0]
                  if splitVal not in chars[pList[-4]]['poses'][pList[-2]] and splitVal != 'pose':
                    chars[pList[-4]]['poses'][pList[-2]][splitVal] = path #New outfit
            elif len(pList) >= 4 and path.startswith(characterImageFolder + pList[-4] + "/outfits_extra/"):
                  if pList[-4] not in chars:
                    chars[pList[-4]] = get_character_indexes() #New character
                  if pList[-2] not in chars[pList[-4]]['outfits_extra']:
                    chars[pList[-4]]['outfits_extra'][pList[-2]] = {} #New outfit extra
                  splitVal = os.path.splitext(pList[-1])[0]
                  if splitVal not in chars[pList[-4]]['outfits_extra'][pList[-2]]:
                    chars[pList[-4]]['outfits_extra'][pList[-2]][splitVal] = path #New pose
            elif path == characterImageFolder + pList[-2] + '/base.png':
              if pList[-2] not in chars:
                chars[pList[-2]] = get_character_indexes() #New character
              chars[pList[-2]]['base'] = path
            elif len(pList) >= 3:
              for val in ['outfits', 'poses', 'expressions', 'outfits_extra']:
                if path.startswith(characterImageFolder + pList[-3] + "/" + val + "/") and pList[-2] == val:
                  if pList[-3] not in chars:
                    chars[pList[-3]] = get_character_indexes()
                  splitVal = os.path.splitext(pList[-1])[0]
                  if splitVal not in chars[pList[-3]][pList[-2]]:
                    chars[pList[-3]][pList[-2]][splitVal] = path
                  break

      for cKey in chars:
          character = chars[cKey]
          if len(character['outfits']) > 0: #Standard directory structure
            for oKey in character['outfits']:
              outfit = character['outfits'][oKey]
              if len(character['poses']) > 0:
                  for pKey in character['poses']:
                      pose = character['poses'][pKey]
                      define_extra(size, side, character, pose, outfit, cKey, oKey, pKey)
              else:
                  define_extra(size, side, character, None, outfit, cKey, oKey, None)
          if len(character['poses']) > 0: #Pose-specific outfits
            for pKey in character['poses']:
              pose = character['poses'][pKey]
              if isinstance(pose, dict):
                posePath = characterImageFolder + cKey + '/poses/' + pKey + '/' + 'pose.png'
                for oKey in pose:
                  outfit = pose[oKey]
                  define_extra(size, side, character, posePath, outfit, cKey, oKey, pKey)
              else:
                  define_extra(size, side, character, pose, None, cKey, None, pKey)
          elif len(character['outfits']) == 0 and len(character['expressions']) > 0:
              #Base sprite contains pose and outfit
              define_extra(size, side, character, None, None, cKey, None, None)

  def define_extra(size, side, character, pose, outfit, cKey, oKey, pKey):
      for eKey in character['expressions']:
          expression = character['expressions'][eKey]
          nameList = tuple([cKey, oKey, pKey, eKey])
          args = [(0, 0), pose, (0, 0), outfit, (0, 0), expression]

          if 'base' in character:
              args = [(0, 0), character['base']] + args
          define_image(size, side, nameList, args)
          for oeKey in character['outfits_extra']:
              outfit_extra = character['outfits_extra'][oeKey]
              if isinstance(outfit_extra, dict):
                if pKey in outfit_extra: #For each pose
                  nameList = tuple([cKey, oKey, oeKey, pKey, eKey])
                  define_image(size, side, nameList, args + [(0, 0), outfit_extra[pKey]])
              else:
                  nameList = tuple([cKey, oKey, oeKey, pKey, eKey])
                  define_image(size, side, nameList, args + [(0, 0), outfit_extra])

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
  #define_chars("sprites/")
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

