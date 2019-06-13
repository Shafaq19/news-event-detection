# Twitter Based Newsstand
This project aims to develop a news event detection framework that will detect newsworthy events from tweets and generate headlines from them.  We will first pass the tweets through threshold based clustering techniques to cluster tweets corresponding to a certain event based on their similarity, retweet map and Links. Finally, we will use those clusters to topic categorize the events and then generate headlines for that event using ML summarization techniques. Our Clustering technique has a recall of around 89% and process 2000 tweets per minute. Future work hopes to optimize this further.
![N|Solid](https://assets.materialup.com/uploads/188ace2a-5833-4642-95a1-0238fcfbccf8/preview)
# Motivation
Before the news is aired on TV channels, its already trending at various social media sites like twitter. Witnesses to the events post their discoveries online and are picked up by news channels subsequently. However, processing of such huge amount of information to filter newsworthy text forces the need for a software that will automatically and efficiently stream through the tweets and detect those tweets that actually correspond to an event. That what twitterNewsstand hopes to acheive. Our system aims to target News Consumers and News agencies, which cover news stories from all over the world and those who are interested in international news.

# New Features!

  - Using NER as a base rather then the traditional TF-IDF vectorization that doesnt allow flexibilty in reconzing unknown words and take too much space.
 - Dynammic threshold based clustering algorithm


You can [also][df1]:
  - Search for news related to relevent topic of interest like technology
  - News events at your beck in just 4 minutes!
  - Responsive and self refreshed


> The overriding design goal for tweetter based newsstand 
> is to make it as easier and faster for journalist to cover stories
> as possible. The idea is that a
> since people are already on site and actively reporting it on tweets
> makes it feasibke for the journalist as they dont have to go onsite or worry something might be missed

### Tech

Newsstand uses a number of open source projects to work properly:

* [NLTK](df1)  - leading platform for building Python programs to work with human language data.
* [Standford NER reconizer](df1) - an awesome named entity reconizer 
* [Python Libararies](dill) Pandas, Numpy and what not!!!
* [OpenCalais.Api] for topic categorization


### Installation

Newsstand requires NER package to run (git clone https://shafaqA15@bitbucket.org/shafaqA15/named-entity-recognizer.git) and run the java gateway
>All code is in the DatasetA/EventDetection folder
DatasetA/Myoutputs has all output files generated
>cluster.csv has tweets and their assigned cluster ids
>summary.csv has headlines along with cluster id
>topics.csv: contains topics

### Plugins


|No Plugins  Needed |
| ------ |


## Credits

Dataset Cittation:
Andrew J. McMinn, Yashar Moshfeghi, Joemon M. Jose. Building a large-scale 
corpus for Evaluating Event Detection on Twitter - Proceedings of the 22nd ACM
international conference on Conference on information & knowledge management.

similarity function taken from paper:
Liu, Xiaomo, Quanzhi Li, Armineh Nourbakhsh, Rui Fang, Merine Thomas, Kajsa Anderson, RussKociuba, et al. 2016.
“Reuters Tracer: A Large Scale System of Detecting and Verifying Real-Time News Events from Twitter.” in the Proceedings
of the 25th ACM International Conference on Information and Knowledge Management, 207–216, Indianapolis, Indiana, October 24–28


FASTNU © [Shafaq Arshad]()