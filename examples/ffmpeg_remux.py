# using ffmpeg and pybdinfo to remux bluray into .mkv file
# Usage:
#   python3 ffmpeg_remux.py /dir/to/the/bluray /path/to/the/output.mkv
import sys
import pprint
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pybdinfo import get_bdinfo


def ffmpeg_remux(bluray_dir, output_path):
    bdinfo = get_bdinfo(bluray_dir)
    pprint.pprint(bdinfo)
    cmd = ['ffmpeg', '-i', 'bluray:{}'.format(bluray_dir), '-map', '0', '-c', 'copy']
    for i, v in enumerate(bdinfo['video']):
        cmd.extend(['-c:v:{}'.format(i), 'copy'])
    for i, a in enumerate(bdinfo['audio']):
        if a['coding_type'] != 'BLURAY_STREAM_TYPE_AUDIO_LPCM':
            cmd.extend(['-c:a:{}'.format(i),
                        'copy',
                        '-metadata:s:a:{}'.format(i),
                        'language={}'.format(a['lang'])])
        else:
            cmd.extend(['-c:a:{}'.format(i),
                        'pcm_s16le',
                        '-metadata:s:a:{}'.format(i),
                        'language={}'.format(a['lang'])])
    for i, s in enumerate(bdinfo['subtitle']):
        cmd.append('-c:s:{}'.format(i))
        cmd.append('copy')
        cmd.append('-metadata:s:s:{}'.format(i))
        cmd.append('language={}'.format(s['lang']))
    cmd.append(output_path)
    subprocess.run(cmd)


ffmpeg_remux(sys.argv[1], sys.argv[2])
