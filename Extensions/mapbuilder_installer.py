# mapbuilder installer for CPSGeo Map Tool

import os 

# we expect a mapbuilder javascript package to have been extracted into
# the skins/mapbuilder directory, resulting in CPSGeo/skins/mapbuilder/lib/...

def install_lib(self):
    """Call in the context of a site portal_maps to install the mapbuilder
    Javascript library"""
    # mapbuilder and lib folders
    self.manage_addProduct['OFSP'].manage_addFolder('mapbuilder')
    self.mapbuilder.manage_addProduct['OFSP'].manage_addFolder('lib')
            
    mb_dir = os.path.join(os.environ['INSTANCE_HOME'], 'Products',
                           'CPSGeo', 'skins')
    os.chdir(mb_dir)
    
    for root, dirs, files in os.walk('mapbuilder/lib'):
        # ignore .svn directories
        if root.find('.svn') > 0:
            continue
        container = self.unrestrictedTraverse(root)
        for d in dirs:
            container.manage_addProduct['OFSP'].manage_addFolder(d)
        for f in files:
            ext = os.path.splitext(f)[1]
            f_path = os.path.join(mb_dir, root, f)
            if ext.lower() in ['.jpg', '.gif', '.png']:
                data = open(f_path).read()
                container.manage_addProduct['OFSP'].manage_addImage(f, data)
            else:
                container.manage_addProduct['OFSP'].manage_addDTMLMethod(f,
                                                        file=open(f_path))

    # Install patched mapbuilder tools and widgets
    # ---------------------------------------------------------------------
    mb_lib = self.mapbuilder.lib

    # GmlPointRenderer
    patchfile = open(os.path.join(mb_dir, 'mapbuilder-patches', 
                                  'GmlPointRenderer.js'), 'r')
    patched_content = patchfile.read()
    renderer = getattr(mb_lib.widget, 'GmlPointRenderer.js')
    renderer.manage_edit(data=patched_content, title='')

    # FeatureBase
    patchfile = open(os.path.join(mb_dir, 'mapbuilder-patches', 
                                  'FeatureBase.js'), 'r')
    mb_lib.tool.manage_addProduct['OFSP'].manage_addDTMLMethod(
                                                'FeatureBase.js',
                                                file=patchfile)

    # Change zoom hardcoded default value from 4 to 1.5
    patchfile = open(os.path.join(mb_dir, 'mapbuilder-patches',
                                  'ZoomIn.js'), 'r')
    patched_content = patchfile.read()
    orig = getattr(mb_lib.widget, 'ZoomIn.js')
    orig.manage_edit(data=patched_content, title='')

    # Change zoom hardcoded default value from 4 to 1.5
    patchfile = open(os.path.join(mb_dir, 'mapbuilder-patches',
                                  'ZoomOut.js'), 'r')
    patched_content = patchfile.read()
    orig = getattr(mb_lib.widget, 'ZoomOut.js')
    orig.manage_edit(data=patched_content, title='')

    # Remove the javascript alert when a document geolocated tried to
    # be rendered on restricted map.
    patchfile = open(os.path.join(mb_dir, 'mapbuilder-patches',
                                   'Proj.js'), 'r')
    patched_content = patchfile.read()
    orig = getattr(mb_lib.model, 'Proj.js')
    orig.manage_edit(data=patched_content, title='')

    # Avoid useless alert at model load time.
    patchfile = open(os.path.join(mb_dir, 'mapbuilder-patches',
                                   'Config.js'), 'r')
    patched_content = patchfile.read()
    orig = getattr(mb_lib.model, 'Config.js')
    orig.manage_edit(data=patched_content, title='')

    # Now, add all cps document icons from Products/CPSDocuments/skins/
    # to the mapbuilder default skin folder
    icon_dir = os.path.join(os.environ['INSTANCE_HOME'], 'Products',
                           'CPSDocument', 'skins', 'cps_document_images')
    items = os.listdir(icon_dir)
    for f in items:
        ext = os.path.splitext(f)[1]
        if ext.lower() in ['.jpg', '.gif', '.png']:
            f_path = os.path.join(icon_dir, f)
            data = open(f_path).read()
            self.mapbuilder.lib.skin.default.images.manage_addProduct['OFSP'].manage_addImage(f, data)

    return 1

