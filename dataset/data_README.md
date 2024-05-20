

[Challenge Webpage](https://sites.google.com/cam.ac.uk/err-hri/)


# Dataset Metadata for ERR@HRI


### Labels:


#### Task 1. Detection of robot mistakes (RM)



* Detect whether there was a robot mistake (e.g., interrupting or not responding to the coachee)
* **Output: presence of robot mistakes: (0) absent; (1) present **


#### Task 2. Detection of user awkwardness (UA)



* Detect whether the coachees display cues of awkwardness towards the robot (e.g., when the coachee feels uncomfortable interacting with the robot without any robot mistakes)
* **Output: presence of  user awkwardness: (0) absent; (1) present **


#### Task 3. Detection of interaction ruptures (IR)



* Detect whether there was an interaction rupturec(i.e. when the robot makes mistakes described in task 1 and when user displays awkwardness towards the robot described in task 2)
* **Output: presence of interaction ruptures: (0) absent; (1) present**

**Total Dataset**

23 participants

89 sessions

41976 seconds of interaction

**Per Subset (train, validation, test)**



* Data subsets were separated so that **_there is no participant overlap_**.
* There is **_one csv file per interaction session, not per participant_**. Participants interacted with the robot throughout multiple sessions, hence **_different csv files may contain data from the same participant._**

* To allow researchers to conduct training with non-overlapping participant folds, a suggested 4-fold split can be found [in this document](./fold_split.csv).

* Only the train and validation data are going to be provided. Researchers may subset the data as desired.
* **_The test set will not be provided_** and will be used only for the final model evaluation by the organizers.

<table>
  <tr>
   <td>
<strong>subset</strong>
   </td>
   <td><strong>number_participants</strong>
   </td>
   <td><strong>number_sessions</strong>
   </td>
   <td><strong>total_time (s)</strong>
   </td>
   <td><strong>time_rm</strong>
   </td>
   <td><strong>proportion_rm</strong>
   </td>
   <td><strong>time_ua (s)</strong>
   </td>
   <td><strong>proportion_ua</strong>
   </td>
   <td><strong>time_ir (s)</strong>
   </td>
   <td><strong>proportion_ir</strong>
   </td>
  </tr>
  <tr>
   <td>train
   </td>
   <td>14
   </td>
   <td>55
   </td>
   <td>31526
   </td>
   <td>4170
   </td>
   <td>0.13
   </td>
   <td>3813
   </td>
   <td>0.12
   </td>
   <td>6581
   </td>
   <td>0.21
   </td>
  </tr>
  <tr>
   <td>val
   </td>
   <td>4
   </td>
   <td>16
   </td>
   <td>11534
   </td>
   <td>1150
   </td>
   <td>0.10
   </td>
   <td>1369
   </td>
   <td>0.12
   </td>
   <td>2098
   </td>
   <td>0.18
   </td>
  </tr>
  <tr>
   <td>test
   </td>
   <td>5
   </td>
   <td>18
   </td>
   <td>10158
   </td>
   <td>1399
   </td>
   <td>0.14
   </td>
   <td>1875
   </td>
   <td>0.18
   </td>
   <td>2738
   </td>
   <td>0.27
   </td>
  </tr>
</table>


_Proportion refers to time labeled as error over the total time of interactions_


### Features:

The dataset provided is fully anonymized. Visual features are extracted from videos collected at **_30 fps._**


#### Openface [[1](https://github.com/TadasBaltrusaitis/OpenFace/)]

Action Units (AU) activation and intensity features are provided, in a total of **35 features** and **30 fps**.


#### Opensmile [[2](https://audeering.github.io/opensmile-python/)]

Features were extracted using a time window of **0.02 s** and at a rate of **100 data points per second.**
The features were computed on the audio extracted from the interaction video. Thus, these features correspond to audio both from the participant and the robot. You can use speaker diarization to zero-out the features in moments when the participant is not taking a turn. An example of this processing can be found [in the training folder](../training/).

Total of **25** features, corresponding to the low level descriptors of feature set eGeMAPSv02.

#### Speaker Diarization

Turn-taking information for each session. This can be used to zero-out Opensmile features or as an additional feature.

#### Openpose [[3](https://github.com/CMU-Perceptual-Computing-Lab/openpose)]

The features provided (at **30 fps**)  _do not correspond directly to the features extracted from Openpose _but rather the relational **distance and velocity** for pairs of spatial body points, in a total of **44** features, corresponding to relational features for 18 body points. For example, the feature distance_4_7 refers to the distance between the hands, while the corresponding velocity is computed over one timeframe. 
