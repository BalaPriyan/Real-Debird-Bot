import logging
import re

from pyrogram import Client, filters
from pyrogram.types import Message
from urllib.parse import unquote, urlparse
from cloudscraper import create_scraper
import os
from time import sleep
from dotenv import load_dotenv
from plugins.button_build import ButtonMaker
from plugins.message_helper import sendMessage

load_dotenv('config.env')

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DEBRID_LINK_API_TOKEN = os.getenv('DEBRID_LINK_API_TOKEN')
REAL_DEBRID_API_TOKEN = os.getenv('REAL_DEBRID_API_TOKEN')

debrid_link_sites = ["1dl.net", "1fichier.com", "alterupload.com", "cjoint.net", "desfichiers.com", "dfichiers.com", "megadl.org", 
                "megadl.fr", "mesfichiers.fr", "mesfichiers.org", "piecejointe.net", "pjointe.com", "tenvoi.com", "dl4free.com", 
                "apkadmin.com", "bayfiles.com", "clicknupload.link", "clicknupload.org", "clicknupload.co", "clicknupload.cc", 
                "clicknupload.link", "clicknupload.download", "clicknupload.club", "clickndownload.org", "ddl.to", "ddownload.com", 
                "depositfiles.com", "dfile.eu", "dropapk.to", "drop.download", "dropbox.com", "easybytez.com", "easybytez.eu", 
                "easybytez.me", "elitefile.net", "elfile.net", "wdupload.com", "emload.com", "fastfile.cc", "fembed.com", 
                "feurl.com", "anime789.com", "24hd.club", "vcdn.io", "sharinglink.club", "votrefiles.club", "there.to", "femoload.xyz", 
                "dailyplanet.pw", "jplayer.net", "xstreamcdn.com", "gcloud.live", "vcdnplay.com", "vidohd.com", "vidsource.me", 
                "votrefile.xyz", "zidiplay.com", "fcdn.stream", "femax20.com", "sexhd.co", "mediashore.org", "viplayer.cc", "dutrag.com", 
                "mrdhan.com", "embedsito.com", "diasfem.com", "superplayxyz.club", "albavido.xyz", "ncdnstm.com", "fembed-hd.com", 
                "moviemaniac.org", "suzihaza.com", "fembed9hd.com", "vanfem.com", "fikper.com", "file.al", "fileaxa.com", "filecat.net", 
                "filedot.xyz", "filedot.to", "filefactory.com", "filenext.com", "filer.net", "filerice.com", "filesfly.cc", "filespace.com", 
                "filestore.me", "flashbit.cc", "dl.free.fr", "transfert.free.fr", "free.fr", "gigapeta.com", "gofile.io", "highload.to", 
                "hitfile.net", "hitf.cc", "hulkshare.com", "icerbox.com", "isra.cloud", "goloady.com", "jumploads.com", "katfile.com", 
                "k2s.cc", "keep2share.com", "keep2share.cc", "kshared.com", "load.to", "mediafile.cc", "mediafire.com", "mega.nz", 
                "mega.co.nz", "mexa.sh", "mexashare.com", "mx-sh.net", "mixdrop.co", "mixdrop.to", "mixdrop.club", "mixdrop.sx", 
                "modsbase.com", "nelion.me", "nitroflare.com", "nitro.download", "e.pcloud.link", "pixeldrain.com", "prefiles.com", "rg.to", 
                "rapidgator.net", "rapidgator.asia", "scribd.com", "sendspace.com", "sharemods.com", "soundcloud.com", "noregx.debrid.link", 
                "streamlare.com", "slmaxed.com", "sltube.org", "slwatch.co", "streamtape.com", "subyshare.com", "supervideo.tv", "terabox.com", 
                "tezfiles.com", "turbobit.net", "turbobit.cc", "turbobit.pw", "turbobit.online", "turbobit.ru", "turbobit.live", "turbo.to", 
                "turb.to", "turb.cc", "turbabit.com", "trubobit.com", "turb.pw", "turboblt.co", "turboget.net", "ubiqfile.com", "ulozto.net", 
                "uloz.to", "zachowajto.pl", "ulozto.cz", "ulozto.sk", "upload-4ever.com", "up-4ever.com", "up-4ever.net", "uptobox.com", 
                "uptostream.com", "uptobox.fr", "uptostream.fr", "uptobox.eu", "uptostream.eu", "uptobox.link", "uptostream.link", "upvid.pro", 
                "upvid.live", "upvid.host", "upvid.co", "upvid.biz", "upvid.cloud", "opvid.org", "opvid.online", "uqload.com", "uqload.co", 
                "uqload.io", "userload.co", "usersdrive.com", "vidoza.net", "voe.sx", "voe-unblock.com", "voeunblock1.com", "voeunblock2.com", 
                "voeunblock3.com", "voeunbl0ck.com", "voeunblck.com", "voeunblk.com", "voe-un-block.com", "voeun-block.net", 
                "reputationsheriffkennethsand.com", "449unceremoniousnasoseptal.com", "world-files.com", "worldbytez.com", "salefiles.com", 
                "wupfile.com", "youdbox.com", "yodbox.com", "youtube.com", "youtu.be", "4tube.com", "academicearth.org", "acast.com", 
                "add-anime.net", "air.mozilla.org", "allocine.fr", "alphaporno.com", "anysex.com", "aparat.com", "www.arte.tv", "video.arte.tv", 
                "sites.arte.tv", "creative.arte.tv", "info.arte.tv", "future.arte.tv", "ddc.arte.tv", "concert.arte.tv", "cinema.arte.tv", 
                "audi-mediacenter.com", "audioboom.com", "audiomack.com", "beeg.com", "camdemy.com", "chilloutzone.net", "clubic.com", "clyp.it", 
                "daclips.in", "dailymail.co.uk", "www.dailymail.co.uk", "dailymotion.com", "touch.dailymotion.com", "democracynow.org", 
                "discovery.com", "investigationdiscovery.com", "discoverylife.com", "animalplanet.com", "ahctv.com", "destinationamerica.com", 
                "sciencechannel.com", "tlc.com", "velocity.com", "dotsub.com", "ebaumsworld.com", "eitb.tv", "ellentv.com", "ellentube.com", 
                "flipagram.com", "footyroom.com", "formula1.com", "video.foxnews.com", "video.foxbusiness.com", "video.insider.foxnews.com", 
                "franceculture.fr", "gameinformer.com", "gamersyde.com", "gorillavid.in", "hbo.com", "hellporno.com", "hentai.animestigma.com", 
                "hornbunny.com", "imdb.com", "instagram.com", "itar-tass.com", "tass.ru", "jamendo.com", "jove.com", "keek.com", "k.to", 
                "keezmovies.com", "khanacademy.org", "kickstarter.com", "krasview.ru", "la7.it", "lci.fr", "play.lcp.fr", "libsyn.com", 
                "html5-player.libsyn.com", "liveleak.com", "livestream.com", "new.livestream.com", "m6.fr", "www.m6.fr", "metacritic.com", 
                "mgoon.com", "m.mgoon.com", "mixcloud.com", "mojvideo.com", "movieclips.com", "movpod.in", "musicplayon.com", "myspass.de", 
                "myvidster.com", "odatv.com", "onionstudios.com", "ora.tv", "unsafespeech.com", "play.fm", "plays.tv", "playvid.com", 
                "pornhd.com", "pornhub.com", "www.pornhub.com", "pyvideo.org", "redtube.com", "embed.redtube.com", "www.redtube.com", 
                "reverbnation.com", "revision3.com", "animalist.com", "seeker.com", "rts.ch", "rtve.es", "videos.sapo.pt", "videos.sapo.cv", 
                "videos.sapo.ao", "videos.sapo.mz", "videos.sapo.tl", "sbs.com.au", "www.sbs.com.au", "screencast.com", "skysports.com", 
                "slutload.com", "soundgasm.net", "store.steampowered.com", "steampowered.com", "steamcommunity.com", "stream.cz", "streamable.com", 
                "streamcloud.eu", "sunporno.com", "teachertube.com", "teamcoco.com", "ted.com", "tfo.org", "thescene.com", "thesixtyone.com", 
                "tnaflix.com", "trutv.com", "tu.tv", "turbo.fr", "tweakers.net", "ustream.tv", "vbox7.com", "veehd.com", "veoh.com", "vid.me", 
                "videodetective.com", "vimeo.com", "vimeopro.com", "player.vimeo.com", "player.vimeopro.com", "wat.tv", "wimp.com", "xtube.com", 
                "yahoo.com", "screen.yahoo.com", "news.yahoo.com", "sports.yahoo.com", "video.yahoo.com", "youporn.com"]


debrid_sites = ['1fichier.com', '2shared.com', '4shared.com', 'alfafile.net', 'anzfile.net', 'backin.net',
                'bayfiles.com', 'bdupload.in', 'brupload.net', 'btafile.com', 'catshare.net', 'clicknupload.me',
                'clipwatching.com', 'cosmobox.org', 'dailymotion.com', 'dailyuploads.net', 'daofile.com',
                'datafilehost.com', 'ddownload.com', 'depositfiles.com', 'dl.free.fr', 'douploads.net',
                'drop.download', 'earn4files.com', 'easybytez.com', 'ex-load.com', 'extmatrix.com',
                'down.fast-down.com', 'fastclick.to', 'faststore.org', 'file.al', 'file4safe.com', 'fboom.me',
                'filefactory.com', 'filefox.cc', 'filenext.com', 'filer.net', 'filerio.in', 'filesabc.com', 'filespace.com',
                'file-up.org', 'fileupload.pw', 'filezip.cc', 'fireget.com', 'flashbit.cc', 'flashx.tv', 'florenfile.com',
                'fshare.vn', 'gigapeta.com', 'goloady.com', 'docs.google.com', 'gounlimited.to', 'heroupload.com',
                'hexupload.net', 'hitfile.net', 'hotlink.cc', 'hulkshare.com', 'icerbox.com', 'inclouddrive.com',
                'isra.cloud', 'katfile.com', 'keep2share.cc', 'letsupload.cc', 'load.to', 'down.mdiaload.com', 'mediafire.com',
                'mega.co.nz', 'mixdrop.co', 'mixloads.com', 'mp4upload.com', 'nelion.me', 'ninjastream.to', 'nitroflare.com',
                'nowvideo.club', 'oboom.com', 'prefiles.com', 'sky.fm', 'rapidgator.net', 'rapidrar.com', 'rapidu.net',
                'rarefile.net', 'real-debrid.com', 'redbunker.net', 'redtube.com', 'rockfile.eu', 'rutube.ru', 'scribd.com',
                'sendit.cloud', 'sendspace.com', 'simfileshare.net', 'solidfiles.com', 'soundcloud.com', 'speed-down.org',
                'streamon.to', 'streamtape.com', 'takefile.link', 'tezfiles.com', 'thevideo.me', 'turbobit.net', 'tusfiles.com',
                'ubiqfile.com', 'uloz.to', 'unibytes.com', 'uploadbox.io', 'uploadboy.com', 'uploadc.com', 'uploaded.net',
                'uploadev.org', 'uploadgig.com', 'uploadrar.com', 'uppit.com', 'upstore.net', 'upstream.to', 'uptobox.com',
                'userscloud.com', 'usersdrive.com', 'vidcloud.ru', 'videobin.co', 'vidlox.tv', 'vidoza.net', 'vimeo.com',
                'vivo.sx', 'vk.com', 'voe.sx', 'wdupload.com', 'wipfiles.net', 'world-files.com', 'worldbytez.com', 'wupfile.com',
                'wushare.com', 'xubster.com', 'youporn.com', 'youtube.com']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class DirectDownloadLinkException(Exception):
    pass


def direct_link_generator(link):
    domain = urlparse(link).hostname
    if not domain:
        raise DirectDownloadLinkException("Error: URL Not Found")
    elif DEBRID_LINK_API_TOKEN and any(x in domain for x in debrid_link_sites):
        return debrid_link(link)
    elif REAL_DEBRID_API_TOKEN and any(x in domain for x in debrid_sites):
        return real_debrid(link)
    else:
        raise DirectDownloadLinkException("Error: Unsupported URL")


def debrid_link(url):
    if not DEBRID_LINK_API_TOKEN:
        raise DirectDownloadLinkException("Debrid-Link API token not provided.")
    
    cget = create_scraper().request
    resp = cget('POST', f"https://debrid-link.com/api/v2/downloader/add?access_token={DEBRID_LINK_API_TOKEN}", data={'url': url}).json()
    if not resp['success']:
        raise DirectDownloadLinkException(f"ERROR: {resp['error']} & ERROR ID: {resp['error_id']}")
    if isinstance(resp['value'], dict):
        return resp['value']['downloadUrl']
    elif isinstance(resp['value'], list):
        details = {'contents': [], 'title': unquote(url.rstrip('/').split('/')[-1]), 'total_size': 0}
        for dl in resp['value']:
            if dl.get('expired', False):
                continue
            item = {
                "path": os.path.join(details['title']),
                "filename": dl['name'],
                "url": dl['downloadUrl']
            }
            if 'size' in dl:
                details['total_size'] += dl['size']
            details['contents'].append(item)
        return details


def real_debrid(url, tor=False):
    if not REAL_DEBRID_API_TOKEN:
        raise DirectDownloadLinkException("Real-Debrid API token not provided.")
        
    def __unrestrict(url, tor=False):
        cget = create_scraper().request
        resp = cget('POST', f"https://api.real-debrid.com/rest/1.0/unrestrict/link?auth_token={REAL_DEBRID_API_TOKEN}", data={'link': url})
        if resp.status_code == 200:
            if tor:
                _res = resp.json()
                return (_res['filename'], _res['download'])
            else:
                return resp.json()['download']
        else:
            raise DirectDownloadLinkException(f"ERROR: {resp.json()['error']}")
            
    def __addMagnet(magnet):
        cget = create_scraper().request
        hash_ = re.search(r'(?<=xt=urn:btih:)[a-zA-Z0-9]+', magnet).group(0)
        resp = cget('GET', f"https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/{hash_}?auth_token={REAL_DEBRID_API_TOKEN}")
        if resp.status_code != 200 or len(resp.json()[hash_.lower()]['rd']) == 0:
            return magnet
        resp = cget('POST', f"https://api.real-debrid.com/rest/1.0/torrents/addMagnet?auth_token={REAL_DEBRID_API_TOKEN}", data={'magnet': magnet})
        if resp.status_code == 201:
            _id = resp.json()['id']
        else:
            raise DirectDownloadLinkException(f"ERROR: {resp.json()['error']}")
        if _id:
            _file = cget('POST', f"https://api.real-debrid.com/rest/1.0/torrents/selectFiles/{_id}?auth_token={REAL_DEBRID_API_TOKEN}", data={'files': 'all'})
            if _file.status_code != 204:
                raise DirectDownloadLinkException(f"ERROR: {resp.json()['error']}")
            
        contents = {'links': []}
        while len(contents['links']) == 0:
            _res = cget('GET', f"https://api.real-debrid.com/rest/1.0/torrents/info/{_id}?auth_token={REAL_DEBRID_API_TOKEN}")
            if _res.status_code == 200:
                contents = _res.json()
            else:
                raise DirectDownloadLinkException(f"ERROR: {_res.json()['error']}")
            sleep(0.5)
        
        details = {'contents': [], 'title': contents['original_filename'], 'total_size': contents['bytes']}

        for file_info, link in zip(contents['files'], contents['links']):
            link_info = __unrestrict(link, tor=True)
            item = {
                "path": os.path.join(details['title'], os.path.dirname(file_info['path']).lstrip("/")), 
                "filename": unquote(link_info[0]),
                "url": link_info[1],
            }
            details['contents'].append(item)
        return details
    
    try:
        if tor:
            details = __addMagnet(url)
        else:
            return __unrestrict(url)
    except Exception as e:
        raise DirectDownloadLinkException(e)
    if isinstance(details, dict) and len(details['contents']) == 1:
        return details['contents'][0]['url']
    return details


@app.on_message(filters.command("rll"))
async def rll(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("Please provide a URL to generate a premium link.")
            return

        url = message.command[1]
        premium_link = direct_link_generator(url)

        if isinstance(premium_link, str):
            await message.reply_text(f"Here is your premium link: {premium_link}")
        else:
            response_message = "Multiple files found:\n"
            for item in premium_link['contents']:
                response_message += f"{item['filename']}: {item['url']}\n"
            await message.reply_text(response_message)

    except DirectDownloadLinkException as e:
        await message.reply_text(str(e))
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await message.reply_text("An error occurred while processing your request.")


@app.on_message(filters.command("rdl"))
async def rdl(client: Client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("Please provide a URL or magnet link to generate a premium link.")
            return

        url = message.command[1]
        premium_link = real_debrid(url, tor='magnet:' in url)

        if isinstance(premium_link, str):
            await message.reply_text(f"Here is your premium link: {premium_link}")
        else:
            response_message = "Multiple files found:\n"
            for item in premium_link['contents']:
                response_message += f"{item['filename']}: {item['url']}\n"
            await message.reply_text(response_message)

    except DirectDownloadLinkException as e:
        await message.reply_text(str(e))
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        await message.reply_text("An error occurred while processing your request.")


@app.on_message(filters.command("start"))
async def start(client, message):
    start_txt = (
        "Hello, I am <b>Real-Debird Bot</b>,\n"
        "I can Generate <b>Premium Link</b>\n"
        "From Many Sites.\n"
        "To Know What Are The Sites Use <code>/help</code>"
        "To use me, <b>join the update channel using the buttons below.</b>"
    )
    buttons = ButtonMaker()
    buttons.ubutton("Master", "https://t.me/BalaPriyan")
    buttons.ubutton("Update", "https://t.me/BalapriyanBots")
    start_markup = buttons.build_menu(2)

    await sendMessage(message, start_txt, start_markup)


@app.on_message(filters.command("help"))
async def help(client, message):
    help_txt = (
        "<code>/rdl</code> {link} \n"
        "To generate premium link "
    )
    buttons = ButtonMaker()
    buttons.ubutton("Master", "https://t.me/BalaPriyan")
    buttons.ubutton("Update", "https://t.me/BalapriyanBots")
    help_markup = buttons.build_menu(2)

    await sendMessage(message, help_txt, help_markup)


if __name__ == "__main__":
    app.run()

