from Service import Service
import os, rp2

class Filesystem(Service):
    mounted = False


    def mount(self):
        self.log('Attempting to mount')
        try:
            bdev = rp2.Flash()
            vfs = os.VfsLfs2(bdev)
            os.mount(vfs, '/flash')
            self.log('Mounting successful')
            self.mounted = True
        except:
            self.log('Mounting unsuccessful')
        

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