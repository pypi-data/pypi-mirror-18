Taggable
--------

>>> from taggable import TaggableSequence
>>> sample = TaggableSequence('Do it')
>>> sample.tag("POS", "VERB")
>>> for tag in sample.tags("POS"):
>>>     print(tag.tag)
>>> list = TaggableSequence([10, 2])



