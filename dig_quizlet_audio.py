import re, argparse, urllib, urllib2, os
from pydub import AudioSegment

def get_audio_urls(url):
  obj = urllib2.urlopen(url).read()

  pat = re.compile(r'http.*?mp3')
  urls = pat.findall(obj, re.I)
  urls = map(lambda x: x.replace('\\', ''), urls)
  return urls

def generate_combined_audio(urls):
  main_audio = AudioSegment.empty()
  silence = AudioSegment.silent(duration=1000)
  tmp_path = os.path.join("/tmp", "tempsong.mp3")
  target_path = "./Combined.mp3"

  for url in urls:
    urllib.urlretrieve(url, tmp_path)
    song = AudioSegment.from_mp3(tmp_path)
    main_audio = main_audio + silence + song

  main_audio.export(target_path, format="mp3")
  os.remove(tmp_path)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('url', type=str, help='url of quizlet page')
  args = parser.parse_args()

  if args.url[:4] != 'http':
    args.url = 'https://' + args.url

  urls = get_audio_urls(args.url)
  generate_combined_audio(urls)
