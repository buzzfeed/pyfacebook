class Model( object ):

  def __init__(self, object_or_dict):
    """
    Initializes a model from an object or a dictionary
    """
    self.copysome( object_or_dict, self, self.attrs_to_copy )


  def copysome( self, objfrom, objto, attrs ):
    """
    Copies the attributes of objfrom into objto.
    Will only copy attributes that appear in the attrs list.

    :param object objfrom: The object that we are copying attibutes from.

    :param object objto: The object that we are copying attributes to.

    :param list attrs: A list of attribute names. Will only copy attributes that appear in this list.

    """
    for a in attrs:
      if hasattr( objfrom, a):
        b = getattr(objfrom, a)
        setattr(objto, a, b);
      else:
        try:
          iter( objfrom )
          if a in objfrom:
            setattr(objto, a, objfrom[ a ])
            continue
        except:
          pass

        setattr(objto, a, None)