
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = 'C91BABC9F94B8569091E0E9A73F2DF27'
    
_lr_action_items = {'LBRACE':([0,1,3,9,10,],[1,1,1,1,1,]),'CONSTANT':([0,1,3,9,10,],[2,2,2,2,2,]),'RBRACE':([2,5,6,7,11,12,13,14,],[-3,-4,-6,11,-2,-1,-5,-7,]),'LSBRACKET':([0,1,3,9,10,],[3,3,3,3,3,]),'RSBRACKET':([2,5,6,8,11,12,13,14,],[-3,-4,-6,12,-2,-1,-5,-7,]),'COMMA':([2,5,6,7,8,11,12,13,14,],[-3,-4,-6,10,10,-2,-1,-5,-7,]),'COLON':([5,],[9,]),'$end':([2,4,5,11,12,13,],[-3,0,-4,-2,-1,-5,]),'NORMSTRING':([0,1,3,9,10,],[5,5,5,5,5,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'root_block':([0,1,3,9,10,],[4,6,6,13,14,]),'block_item_list':([1,3,],[7,8,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> root_block","S'",1,None,None,None),
  ('root_block -> LSBRACKET block_item_list RSBRACKET','root_block',3,'p_root_block','file_parser.py',67),
  ('root_block -> LBRACE block_item_list RBRACE','root_block',3,'p_root_block','file_parser.py',68),
  ('root_block -> CONSTANT','root_block',1,'p_root_block','file_parser.py',69),
  ('root_block -> NORMSTRING','root_block',1,'p_root_block','file_parser.py',70),
  ('root_block -> NORMSTRING COLON root_block','root_block',3,'p_root_block','file_parser.py',71),
  ('block_item_list -> root_block','block_item_list',1,'p_block_item_list','file_parser.py',76),
  ('block_item_list -> block_item_list COMMA root_block','block_item_list',3,'p_block_item_list','file_parser.py',77),
  ('empty -> <empty>','empty',0,'p_empty','file_parser.py',84),
]
