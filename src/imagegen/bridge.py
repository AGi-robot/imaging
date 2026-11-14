"""Bridge the raster painting engine into the canvas action language.

The 'image' kind belongs to imagegen, not to canvas: the vector language
stays imagegen-agnostic, and agents that never load a painting engine never
see the kind in their tool schema.
"""
from canvas.engine import register_action_kind

PAINT_INSTRUCTIONS = '''A real raster painting engine is available. For a requested picture or painting,
prefer one image action instead of approximating the subject with many vector shapes.
The vector painting instructions above apply when editable vector art is specifically requested.
You can place an AI-painted picture on the canvas
with an image action: {"kind":"image","prompt":"<detailed English scene description>",
"x":400,"y":150,"width":500,"height":400}. The prompt must be a rich text-to-image
description of the whole picture (subject, setting, style, medium, lighting, palette,
composition); it is rendered by a separate painting model and placed at x,y with the given
size, so choose the placement deliberately relative to the other objects. Use an image
action when the user asks for a picture, photograph, painting, poster, realistic scene,
textured subject, or anything vector shapes cannot convey well; the painted picture is
finished art by itself, so do not draw vector outlines on top of it unless the user asks
for a mixed-media piece. Use x=0,y=0,width=1000,height=650 for a full-canvas picture unless another placement is requested.
Place image actions first in a pass (later actions draw on top of
them), at most two image actions per request, and prefer one strong picture over several
small ones. Painted images cannot be recolored; they can be moved, sized at placement or
deleted and painted again with a new prompt. Tell the user in the response field what you
painted for them.'''


def _image_validator(action, item, *, allow_image_layers=False):
    width = min(item.get('width', 1000), 1000)
    height = min(item.get('height', 650), 650)
    width, height = max(16, width), max(16, height)
    item['width'] = width
    item['height'] = height
    item['x'] = min(item.get('x', 0), 1000 - width)
    item['y'] = min(item.get('y', 0), 650 - height)
    # Browser artwork can contain older pictures without a stored prompt.
    # Their bitmap stays in the browser; only metadata enters LLM context.
    if not item.get('prompt', '').strip():
        if allow_image_layers and item.get('id'):
            item['prompt'] = 'Existing painted image'
        else:
            raise ValueError('Image actions need a painting prompt')


def register_image_kind():
    """Register the 'image' kind into the canvas language (idempotent)."""
    register_action_kind(
        'image',
        properties={
            'prompt': {'type': 'string', 'maxLength': 800,
                       'description': 'Detailed English scene description for a raster painting (kind image): subject, style, medium, lighting, composition'},
        },
        validator=_image_validator,
    )
