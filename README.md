# Twitter Based Newstand
This project aims to develop a news event detection framework that will detect newsworthy events from tweets and generate headlines from them. 
## Instalation
Newsstand requires the [NER package](https://shafaqA15@bitbucket.org/shafaqA15/named-entity-recognizer.git) and run the `java gateway`

_All code is in the DatasetA/EventDetection folder DatasetA/Myoutputs has all output files generated cluster.csv has tweets and their assigned cluster ids summary.csv has headlines along with cluster id topics.csv: contains topics_

- [x] Clone the repository by running
         `git clone https://github.com/Shafaq19/Twitter-News-Event-Detection.git`

- [ ] you need to register for a api key for 
 - [intelligent tagging at OpenCalasis](https://www.refinitiv.com/en/products/intelligent-tagging-text-analytics)
 - [twitter api](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens)
- [ ] if you are using python envirment install the dependencies by
`pip install -r requirements.txt`
else conda users can do `conda install`

- [ ] run DatasetA/EventDetection/Mainfile.py and check the outputs at Dataset/Myoutputs folder

Congrats You are all set!:+1:
## Features

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

## Plugins


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
