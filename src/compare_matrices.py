#
#
#
"""
    Compute the best translation to match two sets of points
    (eg. representing adjacency matrices).

    :TODO:

    0: Make output useful:
           - apply the translation and obtain the common matrix,
           - output the common matrix to file,
           - output list of conserved or unique interactions.

    1: find a way to obtain union of m1 and m2 ...

    2: A possible extension, instead of considering only translations p1 - p2,
    we could also consider  translations p2 -> points close to p1.

    3: implement further tests of the alignment, eg a random matrix and the same matrix with small perturbations ...

    Algorithm proposed by Tom Madej.
    Implemented by Adriaan Ludl.

    (ISMB viralHackathon 2020)
    2020.07.16
"""
import numpy as np
import pandas as pan
from scipy.sparse import coo_matrix

from datetime import datetime
import sys
#name1=sys.argv[1]
#name2=sys.argv[2]
#delta=int(sys.argv[3])

def main( name1, name2, delta):
    """
    Main function:
      - load the data specified by input arguments,
      - find best translation (of rows and columns) on matrix 2 to align with matrix 1,
      - write the best solution to an output file.

    Inputs:
    :name1: str, name of the first input data set,
    :name2: str, name of the second input data set,
    :delta:  integer, the tolerance for closeness.
    """
    #input_path = '../data/distance_matrices_fromInteractionSortedHTML/'
    input_path = '../data/contact_distance_matrices_fromInteractionSortedHTML/NumContact/'
    suffix = '_NumContact.csv'

    m1 = load_data_as_array( name1, input_path, suffix )
    m2 = load_data_as_array( name2, input_path, suffix )

    #
    #   TODO: find a way to obtain union of m1 and m2 ...
    #

    mnz1 = m1!=0
    mnz2 = m2!=0
    n1 = (m1!=0).sum().sum()
    n2 = (m2!=0).sum().sum()
    max_score = min( n1, n2 )

    best_score, best_translation = max_score, point(0,0)
    #if not (mnz1 == mnz2).all():
    if not np.array_equal( mnz1, mnz2 ):
        list_1 = convert_matrix_to_list_of_points( m1 )
        list_2 = convert_matrix_to_list_of_points( m2 )
        #max_score_lists = min( list_1.nnz, list_2.nnz )
        max_score_lists = min( len(list_1), len(list_2) )
        if max_score != max_score_lists :
            print('#  Warning, mismath of max_scores. Check your data ...')
        best_score, best_translation = find_best_translation( list_1, list_2, delta )

    header_str = '# data set 1: ' + name1
    header_str += '\n# data set 2: ' + name2
    header_str += '\n# best score for translation: {} ; maximum possible score: {}'
    header_str = header_str.format( best_score, max_score )

    print(header_str)
    print('best translation is: ', best_translation.to_string())

    output_path = input_path
    write_translation( output_path + 'best_translation_for_'+ name1 +'_'+name2+'_delta_'+str(delta)+'.csv',
                        best_translation, header_str )

    #
    #   :TODO:
    #       - apply the translation and obtain the common matrix,
    #       - output the common matrix to file,
    #       - output list of conserved or unique interactions.
    #
    

def simple_test(a):
    """ Docstring for simple_test.
    Run a simple test on a block diagonal matrix with ones on the diagonal.

    """
    #a = 2   # size of the blocks
    n = 2*a # size of the full matrix
    block_shape = (a,a)

    import numpy as np
    id_a = np.identity( a )
    zeros_a = np.zeros( block_shape )

    m1 = np.block( [ [ id_a, zeros_a], [ zeros_a, zeros_a ] ] ) # a block matrix ...
    m2 = np.block( [ [ zeros_a, zeros_a], [ zeros_a, id_a ] ] ) # a block matrix ...
    list_1 = convert_matrix_to_list_of_points( m1 )
    list_2 = convert_matrix_to_list_of_points( m2 )

    max_score_lists = min( len(list_1), len(list_2) )
    #max_score_lists = min( list_1.nnz, list_2.nnz )
    best_score, best_translation = find_best_translation( list_1, list_2, delta )

    header_str = '# data set 1: ' + name1
    header_str += '\n# data set 2: ' + name2
    header_str += '\n# best score for translation:{} ; maximum possible score: {}'
    header_str = header_str.format( best_score, max_score_lists )

    print(header_str)
    print('best translation is: ', best_translation.to_string())

    output_path = './'
    write_translation( output_path + 'best_translation_for_test_'+ str(n) +'.csv',
                        best_translation, header_str )


def load_data_as_array( name_of_data, data_path, suffix = '_distance_matrix.csv' ):
    """
    Load the data named as input, from the path given
    as a list of point objects.

    Inputs:
    :name_of_data:  string, name of the data instance (eg protein identifier),
    :data_path:  string, path to look up for the data.

    :returns: numpy array.
    """
    df = pan.read_csv( data_path + name_of_data + suffix, 
                        index_col=0 )
    return df.to_numpy()

def convert_matrix_to_list_of_points( m ):
    """
    Convert a matrix to a list of points,
    coordinates are indices where the values o the matrix are non zero.

    Inputs:
    :m:  numerical, numpy array.

    :returns: list of points.
    """
    #l = coo_matrix(m).tolil()
    #print('lil matrix type')
    #print(l)
    #return zip(l.row,l.col,l.data)
    l = coo_matrix(m)
    #print('coo matrix type')
    #print(coo_matrix(m))
    m_list = []
    for i,j,v in zip(l.row,l.col,l.data):
        m_list.append( point(i,j,v)  )
    return m_list


def find_best_translation( list_1, list_2, delta ):
    """
    This function does a brute force search to find the best alignment
    of the points in the two input lists.

    Inputs:
    :list_1: a list of point objects (integer coordinates),
    :list_2: another list of point objects (integer coordinates),
    :delta:  integer, the tolerance for closeness.

    :returns: best_score of the translation, best_translation a point object.
    """
    best_score = 0
    best_translation = point(0,0)

    for p1 in list_1:
        for p2 in list_2:
            # translation: p2 to p1
            #if p2.is_close_to(p1,delta):
                tr = p1.subtract(p2)
                list_tr = apply_translation(list_2, tr)
                count=0
                for p3 in list_tr:
                    for p4 in list_1:
                        if p4.is_close_to(p3,delta):
                            count += 1
                if count > best_score:
                    best_score = count
                    best_translation = tr
    return best_score, best_translation


def write_translation(out_filename, a_translation, a_header):
    with open(out_filename,'w') as f:
        f.write( a_header +'\n' )
        f.write( a_translation.to_string() )


def apply_translation( list0, pt0 ):
    """
    This function translates a list of points with respect to another fix point.

    Inputs:
    :list0: a list of point objects,
    :pt0: a point with x,y coordinates,

    :returns: list of points that have been moved towards pt0.
    """
    list_moved = []
    for p in list0:
        # pm = p.subtract( pt0 )
        #list_moved.append( p.subtract( pt0 ) )
        list_moved.append( p.add( pt0 ) )
    return list_moved


class point:
    def __init__(self, x, y, v=1):
        self.x = x
        self.y = y
        self.value = v

    def man_distance(self, q):
        return abs(self.x - q.x) + abs(self.y - q.y)

    def is_close_to(self, q, delta):
        return self.man_distance(q) <= delta

    def add(self, q):
        xs = self.x + q.x
        ys = self.y + q.y
        return point(xs,ys)

    def subtract(self, q):
        xs = self.x - q.x
        ys = self.y - q.y
        return point(xs,ys)

    def to_string(self):
        return '{0:d},{1:d}'.format(self.x,self.y)
        #return '{},{}'.format(x,y)

#
#
#
t0 = datetime.now()
print('# Started at :',t0)

### RUN the code
#simple_test(2*4*20)
#simple_test(20)

name1='6M0J'
name2='2AJF'
delta=1
main( name1, name2, delta )

print('#    it took:', datetime.now() - t0)
t0 = datetime.now()
print('# Finished at :',t0)

# EOF.
