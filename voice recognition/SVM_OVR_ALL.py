# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 18:02:57 2021

@author: QU-user
"""



from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import os 
from sklearn.model_selection import StratifiedKFold
from skimage import io 
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
from sklearn.model_selection import train_test_split
#from sklearn import svm
#from sklearn.preprocessing import LabelEncoder
import time
classes=["Alexa","Google","Seven","Happy","Noise"]
#arrays to store features and labels

flattened_Features=[]

lables=[]



for c in classes:
    img_Path=os.path.join("Spectro_final_16khz",c)
    
    for image in os.listdir(img_Path):
        
        current_Image=io.imread(os.path.join(img_Path,image),as_gray=True)
        current_Image=resize(current_Image, (64,64,1))
        flatten_Image=current_Image.flatten()
        flattened_Features.append(flatten_Image)
        lables.append(classes.index(c))
        
X=np.array(flattened_Features)
Y=np.array(lables)

print(" images feature extraction completed ")




X1_train, X1_test, y1_train, y1_test = train_test_split( X, Y, test_size=0.2, random_state=42)


#parameter grid search to select best hyper parameter , with cross validation 
Hyper_parameters= {}

start_grid=time.time()

for c in classes:
    print("Grid Search for {} vs rest".format(c))
    x=X1_train.copy()
    y=y1_train.copy()
    
    y=(y==classes.index(c)).astype(int)

    parameter_grid = {'C': [0.1,1, 10, 100], 'gamma': [0.1,0.01,0.001],'kernel': ['rbf', 'poly', 'sigmoid']}

#parameter_grid = {'C': [0.1], 'gamma': [0.1],'kernel': ['poly','sigmoid' ]} # this is just for testing the code, this line should be commented and uncomment the above line 

    grid = GridSearchCV(svm.SVC(),parameter_grid,refit=False,scoring='accuracy', return_train_score=False,verbose=1,n_jobs=-1,cv=10) # cv=10 fold cross validation 
    grid.fit(x,y)


#get all parameter combinations to a data frame
    param_combinations=pd.DataFrame(grid.cv_results_['params'])

#get test score of each parameter combination to a data frame
    test_score=pd.DataFrame(grid.cv_results_['mean_test_score'])

#combine the dataframes
    parameters_stat=pd.concat([param_combinations,test_score], axis=1, join='inner') #it can be used to get the best parameter combinations, plot the graph of validation accuracy of each parameter combination

    parameters_stat=parameters_stat.rename({0: 'test_score'},axis=1)

    print("Hyper parameters")

    print(parameters_stat)

#get the row with maximum value of test score

    m_row=parameters_stat['test_score'].argmax()

#best hyperparameters

    b_C=parameters_stat.iloc[m_row]['C']

    b_gamma=parameters_stat.iloc[m_row]['gamma']

    b_kernel=parameters_stat.iloc[m_row]['kernel']
    
    Hyper_parameters['SVM_OVR_{} vs rest'.format(c)]=[b_C,b_gamma,b_kernel]
    
    parameters_stat.to_csv('./SVM_Results_16khz/SVM_OVR_{} vs rest.csv'.format(c))
    
    print("Grid Search for {} vs rest completed".format(c))

stop_grid=time.time()    


grid_time=stop_grid-start_grid

k_Folds = StratifiedKFold(n_splits=5)
k_Folds.get_n_splits(X,Y)

#X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size=0.2, random_state=42)
Fold=1

accuracy=[]

f1_Score_sep= []
f1_Score_micro=[]
f1_Score_macro=[]


p_Score_sep=[]
p_Score_micro=[]
p_Score_macro=[]

r_Score_sep=[]
r_Score_micro=[]
r_Score_macro=[]


Train_time=[]
Test_time=[]

for train_index,test_index in k_Folds.split(X,Y):
        print("Starting fold {}".format(Fold))
        true_Confidence = []
        classifiers_List=[]
        classifiers={}
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = Y[train_index], Y[test_index]

        start_train=time.time()        
        for c in classes:
    

           y=y_train==classes.index(c)

           y=y.astype(int) #convert boolean values to integers

#Y=to_categorical(Y) #Encode the labels, lable encoding is required for ANN in keras library 
           h_Param=Hyper_parameters['SVM_OVR_{} vs rest'.format(c)]
   
           model=svm.SVC(C=h_Param[0],gamma=h_Param[1],kernel=h_Param[2],probability=True,verbose=True)
           

           
           model.fit(X_train,y)
           
           
           

           
           classifiers["SVM_OVR_{}vsRest".format(c)]=model
           classifiers_List.append("SVM_OVR_{}vsRest".format(c))
           print("SVM_OVR_{}vsRest training completed".format(c))
        stop_train=time.time()
		tr_time=stop_train-start_train
           
        Train_time.append(tr_time)
        confidence_Score=[]
        true_Confidence = []
        
        start_test=time.time()
        
        for clfr in classifiers_List:
    
            clf=classifiers[clfr]
            probab=clf.predict_proba(X_test)
            confidence_Score.append(probab)
            true_Confidence.append(probab[:,1])
    
        final_Confidence=np.array(true_Confidence)

        predictions=np.argmax(final_Confidence,axis=0)
        
        stop_test=time.time()
        
        te_time=stop_test-start_test
        Test_time.append(te_time)
        
        acc=(y_test==predictions).mean()*100
        
        f1_Score_s= f1_score(y_test, predictions, average=None)
        f1_Score_mi=f1_score(y_test, predictions, average='micro')
        f1_Score_ma=f1_score(y_test, predictions, average='macro')


        p_Score_s= precision_score(y_test, predictions, average=None)
        p_Score_mi=precision_score(y_test, predictions, average='micro')
        p_Score_ma=precision_score(y_test, predictions, average='macro')
        
        
        r_Score_s= recall_score(y_test, predictions, average=None)
        r_Score_mi=recall_score(y_test, predictions, average='micro')
        r_Score_ma=recall_score(y_test, predictions, average='macro')



        f1_Score_sep.append(f1_Score_s)
        f1_Score_micro.append(f1_Score_mi)
        f1_Score_macro.append(f1_Score_ma)


        p_Score_sep.append(p_Score_s)
        p_Score_micro.append(p_Score_mi)
        p_Score_macro.append(p_Score_ma)
        
        r_Score_sep.append(r_Score_s)
        r_Score_micro.append(r_Score_mi)
        r_Score_macro.append(r_Score_ma)
        
        accuracy.append(acc)
        
        print("accuracy={}".format(acc))
        print("fold {} finished".format(Fold))
        
        Fold=Fold+1
        

print ( " Final average accuracy : {}".format(np.array(accuracy).mean()))
 

       
#Save final classifiers
    
# classifier_File=open("./SVM_Results_16khz/SVM_OVR_CLF.pkl","wb")
# pickle.dump(classifiers,classifier_File)
# classifier_File.close()



# load saved classifiers and predict on single fature / image , required for real time system

# clf_file=open("./SVM_Results_16khz/SVM_OVR_CLF.pkl","rb")
# classifiers_new=pickle.load(clf_file)
    
# for clfr in classifiers_List:
    
#             clf=classifiers_new[clfr]
#             probab=clf.predict_proba(np.array[flattened_feature])
#             confidence_Score.append(probab)
#             true_Confidence.append(probab[:,1])
    
# final_Confidence=np.array(true_Confidence)

# predictions=np.argmax(final_Confidence,axis=0)

# print("the class is {}".format(classes[predictions[0]]))



