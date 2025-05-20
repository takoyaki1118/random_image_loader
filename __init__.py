# __init__.py (例: ComfyUI/custom_nodes/my_custom_nodes/__init__.py の場合)
# もし、random_image_loader.py を custom_nodes 直下に置いたなら、
# from .random_image_loader import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS となります。

# random_image_loader.py が custom_nodes/random_image_loader.py にある場合
from .random_image_loader import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 他のカスタムノードのマッピングがある場合は、それらも維持するようにしてください
# 例:
# from .other_node_file import NODE_CLASS_MAPPINGS as OTHER_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as OTHER_DISPLAY_MAPPINGS
# NODE_CLASS_MAPPINGS.update(OTHER_MAPPINGS)
# NODE_DISPLAY_NAME_MAPPINGS.update(OTHER_DISPLAY_MAPPINGS)


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']