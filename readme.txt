<Structure>
process_calculation/
---- main.py
---- myconfig/
    __init__.py
    config.py
    cost_calculation.py
    cost_estimation.py
    loader.py
    plotter.py

---- DATA/
    steel_production.csv
    CEPCI.csv

1. csvファイル作成
2. config.pyでcsvファイルを読み込み、データを作り、__all__にいれる
3. cost_calculation.pyで、まずデータを.configからimportした後、そのデータを使って計算するコードを作る
4. __init__.pyで、ます外に出したい関数を.configからimportしたあと、それを__all__にいれる
5. main.pyで、myconfigから使いたい関数をimportして、自由に使える

*config.pyはデータのロード用
*__init__.pyはmyconfigフォルダから外に出るものを管理

*config.py内で__all__を指定することにより、importしたデータと実際に使うデータを区別することができる
*__init__.pyで指定することにより、表に出る関数と裏に隠しておく関数を分けておくことができる
*__init__.pyでの__all__の指定は、main.pyで「from myconfig import *」のときにimportされる関数を指定できる
*config.pyで指定することにより、表に出るデータセットを一元的に管理できる(恐らく、データセットを操作したものを渡したいときに便利)