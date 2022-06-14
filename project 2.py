import math
import copy
import time

start_time=time.time()
# This function checks if the over all accuracy with the feature is better or without the feature
def add_feature2(acc, acccurr, test):
    feature_local = 0
    if acc > acccurr:
        acccurr = acc
        feature_local = test
    return feature_local,acccurr
def realgame(add_this, frwdfeature_s, frwdfinal,best_acc,check2,check22,val):
    if add_this >= 0:
      if val ==1:
        frwdfeature_s.append(add_this)
        frwdfinal.append(add_this)
      elif val ==2:
        frwdfeature_s.remove(add_this)
        frwdfinal.remove(add_this)		
        print ('\n\nFeature set ', frwdfeature_s, ' was best, accuracy is ', best_acc, '%\n\n')
    else:
        print ('\n\n(Warning, Accuracy has decreased! Continuing search in case of local maxima)')
        if val ==1:
            frwdfeature_s.append(check2)
        elif val ==2:
            frwdfeature_s.remove(check2)
        print ('Feature set ', frwdfeature_s, ' was best, accuracy is ', check22, '%\n\n')
    print ('Finished search!! The best feature subset is', frwdfinal, ' which has an accuracy of accuracy:', best_acc, '%')

# This is forward selection and backward elimination
# Its chooses features one by one using leave-out and nearest neighbor algorithm.
# It returns a final feature subset with best accuracy
def featureselection(method, data, accr):
    if method == 'forward':
        featureset = []
        final_features = []
        BestAcc = 0.0
        for i in range(num_features):
            feature_add,Acccurr,val = -1,0.0,1
            for j in range(1, num_features + 1):
                if j not in featureset:
                    current = copy.deepcopy(featureset)
                    current.append(j)
                    acc = leave_out(data, current)
                    print ('\tUsing feature(s) ', current, ' accuracy is ', acc, '%')
                    check2,check22 =  add_feature2(acc, Acccurr, j)
                    if acc > BestAcc:
                        BestAcc = max(BestAcc,acc)
                        feature_add = j
            realgame(feature_add, featureset, final_features,BestAcc,check2,check22,val)
    else:	
        featureset = [i+1 for i in range(num_features)]
        final_features = [i+1 for i in range(num_features)]	
        beatacc,val = accr,2
        for i in range(num_features):
            Feature_remove,localAccuracy = -1,0.0
            for j in range(1, num_features + 1):
                if j in featureset:
                    current = copy.deepcopy(featureset)
                    current.remove(j)
                    acc = leave_out(data, current)
                    print ('\tUsing feature(s) ', current, ' accuracy is ', acc, '%')
                    if acc > beatacc:
                        beatacc = acc
                        Feature_remove = j
                    check2,check22 =  add_feature2(acc, localAccuracy, j)
            realgame(Feature_remove, featureset, final_features,beatacc,check2,check22,val) 

# Nearest_Neighbor_Classifier function calculates euclidean distance between each data point and finds minimum distance. 
def Nearest_Neighbor_Classifier(data, row_data, final_subset):
	Neighbor = 0
	minimum_distance = float('inf')
	for i in range(num_instances):
		if row_data != i:
			euclidean_distance = 0
			for j in range(len(final_subset)):
				euclidean_distance +=  pow((data[i][final_subset[j]] - data[row_data][final_subset[j]]), 2)
			euclidean_distance = math.sqrt(euclidean_distance)
			if euclidean_distance < minimum_distance:
				Neighbor = i 
				minimum_distance = euclidean_distance
	return Neighbor
# checks if the class label match the neighbor of the data point	
def class_validation(neighbor,data,leave):
    if data[neighbor][0] != data[leave][0]:
        return False
    return True

#calculates accuracy
def calc_accuracy(correct_instances):
    acc=correct_instances / num_instances * 100
    return acc

# this function chooses one instance in all instance one after other.
def leave_out(data, fe_subset):
	correct_instances = 0
	for i in range(num_instances):
		leave = i
		neighbor = Nearest_Neighbor_Classifier(data, i, fe_subset)
		if class_validation(neighbor,data,leave):
			correct_instances = correct_instances + 1
	return calc_accuracy(correct_instances)



# data is loaded and number of features and number of instances are found out.
start_time=time.time()
print ('Welcome to Shreya\'s Feature Selection Algorithm.')
file = input('Type in the name of the file to test: ')
data = open(file, 'r')
features= data.readline()
features=features.split()
num_features = len(features) - 1
data.seek(0)
num_instances = sum(1 for line in data)
data.seek(0)
instances = [[] for i in range(num_instances)]
for i in range(num_instances):
	instances[i] = [float(j) for j in data.readline().split()]

# We choose the algorithm between Forward Selection and Backward Elimination
print ('Type the number of the algorithm you want to run.')
print ('1. Forward Selection')
print ('2. Backward Elimination')
choice = int(input())
print ('This dataset has {} features (not including the class attribute), with {} instances.'.format(num_features,num_instances))

featurelist = []
featurelist = [i for i in range(1,num_features+1)]
accuracy = leave_out(data, featurelist)
print ('Running nearest neighbor with all ', num_features, ' features, using "leaving-one-out" evaluation, I get an accuracy of ', accuracy, '%.')
print ('Beginning search.\n\n')
if choice == 1:
	featureselection('forward',instances, None)
elif choice == 2:
	featureselection('backward',instances, accuracy)
print("Time Taken:",time.time()-start_time)
