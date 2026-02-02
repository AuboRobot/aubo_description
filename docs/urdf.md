# urdf文件创建

## 附: 算法部输出文档

## 1. DH 参数说明

* 机械臂型号,  urdf中的robot name属性和文件名的前缀 三者保持一致

* 包括world坐标系和base与world的连接关系 (可以通过算法库接口进行设置)
* 运动学DH参数 (关节坐标系之间的变换关系)
* 动力学参数 (连杆的惯性张量, 质心, 质量)
* 连杆的显示模型(非必须)
* 连杆的碰撞模型
* 关节的软限位
* 关节的最大输出力矩
* 关节的最大速度和最大加速度
* 关节的转动惯量
* 关节的减速比(该参数在精确控制中需要调整)
* 关节的力矩常数
* 关节的刚度, 阻尼, 偏置(目前不需要)
* 配套的srdf文件

## 2. URDF/SRDF 文件说明

在urdf文件中，质心、质量、惯量等信息显示在link中，DH参数信息在joint中显示，下面以i5的link2为例进行说明

1、link信息

```xml
  <link name="upperArm_Link">
    <inertial>
      <origin xyz="0.2040 0 0.0196" rpy="0 0 0" />
      （质心在其参考坐标系2号坐标系下的位置，rpy均为0代表着质心处的坐标系与2号坐标系方向相同）
      <mass value="11.28" />
      （link的质量）
      <inertia ixx="0.0305" ixy="0" ixz="0" iyy="0.4505" iyz="0" izz="0.4400" />
      （link的惯量，所参考坐标系位置在link质心，方向与2号坐标系相同）
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <mesh filename="package://aubo_description/meshes/aubo_i5/visual/link2.3ds" />
      </geometry>
      <material name="">
        <color rgba="1 1 1 1" />
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <mesh filename="package://aubo_description/meshes/aubo_i5/collision/link2.STL" />
      </geometry>
    </collision>
  </link>
```

2、joint信息

```xml
  <joint name="upperArm_joint" type="revolute">
    <origin xyz="0 0.1215 0" rpy="-1.5707963267948966192313216916398 -1.5707963267948966192313216916398 0" />
    （origin xyz为其参考坐标系2号坐标系，相对于前一坐标系1号坐标系的位置）
    （origin rpy为1号坐标系按xyz固定角方式旋转至2号坐标系绕各轴旋转的角度值）
    <parent link="shoulder_Link" />
    <child link="upperArm_Link" />
    <axis xyz="0 0 1" />
    <limit lower="-3.054326190990076759616458844855" upper="3.054326190990076759616458844855" effort="133" start_stop="207" velocity="2.5964" />
    （关节运动范围下限，关节运动范围上线，关节谐波平均负载扭矩，关节谐波起停扭矩，关节最大速度）
    <property inertia="2.0" damping="0" stiffness="0" offset="0" motor_constant="8.72" ratio="121"/>
    （关节输出端转子惯量，关节阻尼，关节刚度，关节零位偏置，关节电机力矩常数，关节减速比）
  </joint>
```



