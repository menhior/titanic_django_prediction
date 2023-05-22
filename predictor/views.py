from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from .models import PredResults
import os
from sklearn.preprocessing import StandardScaler
from django.http import HttpResponse

def predict(request):
    return render(request, 'predict.html')


def predict_chances(request):

    if request.POST.get('action') == 'post':

        # Receive data from client
        pclass = request.POST.get('pclass')
        sibsp = request.POST.get('sibsp')
        parch = request.POST.get('parch')
        title = request.POST.get('ptitle')
        age = float(request.POST.get('age'))
        #sex = request.POST.get('sex')
        embarked = request.POST.get('embarked')

        sex_male=0
        sex_female=0
        sex='test'
        pclass_repl='test'
        title_repl='test'

        if sibsp == 'No one' and parch == 'No one':
            isalone = 1
        else:
            isalone = 0

        if title == 'Mr':
            title = 1
            sex_male = 1
            sex_female = 0
        elif title == 'Miss':
            title = 2
            sex_male = 0
            sex_female = 1
        elif title == 'Mrs':
            title = 3
            sex_male = 0
            sex_female = 1
        elif title == 'Master':
            title = 4
            sex_male = 1
            sex_female = 0
        elif title == 'Other':
            title = 5
            sex_male = 1
            sex_female = 0

        if sex_male == 1:
            sex = 'Male'
        else:
            sex = 'Female'


        if pclass == '1st Class':
            pclass = 1
        elif pclass == '2nd Class':
            pclass = 2
        elif pclass == '3rd Class':
            pclass = 3

        """if sex == 'Male':
                                    sex_male = 1
                                    sex_female = 0
                                elif sex == 'Female':
                                    sex_male = 0
                                    sex_female = 1"""

        if embarked == 'Cherbourg':
            embarked_C = 1
            embarked_Q = 0
            embarked_S = 0
        elif embarked == 'Queenstown':
            embarked_C = 0
            embarked_Q = 1
            embarked_S = 0
        elif embarked == 'Southampton':
            embarked_C = 0
            embarked_Q = 0
            embarked_S = 1


        features = ["Pclass", "Sex_male", 'Sex_female', "IsAlone","Age", "Embarked_C", "Embarked_Q", "Embarked_S", "Title"]

        data = {features[0]: pclass, features[3]: isalone, features[4]: age, features[8]: title,
        features[2]: sex_female, features[1]: sex_male,  features[5]: embarked_C, features[6]: embarked_Q,
        features[7]: embarked_S,}

        df = pd.DataFrame(data, index=[0])
        X = pd.get_dummies(df)
        print(X)
        """scaler=StandardScaler()
        scaler.fit(X)
        print(X.head())
        X_scaled = scaler.transform(X)
        print(X_scaled)"""

        # Unpickle model
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #model_dir = os.path.join(os.path.dirname(BASE_DIR), 'titanicpred', 'model')
        #pickle_model = os.path.join(os.path.dirname(BASE_DIR), 'titanicpred', 'model', 'model.pickle')
        pickle_model = os.path.join(os.path.dirname(BASE_DIR), 'app', 'model.pickle')
        files = os.listdir(BASE_DIR)
        #model_files = os.listdir(model_dir)
        print("Files in %r: %s" % (BASE_DIR, files))
        #print("Files in %r: %s" % (model_dir, model_files))
        #print(pickle_model)
        model = pd.read_pickle(pickle_model)
        #print(model)
        # Make prediction
        result = model.predict(X)

        if result[0] == 0:
            classification = 'Did not survive'
        elif result[0] == 1:
            classification = 'Survived' 


        print(classification)
        PredResults.objects.create(pclass=pclass, sibsp=sibsp, parch=parch, age=age, sex=sex,
                                   embarked=embarked, classification=classification, title=title)

        return JsonResponse({'result': classification, 'pclass': pclass,
                             'sibsp': sibsp, 'parch': parch, 'age': age,
                             'sex': sex, 'embarked': embarked, 'ptitle': title,},
                            safe=False)

        """return JsonResponse({'title': title,},
                            safe=False)"""

        #return HttpResponse('Hello')

def view_results(request):
    #return HttpResponse('Hello')
    # Submit prediction and show all
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)