import utils
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.rcParams.update({'font.size': 20})
plt.rcParams["figure.dpi"] = 120
plt.rcParams["figure.figsize"] = (16, 9)
plt.rc('xtick',labelsize=8)
plt.rc('ytick',labelsize=8)
plt.rc('legend',fontsize=16)
# plt.rcParams['axes.titlepad'] = -20 
def loadimage(path):
    return utils.image2byte((utils.imread(path)))


def add_noise_to_image(image_bytes, prb):
    image_bits = utils.String_to_BitList(image_bytes)
    
    
    image_bits = utils.channelError(image_bits[:-16*16], prb) + image_bits[-16*16:]
    
    # image_bits = utils.channelError(image_bits[-16*9:], prb) + image_bits[:-16*9]
    return utils.BitList_to_String(image_bits)





def plotImages(imagesList, rows, cols, number = 100, trialOrder = ["DES" , "AES-128" , "AES-192" , "AES-256"]):
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    # trialOrder = ["DES" , "AES-128" , "AES-192" , "AES-256"]
    figure = plt.figure(figsize=(18,12), dpi= 120)
    figure.tight_layout()
    print(len(trialOrder))
    figure.suptitle(f'The decrypted images (monalisa{number}) for the {len(trialOrder)} trials with different error rates')
    gs = gridspec.GridSpec(ncols=cols, nrows=rows, figure=figure, wspace= 0, hspace=0.1)
    
    
    pltDics = {}
    for errIx, err in enumerate(channelErr):

        for trIx, trial in enumerate(trialOrder):
            # , sharex = 
            if (not errIx) or (not trIx):
                pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx])
                # if not errIx:
                    
                #     pltDics[(err, trial)].set_title(f'trial: {trial}', fontsize = 14)
                # if not trIx:    
                #     pltDics[(err, trial)].set_ylabel(f'Error rate: {err}', fontsize = 14)
            else:
                pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx], sharex = pltDics[(channelErr[errIx], trialOrder[0])], sharey =  pltDics[(channelErr[0], trialOrder[trIx])])
                
            
            pltDics[(err, trial)].set_xticklabels([])
            pltDics[(err, trial)].set_yticklabels([])
            pltDics[(err, trial)].set_aspect('equal')
            pltDics[(err, trial)].plot(projection = utils.imshow_(imagesList[errIx][trIx], title1= ''))
            if (not errIx) or (not trIx):
                # pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx])
                if not errIx:
                    
                    pltDics[(err, trial)].set_title(f'encryption: \n {trial}', fontsize = 18, c = 'teal')
                if not trIx:    
                    pltDics[(err, trial)].set_ylabel(f'Error rate: \n {err}', fontsize = 18, c = 'teal')
    
    figure.show()
    
    
    return

def plotDistortions(pixelDistortions, trialOrder = ["DES" , "AES-128" , "AES-192" , "AES-256"]):

    cipherTypes  = []
    for ix in range(len(pixelDistortions[0])):
        
        ctype = [lst[ix] for lst in pixelDistortions]
        cipherTypes.append(ctype)
    
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    
    figure = plt.figure(figsize=(8,7), dpi= 120)
    figure.suptitle('the effect of channel error on pixel error rate \n for different encryption techniques', fontsize = 18)
    plt.ylabel('The pixel error rate')
    plt.xlabel('The channel error rate')
    def incr(lst, i):
        return [x+i for x in lst]
    for i in range(len(trialOrder)):
        plt.scatter(list(map(str, channelErr))[::-1], incr(cipherTypes[i] , min(cipherTypes[i]) *0.01*(i%2)), label = trialOrder[i], alpha = 0.4)
        
    
    plt.legend()
    
    figure.show()


    

import pandas as pd

def mini_distortions_plot(distortions):
    assert len(distortions) == 4
    # sizes = ['M_100','M_200','M_300','M_400']
    
    # plt.scatter(sizes,distortions)
    
    
    
    sizes = ['M_100','M_200','M_300','M_400']
    s = [4,8,16,20]
    # fig=plt.figure()
    
    # ax=fig.add_subplot(111, label="1")
    # ax2=fig.add_subplot(111, label="2", frame_on=False)
    
    # ax.plot(sizes, times, color="C0")
    # ax.set_xlabel("monalisa pictures", color="C0")
    
    # ax2.plot(s, times, color="C1", alpha = 0.7)
    # ax2.xaxis.tick_top()
    # ax2.set_xlabel('image size (kbytes)', color="C1")
    # ax2.xaxis.set_label_position('top')
    # ax2.tick_params(axis='x', colors="C1")
    
    # plt.plot(projection = ax )
    # plt.plot(projection = ax2)
    plt.plot(sizes, distortions)
    plt.scatter(sizes,distortions)
    for i, dist in enumerate(distortions):
        plt.annotate(round(dist, 3), ( sizes[i], dist + dist/10 ), fontsize = 6)
    # plt.gca().twiny()
    ax2 = plt.gca().twiny()
    ax2.plot(s, distortions, alpha = 0.6, c = 'red')
    ax2.tick_params(axis='x', labelcolor= 'red')
    ax2.set_xlabel('size in Kbytes', color='red', fontsize = 8)
    
    
    
    return plt

def plotDistortions_vssize(pixelDistortions_size, rows, cols, trialOrder = ["DES", "DES3", "AES-128", "RC4"]):  
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    figure = plt.figure(figsize=(16,9), dpi= 100)
    # figure.tight_layout()
    figure.suptitle('The pixel error rate with increasing image size for all encryption technique and error rates', y = 1.04)
    figure.supylabel('Pixel error-rate')
    figure.supxlabel('Images with increasing size')
    
    
    gs = gridspec.GridSpec(ncols=cols, nrows=rows, figure=figure, wspace= 0.1, hspace= 0.5)
    
    
    pltDics = {}
    for errIx, err in enumerate(channelErr):

        for trIx, trial in enumerate(trialOrder):
            # , sharex = 
            if (not errIx) and (not trIx):
                
                pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx])
                

                
                
            
                

            else:
                pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx], sharex = pltDics[(channelErr[0], trialOrder[0])])
                # pltDics[(channelErr[0], trialOrder[0])].get_shared_x_axes().join(pltDics[(err, trial)])
                # pltDics[(channelErr[0], trialOrder[0])]
                
                
            
            # pltDics[(err, trial)].set_xticklabels([])
            # pltDics[(err, trial)].set_yticklabels([])
            # pltDics[(err, trial)].set_aspect('equal')
            
            
            pltDics[(err, trial)].plot(projection = mini_distortions_plot([distortion_sizes[errIx][trIx] for distortion_sizes in pixelDistortions_size]))
            if (not errIx) or (not trIx):
                if not errIx:
                    pltDics[(err, trial)].set_title(f'encryption: \n {trial}', fontsize = 18, c = 'teal')

                if not trIx:    
                    pltDics[(err, trial)].set_ylabel(f'Error rate: \n {err}', fontsize = 18, c = 'teal')
            
            if trIx:
                pltDics[(err, trial)].tick_params(axis="y", labelsize=0)
                
    m1, m2, m3 = max(max([time_lists[0] for time_lists in pixelDistortions_size])),max(max([time_lists[1] for time_lists in pixelDistortions_size])),max(max([time_lists[2] for time_lists in pixelDistortions_size]))
    for i in range(len(trialOrder)):
        pltDics[(channelErr[0], trialOrder[i])].set_ylim([0, m1*1.2])
        pltDics[(channelErr[1], trialOrder[i])].set_ylim([0, m2*1.2])
        pltDics[(channelErr[2], trialOrder[i])].set_ylim([0, m3*1.2])

    
    figure.show()
    
    
    
def plotTime(timeComplexity, trialOrder = ["DES" , "AES-128" , "AES-192" , "AES-256"], name = 'Time'):
    
    channelErr = [10e-4 ,10e-5 , 10e-6 ]

    figure = plt.figure(figsize=(16,9), dpi= 100)
    gs = gridspec.GridSpec(ncols=3, nrows=1, figure=figure)
    
    cipherTypes  = []
    for ix in range(len(timeComplexity[0])):
        
        ctype = [lst[ix] for lst in timeComplexity]
        cipherTypes.append(ctype)
    
    
    DF_IX = [
        sum([ [i]*len(channelErr) for i in trialOrder], []),
        sum([channelErr]*len(trialOrder), [])
        ]
    
    cols = [f'{name}']
    
    time_dataframe = pd.DataFrame(index = DF_IX, columns = cols)
    
    time_dataframe.index.set_names(['Technique', 'channel error'], inplace= True)
    
    for err_ix, err in enumerate(list(map(str,channelErr))):
        for tr_ix, trial in enumerate(trialOrder):
            time_dataframe.loc[trialOrder[tr_ix], channelErr[err_ix]][f'{name}'] = timeComplexity[err_ix][tr_ix]
            # time_dataframe.loc[trialOrder[tr_ix], channelErr[err_ix]][' '] = timeComplexity[err_ix][tr_ix][1]
            
    print('\n', time_dataframe)

    
    time_dataframe.unstack().plot(  kind = 'bar', stacked = False, title = f'The {name} for \n each encryption technique and the error rates', legend = True)
    
def mini_time_plot(times):
    assert len(times) == 4
    for i in times:
        assert type(i) == float
    sizes = ['M_100','M_200','M_300','M_400']
    s = [4,8,16,20]
    # fig=plt.figure()
    
    # ax=fig.add_subplot(111, label="1")
    # ax2=fig.add_subplot(111, label="2", frame_on=False)
    
    # ax.plot(sizes, times, color="C0")
    # ax.set_xlabel("monalisa pictures", color="C0")
    
    # ax2.plot(s, times, color="C1", alpha = 0.7)
    # ax2.xaxis.tick_top()
    # ax2.set_xlabel('image size (kbytes)', color="C1")
    # ax2.xaxis.set_label_position('top')
    # ax2.tick_params(axis='x', colors="C1")
    
    # plt.plot(projection = ax )
    # plt.plot(projection = ax2)
    plt.plot(sizes, times)
    plt.scatter(sizes,times)
    for i, dist in enumerate(times):
        plt.annotate(round(dist, 3), ( sizes[i], dist + dist/10 ), fontsize = 6)
    # plt.gca().twiny()
    ax2 = plt.gca().twiny()
    ax2.plot(s, times, alpha = 0.6, c = 'red')
    ax2.tick_params(axis='x', labelcolor= 'red')
    ax2.set_xlabel('size in Kbytes', color='red', fontsize = 8)

    return plt
   
    
def plotTime_vssize(timeComplexity_size, rows, cols, trialOrder = ["DES" , "AES-128" , "AES-192" , "AES-256"]):
    
    channelErr = [10e-4 ,10e-5 , 10e-6 ]
    figure = plt.figure(figsize=(16,9), dpi= 100)
    # figure.tight_layout()
    figure.suptitle('The total time with increasing image size for all encryption technique and error rates', y = 1.04)
    figure.supylabel('Total time in seconds')
    figure.supxlabel('Images with increasing sizes')
    
    
    gs = gridspec.GridSpec(ncols=cols, nrows=rows, figure=figure, wspace= 0.1, hspace= 0.5)
    
    
    pltDics = {}
    for errIx, err in enumerate(channelErr):

        for trIx, trial in enumerate(trialOrder):
            # , sharex = 
            if (not errIx) and (not trIx):
                
                pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx])
                

                
                
            
                

            else:
                pltDics[(err, trial)] = figure.add_subplot(gs[errIx, trIx], sharex = pltDics[(channelErr[0], trialOrder[0])])
                # pltDics[(channelErr[0], trialOrder[0])].get_shared_x_axes().join(pltDics[(err, trial)])
                # pltDics[(channelErr[0], trialOrder[0])]
                
                
            
            # pltDics[(err, trial)].set_xticklabels([])
            # pltDics[(err, trial)].set_yticklabels([])
            # pltDics[(err, trial)].set_aspect('equal')
            
            ax = mini_time_plot([time_lists[errIx][trIx] for time_lists in timeComplexity_size])
            pltDics[(err, trial)].plot(projection = ax)
            
            
            if (not errIx) or (not trIx):
                if not errIx:
                    pltDics[(err, trial)].set_title(f'encryption: \n {trial}', fontsize = 18, c = 'teal')

                if not trIx:    
                    pltDics[(err, trial)].set_ylabel(f'Error rate: \n {err}', fontsize = 18, c = 'teal')
            
            if trIx:
                pltDics[(err, trial)].tick_params(axis="y", labelsize=0)
    
    m1, m2, m3 = max(max([time_lists[0] for time_lists in timeComplexity_size])),max(max([time_lists[1] for time_lists in timeComplexity_size])),max(max([time_lists[2] for time_lists in timeComplexity_size]))
    for i in range(len(trialOrder)):
        pltDics[(channelErr[0], trialOrder[i])].set_ylim([0, m1 + 0.5])
        pltDics[(channelErr[1], trialOrder[i])].set_ylim([0, m2 + 0.5])
        pltDics[(channelErr[2], trialOrder[i])].set_ylim([0, m3 + 0.5])
    
    
    
    figure.show()

    
    
    
    
    