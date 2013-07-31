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

"""
The edX trackinglog schema...
"track_trackinglog"
    ("username" varchar(32) NOT NULL,
    "dtcreated" datetime NOT NULL,
    "event_source" varchar(32) NOT NULL,
    "event_type" varchar(512) NOT NULL,
    "ip" varchar(32) NOT NULL,
    "agent" varchar(256) NOT NULL,
    "event" text NOT NULL,
        {"id":"i4x-MITx-6_002x-video-S1V1_Motivation_for_6_002x",
        "code":"4rpg8Bq6hb4",
        "currentTime":0,
        "speed":"1.0"}
    "host" varchar(64) NOT NULL DEFAULT '',
    "time" datetime NOT NULL,
    "id" integer PRIMARY KEY,
    "page" varchar(512) NULL);
"""
EDX_CONF = {
    ### properties ###
    # Does the video autoplay?
    'AUTOPLAY_VIDEOS': True,
    # Where is this video hosted?
    'VIDEO_HOST': 'youtube',
    # Where is the absolute timestamp of an event stored?
    'TIMESTAMP': 'time',
    # Where is the event type information stored?
    'TYPE_EVENT': 'event_type',
    # Where is the username stored?
    'USERNAME': 'username',
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
        try:
            obj = ast.literal_eval(obj)
        except ValueError:
            pass
            #print "value error, ignoring line"
        except SyntaxError:
            pass
            #print "syntax error, ignoring line"
    if isinstance(prop, str) or isinstance(prop, unicode):
        if prop not in obj:
            return ""
        else:
            return obj[prop]
    elif isinstance(prop, list):
        if len(prop) == 2:
            return get_inner_prop(obj[prop[0]], prop[1])
        if len(prop) == 1:
            try:
                value = obj[prop[0]]
            except:
                value = ""
            return value
    return ""


def get_prop(obj, prop):
    """
    Get property values for the given (obj, prop) pair.
    """
    if prop == "" or prop not in CONF:
        return ""
    feature = CONF[prop]
    return get_inner_prop(obj, feature)
