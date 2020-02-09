# 关于python无法正常读取P3类型的ppm图片
PIL库以及pillow库只能支持P4 P5 P6类型的ppm图的读取，python2可以选择PythonMagick库代替，Python3使用opencv代替。

# RecursionError: maximum recursion depth exceeded
在代码中加入最大递归深度限制