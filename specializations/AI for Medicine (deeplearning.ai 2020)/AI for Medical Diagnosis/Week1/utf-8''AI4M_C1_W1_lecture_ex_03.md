
## AI for Medicine Course 1 Week 1 lecture exercises

<a name="densenet"></a>
# Densenet

In this week's assignment, you'll be using a pre-trained Densenet model for image classification. 

Densenet is a convolutional network where each layer is connected to all other layers that are deeper in the network
- The first layer is connected to the 2nd, 3rd, 4th etc.
- The second layer is connected to the 3rd, 4th, 5th etc.

Like this:

<img src="densenet.png" alt="U-net Image" width="400" align="middle"/>

For a detailed explanation of Densenet, check out the source of the image above, a paper by Gao Huang et al. 2018 called [Densely Connected Convolutional Networks](https://arxiv.org/pdf/1608.06993.pdf).

The cells below are set up to provide an exploration of the Keras densenet implementation that you'll be using in the assignment. Run these cells to gain some insight into the network architecture. 


```python
# Import Densenet from Keras
from keras.applications.densenet import DenseNet121
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras import backend as K
```

    Using TensorFlow backend.


For your work in the assignment, you'll be loading a set of pre-trained weights to reduce training time.


```python
# Create the base pre-trained model
base_model = DenseNet121(weights='./nih/densenet.hdf5', include_top=False);
```

    WARNING:tensorflow:From /opt/conda/lib/python3.6/site-packages/tensorflow_core/python/ops/resource_variable_ops.py:1630: calling BaseResourceVariable.__init__ (from tensorflow.python.ops.resource_variable_ops) with constraint is deprecated and will be removed in a future version.
    Instructions for updating:
    If using Keras pass *_constraint arguments to layers.
    WARNING:tensorflow:From /opt/conda/lib/python3.6/site-packages/keras/backend/tensorflow_backend.py:4070: The name tf.nn.max_pool is deprecated. Please use tf.nn.max_pool2d instead.
    
    WARNING:tensorflow:From /opt/conda/lib/python3.6/site-packages/keras/backend/tensorflow_backend.py:4074: The name tf.nn.avg_pool is deprecated. Please use tf.nn.avg_pool2d instead.
    


View a summary of the model


```python
# Print the model summary
base_model.summary()
```

    Model: "densenet121"
    __________________________________________________________________________________________________
    Layer (type)                    Output Shape         Param #     Connected to                     
    ==================================================================================================
    input_1 (InputLayer)            (None, None, None, 3 0                                            
    __________________________________________________________________________________________________
    zero_padding2d_1 (ZeroPadding2D (None, None, None, 3 0           input_1[0][0]                    
    __________________________________________________________________________________________________
    conv1/conv (Conv2D)             (None, None, None, 6 9408        zero_padding2d_1[0][0]           
    __________________________________________________________________________________________________
    conv1/bn (BatchNormalization)   (None, None, None, 6 256         conv1/conv[0][0]                 
    __________________________________________________________________________________________________
    conv1/relu (Activation)         (None, None, None, 6 0           conv1/bn[0][0]                   
    __________________________________________________________________________________________________
    zero_padding2d_2 (ZeroPadding2D (None, None, None, 6 0           conv1/relu[0][0]                 
    __________________________________________________________________________________________________
    pool1 (MaxPooling2D)            (None, None, None, 6 0           zero_padding2d_2[0][0]           
    __________________________________________________________________________________________________
    conv2_block1_0_bn (BatchNormali (None, None, None, 6 256         pool1[0][0]                      
    __________________________________________________________________________________________________
    conv2_block1_0_relu (Activation (None, None, None, 6 0           conv2_block1_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block1_1_conv (Conv2D)    (None, None, None, 1 8192        conv2_block1_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block1_1_bn (BatchNormali (None, None, None, 1 512         conv2_block1_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block1_1_relu (Activation (None, None, None, 1 0           conv2_block1_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block1_2_conv (Conv2D)    (None, None, None, 3 36864       conv2_block1_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block1_concat (Concatenat (None, None, None, 9 0           pool1[0][0]                      
                                                                     conv2_block1_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block2_0_bn (BatchNormali (None, None, None, 9 384         conv2_block1_concat[0][0]        
    __________________________________________________________________________________________________
    conv2_block2_0_relu (Activation (None, None, None, 9 0           conv2_block2_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block2_1_conv (Conv2D)    (None, None, None, 1 12288       conv2_block2_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block2_1_bn (BatchNormali (None, None, None, 1 512         conv2_block2_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block2_1_relu (Activation (None, None, None, 1 0           conv2_block2_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block2_2_conv (Conv2D)    (None, None, None, 3 36864       conv2_block2_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block2_concat (Concatenat (None, None, None, 1 0           conv2_block1_concat[0][0]        
                                                                     conv2_block2_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block3_0_bn (BatchNormali (None, None, None, 1 512         conv2_block2_concat[0][0]        
    __________________________________________________________________________________________________
    conv2_block3_0_relu (Activation (None, None, None, 1 0           conv2_block3_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block3_1_conv (Conv2D)    (None, None, None, 1 16384       conv2_block3_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block3_1_bn (BatchNormali (None, None, None, 1 512         conv2_block3_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block3_1_relu (Activation (None, None, None, 1 0           conv2_block3_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block3_2_conv (Conv2D)    (None, None, None, 3 36864       conv2_block3_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block3_concat (Concatenat (None, None, None, 1 0           conv2_block2_concat[0][0]        
                                                                     conv2_block3_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block4_0_bn (BatchNormali (None, None, None, 1 640         conv2_block3_concat[0][0]        
    __________________________________________________________________________________________________
    conv2_block4_0_relu (Activation (None, None, None, 1 0           conv2_block4_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block4_1_conv (Conv2D)    (None, None, None, 1 20480       conv2_block4_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block4_1_bn (BatchNormali (None, None, None, 1 512         conv2_block4_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block4_1_relu (Activation (None, None, None, 1 0           conv2_block4_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block4_2_conv (Conv2D)    (None, None, None, 3 36864       conv2_block4_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block4_concat (Concatenat (None, None, None, 1 0           conv2_block3_concat[0][0]        
                                                                     conv2_block4_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block5_0_bn (BatchNormali (None, None, None, 1 768         conv2_block4_concat[0][0]        
    __________________________________________________________________________________________________
    conv2_block5_0_relu (Activation (None, None, None, 1 0           conv2_block5_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block5_1_conv (Conv2D)    (None, None, None, 1 24576       conv2_block5_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block5_1_bn (BatchNormali (None, None, None, 1 512         conv2_block5_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block5_1_relu (Activation (None, None, None, 1 0           conv2_block5_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block5_2_conv (Conv2D)    (None, None, None, 3 36864       conv2_block5_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block5_concat (Concatenat (None, None, None, 2 0           conv2_block4_concat[0][0]        
                                                                     conv2_block5_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block6_0_bn (BatchNormali (None, None, None, 2 896         conv2_block5_concat[0][0]        
    __________________________________________________________________________________________________
    conv2_block6_0_relu (Activation (None, None, None, 2 0           conv2_block6_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block6_1_conv (Conv2D)    (None, None, None, 1 28672       conv2_block6_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block6_1_bn (BatchNormali (None, None, None, 1 512         conv2_block6_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv2_block6_1_relu (Activation (None, None, None, 1 0           conv2_block6_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv2_block6_2_conv (Conv2D)    (None, None, None, 3 36864       conv2_block6_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv2_block6_concat (Concatenat (None, None, None, 2 0           conv2_block5_concat[0][0]        
                                                                     conv2_block6_2_conv[0][0]        
    __________________________________________________________________________________________________
    pool2_bn (BatchNormalization)   (None, None, None, 2 1024        conv2_block6_concat[0][0]        
    __________________________________________________________________________________________________
    pool2_relu (Activation)         (None, None, None, 2 0           pool2_bn[0][0]                   
    __________________________________________________________________________________________________
    pool2_conv (Conv2D)             (None, None, None, 1 32768       pool2_relu[0][0]                 
    __________________________________________________________________________________________________
    pool2_pool (AveragePooling2D)   (None, None, None, 1 0           pool2_conv[0][0]                 
    __________________________________________________________________________________________________
    conv3_block1_0_bn (BatchNormali (None, None, None, 1 512         pool2_pool[0][0]                 
    __________________________________________________________________________________________________
    conv3_block1_0_relu (Activation (None, None, None, 1 0           conv3_block1_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block1_1_conv (Conv2D)    (None, None, None, 1 16384       conv3_block1_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block1_1_bn (BatchNormali (None, None, None, 1 512         conv3_block1_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block1_1_relu (Activation (None, None, None, 1 0           conv3_block1_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block1_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block1_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block1_concat (Concatenat (None, None, None, 1 0           pool2_pool[0][0]                 
                                                                     conv3_block1_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block2_0_bn (BatchNormali (None, None, None, 1 640         conv3_block1_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block2_0_relu (Activation (None, None, None, 1 0           conv3_block2_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block2_1_conv (Conv2D)    (None, None, None, 1 20480       conv3_block2_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block2_1_bn (BatchNormali (None, None, None, 1 512         conv3_block2_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block2_1_relu (Activation (None, None, None, 1 0           conv3_block2_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block2_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block2_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block2_concat (Concatenat (None, None, None, 1 0           conv3_block1_concat[0][0]        
                                                                     conv3_block2_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block3_0_bn (BatchNormali (None, None, None, 1 768         conv3_block2_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block3_0_relu (Activation (None, None, None, 1 0           conv3_block3_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block3_1_conv (Conv2D)    (None, None, None, 1 24576       conv3_block3_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block3_1_bn (BatchNormali (None, None, None, 1 512         conv3_block3_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block3_1_relu (Activation (None, None, None, 1 0           conv3_block3_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block3_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block3_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block3_concat (Concatenat (None, None, None, 2 0           conv3_block2_concat[0][0]        
                                                                     conv3_block3_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block4_0_bn (BatchNormali (None, None, None, 2 896         conv3_block3_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block4_0_relu (Activation (None, None, None, 2 0           conv3_block4_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block4_1_conv (Conv2D)    (None, None, None, 1 28672       conv3_block4_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block4_1_bn (BatchNormali (None, None, None, 1 512         conv3_block4_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block4_1_relu (Activation (None, None, None, 1 0           conv3_block4_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block4_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block4_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block4_concat (Concatenat (None, None, None, 2 0           conv3_block3_concat[0][0]        
                                                                     conv3_block4_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block5_0_bn (BatchNormali (None, None, None, 2 1024        conv3_block4_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block5_0_relu (Activation (None, None, None, 2 0           conv3_block5_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block5_1_conv (Conv2D)    (None, None, None, 1 32768       conv3_block5_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block5_1_bn (BatchNormali (None, None, None, 1 512         conv3_block5_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block5_1_relu (Activation (None, None, None, 1 0           conv3_block5_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block5_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block5_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block5_concat (Concatenat (None, None, None, 2 0           conv3_block4_concat[0][0]        
                                                                     conv3_block5_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block6_0_bn (BatchNormali (None, None, None, 2 1152        conv3_block5_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block6_0_relu (Activation (None, None, None, 2 0           conv3_block6_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block6_1_conv (Conv2D)    (None, None, None, 1 36864       conv3_block6_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block6_1_bn (BatchNormali (None, None, None, 1 512         conv3_block6_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block6_1_relu (Activation (None, None, None, 1 0           conv3_block6_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block6_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block6_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block6_concat (Concatenat (None, None, None, 3 0           conv3_block5_concat[0][0]        
                                                                     conv3_block6_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block7_0_bn (BatchNormali (None, None, None, 3 1280        conv3_block6_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block7_0_relu (Activation (None, None, None, 3 0           conv3_block7_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block7_1_conv (Conv2D)    (None, None, None, 1 40960       conv3_block7_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block7_1_bn (BatchNormali (None, None, None, 1 512         conv3_block7_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block7_1_relu (Activation (None, None, None, 1 0           conv3_block7_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block7_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block7_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block7_concat (Concatenat (None, None, None, 3 0           conv3_block6_concat[0][0]        
                                                                     conv3_block7_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block8_0_bn (BatchNormali (None, None, None, 3 1408        conv3_block7_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block8_0_relu (Activation (None, None, None, 3 0           conv3_block8_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block8_1_conv (Conv2D)    (None, None, None, 1 45056       conv3_block8_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block8_1_bn (BatchNormali (None, None, None, 1 512         conv3_block8_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block8_1_relu (Activation (None, None, None, 1 0           conv3_block8_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block8_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block8_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block8_concat (Concatenat (None, None, None, 3 0           conv3_block7_concat[0][0]        
                                                                     conv3_block8_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block9_0_bn (BatchNormali (None, None, None, 3 1536        conv3_block8_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block9_0_relu (Activation (None, None, None, 3 0           conv3_block9_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block9_1_conv (Conv2D)    (None, None, None, 1 49152       conv3_block9_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block9_1_bn (BatchNormali (None, None, None, 1 512         conv3_block9_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block9_1_relu (Activation (None, None, None, 1 0           conv3_block9_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv3_block9_2_conv (Conv2D)    (None, None, None, 3 36864       conv3_block9_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv3_block9_concat (Concatenat (None, None, None, 4 0           conv3_block8_concat[0][0]        
                                                                     conv3_block9_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv3_block10_0_bn (BatchNormal (None, None, None, 4 1664        conv3_block9_concat[0][0]        
    __________________________________________________________________________________________________
    conv3_block10_0_relu (Activatio (None, None, None, 4 0           conv3_block10_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv3_block10_1_conv (Conv2D)   (None, None, None, 1 53248       conv3_block10_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv3_block10_1_bn (BatchNormal (None, None, None, 1 512         conv3_block10_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv3_block10_1_relu (Activatio (None, None, None, 1 0           conv3_block10_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv3_block10_2_conv (Conv2D)   (None, None, None, 3 36864       conv3_block10_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv3_block10_concat (Concatena (None, None, None, 4 0           conv3_block9_concat[0][0]        
                                                                     conv3_block10_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv3_block11_0_bn (BatchNormal (None, None, None, 4 1792        conv3_block10_concat[0][0]       
    __________________________________________________________________________________________________
    conv3_block11_0_relu (Activatio (None, None, None, 4 0           conv3_block11_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv3_block11_1_conv (Conv2D)   (None, None, None, 1 57344       conv3_block11_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv3_block11_1_bn (BatchNormal (None, None, None, 1 512         conv3_block11_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv3_block11_1_relu (Activatio (None, None, None, 1 0           conv3_block11_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv3_block11_2_conv (Conv2D)   (None, None, None, 3 36864       conv3_block11_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv3_block11_concat (Concatena (None, None, None, 4 0           conv3_block10_concat[0][0]       
                                                                     conv3_block11_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv3_block12_0_bn (BatchNormal (None, None, None, 4 1920        conv3_block11_concat[0][0]       
    __________________________________________________________________________________________________
    conv3_block12_0_relu (Activatio (None, None, None, 4 0           conv3_block12_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv3_block12_1_conv (Conv2D)   (None, None, None, 1 61440       conv3_block12_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv3_block12_1_bn (BatchNormal (None, None, None, 1 512         conv3_block12_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv3_block12_1_relu (Activatio (None, None, None, 1 0           conv3_block12_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv3_block12_2_conv (Conv2D)   (None, None, None, 3 36864       conv3_block12_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv3_block12_concat (Concatena (None, None, None, 5 0           conv3_block11_concat[0][0]       
                                                                     conv3_block12_2_conv[0][0]       
    __________________________________________________________________________________________________
    pool3_bn (BatchNormalization)   (None, None, None, 5 2048        conv3_block12_concat[0][0]       
    __________________________________________________________________________________________________
    pool3_relu (Activation)         (None, None, None, 5 0           pool3_bn[0][0]                   
    __________________________________________________________________________________________________
    pool3_conv (Conv2D)             (None, None, None, 2 131072      pool3_relu[0][0]                 
    __________________________________________________________________________________________________
    pool3_pool (AveragePooling2D)   (None, None, None, 2 0           pool3_conv[0][0]                 
    __________________________________________________________________________________________________
    conv4_block1_0_bn (BatchNormali (None, None, None, 2 1024        pool3_pool[0][0]                 
    __________________________________________________________________________________________________
    conv4_block1_0_relu (Activation (None, None, None, 2 0           conv4_block1_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block1_1_conv (Conv2D)    (None, None, None, 1 32768       conv4_block1_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_1_bn (BatchNormali (None, None, None, 1 512         conv4_block1_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_1_relu (Activation (None, None, None, 1 0           conv4_block1_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block1_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block1_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block1_concat (Concatenat (None, None, None, 2 0           pool3_pool[0][0]                 
                                                                     conv4_block1_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_0_bn (BatchNormali (None, None, None, 2 1152        conv4_block1_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_0_relu (Activation (None, None, None, 2 0           conv4_block2_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block2_1_conv (Conv2D)    (None, None, None, 1 36864       conv4_block2_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_1_bn (BatchNormali (None, None, None, 1 512         conv4_block2_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_1_relu (Activation (None, None, None, 1 0           conv4_block2_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block2_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block2_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block2_concat (Concatenat (None, None, None, 3 0           conv4_block1_concat[0][0]        
                                                                     conv4_block2_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_0_bn (BatchNormali (None, None, None, 3 1280        conv4_block2_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_0_relu (Activation (None, None, None, 3 0           conv4_block3_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block3_1_conv (Conv2D)    (None, None, None, 1 40960       conv4_block3_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_1_bn (BatchNormali (None, None, None, 1 512         conv4_block3_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_1_relu (Activation (None, None, None, 1 0           conv4_block3_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block3_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block3_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block3_concat (Concatenat (None, None, None, 3 0           conv4_block2_concat[0][0]        
                                                                     conv4_block3_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_0_bn (BatchNormali (None, None, None, 3 1408        conv4_block3_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_0_relu (Activation (None, None, None, 3 0           conv4_block4_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block4_1_conv (Conv2D)    (None, None, None, 1 45056       conv4_block4_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_1_bn (BatchNormali (None, None, None, 1 512         conv4_block4_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_1_relu (Activation (None, None, None, 1 0           conv4_block4_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block4_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block4_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block4_concat (Concatenat (None, None, None, 3 0           conv4_block3_concat[0][0]        
                                                                     conv4_block4_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_0_bn (BatchNormali (None, None, None, 3 1536        conv4_block4_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_0_relu (Activation (None, None, None, 3 0           conv4_block5_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block5_1_conv (Conv2D)    (None, None, None, 1 49152       conv4_block5_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_1_bn (BatchNormali (None, None, None, 1 512         conv4_block5_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_1_relu (Activation (None, None, None, 1 0           conv4_block5_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block5_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block5_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block5_concat (Concatenat (None, None, None, 4 0           conv4_block4_concat[0][0]        
                                                                     conv4_block5_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_0_bn (BatchNormali (None, None, None, 4 1664        conv4_block5_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_0_relu (Activation (None, None, None, 4 0           conv4_block6_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block6_1_conv (Conv2D)    (None, None, None, 1 53248       conv4_block6_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_1_bn (BatchNormali (None, None, None, 1 512         conv4_block6_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_1_relu (Activation (None, None, None, 1 0           conv4_block6_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block6_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block6_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block6_concat (Concatenat (None, None, None, 4 0           conv4_block5_concat[0][0]        
                                                                     conv4_block6_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block7_0_bn (BatchNormali (None, None, None, 4 1792        conv4_block6_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block7_0_relu (Activation (None, None, None, 4 0           conv4_block7_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block7_1_conv (Conv2D)    (None, None, None, 1 57344       conv4_block7_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block7_1_bn (BatchNormali (None, None, None, 1 512         conv4_block7_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block7_1_relu (Activation (None, None, None, 1 0           conv4_block7_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block7_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block7_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block7_concat (Concatenat (None, None, None, 4 0           conv4_block6_concat[0][0]        
                                                                     conv4_block7_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block8_0_bn (BatchNormali (None, None, None, 4 1920        conv4_block7_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block8_0_relu (Activation (None, None, None, 4 0           conv4_block8_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block8_1_conv (Conv2D)    (None, None, None, 1 61440       conv4_block8_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block8_1_bn (BatchNormali (None, None, None, 1 512         conv4_block8_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block8_1_relu (Activation (None, None, None, 1 0           conv4_block8_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block8_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block8_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block8_concat (Concatenat (None, None, None, 5 0           conv4_block7_concat[0][0]        
                                                                     conv4_block8_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block9_0_bn (BatchNormali (None, None, None, 5 2048        conv4_block8_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block9_0_relu (Activation (None, None, None, 5 0           conv4_block9_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block9_1_conv (Conv2D)    (None, None, None, 1 65536       conv4_block9_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block9_1_bn (BatchNormali (None, None, None, 1 512         conv4_block9_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block9_1_relu (Activation (None, None, None, 1 0           conv4_block9_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv4_block9_2_conv (Conv2D)    (None, None, None, 3 36864       conv4_block9_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv4_block9_concat (Concatenat (None, None, None, 5 0           conv4_block8_concat[0][0]        
                                                                     conv4_block9_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv4_block10_0_bn (BatchNormal (None, None, None, 5 2176        conv4_block9_concat[0][0]        
    __________________________________________________________________________________________________
    conv4_block10_0_relu (Activatio (None, None, None, 5 0           conv4_block10_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block10_1_conv (Conv2D)   (None, None, None, 1 69632       conv4_block10_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block10_1_bn (BatchNormal (None, None, None, 1 512         conv4_block10_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block10_1_relu (Activatio (None, None, None, 1 0           conv4_block10_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block10_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block10_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block10_concat (Concatena (None, None, None, 5 0           conv4_block9_concat[0][0]        
                                                                     conv4_block10_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block11_0_bn (BatchNormal (None, None, None, 5 2304        conv4_block10_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block11_0_relu (Activatio (None, None, None, 5 0           conv4_block11_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block11_1_conv (Conv2D)   (None, None, None, 1 73728       conv4_block11_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block11_1_bn (BatchNormal (None, None, None, 1 512         conv4_block11_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block11_1_relu (Activatio (None, None, None, 1 0           conv4_block11_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block11_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block11_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block11_concat (Concatena (None, None, None, 6 0           conv4_block10_concat[0][0]       
                                                                     conv4_block11_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block12_0_bn (BatchNormal (None, None, None, 6 2432        conv4_block11_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block12_0_relu (Activatio (None, None, None, 6 0           conv4_block12_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block12_1_conv (Conv2D)   (None, None, None, 1 77824       conv4_block12_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block12_1_bn (BatchNormal (None, None, None, 1 512         conv4_block12_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block12_1_relu (Activatio (None, None, None, 1 0           conv4_block12_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block12_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block12_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block12_concat (Concatena (None, None, None, 6 0           conv4_block11_concat[0][0]       
                                                                     conv4_block12_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block13_0_bn (BatchNormal (None, None, None, 6 2560        conv4_block12_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block13_0_relu (Activatio (None, None, None, 6 0           conv4_block13_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block13_1_conv (Conv2D)   (None, None, None, 1 81920       conv4_block13_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block13_1_bn (BatchNormal (None, None, None, 1 512         conv4_block13_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block13_1_relu (Activatio (None, None, None, 1 0           conv4_block13_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block13_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block13_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block13_concat (Concatena (None, None, None, 6 0           conv4_block12_concat[0][0]       
                                                                     conv4_block13_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block14_0_bn (BatchNormal (None, None, None, 6 2688        conv4_block13_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block14_0_relu (Activatio (None, None, None, 6 0           conv4_block14_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block14_1_conv (Conv2D)   (None, None, None, 1 86016       conv4_block14_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block14_1_bn (BatchNormal (None, None, None, 1 512         conv4_block14_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block14_1_relu (Activatio (None, None, None, 1 0           conv4_block14_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block14_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block14_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block14_concat (Concatena (None, None, None, 7 0           conv4_block13_concat[0][0]       
                                                                     conv4_block14_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block15_0_bn (BatchNormal (None, None, None, 7 2816        conv4_block14_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block15_0_relu (Activatio (None, None, None, 7 0           conv4_block15_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block15_1_conv (Conv2D)   (None, None, None, 1 90112       conv4_block15_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block15_1_bn (BatchNormal (None, None, None, 1 512         conv4_block15_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block15_1_relu (Activatio (None, None, None, 1 0           conv4_block15_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block15_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block15_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block15_concat (Concatena (None, None, None, 7 0           conv4_block14_concat[0][0]       
                                                                     conv4_block15_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block16_0_bn (BatchNormal (None, None, None, 7 2944        conv4_block15_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block16_0_relu (Activatio (None, None, None, 7 0           conv4_block16_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block16_1_conv (Conv2D)   (None, None, None, 1 94208       conv4_block16_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block16_1_bn (BatchNormal (None, None, None, 1 512         conv4_block16_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block16_1_relu (Activatio (None, None, None, 1 0           conv4_block16_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block16_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block16_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block16_concat (Concatena (None, None, None, 7 0           conv4_block15_concat[0][0]       
                                                                     conv4_block16_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block17_0_bn (BatchNormal (None, None, None, 7 3072        conv4_block16_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block17_0_relu (Activatio (None, None, None, 7 0           conv4_block17_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block17_1_conv (Conv2D)   (None, None, None, 1 98304       conv4_block17_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block17_1_bn (BatchNormal (None, None, None, 1 512         conv4_block17_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block17_1_relu (Activatio (None, None, None, 1 0           conv4_block17_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block17_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block17_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block17_concat (Concatena (None, None, None, 8 0           conv4_block16_concat[0][0]       
                                                                     conv4_block17_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block18_0_bn (BatchNormal (None, None, None, 8 3200        conv4_block17_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block18_0_relu (Activatio (None, None, None, 8 0           conv4_block18_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block18_1_conv (Conv2D)   (None, None, None, 1 102400      conv4_block18_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block18_1_bn (BatchNormal (None, None, None, 1 512         conv4_block18_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block18_1_relu (Activatio (None, None, None, 1 0           conv4_block18_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block18_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block18_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block18_concat (Concatena (None, None, None, 8 0           conv4_block17_concat[0][0]       
                                                                     conv4_block18_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block19_0_bn (BatchNormal (None, None, None, 8 3328        conv4_block18_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block19_0_relu (Activatio (None, None, None, 8 0           conv4_block19_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block19_1_conv (Conv2D)   (None, None, None, 1 106496      conv4_block19_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block19_1_bn (BatchNormal (None, None, None, 1 512         conv4_block19_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block19_1_relu (Activatio (None, None, None, 1 0           conv4_block19_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block19_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block19_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block19_concat (Concatena (None, None, None, 8 0           conv4_block18_concat[0][0]       
                                                                     conv4_block19_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block20_0_bn (BatchNormal (None, None, None, 8 3456        conv4_block19_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block20_0_relu (Activatio (None, None, None, 8 0           conv4_block20_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block20_1_conv (Conv2D)   (None, None, None, 1 110592      conv4_block20_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block20_1_bn (BatchNormal (None, None, None, 1 512         conv4_block20_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block20_1_relu (Activatio (None, None, None, 1 0           conv4_block20_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block20_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block20_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block20_concat (Concatena (None, None, None, 8 0           conv4_block19_concat[0][0]       
                                                                     conv4_block20_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block21_0_bn (BatchNormal (None, None, None, 8 3584        conv4_block20_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block21_0_relu (Activatio (None, None, None, 8 0           conv4_block21_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block21_1_conv (Conv2D)   (None, None, None, 1 114688      conv4_block21_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block21_1_bn (BatchNormal (None, None, None, 1 512         conv4_block21_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block21_1_relu (Activatio (None, None, None, 1 0           conv4_block21_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block21_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block21_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block21_concat (Concatena (None, None, None, 9 0           conv4_block20_concat[0][0]       
                                                                     conv4_block21_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block22_0_bn (BatchNormal (None, None, None, 9 3712        conv4_block21_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block22_0_relu (Activatio (None, None, None, 9 0           conv4_block22_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block22_1_conv (Conv2D)   (None, None, None, 1 118784      conv4_block22_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block22_1_bn (BatchNormal (None, None, None, 1 512         conv4_block22_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block22_1_relu (Activatio (None, None, None, 1 0           conv4_block22_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block22_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block22_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block22_concat (Concatena (None, None, None, 9 0           conv4_block21_concat[0][0]       
                                                                     conv4_block22_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block23_0_bn (BatchNormal (None, None, None, 9 3840        conv4_block22_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block23_0_relu (Activatio (None, None, None, 9 0           conv4_block23_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block23_1_conv (Conv2D)   (None, None, None, 1 122880      conv4_block23_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block23_1_bn (BatchNormal (None, None, None, 1 512         conv4_block23_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block23_1_relu (Activatio (None, None, None, 1 0           conv4_block23_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block23_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block23_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block23_concat (Concatena (None, None, None, 9 0           conv4_block22_concat[0][0]       
                                                                     conv4_block23_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block24_0_bn (BatchNormal (None, None, None, 9 3968        conv4_block23_concat[0][0]       
    __________________________________________________________________________________________________
    conv4_block24_0_relu (Activatio (None, None, None, 9 0           conv4_block24_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block24_1_conv (Conv2D)   (None, None, None, 1 126976      conv4_block24_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block24_1_bn (BatchNormal (None, None, None, 1 512         conv4_block24_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv4_block24_1_relu (Activatio (None, None, None, 1 0           conv4_block24_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv4_block24_2_conv (Conv2D)   (None, None, None, 3 36864       conv4_block24_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv4_block24_concat (Concatena (None, None, None, 1 0           conv4_block23_concat[0][0]       
                                                                     conv4_block24_2_conv[0][0]       
    __________________________________________________________________________________________________
    pool4_bn (BatchNormalization)   (None, None, None, 1 4096        conv4_block24_concat[0][0]       
    __________________________________________________________________________________________________
    pool4_relu (Activation)         (None, None, None, 1 0           pool4_bn[0][0]                   
    __________________________________________________________________________________________________
    pool4_conv (Conv2D)             (None, None, None, 5 524288      pool4_relu[0][0]                 
    __________________________________________________________________________________________________
    pool4_pool (AveragePooling2D)   (None, None, None, 5 0           pool4_conv[0][0]                 
    __________________________________________________________________________________________________
    conv5_block1_0_bn (BatchNormali (None, None, None, 5 2048        pool4_pool[0][0]                 
    __________________________________________________________________________________________________
    conv5_block1_0_relu (Activation (None, None, None, 5 0           conv5_block1_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block1_1_conv (Conv2D)    (None, None, None, 1 65536       conv5_block1_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_1_bn (BatchNormali (None, None, None, 1 512         conv5_block1_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_1_relu (Activation (None, None, None, 1 0           conv5_block1_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block1_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block1_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block1_concat (Concatenat (None, None, None, 5 0           pool4_pool[0][0]                 
                                                                     conv5_block1_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_0_bn (BatchNormali (None, None, None, 5 2176        conv5_block1_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_0_relu (Activation (None, None, None, 5 0           conv5_block2_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block2_1_conv (Conv2D)    (None, None, None, 1 69632       conv5_block2_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_1_bn (BatchNormali (None, None, None, 1 512         conv5_block2_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_1_relu (Activation (None, None, None, 1 0           conv5_block2_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block2_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block2_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block2_concat (Concatenat (None, None, None, 5 0           conv5_block1_concat[0][0]        
                                                                     conv5_block2_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_0_bn (BatchNormali (None, None, None, 5 2304        conv5_block2_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_0_relu (Activation (None, None, None, 5 0           conv5_block3_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block3_1_conv (Conv2D)    (None, None, None, 1 73728       conv5_block3_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_1_bn (BatchNormali (None, None, None, 1 512         conv5_block3_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_1_relu (Activation (None, None, None, 1 0           conv5_block3_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block3_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block3_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block3_concat (Concatenat (None, None, None, 6 0           conv5_block2_concat[0][0]        
                                                                     conv5_block3_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block4_0_bn (BatchNormali (None, None, None, 6 2432        conv5_block3_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block4_0_relu (Activation (None, None, None, 6 0           conv5_block4_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block4_1_conv (Conv2D)    (None, None, None, 1 77824       conv5_block4_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block4_1_bn (BatchNormali (None, None, None, 1 512         conv5_block4_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block4_1_relu (Activation (None, None, None, 1 0           conv5_block4_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block4_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block4_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block4_concat (Concatenat (None, None, None, 6 0           conv5_block3_concat[0][0]        
                                                                     conv5_block4_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block5_0_bn (BatchNormali (None, None, None, 6 2560        conv5_block4_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block5_0_relu (Activation (None, None, None, 6 0           conv5_block5_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block5_1_conv (Conv2D)    (None, None, None, 1 81920       conv5_block5_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block5_1_bn (BatchNormali (None, None, None, 1 512         conv5_block5_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block5_1_relu (Activation (None, None, None, 1 0           conv5_block5_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block5_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block5_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block5_concat (Concatenat (None, None, None, 6 0           conv5_block4_concat[0][0]        
                                                                     conv5_block5_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block6_0_bn (BatchNormali (None, None, None, 6 2688        conv5_block5_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block6_0_relu (Activation (None, None, None, 6 0           conv5_block6_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block6_1_conv (Conv2D)    (None, None, None, 1 86016       conv5_block6_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block6_1_bn (BatchNormali (None, None, None, 1 512         conv5_block6_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block6_1_relu (Activation (None, None, None, 1 0           conv5_block6_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block6_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block6_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block6_concat (Concatenat (None, None, None, 7 0           conv5_block5_concat[0][0]        
                                                                     conv5_block6_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block7_0_bn (BatchNormali (None, None, None, 7 2816        conv5_block6_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block7_0_relu (Activation (None, None, None, 7 0           conv5_block7_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block7_1_conv (Conv2D)    (None, None, None, 1 90112       conv5_block7_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block7_1_bn (BatchNormali (None, None, None, 1 512         conv5_block7_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block7_1_relu (Activation (None, None, None, 1 0           conv5_block7_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block7_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block7_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block7_concat (Concatenat (None, None, None, 7 0           conv5_block6_concat[0][0]        
                                                                     conv5_block7_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block8_0_bn (BatchNormali (None, None, None, 7 2944        conv5_block7_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block8_0_relu (Activation (None, None, None, 7 0           conv5_block8_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block8_1_conv (Conv2D)    (None, None, None, 1 94208       conv5_block8_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block8_1_bn (BatchNormali (None, None, None, 1 512         conv5_block8_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block8_1_relu (Activation (None, None, None, 1 0           conv5_block8_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block8_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block8_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block8_concat (Concatenat (None, None, None, 7 0           conv5_block7_concat[0][0]        
                                                                     conv5_block8_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block9_0_bn (BatchNormali (None, None, None, 7 3072        conv5_block8_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block9_0_relu (Activation (None, None, None, 7 0           conv5_block9_0_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block9_1_conv (Conv2D)    (None, None, None, 1 98304       conv5_block9_0_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block9_1_bn (BatchNormali (None, None, None, 1 512         conv5_block9_1_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block9_1_relu (Activation (None, None, None, 1 0           conv5_block9_1_bn[0][0]          
    __________________________________________________________________________________________________
    conv5_block9_2_conv (Conv2D)    (None, None, None, 3 36864       conv5_block9_1_relu[0][0]        
    __________________________________________________________________________________________________
    conv5_block9_concat (Concatenat (None, None, None, 8 0           conv5_block8_concat[0][0]        
                                                                     conv5_block9_2_conv[0][0]        
    __________________________________________________________________________________________________
    conv5_block10_0_bn (BatchNormal (None, None, None, 8 3200        conv5_block9_concat[0][0]        
    __________________________________________________________________________________________________
    conv5_block10_0_relu (Activatio (None, None, None, 8 0           conv5_block10_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block10_1_conv (Conv2D)   (None, None, None, 1 102400      conv5_block10_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block10_1_bn (BatchNormal (None, None, None, 1 512         conv5_block10_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block10_1_relu (Activatio (None, None, None, 1 0           conv5_block10_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block10_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block10_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block10_concat (Concatena (None, None, None, 8 0           conv5_block9_concat[0][0]        
                                                                     conv5_block10_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block11_0_bn (BatchNormal (None, None, None, 8 3328        conv5_block10_concat[0][0]       
    __________________________________________________________________________________________________
    conv5_block11_0_relu (Activatio (None, None, None, 8 0           conv5_block11_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block11_1_conv (Conv2D)   (None, None, None, 1 106496      conv5_block11_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block11_1_bn (BatchNormal (None, None, None, 1 512         conv5_block11_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block11_1_relu (Activatio (None, None, None, 1 0           conv5_block11_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block11_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block11_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block11_concat (Concatena (None, None, None, 8 0           conv5_block10_concat[0][0]       
                                                                     conv5_block11_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block12_0_bn (BatchNormal (None, None, None, 8 3456        conv5_block11_concat[0][0]       
    __________________________________________________________________________________________________
    conv5_block12_0_relu (Activatio (None, None, None, 8 0           conv5_block12_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block12_1_conv (Conv2D)   (None, None, None, 1 110592      conv5_block12_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block12_1_bn (BatchNormal (None, None, None, 1 512         conv5_block12_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block12_1_relu (Activatio (None, None, None, 1 0           conv5_block12_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block12_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block12_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block12_concat (Concatena (None, None, None, 8 0           conv5_block11_concat[0][0]       
                                                                     conv5_block12_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block13_0_bn (BatchNormal (None, None, None, 8 3584        conv5_block12_concat[0][0]       
    __________________________________________________________________________________________________
    conv5_block13_0_relu (Activatio (None, None, None, 8 0           conv5_block13_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block13_1_conv (Conv2D)   (None, None, None, 1 114688      conv5_block13_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block13_1_bn (BatchNormal (None, None, None, 1 512         conv5_block13_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block13_1_relu (Activatio (None, None, None, 1 0           conv5_block13_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block13_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block13_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block13_concat (Concatena (None, None, None, 9 0           conv5_block12_concat[0][0]       
                                                                     conv5_block13_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block14_0_bn (BatchNormal (None, None, None, 9 3712        conv5_block13_concat[0][0]       
    __________________________________________________________________________________________________
    conv5_block14_0_relu (Activatio (None, None, None, 9 0           conv5_block14_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block14_1_conv (Conv2D)   (None, None, None, 1 118784      conv5_block14_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block14_1_bn (BatchNormal (None, None, None, 1 512         conv5_block14_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block14_1_relu (Activatio (None, None, None, 1 0           conv5_block14_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block14_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block14_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block14_concat (Concatena (None, None, None, 9 0           conv5_block13_concat[0][0]       
                                                                     conv5_block14_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block15_0_bn (BatchNormal (None, None, None, 9 3840        conv5_block14_concat[0][0]       
    __________________________________________________________________________________________________
    conv5_block15_0_relu (Activatio (None, None, None, 9 0           conv5_block15_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block15_1_conv (Conv2D)   (None, None, None, 1 122880      conv5_block15_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block15_1_bn (BatchNormal (None, None, None, 1 512         conv5_block15_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block15_1_relu (Activatio (None, None, None, 1 0           conv5_block15_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block15_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block15_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block15_concat (Concatena (None, None, None, 9 0           conv5_block14_concat[0][0]       
                                                                     conv5_block15_2_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block16_0_bn (BatchNormal (None, None, None, 9 3968        conv5_block15_concat[0][0]       
    __________________________________________________________________________________________________
    conv5_block16_0_relu (Activatio (None, None, None, 9 0           conv5_block16_0_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block16_1_conv (Conv2D)   (None, None, None, 1 126976      conv5_block16_0_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block16_1_bn (BatchNormal (None, None, None, 1 512         conv5_block16_1_conv[0][0]       
    __________________________________________________________________________________________________
    conv5_block16_1_relu (Activatio (None, None, None, 1 0           conv5_block16_1_bn[0][0]         
    __________________________________________________________________________________________________
    conv5_block16_2_conv (Conv2D)   (None, None, None, 3 36864       conv5_block16_1_relu[0][0]       
    __________________________________________________________________________________________________
    conv5_block16_concat (Concatena (None, None, None, 1 0           conv5_block15_concat[0][0]       
                                                                     conv5_block16_2_conv[0][0]       
    __________________________________________________________________________________________________
    bn (BatchNormalization)         (None, None, None, 1 4096        conv5_block16_concat[0][0]       
    __________________________________________________________________________________________________
    relu (Activation)               (None, None, None, 1 0           bn[0][0]                         
    ==================================================================================================
    Total params: 7,037,504
    Trainable params: 6,953,856
    Non-trainable params: 83,648
    __________________________________________________________________________________________________



```python
# Print out the first five layers
layers_l = base_model.layers

print("First 5 layers")
layers_l[0:5]
```

    First 5 layers





    [<keras.engine.input_layer.InputLayer at 0x7f2868c234a8>,
     <keras.layers.convolutional.ZeroPadding2D at 0x7f2868c23780>,
     <keras.layers.convolutional.Conv2D at 0x7f2868c23898>,
     <keras.layers.normalization.BatchNormalization at 0x7f2868c23f28>,
     <keras.layers.core.Activation at 0x7f2868c23f60>]




```python
# Print out the last five layers
print("Last 5 layers")
layers_l[-6:-1]
```

    Last 5 layers





    [<keras.layers.normalization.BatchNormalization at 0x7f282403ea58>,
     <keras.layers.core.Activation at 0x7f282403ed68>,
     <keras.layers.convolutional.Conv2D at 0x7f2824050668>,
     <keras.layers.merge.Concatenate at 0x7f2824077860>,
     <keras.layers.normalization.BatchNormalization at 0x7f2824077978>]




```python
# Get the convolutional layers and print the first 5
conv2D_layers = [layer for layer in base_model.layers 
                if str(type(layer)).find('Conv2D') > -1]
print("The first five conv2D layers")
conv2D_layers[0:5]
```

    The first five conv2D layers





    [<keras.layers.convolutional.Conv2D at 0x7f2868c23898>,
     <keras.layers.convolutional.Conv2D at 0x7f28683c6fd0>,
     <keras.layers.convolutional.Conv2D at 0x7f2868378da0>,
     <keras.layers.convolutional.Conv2D at 0x7f2868333eb8>,
     <keras.layers.convolutional.Conv2D at 0x7f28682ecd68>]




```python
# Print out the total number of convolutional layers
print(f"There are {len(conv2D_layers)} convolutional layers")
```

    There are 120 convolutional layers



```python
# Print the number of channels in the input
print("The input has 3 channels")
base_model.input
```

    The input has 3 channels





    <tf.Tensor 'input_1:0' shape=(?, ?, ?, 3) dtype=float32>




```python
# Print the number of output channels
print("The output has 1024 channels")
x = base_model.output
x
```

    The output has 1024 channels





    <tf.Tensor 'relu/Relu:0' shape=(?, ?, ?, 1024) dtype=float32>




```python
# Add a global spatial average pooling layer
x_pool = GlobalAveragePooling2D()(x)
x_pool
```




    <tf.Tensor 'global_average_pooling2d_1/Mean:0' shape=(?, 1024) dtype=float32>




```python
# Define a set of five class labels to use as an example
labels = ['Emphysema', 
          'Hernia', 
          'Mass', 
          'Pneumonia',  
          'Edema']
n_classes = len(labels)
print(f"In this example, you want your model to identify {n_classes} classes")
```

    In this example, you want your model to identify 5 classes



```python
# Add a logistic layer the same size as the number of classes you're trying to predict
predictions = Dense(n_classes, activation="sigmoid")(x_pool)
print(f"Predictions have {n_classes} units, one for each class")
predictions
```

    Predictions have 5 units, one for each class





    <tf.Tensor 'dense_1/Sigmoid:0' shape=(?, 5) dtype=float32>




```python
# Create an updated model
model = Model(inputs=base_model.input, outputs=predictions)
```


```python
# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy')
# (You'll customize the loss function in the assignment!)
```

#### This has been a brief exploration of the Densenet architecture you'll use in this week's graded assignment!
