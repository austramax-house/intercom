from App import App

app = App()
app.setup()
app.start()


# ## INIT FS
# def initFS():
#     bdev = rp2.Flash()
#     vfs = os.VfsLfs2(bdev)
#     os.mount(vfs, '/flash')
#
#
# ## MAIN
# def main():
#     print('Starting Austramax App')
#    
#     # mount filesystem
#     try:
#         print('Attempting to initialize filesystem')
#         initFS()
#         led.on()
#         print('Filesystem initialized')
#     except:
#         print('Failed to mount filesystem')
#         return flashLED()
#    
#     # check for wifi settings
#
#
# main()