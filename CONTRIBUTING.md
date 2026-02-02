# 机器人型号导入与设计标准化流程

## 1. 概述

本文档定义了从机器人型号设计需求到最终模型发布的完整标准化流程，确保：
- 模型参数来源一致
- URDF/SRDF/Mesh/Config文件可追溯、可校核、可量产
- 性能规格参数（负载、力矩、速度、工作空间）可复现、可验证

## 2. 机械臂设计流程

### 2.1 设计流程概览

| 步骤                  | 子步骤                     | 输入                                                | 输出                        | 负责人         | 相关文档/工具                                                |
| --------------------- | -------------------------- | --------------------------------------------------- | --------------------------- | -------------- | ------------------------------------------------------------ |
| **1. 确定设计需求**   |                            | 1. 竞品调研<br>2. 确定设计目标                      | 设计目标参数表              | 产品经理       | 完善[设计规格模板](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm)中需求参数部分 |
| **2. 机械臂设计**     | **2.1 关节减速器初步选型** | 1. 期望速度<br>2. 减速器规格书                      | 减速器型号                  | 机械部         | 谐波减速器规格书                                             |
|                       | **2.2 杆长设计**           | 期望臂展                                            | URDF文件                    | 机械部         |                                                              |
|                       | **2.3 关节力矩初步估计**   | 1. 初步URDF<br>2. 负载质量质心                      | 关节最大重力矩              | 机械部+算法部  | 工具开发中（暂时联系紫衣），工具开发完成后由机械部负责       |
|                       | **2.4 关节力矩校核**       | 1. 初步URDF<br>2. 负载质量质心<br>3. 关节最大重力矩 | 校核结果                    | 机械部+算法部  | [完善设计规格模板](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm)中设计校核部分<br />工具开发中（暂时联系紫衣），工具开发完成后由机械部负责 |
|                       | **2.5 输出负载偏移曲线**   | URDF文件                                            | 负载偏移曲线                | 算法部         | 在[设计规格模板](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm)处添加偏移曲线<br />工具开发中（暂时联系紫衣），工具开发完成后由机械部负责 |
| **3. 会议评审确定**   |                            | 校核结果                                            | 最终URDF(type_name_T0.urdf) | 产品+机械+算法 | [设计规格模板](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm) |
| **4. 最终版URDF提交** |                            | URDF文件                                            | aubo_description提交MR      | 机械部         | 提交MR                                                       |

### 2.2 详细设计步骤

#### 2.2.1 确定设计需求
1. **竞品调研**：调研竞品机械臂，确认模块型号，完善竞品调研表格
   - 竞品资料存放位置：研发中心-算法部-竞品信息
   
2. **确定设计需求**：
   - 完善[机械臂设计需求表格](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm)
   - 明确应用场景（装配、搬运、焊接等），是否考虑侧装，是否存在关节传感器
   - 选择构型和自由度配置（若构型或自由度为新增类型，需要算法提供坐标系）
   - 期望臂展长度，以及负载

#### 2.2.2 机械臂设计
1. **关节减速器初步选型**：
   - 根据竞品调研结果，初步确定模块型号
   - 查找模块表格，确定模块的质量质心

2. **杆长初步设计**：
   - 根据期望臂展长度，设计杆长比例（a2/(a3+d5)在0.8-1.2之间；最佳比例为1）
   - 杆长比例推荐1：1
   - 杆长mm位尽量为整数

3. **关节力矩初步计算**：
   - 输出根据初步设计杆长和模块初步选型生成初步URDF文件
   - 以负载偏移曲线构型，满载，负载偏移100mm计算机械臂重力矩（G_payload）

4. **关节力矩校核**：
   - **校核标准**：
     - G_payload 2、3、4关节小于启停力矩的α倍
       - 启停力矩 > 841：α = 0.9
       - 否则：α = 0.8
     - G_payload 3、4关节接近平均负载扭矩
   - 如不满足标准，重新选择减速比

5. **重新调整设计**（关节力矩不满足校核标准时）：
   - **关节减速器选型**：根据校核结果确认是否需要更换减速机模块/速比
   - **杆长调整**：以2、3、4关节力矩能力，对a2、a3进行微调（模块确定后d5确定）
     - 如果2关节比较极限，缩短a2
     - 如果3关节比较极限，缩短a3
   - **关节力矩计算**：根据调整的杆长和模块，重新输出URDF
   - **关节力矩校核**：重新校核

6. **输出负载偏移曲线**：
   - 根据URDF文件生成负载偏移曲线
   - 更新[设计规格模板](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm)

#### 2.2.3 会议评审确定
- 会议评审确定最终方案
- 输出最终的URDF文件（type_name_T0.urdf）
- 更新[参数表格](https://alidocs.dingtalk.com/i/nodes/NkDwLng8ZLzXBb21Sjem7p0wVKMEvZBY)

#### 2.2.4 最终版URDF文件提交
- 将最终版URDF文件提交到arcs/aubo_description仓库中

## 3. 模型文件生成流程

### 3.1 模型生成流程概览

| 步骤                      | 输入                                                         | 输出                                                         | 负责部门/角色   | 相关文档/表格                                                |
| ------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | --------------- | ------------------------------------------------------------ |
| 1. 填写型号参数统计表格   | 1. 标准机械臂名称<br>2. 产品硬件参数指标<br>3. 机械模型      | 1. 基本信息<br>2. 产品机械图（带尺寸）                       | 产品经理+机械部 | 型号统计表（由产品经理提供）                                 |
| 2. 建立DH坐标系           | 1. 产品机械图（带尺寸）<br>2. Z轴正方向标注                  | 1. 坐标系图<br>2. DH参数                                     | 算法部          | 坐标系图和DH参数在[机器人参数汇总](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWygkE3oRTkELE4y7JkyEqBQm?utm_scene=team_space)维护 |
| 3. URDF文件生成           | 1. 坐标系图<br>2. 理论动力学模型参数<br>3. 机器人关节参数    | 1. URDF文件(type_name.urdf)<br>2. 动力学参数和关节参数       | 机械部+算法部   | 机械部提交URDF文件（提交MR），算法部校核                     |
| 4. 导出渲染模型和碰撞模型 | 1. 三维机械模型<br>2. 材质颜色规范（RGB值）                  | 1. 渲染模型(.3ds, .DAE)<br>2. 碰撞模型(.STL)                 | 机械部+算法部   | [导出渲染模型和碰撞模型教程](http://git.aubo-robotics.cn:8001/arcs/aubo_description/-/blob/master/docs/meshes_export.md) |
| 5. SRDF文件生成           | 1. URDF文件<br>2. mesh文件                                   | SRDF文件(type_name.srdf)                                     | 算法部          | 算法部提交SRDF文件，后期生成工具后由机械部提交               |
| 6. 配置文件               | 第1步的表格信息                                              | 1. 机器人config文件<br>2. 关节config文件<br>3. 控制柜config文件 | 软件部          | 由软件部提交机械臂config文件                                 |
| 7. 验证                   | 1. URDF模型文件<br>2. SRDF文件<br>3. mesh文件<br>4. config文件 | 模型显示结果                                                 | 软件部          | 软件部验证模型显示是否正确                                   |
| 8. 性能规格输出           | URDF文件                                                     | 负载偏移曲线图                                               | 算法部          | 算法部提供负载偏移曲线图，后期生成工具后由机械部提交         |

### 3.2 详细模型生成步骤

#### 3.2.1 填写型号参数统计表格
- 从模板中选择对应的系列模板，如i系列选择`aubo_i.xlsx`
- 重命名为具体型号，如`aubo_i5_10.xlsx`
- 完成表格填写：
  - a. 基本信息：包括型号、关节限制等
  - b. DH参数：根据图例填写尺寸参数

#### 3.2.2 建立DH坐标系
机械部机械工程师给出产品机械图并标注出Z轴正方向并提供正确的动力学参数、机器人关节参数等，算法部建立DH坐标系并将建立好的坐标系及相关参数同步到[机器人参数汇总](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWygkE3oRTkELE4y7JkyEqBQm?utm_scene=team_space)中。

**坐标系建立规则**：

1. 坐标系原点位于两坐标系z轴交点
2. 坐标系0的y轴方向和机械臂/机器人行插方向保持一致
3. 坐标系6的y轴方向和末端突起的地方保持一致
4. 坐标系6的z方向指向法兰外法线方向（特殊要求除外）
5. 使DH参数中有尽可能多的0

#### 3.2.3 URDF文件生成
1. **URDF文件生成**：由机械部完成[SolidWorks导出URDF文件步骤](docs/SolidWorks_export_URDF_step.md)

2. **动力学参数更新**：
   
   - 测量方案：[动力学模型建立教程](https://alidocs.dingtalk.com/uni-preview?extension=doc&bizType=document&watermark=true&cloudSpaceDentryId=206202222005&cloudSpaceSpaceId=9206440325&version=1&scene=universalSpace&mainsiteOrigin=mainsite&spaceId=9206440325&fileSize=4247040&dentryUuid=bva6QBXJwZKPyRMpu64znZnqVn4qY5Pr&isMobile=false&fileId=206202222005)
   - 脚本：读取Excel参数表，更新URDF中的惯性元素
   ```matlab
   % excelFileName：存放动力学参数的Excel文件名称
   % urdfFileName：原始URDF文件名称
   % newFileName：生成的新URDF文件名称
   update_urdf_from_excel(excelFileName, urdfFileName, newFileName);
   ```

3. **URDF文件中各个参数含义：**

   以i5为例介绍一下urdf文件中各个参数的含义：

   ```html
     <link name="shoulder_Link">
       <inertial>
         <origin xyz="-0.00001 0.001807 -0.013854" rpy="0 0 0" />//关节重心位置
         <mass value="4.848581" />//关节质量
         <inertia ixx="0.011842" ixy="0" ixz="0.000004" iyy="0.0118" iyz="-0.000103" izz="0.008103" />//关节惯性参数
       </inertial>
       <visual>
         <origin xyz="0 0 0" rpy="0 0 0" />
         <geometry>
           <mesh filename="package://aubo_description/meshes/aubo_i5/visual/link1.DAE" />//对应的关节dae文件路径
         </geometry>
         <material name="">
           <color rgba="1 1 1 1" />
         </material>
       </visual>
       <collision>
         <origin xyz="0 0 0" rpy="0 0 0" />
         <geometry>
           <mesh filename="package://aubo_description/meshes/aubo_i5/collision/link1.STL" />//对应的关节stl文件路径
         </geometry>
       </collision>
     </link>
   
   ```

   ```html
     <joint name="shoulder_joint" type="revolute">
       <origin xyz="0 0 0.122" rpy="0 0 3.1415926535897932384626433832795" /> //rpy值，DH参数表中的角度为欧拉角
       <parent link="base_link" />//父关节
       <child link="shoulder_Link" />//子关节
       <axis xyz="0 0 1" />//代表z轴正方向和旋转轴方向保持一致，一般均为0 0 1
       <limit lower="-6.283185307179586476925286766559" upper="6.283185307179586476925286766559" effort="133" start_stop="207" velocity="2.5964" />//lower/upper:运动下/上限 effort：平均转矩容许最大值 start_stop：启动，停止容许最大转矩  velocity：关节允许最大速度
       <property inertia="2.027236783" damping="0" stiffness="0" offset="0" motor_constant="8.72" ratio="121" protect_max_torque="80.0" equa_inertia="1.5" collision_detection_para = "50 50 30 20"/>//inertia：转子惯量 damping：关节阻尼 stiffness：关节刚度  motor_constant：力矩系数 ratio：减速比 protect_max_torque：最大保护力矩 equa_inertia：等效惯量 collision_detection_para： 碰撞参数  
     </joint>
   ```

#### 3.2.4 导出渲染模型和碰撞模型

- 渲染模型和碰撞模型的导出是从机械三维制图到控制器甚至算法用于计算的模型的转换过程，详细导出方法请参考[导出碰撞模型和渲染模型说明](docs/meshes_export.md)

- STL文件验证(后期工具开发完成后由机械部使用工具验证)：

  ```matlab
  robot = importrobot('aubo_i5.urdf');
  show(robot);
  ```

- **各系列颜色（RGB）值**：
  - i系列/T系列：橙色：232,131,0；黑色：52,52,52
  - C系列：白色：255,255,255；蓝色：2,68,235；灰色：160,160,160
  - E系列：白色：255,255,255；灰色：105,105,105
  - aubo_C5_39：灰色：185,185,185
  - 机械臂显示模型除受到RGB值影响外还受到材质等的影响，以机械部/事业部给出为准

#### 3.2.5 SRDF文件生成

​	目前由算法部生成，后期工具开发完成后由机械部使用工具生成，步骤：

1. 将机器人相关模型添加到build/aubo_description文件夹下
2. 打开仿真平台0.39.x-stable，点击model模块下的生成SRDF按钮

#### 3.2.6 配置文件
1. **机器人配置文件**：
   
   ```toml
   [DH]
   a = [0.00000, -0.42500, -0.39220, 0.00000, 0.00000, 0.0000]
   d = [0.1625, 0.00000, 0.00000, 0.1333, 0.09970, 0.0996]
   alpha = [1.570796327, 0, 0, 1.570796327, -1.570796327, 0]
   q_home_offset = [0, -0.26179938779914943653855361527329, 1.7453292519943295769236907684886, 0.43633231299858239423092269212215, 1.5707963267948966192313216916398, 0]
   joint_direction = [1, 1, -1, 1, 1, 1]
   
   [Joint]
   joint = ['joint_M25B_h402', 'joint_M25B_h402', 'joint_M25B_h402', 'joint_M14B_h402.conf', 'joint_M14B_h402.conf', 'joint_M14B_h402.conf']
   
   [Payload]
   mass = 5.0
   
   [ControlBox]
   controlBox = 'cb_standard.conf'
   ```
   
2. **关节配置文件**：
   ```toml
   gear_ratio = 101
   min_limit = -3.054326190990076759616458844855
   max_limit = 3.054326190990076759616458844855
   v_max = 3.1101767270538953060780169494467
   a_max = 20.0
   ```

3. **控制柜配置文件**：
   ```toml
   num = 16
   name = ["DI00", "DI01", "DI02", "DI03", "DI04", "DI05", "DI06", "DI07", "DI10", "DI11", "DI12", "DI13", "DI14", "DI15", "DI16", "DI17"]
   ```

#### 3.2.7 验证
1. 安装ARCS虚拟机：[ARCS虚拟机映像安装说明](https://docs.aubo-robotics.cn/application_notes/06-arcs-virtual-machine/)
2. 将机械臂模型文件放置在opt/arcs/版本号/aubo_description对应文件夹下
3. 更改aubo_control.conf文件：
   ```toml
   [[RobotHw]]
       location = "extensions/fake_robot/fake_robot.so"
       [RobotHw.options]
           model_type = "aubo_i20"
           model_subtype = ""
           controlbox_type = "cb_standard"
   
   [[RobotModule]]
       alias = "rob1"
       enable = true
       robot_type = "aubo_i20"
       collision_detect_enable = true
   ```
4. 打开ARCS软件，上电，点击移动，改变各个关节角度，验证模型准确性

#### 3.2.8 性能规格输出
- **负载偏移曲线**：[代码链接](http://git.aubo-robotics.cn:8001/aral/matlab/-/blob/main/applications/Plot_Payload_Offset_Curve/plot_payload_offset.m?ref_type=heads)
- **工作空间**：[代码链接](http://git.aubo-robotics.cn:8001/aral/matlab/-/blob/main/applications/Singularity_Analysis/Singular_JointSpace_i5.m?ref_type=heads)
- **灵活工作空间**：[代码链接](http://git.aubo-robotics.cn:8001/aral/matlab/-/blob/main/applications/Singularity_Analysis/Singular_JointSpace_i5.m?ref_type=heads)
- **末端最大线速度**：已有工具，相关issue: [issue 14916](http://git.aubo-robotics.cn:8001/arcs/TR/-/issues/14916)
- **动力学参数统计表**：
  - 将URDF文件放入interface/build/aubo_description/urdf文件夹下
  - 在interface工程中运行testReadUrdf生成动力学模型参数理论计算值

## 4. 版本管理与提交

### 4.1 文件命名规范
- URDF文件：`type_name.urdf`（最终版为`type_name_T0.urdf`）
- 配置文件：`type_name.conf`
- Mesh文件：按照系列分类存放

### 4.2 提交流程
1. 机械部提交URDF和mesh文件到[aubo_description仓库](http://git.aubo-robotics.cn:8001/arcs/aubo_description)
2. 算法部提交SRDF文件(后期工具开发完成由机械部提交)
3. 软件部提交配置文件
4. 由算法部和软件部审核通过后合并

### 4.3 版本控制
- 设计过程中的URDF文件命名为`type_name_T0.urdf`
- 最终发布版本使用标准命名`type_name.urdf`
- 所有设计文档和参数表格在钉钉文档中统一维护

## 5. 附录

### 5.1 相关文档链接
- [设计规格模板](https://alidocs.dingtalk.com/i/nodes/93NwLYZXWyDvLmerckX4D2gl8kyEqBQm)
- [参数维护表格](https://alidocs.dingtalk.com/i/nodes/NkDwLng8ZLzXBb21Sjem7p0wVKMEvZBY)
- [ARCS虚拟机安装说明](https://docs.aubo-robotics.cn/application_notes/06-arcs-virtual-machine/)
