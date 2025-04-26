# todo ORM操作

# pip install tortoise-orm
# pip install aiomysql
# pip install aerich

# todo 测试数据
# mysql> create database fastapi charset utf8;
# mysql> show create database fastapi;

# todo 学习 ORM迁移
# https://www.bilibili.com/video/BV1Ya4y1D7et?spm_id_from=333.788.player.switch&vd_source=be21f48b876460dfe25064d745fdc372&p=27

# todo aerich 是一种 ORM 迁移工具，需要结合 tortoise 异步 orm 框架使用。安装 aerich
# 步骤1：初始化配置，aerich init -t setting.TORTOISE_ORM      # 其中setting是目录下配置文件，TORTOISE_ORM 配置的位置
(py310) localhost-2:09ORM linghuchong$ aerich init -t setting.TORTOISE_ORM
Success writing aerich config to pyproject.toml
Success creating migrations folder ./migrations
# 初始化完会在当前目录生成一个文件：pyproject.toml 和一个文件夹：migrations
# pyproject.toml：保存配置文件路径，低版本可能是 aerich.ini
# migrations：存放迁移文件

# 步骤2：初始化数据库，aerich init-db
# 如果 TORTOISE_ORM 配置文件中的 models 改了名，则执行这条命令时需要增加 --app 参数，来指定你修改的名字
(py310) localhost-2:09ORM linghuchong$ aerich init-db
Success creating app migration folder migrations/models
Success generating initial migration file for app "models"

结果：数据库fastapi中生成了6张表，其中aerich不用管，其他表 clas\course\student\teacher\student_course

步骤3：更新模型并进行迁移
# 修改 model 类，重新生成迁移文件，比如添加一个字段
# class Course (Model):
# ...
# addr = fields.CharField (max_length=255)
# aerich migrate [--name] (标记修改操作) # aerich migrate --name add_column
# 迁移文件名的格式为 {version_num}{datetime}{name|update}.json。
(py310) localhost-2:09ORM linghuchong$ aerich migrate
Success creating migration file 1_20250426213816_update.py   //生成1_20220827155504_update.sql，里面记录了 upgrade 和 downgrade
(py310) localhost-2:09ORM linghuchong$ aerich upgrade   //执行1_20220827155504_update.sql 中update
Success upgrading to 1_20250426213816_update.py

# todo aerich downgrade   //执行1_20220827155504_update.sql 中downdate
# todo aerich history //查看历史记录

