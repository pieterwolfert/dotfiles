import dbus
import time
 
bus = dbus.SessionBus()
try :
    quodlibet_bus = bus.get_object('net.sacredchao.QuodLibet','/net/sacredchao/QuodLibet')
except dbus.exceptions.DBusException:
    quodlibet_bus = False
try :
    spotify_bus = bus.get_object('org.mpris.MediaPlayer2.spotify','/org/mpris/MediaPlayer2')
    spotify_interface = dbus.Interface(spotify_bus,'org.mpris.MediaPlayer2.Player')
    spotify_properties = dbus.Interface(spotify_bus,'org.freedesktop.DBus.Properties')
except dbus.exceptions.DBusException:
    spotify_bus = False
 
is_playing = False
 
if quodlibet_bus :
    is_playing = quodlibet_bus.IsPlaying()
    if is_playing :
        symbol = ''
    else :
        symbol = ''
    try:
        song = quodlibet_bus.CurrentSong()
        artist = str(song['artist'])
        title = str(song['title'])
        length = divmod(float(song['~#length']),60)
        current_pos = (divmod(quodlibet_bus.GetPosition()/1000,60))
        output = f"{symbol} {artist} - {title} {int(current_pos[0]):0>2}:{int(current_pos[1]):0>2}/{int(length[0]):0>2}:{int(length[1]):0>2}"
    except :
        output = f"{symbol} Nothing Playing"
 
if spotify_bus and not is_playing:
    is_playing = spotify_properties.Get('org.mpris.MediaPlayer2.Player','PlaybackStatus')
    if is_playing == 'Playing' :
        symbol = ''
    else :
        symbol = ''
    meta = spotify_properties.Get('org.mpris.MediaPlayer2.Player','Metadata')
 
    artist = str(meta['xesam:artist'][0])
    title = str(meta['xesam:title'])
    length = divmod(meta['mpris:length'] / 1000000,60)
    output = f"{symbol} {artist} - {title} {int(length[0]):0>2}:{int(length[1]):0>2}"
 
print(output)
