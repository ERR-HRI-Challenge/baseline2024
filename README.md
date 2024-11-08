# ERR @ HRI 2024

Website: https://sites.google.com/cam.ac.uk/err-hri

The ERR@HRI challenge aims at addressing the problem of failure detection in human-robot interaction (HRI) by providing the community with the means to benchmark efforts for mono-modal vs. multi-modal robot failure detection in HRI. 

### Table of contents:

* [Dataset](#dataset)
* [Training](#training)
* [Submission](#submission)
* [Proceedings](#proceedings)

## Dataset 

The dataset README can be found [here](./dataset/data_README.md).


## Training


The data used for training was obtained using the jupyter notebook [preprocess.ipynb](./training/preprocess.ipynb).

The datasets used for training and testing can be downloaded from the initial drive with the dataset.


### Important notes for training:

* ['vel_1_x', 'vel_1_y', 'vel_8_x', 'vel_8_y', 'dist_1_8', 'vel_dist_1_8', 'dist_7_0', 'dist_4_0', 'vel_7_x', 'vel_7_y', 'vel_4_x', 'vel_4_y','vel_dist_7_0', 'vel_dist_4_0'] — these features were excluded from the analysis as they’re absent in most sessions.

* As a consequence, models are trained with a feature set of 90 features.

* Openface timestamps are not fully matching the frames. For this reason, we used the **frame number** as the time reference.

* All the rows with NaN are removed.

* Openface and Openpose features are directly matched by frames.

* Opensmile is matched with the timestamp to the Openface/Openpose frames (frame x 30 = time in seconds).

* Dataset frequency is thus 30 samples per second.


You can find the scripted used to calculate model performance in [get_metrics.py](./training/get_metrics.py).

The script used to process the data into the training dataset is [createDataSplits.py](./training/createDataSplits.py).

### Baseline models

The final baseline models can be found in [baseline](./baseline)

All the models were training using Keras.

Tolerance for metrics is of 1 sample. Performances reported on the unreleased dataset.

#### Robot Mistake

* Seed: 42
* Model: single-layer GRU


                model = keras.Sequential()
                model.add(GRU(units = unit, input_shape = (sequence_length, X_train.shape[1])))
                model.add(layers.Dropout(dropout))
                model.add(layers.Dense(units=num_classes, activation = activation))


* Dataset: normalized

| **Parameter**     | **Value** |
|-------------------|-----------|
| sequence length   | $5$ |
| unit              | $128$ |
| dropout           | $0.2$ |
| activation          | softmax |
| loss function          | categorical_crossentropy |
| optimizer          | Adam |
| learning rate        | $0.0001$ |
| batch size         | $2048$ |
| epochs         | $500$ |


| **Metric**     | **Performance** |
|-------------------|-----------|
| macro accuracy   | $0.7134922510020435$ |
| macro precision             | $0.5559300234458304$ |
| macro recall          | $0.540890884595122$ |
| macro f1 score    | $0.5418411044660401$ |
| tolerant accuracy        | $0.7141720240241733$ |
| tolerant precision        | $0.5575682319746725$ |
| tolerant recall       | $0.5421935733140711$ |
| tolerant f1      | $0.5433503856916844$ |



#### User Awkwardness

* Seed: 42
* Model: single-layer BiLSTM


                model = keras.Sequential()
                model.add(Bidirectional(LSTM(units = unit, input_shape = (sequence_length, X_train.shape[1]))))
                model.add(layers.Dropout(dropout))
                model.add(layers.Dense(units=num_classes, activation = activation))


* Dataset: normalized

| **Parameter**     | **Value** |
|-------------------|-----------|
| sequence length   | $5$ |
| unit              | $256$ |
| dropout           | $0.2$ |
| activation          | sigmoid |
| loss function          | categorical_crossentropy |
| optimizer          | Adam |
| learning rate        | $0.0001$ |
| batch size         | $512$ |
| epochs         | $200$ |


| **Metric**     | **Performance** |
|-------------------|-----------|
| macro accuracy   | $0.7307435639173164$ |
| macro precision             | $0.5635818543654784$ |
| macro recall          | $0.5735588617316334$ |
| macro f1 score    | $0.566976689570101$ |
| tolerant accuracy        | $0.7320658053445082$ |
| tolerant precision        | $0.5661679460333295$ |
| tolerant recall       | $0.576763276792829$ |
| tolerant f1      | $0.5697834652888063$ |

#### Interaction Rupture

* Seed: 42
* Model: single-layer BiLSTM


                model = keras.Sequential()
                model.add(Bidirectional(LSTM(units = unit, input_shape = (sequence_length, X_train.shape[1]))))
                model.add(layers.Dropout(dropout))
                model.add(layers.Dense(units=num_classes, activation = activation))


* Dataset: non-normalized

| **Parameter**     | **Value** |
|-------------------|-----------|
| sequence length   | $5$ |
| unit              | $256$ |
| dropout           | $0.2$ |
| activation          | softmax |
| loss function          | categorical_crossentropy |
| optimizer          | Adam |
| learning rate        | $0.0001$ |
| batch size         | $4096$ |
| epochs         | $500$ |


| **Metric**     | **Performance** |
|-------------------|-----------|
| macro accuracy   | $0.6846018975615216$ |
| macro precision             | $0.5554184955430482$ |
| macro recall          | $0.5026821814637205$ |
| macro f1 score    | $0.4196414813960051$ |
| tolerant accuracy        | $0.6859199940312612$ |
| tolerant precision        | $0.5879408152777608$ |
| tolerant recall       | $0.5047824945292528$ |
| tolerant f1      | $0.42395310101831235$ |




## Submission

### Submission Instructions

#### Code and Results Submission

**Important Dates:**
**Test set release:** 12th June
**Final code and results submission:** 23rd June

Participants should submit their code and results via email (errathri@gmail.com).

If the attachment are too large, participants can create a zip uploaded on the cloud. However, the last edit should be by the final deadline (**23rd of June**).

We will release the test set without labels on the **12th of June** and participants will have ten days to refine their models and submit their codes and results (deadline 23rd June).

#### Paper Submission
**Deadline:** 14th July via EasyChair (link will be added soon)


### Submission Materials

The test dataset will be made available to researchers. By the submission deadline, participants will submit their models predictions, up to three for each task (RM, UA, IR) in which they decided to participate.

Each participant can submit **three models/predictions per task**.

Submissions must be fully reproducible - that is, given the models, the evaluation team should be able to obtain the same predictions from the test dataset. As such, submission materials for each task are:

* y_pred (1 dimensional array of predictions from the test dataset)

* script used to extract groundtruth arrays (i.e., function which takes as input the path to one or multiple session label csv file, and outputs a 1-dimensional array of the groundtruth labels of the data)
  * must be well documented so its use is intuitive
  * must include information about prediction frequency

* model and model weights

* seed used to obtain predictions



### Evaluation

The submitted models, for each task, will be evaluated on two tracks: **overall performance** and **time-tolerant performance**. 

#### Overall performance

We will rank models based on the combined rankings of accuracy and F1-score.

Example: _models are ranked based on accuracy and given points based on their position (1,2,3...). The same process takes place to F1-score. The best model is that which the combined number of points is lowest (min = 2 points)._

#### Time-tolerant performance

We will rank models based on the combined rankings of accuracy and F1-score.




## Proceedings:

Micol Spitale, Maria Teresa Parreira, Maia Stiber, Minja Axelsson, Neval Kara, Garima Kankariya, Chien-Ming Huang, Malte Jung, Wendy Ju, and Hatice Gunes. 2024. ERR@HRI 2024 Challenge: Multimodal Detection of Errors and Failures in Human-Robot Interactions. In Proceedings of the 26th International Conference on Multimodal Interaction (ICMI '24). Association for Computing Machinery, New York, NY, USA, 652–656. https://doi.org/10.1145/3678957.3689030

```
@inproceedings{10.1145/3678957.3689030,
author = {Spitale, Micol and Parreira, Maria Teresa and Stiber, Maia and Axelsson, Minja and Kara, Neval and Kankariya, Garima and Huang, Chien-Ming and Jung, Malte and Ju, Wendy and Gunes, Hatice},
title = {ERR@HRI 2024 Challenge: Multimodal Detection of Errors and Failures in Human-Robot Interactions},
year = {2024},
isbn = {9798400704628},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3678957.3689030},
doi = {10.1145/3678957.3689030},
pages = {652–656},
numpages = {5},
keywords = {Benchmarking., Error Detection, Human-Robot Interaction, Multimodal Interaction, Robot Failure},
location = {San Jose, Costa Rica},
series = {ICMI '24}
}
```
