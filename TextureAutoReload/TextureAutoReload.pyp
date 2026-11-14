import c4d, os, sys, importlib
from c4d import plugins, bitmaps

# GLOBALS

pluginPath = os.path.dirname( __file__ )
modulePath = os.path.join( pluginPath, "modules" )
resourcesPath = os.path.join( pluginPath, "res" )

g_Thread = None
g_Data = {}

# GLOBALS END

# LOAD LIBS

sys.path.insert( 0, modulePath )

try:

    from Texture_Auto_Reload import constants
    from Texture_Auto_Reload import lib

finally:

    sys.path.pop( 0 )

def test():

    doc = c4d.documents.GetActiveDocument()

    if doc is None or not doc.IsAlive(): return

    currentDocumentPath = doc.GetDocumentPath()

    # skip unsaved documents with empty paths

    if currentDocumentPath == "": return

    assets = []

    result = c4d.documents.GetAllAssetsNew( doc, False, "", c4d.ASSETDATA_FLAG_TEXTURESONLY, assets )

    if not result: return

    modifiedShaders = []

    for asset in assets:

        path = asset[ "filename" ]

        try:

            modDate = os.path.getmtime( path )

        except OSError:

            continue

        key = lib.normalisePath( path )

        previousModDate = g_Data.get( key, 0 )

        if previousModDate > 0 and modDate > previousModDate:

            owner = asset.get( "owner" )

            if owner and owner.GetType() == c4d.Xbitmap: modifiedShaders.append( owner )

        g_Data[ key ] = modDate

    for shader in modifiedShaders:

        c4d.CallButton( shader, c4d.BITMAPSHADER_RELOADIMAGE )

    if modifiedShaders: c4d.EventAdd()

def endThread():

    global g_Thread

    if g_Thread is None: return

    g_Thread.End()

    g_Thread = None

    print( "Texture Auto Reload stopped" )

def PluginMessage( id, data ):

    if id in ( c4d.C4DPL_ENDACTIVITY, c4d.C4DPL_RELOADPYTHONPLUGINS ):

        if g_Thread != None: endThread()

    if id == c4d.C4DPL_RELOADPYTHONPLUGINS:

        importlib.reload( constants )
        importlib.reload( lib )

    return False

class TextureAutoReloadMessage( plugins.MessageData ):

    def CoreMessage( self, id, msg ):

        if id == constants.EVENT_ID_RUN_TEST: 
            
            try:

                test()

            finally:

                if g_Thread: g_Thread.ResetEventPending()

        return False

class TextureAutoReload( plugins.CommandData ):
    
    def Execute( self, doc ):

        global g_Thread

        if g_Thread is None:

            g_Thread = lib.RepeatingTimerThread( constants.EVENT_ID_RUN_TEST, constants.CHECK_INTERVAL, constants.TITLE )

            result = g_Thread.Start( c4d.THREADMODE_ASYNC, c4d.THREADPRIORITYEX_LOWEST )

            if result: 
                
                print( "Texture Auto Reload running…" )

            else:
                
                g_Thread = None

                print( "Texture Auto Reload could not start" )

        else:

            endThread()

        return True

    def GetState( self, doc ):

        state = c4d.CMD_ENABLED

        if g_Thread is not None: state |= c4d.CMD_VALUE

        return state

class TextureAutoReloadClearData( plugins.CommandData ):
    
    def Execute( self, doc ):

        print( "{} path keys/file last mod date/times cleared".format( len( g_Data ) ) )
        
        g_Data.clear()

        # print( "TextureAutoReload data cache cleared" )

        return True

if __name__ == "__main__":

    theBitmap = bitmaps.BaseBitmap()
    
    theBitmap.InitWith( os.path.join( resourcesPath, "icon.tif" ) )

    plugins.RegisterCommandPlugin( id = constants.MAIN_COMMAND_PLUGIN_ID, 
                                   str = constants.MAIN_COMMAND_NAME, 
                                   info = 0, 
                                   icon = theBitmap, 
                                   help = constants.MAIN_COMMAND_HELP, 
                                   dat = TextureAutoReload() )

    theBitmap.InitWith( os.path.join( resourcesPath, "icon-clear-cache.tif" ) )                         

    plugins.RegisterCommandPlugin( id = constants.CLEAR_COMMAND_PLUGIN_ID, 
                                   str = constants.CLEAR_COMMAND_NAME, 
                                   info = 0, 
                                   icon = theBitmap, 
                                   help = constants.CLEAR_COMMAND_HELP, 
                                   dat = TextureAutoReloadClearData() )

    plugins.RegisterMessagePlugin(
        id = constants.TIMER_MESSAGE_DELEGATE,
        str = "",
        info = 0,
        dat = TextureAutoReloadMessage() )
