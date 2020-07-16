#
#
#
"""
    Compute the best translation to match two sets of points
    (eg. representing adjacency matrices).

    For now:
        - return numerical indices, label and min of number of contacts ...
        - get dimensions of matrix of common interactions.

    :TODO:

    0: Make output useful:
           - apply the translation and obtain the common matrix,
           - output the common matrix to file,
           - output list of conserved or unique interactions.

    1: find a way to obtain union of m1 and m2 ...

    2: A possible extension, instead of considering only translations p1 - p2,
    we could also consider  translations p2 -> points close to p1.

    3: implement further tests of the alignment, eg a random matrix and the same matrix with small perturbations ...
    
    4: use periodic matching with a modulo on distances ... or a convolutional version ...

    Algorithm proposed by Tom Madej.
    Implemented by Adriaan Ludl.

    (ISMB viralHackathon 2020)
    2020.07.16
"""
import numpy as np
import pandas as pan
from scipy.sparse import coo_matrix

import seaborn as sns
import matplotlib.pyplot as plt

from datetime import datetime
import os
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
    type_of_data = 'NumContact'
    input_path = '../data/contact_distance_matrices_fromInteractionSortedHTML/NumContact/'
    suffix = '_NumContact.csv'

    m1 = load_data_as_array( name1, input_path, suffix )
    m2 = load_data_as_array( name2, input_path, suffix )

    #
    #   TODO: find a way to obtain union of m1 and m2 ...
    #

    area_factor = ((2*delta)**2)

    mnz1 = m1!=0
    mnz2 = m2!=0
    n1 = (m1!=0).sum().sum()
    n2 = (m2!=0).sum().sum()
    bound_max_score = area_factor * min( n1, n2 )

    best_score, best_translation = bound_max_score, point(0,0)
    #if not (mnz1 == mnz2).all():
    if not np.array_equal( mnz1, mnz2 ):
        list_1 = convert_matrix_to_list_of_points( m1 )
        list_2 = convert_matrix_to_list_of_points( m2 )
        #max_score_lists = min( list_1.nnz, list_2.nnz )
        max_score_lists = area_factor*min( len(list_1), len(list_2) )
        if bound_max_score != max_score_lists :
            print('#  Warning, mismath of max_scores. Check your data ...')
        best_score, best_translation = find_best_translation( list_1, list_2, delta )

    header_str = '# data set 1: ' + name1
    header_str += '\n# data set 2: ' + name2
    header_str += '\n# best score for translation: {} ; bound on maximum possible score: {}'
    header_str = header_str.format( best_score, bound_max_score )

    print(header_str)
    print('best translation is: ', best_translation.to_string())

    output_path = input_path+'/comparative_alignment/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    write_translation( output_path + 'best_translation_for_'+ name1 +'_'+name2+'_delta_'+str(delta)+'.csv',
                        best_translation, header_str )

    #
    #   :TODO:
    #       - apply the translation and obtain the common matrix,
    #       - output the common matrix to file,
    #       - output list of conserved or unique interactions.
    #
    #    For now:
    #        - return numerical indices, label and min of number of contacts ...
    #        - get dimensions of matrix of common interactions.
    #
    nr1,nc1 = m1.shape
    nr2,nc2 = m2.shape
    #nc_rows = abs(best_translation.x) + min(nr1,nr2)
    nc_rows = abs(best_translation.x) + min(nr1,nr2)
    nc_cols = abs(best_translation.y) + max(nc1,nc2)
    m_common_shape = [nc_rows, nc_cols]
    list_labeled_contacts, df_common_values, df_common_labels = merge_point_lists( best_translation,
                                                list_1, list_2,
                                                name1, name2, delta,
                                                m_common_shape )

    make_plot( df_common_values, 'common_values_', 'Greys', output_path, ['chain E','chain A'] )
    make_plot_categorical( df_common_labels, 'common_labels_', 'Pastel1_r', output_path, ['chain E','chain A'] )
    #make_plot_categorical( df_common_labels, 'common_labels_', 'viridis', output_path, ['chain E','chain A'] )
    #make_plot( df_common_values, 'common_values_', 'Greys', output_path, [name1,name2] )


    partial_file_name_string = name1 +'_'+name2+'_delta_'+str(delta)
    write_list( output_path + 'list_labeled_contacts_for_'+ partial_file_name_string,
                        list_labeled_contacts, header_str )

    file_name_for_labels = 'common_labels_for_'+ partial_file_name_string+'.csv'
    df_common_labels.to_csv(output_path + file_name_for_labels )

    file_name_for_values = 'common_values_'+type_of_data+'_for_'+ partial_file_name_string+'.csv'
    df_common_values.to_csv(output_path + file_name_for_values )

    #write_matrix( output_path + 'common_matrix_for_'+ name1 +'_'+name2+'_delta_'+str(delta)+'.csv',
    #                    m_common, header_str )


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
    header_str += '\n# best score for translation: {} ; bound on maximum possible score: {}'
    header_str = header_str.format( best_score, bound_max_score )

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

    make_plot( df, 'input_'+name_of_data, 'Greys', data_path, ['chain E','chain A'] )

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


def merge_point_lists( a_translation, list_1, list_2, name_1, name_2, delta, m_common_shape ):
    """ Function doc
    Merge a list of points ...
    """
    common_label = 'both'
    #common_label = '_both_'
    n_rows, n_cols = m_common_shape
    df_common_labels = pan.DataFrame(columns=range(n_cols), index=range(n_rows)).astype(type(str(0)))
    df_common_values = pan.DataFrame(columns=range(n_cols), index=range(n_rows)).astype('float')
    for p1 in list_1:
        df_common_labels.iloc[p1.x,p1.y] = name_1
        df_common_values.iloc[p1.x,p1.y] = p1.value

    list_tr = apply_translation(list_2, a_translation)
    for p2 in list_tr:
        was_matched = 0
        for p1 in list_1:
            if p1.is_close_to(p2,delta):
                was_matched += 1
                df_common_labels.iloc[p1.x,p1.y] = common_label
                df_common_values.iloc[p1.x,p1.y] = min(p1.value, p2.value)

        if was_matched < 1 :
            df_common_labels.iloc[p2.x,p2.y] = name_2
            df_common_values.iloc[p2.x,p2.y] = p2.value

    print(df_common_labels.info(verbose=True))
    merged_list = convert_matrix_to_list_of_points(
                        df_common_labels.to_numpy(dtype=type(str(0)) ))
                        #df_common_labels.to_numpy(dtype='string', na_value=''))
    return merged_list, df_common_values, df_common_labels



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

#
#   Functions to write output:
#

def write_matrix(out_filename, a_matrix, a_header):
    np.savetxt( out_filename, a_matrix, delimiter=',', header=a_header )

def write_list(out_filename, a_list, a_header):
    with open(out_filename,'w') as f:
        f.write( a_header +'\n' )
        for point in a_list:
            #f.write( '{},{},{},{}'.format(*line) +'\n' )
            f.write( point.to_string_full() +'\n' )

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
    def __init__(self, x, y, v=1.0, l=''):
        self.x = x
        self.y = y
        self.value = v
        self.label = l

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

    def to_string_full(self):
        return '{0:d},{1:d},{2:s},{3:}'.format(self.x,self.y,self.label,self.value)


def make_plot_categorical( df, data_name, cmap_name, outpath, ax_labels='A B'.split() ):
    """ Docstring for function.
    :df: pandas.DataFrame, contains values of contact matrix to plot.
    :data_name: string, name of the data to plot.
    
    NOTE: use bokeh for this purpose as it has categorical heatmaps built in.
        http://docs.bokeh.org/en/0.11.1/docs/gallery/heatmap_chart.html
    """    
    value_to_int = {j:i for i,j in enumerate(pan.unique(df.values.ravel()))} # like you did
    n = len(value_to_int)    
    # colorsmaps: Reds, Blues, Greens, Greys
    plt.cla()
    ax = sns.heatmap( df.replace(value_to_int) , cmap=cmap_name  )
    #splot.figure.set_x( data_name.replace('_',' ') )
    ax.set_title( data_name.replace('_',' ') )
    #ax.set_axis_labels( *ax_labels )

    # modify colorbar:
    colorbar = ax.collections[0].colorbar 
    r = colorbar.vmax - colorbar.vmin 
    #colorbar.set_ticks([colorbar.vmin + r / float(n) * (0.7 + i) for i in range(n)])
    colorbar.set_ticks([colorbar.vmin + (0.9+r) / float(n) * (0.05 + i) for i in range(n)])
    colorbar.set_ticklabels(list(value_to_int.keys()))                                          

    ax.set_xlabel( ax_labels[0] )
    ax.set_ylabel( ax_labels[1] )
    ax.set_aspect('equal')
    ax.figure.savefig( outpath+ data_name +  "categ.png", bbox_inches='tight', dpi=200)
    plt.clf()



def make_plot( df, data_name, cmap_name, outpath, ax_labels='A B'.split() ):
    """ Docstring for function.
    :df: pandas.DataFrame, contains values of contact matrix to plot.
    :data_name: string, name of the data to plot.
    """
    #data_name = data_file_name.split()[-1]
    # load data as dataframe
    # convert to adjacency matrix
    # apply sorting of rows and columns where applicable
    # make plot and save
    # colorsmaps: Reds, Blues, Greens, Greys
    plt.cla()
    ax = sns.heatmap( df , cmap=cmap_name, vmin=0  )
    #splot.figure.set_x( data_name.replace('_',' ') )
    ax.set_title( data_name.replace('_',' ') )
    #ax.set_axis_labels( *ax_labels )
    ax.set_xlabel( ax_labels[0] )
    ax.set_ylabel( ax_labels[1] )
    ax.set_aspect('equal')

    ax.figure.savefig( outpath+ data_name +  ".png", bbox_inches='tight', dpi=200)
    plt.clf()


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
