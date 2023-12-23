import streamlit as st
import pickle
import numpy as np

# Load pickled data
model = pickle.load(open('model.pkl', 'rb'))
videos_id = pickle.load(open('videos_id.pkl', 'rb'))
final_df = pickle.load(open('final_df.pkl', 'rb'))
PivotTable = pickle.load(open('PivotTable.pkl', 'rb'))
all_topics = pickle.load(open('all_topics.pkl', 'rb'))

def fetch_poster(suggestion):
    topic_name = []
    video_index = []
    video_url = []
    video = []
    for i in range(len(suggestion)):
        video_id = PivotTable.index[suggestion[i]]
        video.append(video_id)

#     for video_id in video:
#         topic_name.append(final_df.index[video_id])

    for ids in video[0]:
         index = np.where(final_df['Video ID'] == ids)[0][0]
         video_index.append(index)

    for idx in video_index:
        url = final_df.iloc[idx]['Video Url']
        video_url.append(url)

    return video_url

def recommend_videos(topic_of_interest):
    for topic in topic_of_interest:
     video_id_matches = np.where(final_df['Topic'] == topic_of_interest)[0]
     

    if len(video_id_matches) == 0:
        st.warning(f"No videos found for the topic: {topic_of_interest}")
        return [], []

    
    video_id = video_id_matches[0]
    if video_id >= PivotTable.shape[0]:
        st.warning("Invalid video_id. Please check your data.")
        return [], []
    #video_id = video_id_matches[0]
 
   # video_id = video_id_matches[0]
    distance, suggestion = model.kneighbors(PivotTable.iloc[video_id, :].values.reshape(1, -1), n_neighbors=5)
    video_url = fetch_poster(suggestion)
    
    video_list = []
    for i in range(len(suggestion)):
        video = PivotTable.index[suggestion[i]]
        for j in video:
            video_list.append(j)

    return video_list, video_url

# Streamlit UI
st.header("Video Recommendations")

# User input
selected_topics = st.selectbox("select topic:",all_topics,key = "value1")
selected_topic2 = st.selectbox("select topic:",all_topics,key = "value2")
selected_topic3 = st.selectbox("select topic:",all_topics,key = "value3")
# selected_topics = [selected_topic1,selected_topic2,selected_topic3]
if st.button('Show Recommendations'):
    result_videos, result_urls = recommend_videos(selected_topics)

    # Display results
    if result_videos and result_urls:
        for fuck in range(min(len(result_videos), 5)):
            st.video(result_urls[fuck])
            st.text(result_videos[fuck])
    else:
        st.warning("No recommendations found.")