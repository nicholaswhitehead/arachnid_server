import tensorflow as tf

def job_func():
    return str(tf.reduce_sum(tf.random.normal([1000, 1000])))