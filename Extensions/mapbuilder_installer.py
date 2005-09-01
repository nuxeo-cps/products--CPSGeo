# mapbuilder installer for CPSGeo Map Tool

import os 

# we expect a mapbuilder javascript package to have been extracted into
# the skins/mb directory, resulting in CPSGeo/skins/mb/mapbuilder/lib/...

def install_lib(self):
    """Call in the context of a site portal_maps to install the mapbuilder
    Javascript library"""
    # mapbuilder and lib folders
    self.manage_addProduct['OFSP'].manage_addFolder('mapbuilder')
    self.mapbuilder.manage_addProduct['OFSP'].manage_addFolder('lib')
            
    mb_dir = os.path.join(os.environ['INSTANCE_HOME'], 'Products',
                           'CPSGeo', 'skins', 'mb')
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

def install_demo_app(self):
    """Call in the context of a site portal_maps to install the demo app
    config and model components"""
    self.manage_addProduct['OFSP'].manage_addFolder('demo')
       
    mb_dir = os.path.join(os.environ['INSTANCE_HOME'], 'Products',
                           'CPSGeo', 'skins', 'mb')
    os.chdir(mb_dir)
    
    for root, dirs, files in os.walk('demo'):
        # ignore .svn directories
        if root.find('.svn') > 0:
            continue
        
        container = self.unrestrictedTraverse(root)
        for f in files:
            ext = os.path.splitext(f)[1]
            f_path = os.path.join(mb_dir, root, f)
            if ext.lower() in ['.pt']:
                #data = open(f_path).read()
                #container.manage_addProduct['PageTemplates'].manage_addPageTemplate(id, text=data)
                # above results in AttributeError: PageTemplates, for now
                # we need to create the index_html manually
                pass
            else:
                container.manage_addProduct['OFSP'].manage_addDTMLMethod(f,
                                                        file=open(f_path))
    return 1


                
