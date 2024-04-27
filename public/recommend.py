from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

import sys
import json



dataset = pd.read_csv("Tourism.csv")



def calculate_recommendation_score(row):
    return row['numberOfReviews'] /row['rawRanking']



def recommend_places_with_similarity(dataset, region, subcategory, subtype=None):
    if subtype:
        filtered_data = dataset[(dataset['Region'] == region) & 
                                (dataset['subcategories'] == subcategory) & 
                                (dataset['subtype'] == subtype)].copy()  
    else:
        filtered_data = dataset[(dataset['Region'] == region) & 
                                (dataset['subcategories'] == subcategory)].copy() 

    if filtered_data.empty:
        return "No recommendations found for the selected region and subcategory."

    filtered_data['recommendation_score'] = filtered_data.apply(calculate_recommendation_score, axis=1)

    vectorizer = TfidfVectorizer()
    if subtype:
        feature_text = filtered_data['subcategories'] + ' ' + filtered_data['subtype'] 
    else:
        feature_text = filtered_data['subcategories']
    feature_matrix = vectorizer.fit_transform(feature_text)

    similarity_matrix = cosine_similarity(feature_matrix, feature_matrix)

    sim_scores = list(enumerate(similarity_matrix[-1]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:]  

    top_indices = [x[0] for x in sim_scores]
    top_recommendations = filtered_data.iloc[top_indices].sort_values(by=['recommendation_score'], ascending=False)

    return top_recommendations[['name', 'rating', 'numberOfReviews', 'recommendation_score']]


if __name__ == '__main__':
    region = sys.argv[1]
    subcategory = sys.argv[2]
    subtype = sys.argv[3] if len(sys.argv) > 3 else None

    recommendations = recommend_places_with_similarity(dataset, region, subcategory, subtype)

    print(json.dumps(recommendations.to_dict(orient='records')))

