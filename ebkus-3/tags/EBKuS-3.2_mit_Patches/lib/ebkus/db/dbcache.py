# coding: latin-1

class DBCache:

    def __init__(self):
        self.data = {}
        
    def clear(self):
        self.data.clear()

    def clear_if_gt(self, no_items):
        if len(self.data) > no_items:
            self.clear()
            
    def undo_cached_fields(self):
        for k,d in self.data.items():
            klass = k[0]
            obj = klass()
            obj.data = d
            obj.undo_cached_fields()
            
    def get(self, object, id = None):
        id = id or object.data.get(object.primarykey)
        cache = self.data
        if id:
            data = cache.get((object.__class__, id))
            if data:
                object.data = data
                return object
            else:
                return None
        otherkeys = object.otherkeys
        data = object.data
        for i in range(len(otherkeys)):
            try:
                values = tuple(map(lambda x,data=data: data[x], otherkeys[i]))
                object.data = cache[(object.__class__, i, values)]
                return object
            except: pass
        return None
        
    def cache(self, object, update_inverses = None):
        id = object.data.get(object.primarykey)
        cache = self.data
        klass = object.__class__
        data = object.data
        otherkeys = object.otherkeys
        if id:
            cache[(klass, id)] = data
            if update_inverses:
                for field, (klass, inversefield) in object.foreignfieldtypes.items():
                    fk = object.data.get(field)
                    if inversefield and fk and self.is_cached(klass, fk):
                        inverselist = klass(fk).data.get(inversefield + '_ids')
                        if not inverselist is None:
                            inverselist.append(id)
        for i in range(len(otherkeys)):
            try:
                values = tuple(map(lambda x, data=data: data[x], otherkeys[i]))
                cache[(klass, i, values)] = data
            except:
              #print 'DBCache-Exception'
                pass
                
    def uncache(self, object, update_inverses = None):
        id = object.data.get(object.primarykey)
        cache = self.data
        klass = object.__class__
        data = object.data
        otherkeys = object.otherkeys
        if id:
            del cache[(klass, id)]
            if update_inverses:
                for field, (klass, inversefield) in object.foreignfieldtypes.items():
                    fk = object.data.get(field)
                    if inversefield and fk:
                        inverselist = klass(fk).data.get(inversefield + '_ids')
                        if not inverselist is None:
                        ##jh: wirft sonst Exception beim delete von n-n, removeteiln
                            try:
                                inverselist.remove(id)
                            except: pass
        for i in range(len(otherkeys)):
            try:
                values = tuple(map(lambda x,data=data: data[x], otherkeys[i]))
                del cache[(klass, i, values)]
            except: pass
            
    def is_cached(self, klass, id):
        return self.data.get((klass, id))
        
    def is_on(self): return 1
    def on(self): pass
    def off(self):
        self.clear()
        self.__class__ = DummyDBCache
    def printe(self): print 'Real'
    
class DummyDBCache:

    def __init__(self): pass
    def clear(self): pass
    def undo_cached_fields(self): pass
    def get(self, object, id = None): pass
    def cache(self, object, update_inverses = None): pass
    def uncache(self, object, update_inverses = None): pass
    def is_cached(self, klass, id): pass
    def is_on(self): return None
    def on(self): pass
    def on(self):
        self.__class__ = DBCache
    def off(self): pass
    def printe(self): print 'DUmmy'
    
