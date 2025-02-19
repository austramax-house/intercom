import Service
import os, rp2


class Filesystem(Service.Service):
    mounted = False
    dir = '/flash'


    def mount(self):
        self.log('Attempting to mount')

        try:
            os.stat(self.dir)
            self.log('Already mounted')
            self.mounted = True
            return
        except:
            pass

        try:
            bdev = rp2.Flash()
            vfs = os.VfsLfs2(bdev)
            os.mount(vfs, self.dir)
            self.log('Mounted successfully')
            self.mounted = True
        except:
            self.log('Unknown error while mounting')
        

    def exists(self, filename) -> bool:
        try:
            open(filename, 'r')
            return True
        except:
            return False


    def read(self, filename):
        stream = open(filename, 'r')
        content = stream.read()
        stream.close()
        return content



    def write(self, filename, content):
        stream = open(filename, 'w')
        stream.write(content)
        stream.close()