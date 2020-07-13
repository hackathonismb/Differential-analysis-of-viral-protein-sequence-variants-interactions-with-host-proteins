# Differential analysis of viral protein sequence variants interactions with host proteins 

Project Contributors: Adriaan Ludl, Mingzhang Yang, Yuchen Ge, Yuk Kei Wan, Ariel Aptekmann, Awtum Brashear, Xavier Watkins, Tom Madej, Philippe Youkharibache

## The task at hand

We have started to develop a flexible analysis of molecular interfaces between 2 arbitrary sets of residues in a tertiary or quaternary structure involving protein, RNA, DNA, small molecules.  It is especially aimed at studying in detail molecular interactions at the atom or residue level.  We can already compare SARS-CoV-1/SARS-CoV-2 interaction networks with ACE2 interactively  for example, or with other beta coronaviruses variants, but we should aim at developing an automated differential binding analysis.   Any other case can be envisioned, yet an outcome of this hackathon project is to develop a general method and provide a useful analysis to the community studying SARS-CoV-2 at the root of the COVID-19 pandemic.


## Why this project is critical and timely

The interaction surface between the viral RBD and the human ACE2 is an important aspect of SARS-CoV-2 pathology and biology. The binding interface of SARS-COV2 has different (and more) anticipated contacts with the ACE2 protein than is expected for SARS-COV-1. This is just one of endless examples in which differential interactions with a protein may be biologically important to the protein of interest. iCn3D already includes many tools to explore the interface between two proteins, and can be modified to allow comparison between the binding potentials of 2 proteins to a third protein. By automating comparison of binding networks in subject and reference sequences, we will enable researchers to quickly and effectively interact with the protein binding mechanism. 

## Our plan towards a solution

We have 4 main goals in order to establish an approachable differential analysis of protein interactions. 

| Aim  | Description |
| ------------- | ------------- |
| 1  | Automated differential residue interaction network identification between 2 arbitrary sets of residues (1 level).   |
| 2  | Contact tracing -- secondary and tertiary interactions. Pathways between interactions.  |
| 3  | Visualization of differential and conserved subnetworks with available tables  |
| 4  | Integration of side-by-side visualizations for 2D networks |

## Implementation

The establishment of a reference-based numbering system that allows comparison between two networks will be essential to this project. 
The creation of contact maps will be a necessary mediator to downstream differential analysis. 
Ultimately, all outcomes will need to be easily visualized and interacted with within the iCn3D interface for maximal impact. 


![image of proposed workflow]
(https://github.com/hackathonismb/Differential-analysis-of-viral-protein-sequence-variants-interactions-with-host-proteins/blob/develop/slides/Team%202A.png)

## Preliminary outcomes


## Future development

During the development of this project, we've established additional goals for the iCn3D ecosystem that would further benefit the field. 
1. Link the interaction window currently at the chain level with computed interaction networks at the residue level
2. Creating a database for SARS-CoV-2 mutations
3. Visualization of intramolecular interactions between 1D maps, especially for H-bonds and Cys bridges
4. Inegration of R into the ecosystem 
