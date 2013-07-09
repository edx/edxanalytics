"""
Configuration for every video player / site.
- Properties (prefix none): names of video properties (e.g., autoplay on?)
- Events (prefix EVT): names of video events (e.g., video_play)

To add a new target, simply copy an existing block, paste, and modify.
- normal values: boolean or string or list with one item
- doesn't exist: empty string or list (e.g., '', [])
- multiple values: list (e.g., ['a', 'b', 'c'])
- hierarchical values: nested list (e.g., ['a', ['aa']])
"""
import ast

EDX_CONF = {
    ### properties ###
    # Does the video autoplay?
    'AUTOPLAY_VIDEOS': True,
    # Is this video hosted on YouTube?
    'HOSTED_ON_YOUTUBE': True,
    # Where is the absolute timestamp of an event stored?
    'TIMESTAMP': 'time',
    # Where is the event type information stored?
    'TYPE_EVENT': 'event_type',
    # Where is the video ID stored?
    'VIDEO_ID': ['event', ['code']],
    # Where is the video name stored?
    'VIDEO_NAME': ['event', ['id']],
    # Where is the relative video timestamp stored?
    'VIDEO_TIME': ['event', ['currentTime']],
    # Where is the play speed stored?
    'VIDEO_SPEED': ['event', ['speed']],

    ### events ###
    # Where is the page open event?
    'EVT_PAGE_OPEN': ['page_open'],
    # Where is the page close event?
    'EVT_PAGE_CLOSE': ['page_close'],
    # Where is the next destination event?
    'EVT_NEXT_DST': ['seq_goto', 'seq_next', 'seq_prev'],
    # Where is the player pause event?
    'EVT_VIDEO_PAUSE': ['pause_video'],
    # Where is the player play event?
    'EVT_VIDEO_PLAY': ['play_video'],
    # Where is the player seek event?
    'EVT_VIDEO_SEEK': [],
    # Where is the fullscreen event?
    'EVT_VIDEO_FULLSCREEN': [],
    # Where is the volume up event?
    'EVT_VIDEO_VOLUME_UP': [],
    # Where is the volume down event?
    'EVT_VIDEO_VOLUME_DOWN': [],
    # Where is the volume mute event?
    'EVT_VIDEO_VOLUME_MUTE': [],
}

# This is how external files access configuration parameters.
# Need to be changed to any other XX_CONF when using non-edX platforms
CONF = EDX_CONF


def get_inner_prop(obj, prop):
    """
    Has recursive handling for hierarchical data formats.
    """
    if isinstance(obj, str) or isinstance(obj, unicode):
        obj = ast.literal_eval(obj)
    if isinstance(prop, str) or isinstance(obj, unicode):
        if prop not in obj:
            return ""
        else:
            return obj[prop]
    elif isinstance(prop, list):
        if len(prop) == 2:
            return get_inner_prop(obj[prop[0]], prop[1])
        if len(prop) == 1:
            return obj[prop[0]]
    return ""


def get_prop(obj, prop):
    """
    Get property values for the given (obj, prop) pair.
    """
    if prop == "" or prop not in CONF:
        return ""
    feature = CONF[prop]
    return get_inner_prop(obj, feature)
