from ulab import numpy as np

def thd_fft_calc

    i1=i2=i3=i4=i5=i6=i7=1
    thd_fft=np.sqrt((i2**2)+(i3**2)+(i4**2)+(i5**2)+(i6**2)+(i7**2))/(i1**2)
    print(thd_fft)
    return thd_fft
    
def thd_thresh_calc
    thd_thresh=np.sqrt(i_thresh**2)/i1
    print(thd_thresh)
    return thd_thresh



#MUST DO HOW TO READ FROM FILE
#USING INPUT FROM THE CLIENT


'''
def thd_calc(user_thresh, max_amp)
    
    thd_1 = user_thresh ** 2
    #thd_2 = np.sqrt(thd2_1)
    #thd_3 = thd2_2/max_amp
    
    return thd_1
    
    
    
thd_perc = thd_calc(30, 60.99953)
print(thd_perc)
'''