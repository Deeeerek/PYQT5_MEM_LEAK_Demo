# PYQT5_MEM_LEAK_Demo
demo for memory leakage


1. demo_matplotlib_animation_mem_leak.py 
    在使用animation function时，随着图形的刷新，看到占用内存不断增大
    目前demo程序，只在GUI画了条不断刷新的直线。
    
2. demo_Qthread_mem_leak.py
    使用了两个进程：
    第一个进程每等待200ms发送信号给主进程，触发第二个进程
    第二个进程等待100ms返回信号
    
    目前都是建立的demo进程，只有空等，但是内存还是会增加，实际的case会有其他任务，内存增加也更明显
