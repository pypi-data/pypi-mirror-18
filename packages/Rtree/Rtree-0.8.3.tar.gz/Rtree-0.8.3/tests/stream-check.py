import numpy as np                                                                  
import rtree                                                                        
import time

def random_tree_stream(points_count, include_object):
    properties = rtree.index.Property()                                             
    properties.dimension = 3                                                        

    points_random = np.random.random((points_count,3,3))                            
    points_bounds = np.column_stack((points_random.min(axis=1),                     
                                     points_random.max(axis=1)))

    
    stacked = zip(np.arange(points_count),                                          
                  points_bounds,                                                    
                  np.arange(points_count))                                              


    tic = time.time()
    tree = rtree.index.Index(stacked,                                               
                             properties = properties)
    toc = time.time()
    print'creation, objects:', include_object, '\tstream method: ', toc-tic

    return tree

def random_tree_insert(points_count, include_object):
    properties = rtree.index.Property()                                             
    properties.dimension = 3                                                        

    points_random = np.random.random((points_count,3,3))                            
    points_bounds = np.column_stack((points_random.min(axis=1),                     
                                     points_random.max(axis=1)))
    tree = rtree.index.Index(properties = properties)
    
    if include_object:
        stacked = zip(np.arange(points_count),                                          
                      points_bounds,                                                    
                      np.arange(points_count))
    else:
        stacked = zip(np.arange(points_count), 
                                points_bounds)
    tic = time.time()
    for arg in stacked:
        tree.insert(*arg)
    toc = time.time()

    print 'creation, objects:', include_object, '\tinsert method: ', toc-tic

    return tree


def check_tree(tree, count):
    # tid should intersect every box, 
    # as our random boxes are all inside [0,0,0,1,1,1]
    tic = time.time()
    tid = list(tree.intersection([-1,-1,-1,2,2,2]))
    toc = time.time()
    ok = (np.unique(tid) - np.arange(count) == 0).all()
    print 'intersection, id method:    ', toc-tic, '\t query ok:', ok

    tic = time.time()
    tid = [i.object for i in tree.intersection([-1,-1,-1,2,2,2], objects=True)]
    toc = time.time()
    ok = (np.unique(tid) - np.arange(count) == 0).all()
    print 'intersection, object method:', toc-tic, '\t query ok:', ok

if __name__ == '__main__':
    count = 10000

    print '\nChecking stream loading\n---------------'
    tree = random_tree_stream(count, False)
    tree = random_tree_stream(count, True)
    
    check_tree(tree, count)

    print '\nChecking insert loading\n---------------'
    tree = random_tree_insert(count, False)
    tree = random_tree_insert(count, True)

    check_tree(tree, count)