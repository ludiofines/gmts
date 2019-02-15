import argparse
import sys
import requests
import re
import json
from urllib.parse import urlparse


parser = argparse.ArgumentParser(description='GetMeTheThatSound.')
parser.add_argument('--url', '-u', type=str, help='provide sc url')
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_usage()
else:
    rcvdUrl = args.url
    r = requests.get(rcvdUrl)
    if r.status_code != 200:
        print('error getting {}-{}'.format(rcvdUrl, r))
    match = re.search(r'var c=(\[.*\]),', r.content.decode('utf-8'))
    if match is None:
        print('cannot get data')
    jData = json.loads(match.group(1))
    for i in jData:
        for ii in i['data']:
            if ii.get('permalink_url') == rcvdUrl:
                urlsUrl = ii['uri']
                urlsUrl += '/streams?client_id=xlfhBPd4OSHwQ9KGtW9ySS26KDOvmhTk'
                print('getting metadata')
                rr = requests.get(urlsUrl)
                sData = rr.json()
                print('done')
                playUrl = sData['hls_mp3_128_url']
                playUrlObj = urlparse(playUrl)
                rr = requests.get(playUrl)
                pData = rr.content.decode('utf-8').split('\n')
                pArray = []
                for line in pData:
                    prefix = playUrlObj.scheme + '://' + playUrlObj.netloc
                    if line.startswith(prefix):
                        pArray.append(line)
                last = urlparse(pArray[-1])
                downUrl = (
                    last.scheme 
                    + '://' 
                    + last.netloc
                    + re.sub(r'/media/[0-9]+/([0-9]+)/(.*\.128\.mp3)', '/media/0/\\1/\\2',last.path, 1)
                    + '?'
                    + last.query
                )
                filename = '/tmp/' + ii['permalink'] + '.mp3'
                print('downloading {}'.format(ii['permalink']))
                rr = requests.get(downUrl, stream=True)
                total_length = rr.headers.get('content-length')
                with open(filename,'wb') as audioData:
                    if total_length is None:
                        audioData.write(rr.content)
                    else:
                        total_length = int(total_length)
                        d = 0
                        num_blocks = 50
                        block_size = int(total_length / num_blocks)
                        for data in rr.iter_content(chunk_size=block_size):
                            d += len(data)
                            audioData.write(data)
                            rcvd = int((num_blocks * d) / total_length)
                            rcvd_perc = int((d / total_length) * 100)
                            bar = '=' * rcvd
                            bar += ' ' * (num_blocks - rcvd)
                            item = ' [{}] {}% from {:.2f} MB\r'.format(
                                bar,
                                rcvd_perc,
                                total_length / 1048576
                            )
                            print(item, sep=' ', end=' ', flush=True)
                        print('')
                print('done {}'.format(filename))

