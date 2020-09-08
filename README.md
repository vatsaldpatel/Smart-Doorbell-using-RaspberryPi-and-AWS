# Smart-Doorbell-using-RaspberryPi-and-AWS

### This code is a part of my Demo Paper which is accepted at ACM IoT 2020. I'll put a link to the paper once it is published.

### Pre-Requisite
* Raspberry Pi 3 B+
* Logitech Webcam
* AWS account

### There are two codes in this repository.
1. The **Rpi_smart_doorbell** runs on the the Raspberry Pi.
2. The **AWS_Lambda_smart_doorbell** runs as a *Lambda* function on AWS.

### To see a demonstration of this Smart Doorbell please watch this youtube video

[![A Cloud-based Smart Doorbell using Low-Cost COTS Devices](http://img.youtube.com/vi/42mx4Z2PDwA/0.jpg)](https://www.youtube.com/watch?v=42mx4Z2PDwA "Cloud-based Smart Doorbell using Low-Cost COTS Devices")

### How the doorbell works?

1. The webcam captures frames of images as per the defined fps.
2. This image is sent to AWS using different Api's.
3. The output of different object detection and Face rekognition Api's is aggregated.
4. The different captured images are stiched together to make a video.
5. A python dictionary containing the information about the object is sent to AWS.
6. AWS stores the data gathered from JSON object it received into a DynamoDB table and stores the video to S3 Storage.
7. AWS notifies the User using push notification on an iOS application.
8. The user can see the different attributes about the detected object through DynamoDB and also watch the video stored in S3 storage.

### The dictionary Output which is sent to AWS
~~~~python
frame_package ={
                'frame_id': frame_id,
                'approx_capture_timestamp' : int(now_ts_utc),
                'rekog_labels' : labels_on_watch_list_set,  
                's3_bucket':s3_bucket,
                'notification': name + " was spotted at your door.",
                'notification_type': str(notification_type), 
                'notification_title' : name + " spotted",
                's3_video_bucket' : 'video',
                's3_key' : 'frames/'+frame_id + '.jpg',
                's3_video_key' :frame_id + '.mp4',
                'external_image_id' : name
                }
~~~~

### Capturing the images and stiching the video
~~~~python
def capture_frames():
def video_making():
def convert_to_bytearray():
~~~~
* **capture_frames** captures the images.
* **video_making** stiches the image and makes a video from it.
* **convert_to_bytearray** converts the image into bytearray which is then sent to AWS.

### Calling AWS Api's
~~~~python
def Face_detection(img_bytes):
def Label_detection(img_bytes):
def Animal_Detection(labels_on_watch_list_set, rekog_response):
def Gun_Detection(img_bytes):
def Text_detection(img_bytes):
def NoteworthyVehicle_Detection(labels_on_watch_list_set, text_list_set):
~~~~
* Different function for different scenarios are made which calls AWS Api's for a specific scenarios.
* The results of all of these are aggregated after calling **Upload_to_aws** function.

### Aggregating the results and Uploading to AWS
~~~~python
def Upload_to_aws(l):
~~~~
* **Upload_to_aws** function aggregates the results, stores them into the python dictionary and sends it to AWS using **AWS Kinesis**.
