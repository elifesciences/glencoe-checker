import sys, json
import requests

'''
glencoe_resp = {
    "media1": {
        "source_href": "https://static-movie-usa.glencoesoftware.com/source/10.7554/659/0f10378e095dde7aaf579af504c4bfdc6fb86550/elife-00569-media1.wmv",
        "doi": "10.7554/eLife.00569.019",
        "flv_href": "https://static-movie-usa.glencoesoftware.com/flv/10.7554/659/0f10378e095dde7aaf579af504c4bfdc6fb86550/elife-00569-media1.flv",
        "uuid": "55f163d5-f0d9-415b-8ae8-ec75ed83b026",
        "title": "",
        "video_id": "media1",
        "solo_href": "https://movie-usa.glencoesoftware.com/video/10.7554/eLife.00569/media1",
        "height": 480,
        "ogv_href": "https://static-movie-usa.glencoesoftware.com/ogv/10.7554/659/0f10378e095dde7aaf579af504c4bfdc6fb86550/elife-00569-media1.ogv",
        "width": 640,
        "href": "elife-00569-media1.wmv",
        "webm_href": "https://static-movie-usa.glencoesoftware.com/webm/10.7554/659/0f10378e095dde7aaf579af504c4bfdc6fb86550/elife-00569-media1.webm",
        "jpg_href": "https://static-movie-usa.glencoesoftware.com/jpg/10.7554/659/0f10378e095dde7aaf579af504c4bfdc6fb86550/elife-00569-media1.jpg",
        "duration": 54.487,
        "mp4_href": "https://static-movie-usa.glencoesoftware.com/mp4/10.7554/659/0f10378e095dde7aaf579af504c4bfdc6fb86550/elife-00569-media1.mp4",
        "legend": "",
        "size": 20452423
    }
}
'''

def dealwithit(gc_data):

    sys.stderr.write(json.dumps(gc_data, indent=4))
    sys.stderr.write('\n')
    sys.stderr.flush()

    sources = {
        'mp4': 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"',
        'webm': 'video/webm; codecs="vp8.0, vorbis"',
        'ogv': 'video/ogg; codecs="theora, vorbis"',
    }
    known_sources = sources.keys()

    for v_id, v_data in gc_data.items():
        # we can't guarantee all of the sources will always be present
        available_sources = filter(lambda mtype: mtype + "_href" in v_data, known_sources)

        # fail if we have partial data
        msg = "number of available sources less than known sources for %r. missing: %s" % \
          (v_id, ", ".join(set(known_sources) - set(available_sources)))
        assert len(available_sources) == len(known_sources), msg

def metadata(msid):
    padded_msid = str(msid).zfill(5)
    doi = "10.7554/eLife." + padded_msid
    url = "https://movie-usa.glencoesoftware.com/metadata/" + doi

    resp = requests.get(url)

    assert resp.status_code != 404, "article has no videos"
    assert resp.status_code == 200, "unhandled status code from Glencoe: %s" % resp.status_code
    
    return resp.json()

def main(msid):
    try:
        dealwithit(metadata(msid))
        return True
    except AssertionError as err:
        print err
        return False

if __name__ == '__main__':
    sys.exit(0) if main(sys.argv[1]) else sys.exit(1)
