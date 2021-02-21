# movie_recommendation
![alt text](https://www.researchgate.net/profile/Lionel-Ngoupeyou-Tondji/publication/323726564/figure/fig5/AS:631605009846299@1527597777415/Content-based-filtering-vs-Collaborative-filtering-Source.png)

Collaborative Filtering
This filtering method is usually based on collecting and analyzing information on user’s behaviors, their activities or preferences, and predicting what they will like based on the similarity with other users.

Content-based filtering
These filtering methods are based on the description of an item and a profile of the user’s preferred choices. In a content-based recommendation system, keywords are used to describe the items, besides, a user profile is built to state the type of item this user likes. 

We will be using k-nearest neighbors algorithm for collaborative filtering.
This is memory-based algorithms, we use the similarities between users and items and use them as weights to predict a rating for a user and an item. The difference is that the similarities in this approach are calculated based on an unsupervised learning model, rather than Pearson correlation or cosine similarity. In this approach, we also limit the number of similar users as k, which makes system more scalable.

This app is deployed in heroku https://movie-recommendation-rohit.herokuapp.com/

To train the model yourself download the dataset from this link http://files.grouplens.org/datasets/movielens/ and extract the files to ml-25m/ dir
We have used the ml-25m.zip which is movielens dataset containing 25 million rating.

Run data_processing_25m.ipynb and final_predict.ipynb to train the model


