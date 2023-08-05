# Copyright(c) 2016, The f-scLVM developers (Florian Buettner, Oliver Stegle)
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from sklearn.decomposition import RandomizedPCA,PCA
import h5py
import scipy as SP
import re
import matplotlib as mpl
import matplotlib.lines as mlines
mpl.use('Agg')
import pylab as plt
import os
import brewer2mpl
import sys
#from fscLVM.utils import *
import fscLVM
from bayesnet.vbfa import *

data_dir = '../../../data/'
out_base = './../results/'

def simpleaxis(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()


def mad(X):
    median = SP.median(X, axis=0)
    return SP.median(abs(X-median), axis=0)
    
def secdev(x):
    return 1/(2*SP.pi)*(SP.exp(-x*x/2.))*(x*x-1)
    
    
def saveFA(FA, out_name=None, saveF=False, out_dir='./'):
    """Saves output of fscLVM.CSparseFA object

    Args:
        FA                 (:class:`fscLVM.CSparseFA`): Factor analysis object, ususally generated using `initFA` function
        out_name                         (str): Name of hdf file to save the model to. Default is `None' for which a filename is created automatically.
        saveF                           (bool): Boolean variable indicating whether to save the imputed expression space.
        out_dir                          (str): data directory where to save the outpout
                                                                      
    """    

    if out_name==None:
        out_name = os.path.join(out_dir,FA.getName()+'.hdf5')
    out_file = h5py.File(out_name,'w')    
    out_file['relevance'] = FA.getRelevance()
    out_file['W'] = FA.getW()
    out_file['X'] = FA.getFactors()     
    out_file['Z'] = FA.getZ()
    out_file['I'] = FA.getAnnotations()
    out_file['terms'] = FA.getTerms()
    out_file['idx_genes'] = FA.idx_genes
    if saveF==True:
        out_file['F'] = FA.getF()
              
    out_file.close()    



def dumpFA(FA):
    """Dumps output of fscLVM.CSparseFA object in a dictionary

    Args:
        FA                 (:class:`fscLVM.CSparseFA`): Factor analysis object, ususally generated using `initFA` function
                                                                      

    Returns:
        dictionary with results
    """    

    out_file ={}
    out_file['relevance'] = FA.getRelevance()
    out_file['W'] = FA.getW()
    out_file['X'] = FA.getFactors()     
    out_file['Z'] = FA.getZ()
    out_file['I'] = FA.getAnnotations()
    out_file['terms'] = FA.getTerms()
    out_file['idx_genes'] = FA.idx_genes
              
    return out_file      


    
    
    
def loadFA(out_name):
    out_file = h5py.File(out_name,'r')    
    res = {}   
    for key in out_file.keys():    
        res[key] = out_file[key]    
    return res
    
    
def plotFactors(FA,idx1=0, idx2=1, X = None,  lab=None, terms=None, cols=None, isCont=True,madFilter=0.4):
    """Scatter plot of 2 factors

    Args:
        FA                 (:class:`fscLVM.CSparseFA`): Factor analysis object, ususally generated using `initFA` function
        idx1                    (int): Index of first factor to be plotted
        idx2                    (int): Index of second factor to be plotted
        lab             (vector_like): Vector of labels for each data point
        isCont                 (bool): Boolean variable indicating whether labels should be interpreted as discrete or continuous
        cols            (vector_like): Vector of colors. Should be the same length as unique labels. Default is `None`, 
                                       then the `brewer2mpl` 
        madFilter             (float): Filter factors by this mean absolute deviation to exclude outliers. 
                                        For large datsets this can be set to 0.                                           
     """       

    if FA!=None:
        print FA
        S = FA.getFactors()
        alpha = FA.getRelevance()
        terms = FA.getTerms()
        MAD = mad(FA.S.E1)
        alpha = (MAD>madFilter)*alpha
        idxF = SP.argsort(-alpha)    
        X1 = FA.S.E1[:,idxF[idx1]]
        X2 = FA.S.E1[:,idxF[idx2]]
    else:
        X1 = X[:,idx1]
        X2 = X[:,idx2]        
    
    if isCont==False:
        uLab = SP.unique(lab)  
        if cols==None:
            try:
                import brewer2mpl
            except ImportError:
                print 'Specify colors using the cols argument or install the brewer2mpl module'
            bmap=brewer2mpl.get_map('Paired', 'Qualitative', len(uLab))
            cols = bmap.hex_colors         
        pList=list()
        for i in range(len(X1)):
            pList.append(plt.plot(X1[i], X2[i], '.',color=cols[SP.where(lab[i]==uLab)[0]]))
        plt.xlabel(terms[idxF[idx1]])
        plt.ylabel(terms[idxF[idx2]])
        lList=list()
        for i in range(len(uLab)):
            lList.append( mlines.Line2D([], [], color=cols[i], marker='.',
                              markersize=7, label=uLab[i], linewidth=0))     
        plt.legend(handles=lList)
    else:
        if lab!=None:
            plt.scatter(X1, X2, c=lab, s=20)
        else:
            plt.scatter(X1, X2, s=20)
        plt.xlabel(terms[idx1])
        plt.ylabel(terms[idx2])
    plt.show()


    
def plotTerms(FA=None, S=None, alpha=None, terms=None, madFilter=.4):
    """Plot terms and their respective relevance

    Args:
        FA                 (:class:`fscLVM.CSparseFA`): Factor analysis object, ususally generated using `initFA` function
        madFilter          (float)           : Filter factors by this mean absolute deviation to exclude outliers. 
                                                For large datsets this can be set to 0.
    """    


    if FA!=None:
        S = FA.getFactors()
        alpha = FA.getRelevance()
        terms = FA.getTerms()
    else:
        assert S!=None
        assert alpha!=None
        assert terms!=None

    MAD = mad(S)
    alpha = (MAD>madFilter)*(alpha)
                 
    idx_sort = SP.argsort(terms)
    Y = alpha[idx_sort]
    X =SP.arange(len(alpha))#[idx_sort]
    plt.plot(X, Y, '.',markersize=10)
    plt.xticks(X, terms[idx_sort], size='small', rotation='vertical')    
    plt.ylabel("Relevance score")
    plt.show()
    
    

def plotFA(FA,Nactive=20,stacked=True, db='MSigDB', madFilter=0.4, unannotated=False):
    """Plot results of f-scLVM

    Identified factors and corresponding gene set size ordered by relevance (white = low relevance; black = high relevance). 
    Top panel: Gene set augmentation, showing the number of genes added (red) and removed (blue) by the model for each factor.

    Args:
        FA                 (:class:`fscLVM.CSparseFA`): Factor analysis object, ususally generated using `initFA` function
        Nactive                                  (int): Numer of terms to be plotted
        stacked                                 (bool): Boolean variable indicating whether bars should be stacked
        db                                      (str): Name of database used, eihter 'MSigDB' or 'REACTOME'
        madFilter                              (float): Filter factors by this mean absolute deviation to exclude outliers. 
                                                        For large datsets this can be set to 0.
        unannotated                             (bool): Indicates whether also unannotated factors should be plotted. Defaults to False.

    """


    pltparams = {'backend': 'pdf',
              'axes.labelsize': 12,
              'font.size': 12,
              'legend.fontsize': 13,
              'xtick.labelsize': 14,
              'ytick.labelsize': 12,
              'text.usetex': False}
              
              
    plt.rcParams.update(pltparams)

    pattern_hidden = re.compile('hidden*')
    pattern_bias = re.compile('bias')


    if db=='REACTOME':
        substring = 'REACTOME_'
    else:
        substring=''

    terms = FA.getTerms()
    X = FA.getFactors()
    I = FA.getAnnotations(unannotated=True)
    Z = FA.getZ()
    rel = FA.getRelevance()

    Ihidden = SP.array([pattern_hidden.match(term) is not None for term in terms])
    Ibias = SP.array([pattern_bias.match(term) is not None for term in terms])


    if unannotated==False:
        iUse = ~Ihidden & ~Ibias
    else:
        iUse = ~Ibias        

    Iprior     = (I[:,iUse])
    Iposterior = (Z[:,iUse]>0.5)
    MAD = mad(X[:,iUse])
    R = (MAD>madFilter)*(rel)[iUse]
    terms = terms[iUse]

    Nactive = min(SP.sum(R>0),Nactive)

    #terms change,s etc. 
    Nprior = Iprior.sum(axis=0)
    #gains
    Ngain  = (Iposterior & (~Iprior)).sum(axis=0)
    #loss
    Nloss  = ((~Iposterior & (Iprior))).sum(axis=0)

    #sort terms by relevance
    Iactive = R.argsort()[::-1][0:Nactive]
    RM = R[Iactive,SP.newaxis]

    xticks_range = SP.arange(Nactive)
    terms[terms=='hidden'] = substring+'Unannotated'
    terms[terms=='hiddenSparse'] = substring+'Unannotated-sparse'
    xticks_text  = list(terms[Iactive])


    xticks_text = [terms[terms.find(substring)+len(substring):30] for terms in xticks_text]
    xticks_text = [terms.capitalize().replace('_',' ') for terms in xticks_text]


    n_gain = []
    n_loss = []
    n_prior = []
    for i in xrange(Nactive):
        n_gain += [Ngain[Iactive[i]]]
        n_loss += [-1.0*Nloss[Iactive[i]]]
        n_prior += [Nprior[Iactive[i]]]


    width = 0.6
    left = SP.arange(Nactive)-0.5 + (1.-width)/2.
    
    fig = plt.figure(2,figsize=(10,6))
    fig.subplots_adjust(bottom=0.3)

    gs = mpl.gridspec.GridSpec(2, 2,height_ratios=[2.,1.],width_ratios=[1.,0.05])
    gs.update(hspace = 0.1)

    #fig.text(0.06, 0.6, 'Number of annotated genes', ha='center', va='center', rotation='vertical', fontsize=17)

    #################################################################################
    ax1 = plt.subplot(gs[1, 0])
    simpleaxis(ax1)
    ax1.set_xlabel('Active pathways', fontsize=15)
    ax1.set_ylabel('Gene set size', fontsize=13.5)
    #im = ax1.imshow(SP.append(RM.T,[[0]],axis=1),origin=[0,0],interpolation='nearest',cmap='Greys',aspect='auto')
    
    minima = 0
    maxima = max(RM)

    norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)

    mapper = mpl.cm.ScalarMappable(norm=norm, cmap='Greys')
    
    colors = []
    for v in RM.flatten():
        colors += [mapper.to_rgba(v)]

    #colors = []
    #for i in xrange(RM.shape[0]):
    #    colors += [im.cmap(im.norm(RM[i]))[0,:-1]]

    y_max = Nprior[Iactive].max()+100.

    bar_rel_importance = ax1.bar(left=SP.arange(Nactive)-0.5 ,width=1.05,height=[y_max]*len(n_prior),bottom=0,color=colors,log=True, edgecolor = 'none')
    bar_annotated = ax1.bar(left=left,width=width,height=n_prior,bottom=0,color='w',log=True,alpha=0.6, edgecolor = 'k')

    ax1.set_ylim([10,y_max])
    ax1.set_xlim([0,Nactive])
    #ax1.set_yticks([])
    #ax1.set_yscale('log')
    plt.xticks(xticks_range,xticks_text,rotation=45,fontsize = 14,ha='right')


    color_bar_ax = plt.subplot(gs[1, 1])
    mpl.colorbar.ColorbarBase(color_bar_ax, cmap='Greys',norm=norm,orientation='vertical',ticks=[minima,maxima])

    #color_bar = fig.colorbar(im, cax=color_bar_ax,ticks=[0., RM.max()])
    color_bar_ax.set_yticklabels([0,1])
    #color_bar_ax.set_yticklabels([0,round(RM.max(),3)])
    #color_bar_ax.set_ylabel('Rel. importance')
    #color_bar.outline.set_visible(False)
    #################################################################################

    ax0 = plt.subplot(gs[0, 0],sharex=ax1)
    simpleaxis(ax0)

    if stacked:
        bar_gain = ax0.bar(left=left,width=width,height=n_gain,bottom=0,color='#861608')
        bar_loss = ax0.bar(left=left,width=width,height=n_loss,bottom=0,color='#0c09a0')
    else: 
        bar_gain = ax0.bar(left=SP.arange(Nactive)-0.5,width=0.5,height=n_gain,bottom=0,color='#861608')
        bar_loss = ax0.bar(left=SP.arange(Nactive),width=0.5,height=n_loss,bottom=0,color='#0c09a0')

    #figure out range to make ylim symmatrix
    ax0.axhline(y=0,linestyle='-',color='gray')

    #ax0.set_yscale('symlog')
    gap = SP.ceil(max(max(n_gain), abs(min(n_loss)))/4.)
    y_max = SP.ceil(max(n_gain)/gap)
    y_min = SP.floor(min(n_loss)/gap)
    yticks = SP.arange(y_min*gap,y_max*gap,gap)
    ax0.set_yticks(yticks)
    ax0.set_ylabel('Gene set augemntation', fontsize=13.5)
    ax0.legend((bar_gain[0],bar_loss[0]),('Gain','Loss'),ncol=1,loc='center left', bbox_to_anchor=(1, 0.5),frameon=False, fontsize=15)
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.show()

    return fig



    

def vcorrcoef(X,y):
    Xm = SP.reshape(SP.mean(X,axis=1),(X.shape[0],1))
    ym = SP.mean(y)
    r_num = SP.sum((X-Xm)*(y-ym),axis=1)
    r_den = SP.sqrt(SP.sum((X-Xm)**2,axis=1)*SP.sum((y-ym)**2))
    r = r_num/r_den
    return r

 
def getIlabel(order, Y, terms, pi,init_factors=None):
    assert (order in ['preTrain', 'PCA'])


    if order=='preTrain':
        assert init_factors!=None
        Ilabel = preTrain(Y, terms, pi,init_factors)
        return Ilabel
    else:
        PCs = SP.zeros((Y.shape[0], pi.shape[1]))
        for k in pi.shape[1]:
            pca = PCA(n_components=1)
            pca.fit_transform(Y[:,pi[:,k]>.5])
            PCs[:,k] = pca.score[:,0]

        X  = pca.fit_transform(Y)
        nFix = (SP.where(terms=='hidden')[0]).min()+len(SP.where(terms=='hidden')[0])
        MPC = abs(vcorrcoef(PCs.T,X.T))[nFix:]
        IpiRev = SP.argsort(MPC.ravel())      
        Ilabel = range(len(terms))
        Ilabel[nFix:] = IpiRev+nFix
        return Ilabel
        

def preTrain(Y, terms, P_I, noise='gauss', nFix=None):
    """Pre-train the f-scLVM factor analysis model.

    Helper function to pre-train the f-scLVM factor analysis model to achieve 
    faster convergence and obtain an initial update order. Called by `initFA`.

    Args:
        Y          (array_like): Matrix of normalised count values of `N` cells 
                                 and `G` variable genes in log-space.
                                 Dimension (:math:`N\\times G`).
        terms     (vector_like): Names of `K` annotated gene sets. Dimension
                                 (:math:`K\\times 0`).
        P_I        (array_like): Matrix specifying the likelihood of 
                                 whether a gene is annotated to a specific factor.
                                 Dimension (:math:`G\\times K`).
        noise              (str): Specifies the observation noise model. Should be either `'gauss'`,`'hurdle'` or `'poisson'`.
                                 Defaults to `gauss`.             
        nFix               (int): Number of terms which should be fixed and updated first. Defaults to `None`, 
                                  resulting in the number of unannotated factors being updated first.                                                            
                               

    Returns:
        A vector containing the initial update order of the terms
    """


    #import fscLVM.core as fscLVM


    init_params = {}
    init_params['noise'] = noise
    init_params['iLatent'] = SP.where(terms=='hidden')[0]    

    pi = P_I.copy()
    K = pi.shape[1]

    #data for sparseFA instance    
    pi[pi>.8] =1-1e-100#0.9999
    pi[pi<.2] =1e-100
    

    init={'init_data':CGauss(Y),'Pi':pi,'terms':terms, 'noise':noise}
    sigmaOff = 1E-3
    sparsity = 'VB'

    #prior on noise level 
    priors = {'Eps': {'priors':[1E-3,1E-3]}}
    #how to initialize network?
    #initType = 'pcaRand'
    terms0=terms
    pi0=pi.copy()
    FA0 = fscLVM.CSparseFA(components=K,sigmaOff=sigmaOff,sigmaOn=SP.ones(pi.shape[1])*1.0,sparsity=sparsity,nIterations=50,permutation_move=False,priors=priors,initType='pcaRand')
    FA0.init(**init)
    if nFix==None:
        nFix = FA0.nKnown+FA0.nLatent
                        
#Fit PCA        
    pca = PCA(n_components=1)
    pca.fit(FA0.Z.E1)
    X = pca.transform(FA0.Z.E1)


#Sort by correlation to PC1    
    MPC = abs(vcorrcoef(FA0.S.E1[:,SP.argsort(FA0.W.Ilabel)].T,X.T))[nFix:]
    Ipi = SP.argsort(-MPC.ravel())
    IpiRev = SP.argsort(MPC.ravel())


    mRange = range(FA0.components)
    mRange[nFix:] = Ipi+nFix
    
    mRangeRev = range(FA0.components)
    mRangeRev[nFix:] = IpiRev+nFix

#Run model for 50 iterations         
    pi = pi0[:,mRange]
    terms = terms0[mRange]     
    init={'init_data':CGauss(Y),'Pi':pi,'terms':terms, 'noise':noise}
    FA = fscLVM.CSparseFA(components=K,sigmaOff=sigmaOff,sigmaOn=SP.ones(pi.shape[1])*1.0,sparsity=sparsity,nIterations=50,permutation_move=False,priors=priors,initType='pcaRand')
    FA.shuffle=True
    FA.init(**init) 
    for j in range(50):
        FA.update()      
        

    #Run reverse model for 50 iterations         
    pi = pi0[:,mRangeRev]
    terms = terms0[mRangeRev]
    init={'init_data':CGauss(Y),'Pi':pi,'terms':terms, 'noise':noise}
    FArev = fscLVM.CSparseFA(components=K,sigmaOff=sigmaOff,sigmaOn=SP.ones(pi.shape[1])*1.0,sparsity=sparsity,nIterations=50,permutation_move=False,priors=priors,initType='pcaRand')
    FArev.shuffle=True
    FArev.init(**init) 

    #FArev.iterate(forceIterations=True, nIterations=nIterations)
    for j in range(50):
        FArev.update() 
            
    #import pdb
    #pdb.set_trace()
    IpiM = (-(0.5*(1./FArev.Alpha.E1[SP.argsort(mRangeRev)][nFix:])+.5*(1./FA.Alpha.E1[SP.argsort(mRange)][nFix:]))).argsort()    

#    IpiM = (-(0.5*(1./FArev.Alpha.E1[SP.argsort(mRangeRev)][nFix:]*FArev.S.E1[:,SP.argsort(mRangeRev)][:,nFix:].std(0))+.5*(1./FA.Alpha.E1[SP.argsort(mRange)][nFix:]*FA.S.E1[:,SP.argsort(mRange)][:,nFix:].std(0)))).argsort()    
    Ilabel = SP.hstack([SP.arange(nFix),IpiM+nFix])

    return Ilabel


def load_hdf5(dFile, data_dir='../../../data/'):  
    """Load input file for f-scLVM

    Loads an hdf file and extracts all the inputs required by f-scLVM 

    Args:
        dFile (str): String contaning the file name of the hdf file with the input data.
        data_dir    (str): Name of the directory containing the input hdf5 file.


    Returns:
        An dictionary containing all the inputs required by f-scLVM.
    """    

    dataFile = h5py.File(os.path.join(data_dir, dFile), 'r')
    data = smartGetDictHdf5(dataFile)
    data['Y'] = data.pop('Yhet').T
    return data






def initFA(Y, terms, I, nHidden=3, nHiddenSparse = 0,pruneGenes=False, FPR=0.99, FNR=0.001, \
            noise='gauss', minGenes=20, do_preTrain=True):
    """Initialise the f-scLVM factor analysis model.

    Required 3 inputs are first, a gene expression matrix `Y` containing normalised count values of `N` cells and `G` 
    variable genes in log-space, second a vector `terms` contaning the names of all annotated gene set (correspondig to annotated factors) 
    and third, a binary inidcator matrix `I` linking `G` genes to `K` terms by indicating which genes are annotated to each factor. 
    A variety of options can be specified as described below. 

    Args:
        Y (array_like): Matrix of normalised count values of `N` cells 
                                 and `G` variable genes in log-space.
                                 Dimension (:math:`N\\times G`).
        terms    (vector_like): Names of `K` annotated gene sets. Dimension
                                 (:math:`K\\times 0`).
        P_I          (array_like): Inidicator matirx specifying
                                 whether a gene is annotated to a specific factor.
                                 Dimension (:math:`G\\times K`).
        FNR             (float): False negative rate of annotations.
                                 Defaults to 0.001
        FPR             (float): False positive rate of annotations.
                                 Defaults to 0.99                                 
        nHidden           (int): Number of unannotated dense factors. Defaults to 3.
        nHiddenSparse       (int): Number of unannotated sparse factors. Defaults to 0. 
                                 This value should be changed to e.g. 5 if the diagnositcs fail. 
        pruneGenes         (bool): prune genes that are not annotated to a least one factor. This option allows fast inference and 
                                   should be set to `True` either if the 
                                   key objective is to rank factors or if the annotations cover all genes of interest.  
                                   Defaults to `False`.
        noise              (str): Specifies the observation noise model. Should be either `'gauss'`,`'hurdle'` or `'poisson'`.
                                 Defaults to `gauss`.                                      
        minGenes          (int): minimum number of genes required per term to retain it  
                                 Defaults to `20`.  
        do_preTrain      (bool): Boolean switch indicating whether pre-training should be used to establish the initial 
                                update order. Can be set to `False` for very large datasets.
                                Defaults to `True`                                                                 

    Returns:
        A :class:`fscLVM.CSparseFA` instance.
    """

    
    #check for consistency of input parameters
    [num_cells,num_genes] = Y.shape
    num_terms             = I.shape[1]

    assert I.shape[0]==num_genes, 'annotation needs to be matched to gene input dimension'
    #OS: check list
    assert noise in ['gauss','hurdle','poisson'], 'invalid noise model'
    assert 0<FNR<1, 'FNR is required to be between 0 and 1'
    assert 0<FNR<1, 'FPR is required to be between 0 and 1'

    #make sure the annotation is boolean
    I = (I>.5)     
    #. filter annotation by min number of required genes
    Iok = I.sum(axis=0)>minGenes
    terms = terms[Iok]
    I     = I[:,Iok]
    num_terms = I.shape[1]


    #create initial pi matrix, which corresponds to the effective prior probability of an annotated link
    pi = SP.zeros([num_genes,num_terms],dtype='float')    
    #default FNR
    pi[:] = FNR
    #active links
    pi[I] = FPR 

    #prune genes?
    if pruneGenes==True:
        idx_genes  = SP.sum(I,1)>0
        Y = Y[:,idx_genes]
        pi = pi[idx_genes,:]
    else:
        idx_genes = SP.arange(Y.shape[1])        


    #center data for Gaussian observation noise
    if noise=='gauss':
        Y-=SP.mean(Y,0)       

    #include hidden variables
    if nHiddenSparse>0:
        piSparse = SP.ones((Y.shape[1],nHiddenSparse))*.01
        idxVar = SP.argsort(-Y.var(0))
        for iH in range(piSparse.shape[1]):
            idxOnH = SP.random.choice(idxVar[:100],20, replace=False)
            piSparse[idxOnH,iH] = 0.99
        pi = SP.hstack([piSparse, pi])
        terms = SP.hstack([SP.repeat('hiddenSparse',nHiddenSparse),terms])

    terms = SP.hstack([SP.repeat('hidden',nHidden), terms])
    pi = SP.hstack([SP.ones((Y.shape[1],nHidden))*.99,pi])
    num_terms += nHidden

#mean term for non-Gaussian noise models
    if noise!='gauss':
        terms = SP.hstack([ 'bias',terms])
        pi = SP.hstack([SP.ones((Y.shape[1],1))*(1.-1e-10),pi])        
        num_terms += nHidden

    if do_preTrain==True:   
        Ilabel = preTrain(Y, terms, pi, noise=noise, nFix=None)
        pi = pi[:,Ilabel]
        terms = terms[Ilabel]    

    init={'init_data':CGauss(Y),'Pi':pi,'terms':terms, 'noise':noise}
    FA = fscLVM.CSparseFA(components=num_terms, idx_genes = idx_genes)   
    FA.init(**init)  
    return FA   



def addKnown(init_factors,dFile,data, idx_known=None):
    dataFile = h5py.File(os.path.join(data_dir, dFile), 'r')
    if len(idx_known)>0:
        known_names = dataFile['known_names'][:][idx_known]
        if len(dataFile['Known'][:].shape)>1:
            known = dataFile['Known'][:].T[:,idx_known]
        else:
            known = dataFile['Known'][:][:,SP.newaxis]
        #known -= known.mean(0)
        #known /= known.std(0)
        data['terms'] = SP.hstack([ known_names,data['terms']])
        pi = SP.hstack([SP.ones((data['Y'].shape[1],len(idx_known)))*.99,data['pi']])
        data['pi'] = pi
        init_factors['Known'] = known
        init_factors['iLatent'] = init_factors['iLatent'] + len(idx_known)

    return init_factors, data



def smartAppend(table,name,value):
    """
    helper function for apppending in a dictionary  
    """ 
    if name not in table.keys():
        table[name] = []
    table[name].append(value)


def dumpDictHdf5(RV,o):
    """ Dump a dictionary where each page is a list or an array """
    for key in RV.keys():
        o.create_dataset(name=key,data=SP.array(RV[key]),chunks=True,compression='gzip')

def smartDumpDictHdf5(RV,o, chunks=True, close_file=True):
    """ Dump a dictionary where each page is a list or an array or still a dictionary (in this case, it iterates)"""
    for key in RV.keys():
        if type(RV[key])==dict:
            g = o.create_group(key)
            smartDumpDictHdf5(RV[key],g)
        else:
            if SP.isscalar(RV[key]):
                o.create_dataset(name=key,data=SP.array(RV[key]),chunks=False)
            else:
                o.create_dataset(name=key,data=SP.array(RV[key]),chunks=True,compression='gzip')
    #if close_file==True: 
        #o.close()
     
def smartGetDictHdf5(o):
    RV={}    
    for key in o.keys():
        if type(o[key])==dict:
            smartGetDictHdf5(RV[key],o[key])
        else:
            if len(o[key].shape)==0:
                RV[key] = o[key][()]
            else:
                RV[key] = o[key][:]
    return RV    
