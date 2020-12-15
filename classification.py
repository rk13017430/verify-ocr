import fasttext
# model = fasttext.train_supervised(input="final.txt")
# model.save_model("final.bin")

model =fasttext.load_model("final.bin")
# labels = model.get_labels()
# print(len(labels))
res = model.predict("kjencjenfkcmeklm hebcjenjkfnej jknberjnfkjrenj")

print(res)

# import pandas as pd
# import re

# df = pd.read_csv ('names.csv', usecols=[0], names=['colA'])
# df['colA'] = df['colA'].apply(lambda x:re.sub('[^A-Za-z]+', ' ', x) )

# df.to_csv('final.csv')

