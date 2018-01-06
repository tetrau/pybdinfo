import ctypes
import ctypes.util
import os

libbluray = ctypes.cdll.LoadLibrary(ctypes.util.find_library('bluray'))


class BLURAY_STREAM_INFO(ctypes.Structure):
    _fields_ = [('coding_type', ctypes.c_uint8),
                ('format', ctypes.c_uint8),
                ('rate', ctypes.c_uint8),
                ('char_code', ctypes.c_uint8),
                ('lang', ctypes.c_char * 4),
                ('pid', ctypes.c_uint16),
                ('aspect', ctypes.c_uint8),
                ('subpath_id', ctypes.c_uint8)]


class BLURAY_CLIP_INFO(ctypes.Structure):
    _fields_ = [('pkt_count', ctypes.c_uint32),
                ('still_mode', ctypes.c_uint8),
                ('still_time', ctypes.c_uint16),
                ('video_stream_count', ctypes.c_uint8),
                ('audio_stream_count', ctypes.c_uint8),
                ('pg_stream_count', ctypes.c_uint8),
                ('ig_stream_count', ctypes.c_uint8),
                ('sec_audio_stream_count', ctypes.c_uint8),
                ('sec_video_stream_count', ctypes.c_uint8),
                ('video_streams', ctypes.POINTER(BLURAY_STREAM_INFO)),
                ('audio_streams', ctypes.POINTER(BLURAY_STREAM_INFO)),
                ('pg_streams', ctypes.POINTER(BLURAY_STREAM_INFO)),
                ('ig_streams', ctypes.POINTER(BLURAY_STREAM_INFO)),
                ('sec_audio_streams', ctypes.POINTER(BLURAY_STREAM_INFO)),
                ('sec_video_streams', ctypes.POINTER(BLURAY_STREAM_INFO)),
                ('start_time', ctypes.c_uint64),
                ('in_time', ctypes.c_uint64),
                ('out_time', ctypes.c_uint64)]


class BLURAY_TITLE_CHAPTER(ctypes.Structure):
    _fields_ = [('idx', ctypes.c_uint32),
                ('start', ctypes.c_uint64),
                ('duration', ctypes.c_uint64),
                ('offset', ctypes.c_uint64),
                ('clip_ref', ctypes.c_uint)]


class BLURAY_TITLE_MARK(ctypes.Structure):
    _fields_ = [('idx', ctypes.c_uint32),
                ('type', ctypes.c_int),
                ('start', ctypes.c_uint64),
                ('duration', ctypes.c_uint64),
                ('offset', ctypes.c_uint64),
                ('clip_ref', ctypes.c_uint)]


class BLURAY_TITLE_INFO(ctypes.Structure):
    _fields_ = [('idx', ctypes.c_uint32),
                ('playlist', ctypes.c_uint32),
                ('duration', ctypes.c_uint64),
                ('clip_count', ctypes.c_uint32),
                ('angle_count', ctypes.c_uint8),
                ('chapter_count', ctypes.c_uint32),
                ('clips', ctypes.POINTER(BLURAY_CLIP_INFO)),
                ('chapters', ctypes.POINTER(BLURAY_TITLE_CHAPTER)),
                ('mark_count', ctypes.c_uint32),
                ('marks', ctypes.POINTER(BLURAY_TITLE_MARK))]


class BLURAY(ctypes.Structure):
    _fields_ = []


bd_open = libbluray.bd_open
bd_open.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
bd_open.restype = ctypes.POINTER(BLURAY)

bd_get_titles = libbluray.bd_get_titles
bd_get_titles.argtypes = (ctypes.POINTER(BLURAY), ctypes.c_uint8, ctypes.c_uint32)
bd_get_titles.restype = ctypes.c_uint32

bd_get_main_title = libbluray.bd_get_main_title
bd_get_main_title.argtypes = (ctypes.POINTER(BLURAY),)
bd_get_main_title.restype = ctypes.c_int

bd_get_title_info = libbluray.bd_get_title_info
bd_get_title_info.argtypes = (ctypes.POINTER(BLURAY), ctypes.c_uint32, ctypes.c_uint)
bd_get_title_info.restype = ctypes.POINTER(BLURAY_TITLE_INFO)

coding_type = {1: 'BLURAY_STREAM_TYPE_VIDEO_MPEG1',
               2: 'BLURAY_STREAM_TYPE_VIDEO_MPEG2',
               3: 'BLURAY_STREAM_TYPE_AUDIO_MPEG1',
               4: 'BLURAY_STREAM_TYPE_AUDIO_MPEG2',
               27: 'BLURAY_STREAM_TYPE_VIDEO_H264',
               128: 'BLURAY_STREAM_TYPE_AUDIO_LPCM',
               129: 'BLURAY_STREAM_TYPE_AUDIO_AC3',
               130: 'BLURAY_STREAM_TYPE_AUDIO_DTS',
               131: 'BLURAY_STREAM_TYPE_AUDIO_TRUHD',
               132: 'BLURAY_STREAM_TYPE_AUDIO_AC3PLUS',
               133: 'BLURAY_STREAM_TYPE_AUDIO_DTSHD',
               134: 'BLURAY_STREAM_TYPE_AUDIO_DTSHD_MASTER',
               144: 'BLURAY_STREAM_TYPE_SUB_PG',
               145: 'BLURAY_STREAM_TYPE_SUB_IG',
               146: 'BLURAY_STREAM_TYPE_SUB_TEXT',
               161: 'BLURAY_STREAM_TYPE_AUDIO_AC3PLUS_SECONDARY',
               162: 'BLURAY_STREAM_TYPE_AUDIO_DTSHD_SECONDARY',
               234: 'BLURAY_STREAM_TYPE_VIDEO_VC1'}
video_format = {1: 'BLURAY_VIDEO_FORMAT_480I',
                2: 'BLURAY_VIDEO_FORMAT_576I',
                3: 'BLURAY_VIDEO_FORMAT_480P',
                4: 'BLURAY_VIDEO_FORMAT_1080I',
                5: 'BLURAY_VIDEO_FORMAT_720P',
                6: 'BLURAY_VIDEO_FORMAT_1080P',
                7: 'BLURAY_VIDEO_FORMAT_576P'}
video_rate = {1: 'BLURAY_VIDEO_RATE_24000_1001',
              2: 'BLURAY_VIDEO_RATE_24',
              3: 'BLURAY_VIDEO_RATE_25',
              4: 'BLURAY_VIDEO_RATE_30000_1001',
              6: 'BLURAY_VIDEO_RATE_50',
              7: 'BLURAY_VIDEO_RATE_60000_1001'}
video_aspect = {2: "BLURAY_ASPECT_RATIO_4_3",
                3: "BLURAY_ASPECT_RATIO_16_9"}
audio_format = {1: 'BLURAY_AUDIO_FORMAT_MONO',
                3: 'BLURAY_AUDIO_FORMAT_STEREO',
                6: 'BLURAY_AUDIO_FORMAT_MULTI_CHAN',
                12: 'BLURAY_AUDIO_FORMAT_COMBO'}
audio_rate = {1: 'BLURAY_AUDIO_RATE_48',
              4: 'BLURAY_AUDIO_RATE_96',
              5: 'BLURAY_AUDIO_RATE_192',
              12: 'BLURAY_AUDIO_RATE_192_COMBO',
              14: 'BLURAY_AUDIO_RATE_96_COMBO'}


def get_bdinfo(bluray_dir: str):
    abs_bluray_dir = os.path.abspath(bluray_dir.encode())
    bluray = bd_open(abs_bluray_dir, b'')
    titles_number = bd_get_titles(bluray, 0, 0)
    main_title_index = bd_get_main_title(bluray)
    main_title_info = bd_get_title_info(bluray, main_title_index, 0).contents
    clip_info = main_title_info.clips.contents
    video_stream_count = clip_info.video_stream_count
    audio_stream_count = clip_info.audio_stream_count
    pg_stream_count = clip_info.pg_stream_count
    ig_stream_count = clip_info.ig_stream_count
    sec_video_stream_count = clip_info.sec_video_stream_count
    sec_audio_stream_count = clip_info.sec_audio_stream_count
    bdinfo = {'video': [],
              'audio': [],
              'subtitle': []}
    for i in range(video_stream_count):
        video_stream = clip_info.video_streams[i]
        bdinfo['video'].append({'coding_type': coding_type[video_stream.coding_type],
                                'format': video_format[video_stream.format],
                                'rate': video_rate[video_stream.rate],
                                'aspect': video_aspect[video_stream.aspect]})
    for i in range(audio_stream_count):
        audio_stream = clip_info.audio_streams[i]
        bdinfo['audio'].append({'coding_type': coding_type[audio_stream.coding_type],
                                'rate': audio_rate[audio_stream.rate],
                                'format': audio_format[audio_stream.format],
                                'lang': audio_stream.lang.decode()})

    for i in range(pg_stream_count):
        pg_stream = clip_info.pg_streams[i]
        bdinfo['subtitle'].append({'coding_type': coding_type[pg_stream.coding_type],
                                   'lang': pg_stream.lang.decode()})
    return bdinfo
