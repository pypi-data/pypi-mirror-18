说明：

此开发模组包供Morningstar Data Production/API QA 团队的成员进行Robot Framework 测试时使用。

这个模组包封装了大家在使用Robot Framework 的过程中需要使用的一些Python函数及方法。

这些封装的方法会随时更新。我尽量保证这些方法的接口的一致性。若实在是不小心使得用户的Test Case出现失败，请联系我确认，并再另行更改。

Benjamin Zhou, 20160923

源代码升级方法：
Step1: 开发并测试你的源代码，确保无误
Step2: 修改CodeLibWrapper.py中的版本编号，版本编号分为三个部分：主版本号、 次版本号和修订版本号。版本号的变更规则为：
       （1）以下情况可对修订版本号进行变更：修改、重构现有方法
       （2）以下情况可对次版本号进行变更：增加主要的类和功能项
       （3）主版本号暂可保留为0
Step3： 执行Package.Bat文件