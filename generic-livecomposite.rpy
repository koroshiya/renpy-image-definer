init python early:

  from itertools import product, combinations
  from copy import deepcopy

  ###
  #Get Character Indexes
  #
  #This function defines the format of all images to be used.
  #There are multiple parameters which need to be set, which will affect how
  #images are processed and stacked.
  #
  #The two main types of indexes are defined by the 'nested' parameter:
  #
  #If nested is False, the values are simple, plain, generic images.
  #The index is a directory, and anything within will be used as a layer.
  #
  #If nested is True, two-level directories are used.
  #The index is a directory, but instead of having images within this directory,
  #there will be further directories, and in THOSE directories are the images to be used.
  #
  #eg.
  #expressions/smile.png
  #poses/arms_crossed/shirt.png
  #poses/hand_behind_head/shirt.png
  #
  #In the above examples, 'expressions' would be an example of a simple layer.
  #'expressions' is the directory, 'smile.png' is an image within that directory.
  #'poses' would be a nested layer. The directories within 'poses' each contain images
  #of their own (outfits, in this case), in addition to one image defined by 'file_name'.
  #
  #Nested indexes are used when common layers need to match, yet come in variations.
  #For example, let's say we have the following files:
  #poses/arms_crossed/pose.png
  #poses/arms_crossed/shirt.png
  #poses/arms_crossed/dress.png
  #poses/hand_behind_head/pose.png
  #poses/hand_behind_head/shirt.png
  #poses/hand_behind_head/dress.png
  #
  #Since poses defines a 'file_name' parameter of 'pose', the 'pose.png' files are
  #used as the base image for each pose. They are displayed above the outfits (since
  #innerAbove is set to False).
  #The other images (shirt, dress), however, are different outfits, which need to be
  #paired with the appropriate pose.
  #So in this case, arms_crossed/pose.png is shown on top of arms_crossed/shirt.png,
  #hand_behind_head/pose.png is shown on top of hand_behind_head/dress.png, and so on.
  #
  #With an expression of 'smile' and a character 'sara', the end result would be the images:
  #sara arms_crossed shirt
  #sara arms_crossed dress
  #sara hand_behind_head shirt
  #sara hand_behind_head dress
  #
  #
  ###PARAMETERS###
  #
  #level: defined the order in which layers are arranged.
  #For example, poses has a level of 2, so it would be lower than expressions.
  #Expressions has a level of 3, so it would be below outfits_extra.
  #So in this case, it would be BaseSprite -> Poses -> Outfits -> Expressions -> OutfitsExtra
  #
  #toggle: if True, the layer becomes optional.
  #eg. You could have both "sara arms_crossed shirt apron" and "sara arms_crossed shirt" defined.
  #Toggleable layers are typically optional extras shown on top of other layers, but which may not
  #always be desireable.
  #
  #nested: explained above.
  #
  #file_name: for 'nested' only.
  #If left out, file_name defaults to the name of the directory.
  #This parameter is used to define an image within nested directories to be shown across
  #all variations of that layer.
  #An example of this was given above, where 'pose' was the file_name.
  #'pose.png' was then required for each inner directory, and shown above or below the other
  #files in that directory.
  #
  #innerAbove: for 'nested' only.
  #Defaults to: False
  #If True, the contents of a nested directory are displayed above the file_name image.
  #If False, the contents are displayed below the file_name image.
  #
  #
  #
  ###HOW TO USE###
  #
  #In an init python block (you can put it in this file, for example), you need to include
  #a line such as: define_characters('sprites/')
  #That would tell the script to go into the 'sprites' directory, and search every folder within.
  #
  #eg. sprites/sara, sprites/misa, etc.
  #Would define a character of sara, a character of misa, and so on.
  #
  #Inside each character folder, you will need to create the directories specified by this method.
  #eg. sprites/sara/expressions
  #
  #Finally, inside the directories, put the images you desire.
  ####
  def get_character_indexes(empty=True, dictionary=False):

    if not dictionary: #If user hasn't defined their own dictionary, use the default.
      dictionary = {
        'expressions':{
          'level':3,
          'toggle':False
        },
        'outfits_extra':{
          'level':4,
          'toggle':True #TODO: look at entegrating ConditionSwitch instead
        },
        'poses':{
          'level':2,
          'nested':True,
          'innerAbove':False,
          'file_name':'pose' #if not defined, look for key
        }
      }

    tmpDict = deepcopy(dictionary)

    if empty:
      for key in tmpDict:
        nest = 'nested' in dictionary[key] and dictionary[key]['nested'] == True
        tmpDict[key].clear()
        if nest:
          tmpDict[key]['iterItems'] = {}
          tmpDict[key]['iterOuter'] = {}
    else:
      for key in tmpDict:
        if 'toggle' not in tmpDict[key]:
          tmpDict[key]['toggle'] = False
        if 'nested' not in tmpDict[key]:
          tmpDict[key]['nested'] = False
        if 'innerAbove' not in tmpDict[key]:
          tmpDict[key]['innerAbove'] = False
        if 'file_name' not in tmpDict[key]:
          tmpDict[key]['file_name'] = key

    return tmpDict

  def write_defs(f, size, args, path_tuple): #TODO: add name
    if f is not None:
      s = 'LiveComposite((' + str(size[0]) + ',' + str(size[1]) + ')'
      for arg in args:
        s += ','
        if isinstance(arg, tuple):
          s += '(' + ','.join([str(x) for x in arg]) + ')'
        else:
          s += '"' + arg + '"'
      s += ')'

      f.write('image '+' '.join(path_tuple)+' = '+s+'\n')

  def define_image(imgSize, characterImageFolder, side, pTuple, argList, flip, f):
    pTuples = (pTuple, )
    sizes = (imgSize, )
    if side:
      pTuples = (pTuple, (('side',) + pTuple))
      sizes = (imgSize, side)

    for i in xrange(0, len(sizes)):
      path_tuple = pTuples[i]
      size = sizes[i]
      args = []

      for i in xrange(0, len(argList)):
          if argList[i] is not None:
              args.extend([(0, 0), characterImageFolder + argList[i]])
      renpy.image(path_tuple, LiveComposite(size, *args))

      write_defs(f, size, args, path_tuple)

      if flip:

          flipArr = args
          for i in xrange(1, len(args), 2):
              flipArr[i] = im.Flip(args[i], horizontal=True)
          plist = list(path_tuple)
          plist.insert(1, 'flip') #flip after char name. eg. sara flip arms_crossed etc.
          renpy.image(tuple(plist), LiveComposite(size, *flipArr))

  ###
  #characterImageFolder: folder to search for characters.
  #eg. 'sprites/' if your characters are in /game/sprites.
  #
  #size: tuple of (x, y); dimensions of the full image.
  #
  #flip: if true, also do a version of the image with the x axis flipped.
  #For character sprites, this simulates a character facing the other way.
  #
  #side: either false, or a tuple of (x, y).
  #A side image would be a small image to be displayed in the textbox; NOT a character sprite.
  #If the value is a size tuple, the side image will be cropped from the top left
  #of the full image, for a total size of x, y.
  #
  #toWrite: if true, the definitions are written to file.
  #It is best to set this to True when you're about to distribute your game,
  #then move the generated rpy file into your game's folder and comment out your
  #define_characters methods.
  #ie. Run this method once with toWrite enabled, so you don't need to run this
  #method again.
  ###
  def define_characters(characterImageFolder, size=(370, 512), flip=True, side=False, toWrite=False, dictionary=False):
      chars = {}
      indexes = get_character_indexes(False, dictionary)

      f = None
      if toWrite:
        f = open('characterDefinitionList.rpy','w')

      for path in renpy.list_files():

          if path.startswith(characterImageFolder):
            path = path[len(characterImageFolder):]
            pList = path.split("/")
            cName = False

            if len(pList) >= 4:
              cName = pList[-4]
            elif len(pList) >= 3:
              cName = pList[-3]

            if cName:
              if cName not in chars:
                chars[cName] = get_character_indexes(True, dictionary) #New character

              if len(pList) >= 4:

                for key in chars[cName]:

                  if pList[1] == key:

                    splitVal = os.path.splitext(pList[-1])[0]

                    if indexes[key]['nested'] == False:
                      if splitVal not in chars[cName][key]:
                        chars[cName][key][splitVal] = path
                    elif splitVal != indexes[key]['file_name']:
                      chars[cName][key]['iterItems'][splitVal] = path
                    else:
                      chars[cName][key]['iterOuter'][pList[-2]] = path

                    break

              elif len(pList) >= 3:

                for key in chars[cName]:

                  if pList[1] == key:

                    splitVal = os.path.splitext(pList[-1])[0]

                    if splitVal not in chars[cName][key]:
                      chars[cName][key][splitVal] = path
                    break

      for cKey in chars:

        toDefine = {}

        for k in indexes:
          toDefine[indexes[k]['level']] = chars[cKey][k]
          if indexes[k]['nested']:
            toDefine[indexes[k]['level']]['selfType'] = k
          if indexes[k]['toggle']:
            toDefine[indexes[k]['level']]['toggle'] = indexes[k]['toggle']

        lists = []
        optionalFields = []

        for key in sorted(toDefine):
          val = toDefine[key]

          if 'selfType' in val:

            sType = val['selfType']
            inx = indexes[sType]
            inAbove = inx['innerAbove']

            lists.append(val['iterItems'])
            lists.append(val['iterOuter'])

            if inx['toggle']:
              optionalFields.append(key)
              optionalFields.append(key+1)

          else:
            if len(val) > 0:

              if 'toggle' in val and val['toggle']:
                if len(val) > 1:
                  optionalFields.append(key)
                del val['toggle']

              if len(val) > 0: #Check again in case 'toggle' was the only value
                lists.append(val)

        del toDefine

        for keys in product(*lists):

          pList = [cKey+'/base.png']

          for i in xrange(0, len(lists)):
            pList.append(lists[i][keys[i]])
          keys = (cKey, ) + keys

          if len(optionalFields) == 0:

            define_image(size, characterImageFolder, side, keys, pList, flip, f)

          else:

            for i in xrange(0, len(optionalFields) + 1):
              
              for opt in combinations(optionalFields, i):

                opt = list(opt)
                opt.sort()
                tempKeys = list(keys)
                tempList = pList

                for o in reversed(opt):
                  del tempKeys[o]
                  del tempList[o]

                tempKeys = tuple(tempKeys)
                define_image(size, characterImageFolder, side, tempKeys, tempList, flip, f)

      if toWrite:
        f.close()

  #define_characters('sprites/', toWrite=True)
  #Example of how to run. Uncomment above line and put your character folders in a 'sprites'
  #folder within your game directory.
