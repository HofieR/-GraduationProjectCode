# -GraduationProjectCode
tree：
        D:.
        ├─bert        #bert模型算法，仅作参考
        │  ├─.idea
        │  │  └─inspectionProfiles
        │  └─simple_data
        ├─bilstm-crf  #bilstm-crf模型算法
        │  ├─input      #输入文件，包含训练集、验证集、测试集、预测数据等
        │  │  ├─target    #预测数据，内含专利与标准的xls文件以及预测结果的json文件
        │  │  └─train     #已经预处理过的json格式的训练集、验证集、测试集
        │  ├─log        #模型训练过程的可视化log
        │  ├─model      #分别用知网原数据、标题数据、摘要数据训练的模型
        │  └─__pycache__
        ├─data        #内含各种未经过处理的原始数据
        │  ├─data_cnki    #知网数据
        │  │  └─json        #处理成json格式的知网数据
        │  ├─data_native  #CLUNER开源数据集
        │  ├─data_ner     #ner的结果
        │  ├─data_target  #专利、标准数据集
        │  ├─data_tran    #翻译后的数据集
        │  └─date_process #爬虫、数据预处理的代码
        │      └─train_data
        │          ├─data_native
        │          └─data_processed
        ├─paper
        └─__pycache__
  
  
