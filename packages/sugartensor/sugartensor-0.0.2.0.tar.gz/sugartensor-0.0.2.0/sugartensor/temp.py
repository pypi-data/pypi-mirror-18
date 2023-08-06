import numpy as np
import cv2
import joblib
import matplotlib.pyplot as plt


# load data
data = joblib.load('/shared/asan/dild/data/patch.manufac.20x20.pkl')['siemens']
images, edges = [], []
for klass in data:
    for im in klass:
        images.append(im)
        # make edge image
        # edges.append(cv2.Canny((im * 255).astype(np.uint8), 10, 100))
        img_blur = cv2.GaussianBlur((im * 255).astype(np.uint8), (21, 21), 0, 0)
        img_sketch = cv2.divide((im * 255).astype(np.uint8), img_blur, scale=256)
        edges.append(img_sketch)

images = np.asarray(images)
edges = np.asarray(edges)

# plot result
_, ax = plt.subplots(10, 10, sharex=True, sharey=True)
for i in range(10):
    for j in range(10):
        ax[i][j].imshow(edges[i * 10 + j + 300], 'gray')
        ax[i][j].set_axis_off()
plt.show()

##

import nltk
nltk.download()

##
import joblib
import numpy as np
import matplotlib.pyplot as plt

# load data
data = joblib.load('/shared/asan/dild/data/patch.manufac.20x20.pkl')['siemens']
X, Y = [], []
for label, klass in enumerate(data):
    for im in klass:
        X.append(im)
        Y.append(label)
X, Y = np.asarray(X), np.asarray(Y)

##

import sugartensor as tf
import numpy as np

with tf.device('/cpu:0'):
    with tf.variable_scope('c'):
        a = tf.get_variable('a', (2000, 2000), dtype=tf.float32, initializer=tf.constant_initializer(1))

with tf.device('/gpu:0'):
    with tf.variable_scope('g'):
        b = tf.get_variable('b', (2000, 2000), dtype=tf.float32, initializer=tf.constant_initializer(1))


##

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())
    for _ in range(100):
        sess.run(tf.matmul(a, a))
print 'finished'
##

tf.get_collection(tf.GraphKeys.VARIABLES)