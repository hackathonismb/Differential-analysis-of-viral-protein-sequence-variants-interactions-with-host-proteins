# -*- coding: utf-8 -*-
#
#  Generate a figure of the contact map between residues from input file.
#
#
import pandas as pan
import seaborn as sns
import matplotlib.pyplot as plt

import sys
protein_code=sys.argv[1]

colors_dict=dict()
colors_dict[ 'H-Bonds' ] = 'Greens'
colors_dict[ 'π-Cation' ] = 'Reds'
colors_dict[ 'π-Stacking' ] = 'Blues'
colors_dict[ 'Ionic' ]   = 'cool' # GTM_gebco_r cool Cyans
colors_dict[ 'halogen' ] = 'RdPu' # spring_r  'Magentas'
colors_dict[ 'contact' ] = 'Greys'

def main( group_name  ):
  """TODO: Docstring for function.

  :arg1: TODO
  :returns: TODO

  """
  data_path = '../data/interaction_matrices_fromLineGraphs/'
  suffix = '_interaction_matrix.csv'
  file_name = data_path + group_name + suffix
  df = pan.read_csv(file_name)

  #df=df.rename(columns=lambda x: x.strip('.'+group_name))
  column_chain_name = df.columns[1].split('.')[1]
  row_chain_name = df.loc[ 1, df.columns[0]].split('.')[1]

  #df=df.rename(columns=lambda x: x.replace('.'+group_name, ''))
  df=df.rename(columns=lambda x: x.split('.')[0])
  #print(df)
  df=df.rename(columns={df.columns[0]:'chain '+ row_chain_name})

  df=df.set_index(df.columns[0])
  #df=df.rename(index=lambda x: x.replace('.'+group_name, ''))
  df=df.rename(index=lambda x: x.split('.')[0])

  axes_labels = ['chain '+column_chain_name, 'chain '+row_chain_name ]

  #print(df)
  #print(df.dtypes)

  #df_all_contacts = df
  #df_all_contacts[df_all_contacts != '0'] = 1
  #df_all_contacts[df_all_contacts == '0'] = 0
  #print(df_all_contacts)
  #print(df_all_contacts.dtypes)

  target_value = '0'
  df_all_contacts = 1 - convert_target(df, target_value)
  print(df_all_contacts)
  make_plot(df_all_contacts, group_name + '_all_contacts', colors_dict[ 'contact' ], axes_labels )

  target_value = 'contact'
  df_contacts = convert_target(df, target_value)
  make_plot(df_contacts, group_name + '_'+target_value, colors_dict[ target_value ], axes_labels )

  target_value = 'H-Bonds'
  df_hbonds = convert_target(df, target_value)
  make_plot(df_hbonds, group_name + '_'+target_value, colors_dict[ target_value ], axes_labels )

  #target_value = 'Ionic'
  #df_contacts = convert_target(df, target_value)
  #make_plot(df_contacts, group_name + '_'+target_value, colors_dict[ target_value ], axes_labels )


def convert_target( df, target ):
    """ Function doc """
    df_targets = df.copy(deep=True)
    df_targets[df_targets != target] = 0
    df_targets[df_targets == target] = 1
    #df_targets[ df_targets.str.contains( target )  ] = 1
    for c in df_targets.columns:
        df_targets[c] = pan.to_numeric(df_targets[c], downcast="float")
    #print(df_targets.dtypes)
    return df_targets

def make_plot( df, data_name, cmap_name, ax_labels='A B'.split() ):
  """TODO: Docstring for function.
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
  ax = sns.heatmap( df , cmap=cmap_name  )
  #splot.figure.set_x( data_name.replace('_',' ') )
  ax.set_title( data_name.replace('_',' ') )
  #ax.set_axis_labels( *ax_labels )
  ax.set_xlabel( ax_labels[0] )
  ax.set_ylabel( ax_labels[1] )
  ax.set_aspect('equal')

  ax.figure.savefig( '../figures/'+ data_name +  ".png", bbox_inches='tight', dpi=200)
  plt.clf()


main(protein_code)
# EOF.
