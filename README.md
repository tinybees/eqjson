# ejson
An smart json,similar to the jquery, read and update the json data.

一个小巧的、完全无依赖的类似jquery写法的读取和更改json的工具，可以按照json的层级或者某个属性读取json数据。

## Installing aelog
- ```pip install ejson```

## Usage
假如json数据如下：
```
[
   {
      'object':{
         'name':'myLittleObject',
         'value':[
            {
               'key2':'value2',
               'key3':'value3',
               'key1':'value1'
            },
            {
               'key33':'value33',
               'key1':'value11'
            },
            {
               'key333':'value333',
               'key1':'value111'
            }
         ],
         'type':'list',
         'valueAsString':[
            'one',
            'two'
         ]
      }
   }
]
```
#### 基本用法：
- 如果要获取name值：则写法为```0.object.name```
- 如果json最外层是{}获取name值：则写法为```object.name```
- 如果要获取valueAsString中的第一个值：则写法为```0.object.valueAsString.0```
- 如果json最外层是{}获取valueAsString中的第一个值：则写法为```object.valueAsString.0```
- 获取value列表中的第一个值的key1值：则写法为```0.object.value.0.key1```
- 获取value列表中的所有的key1值：则写法为```0.object.value.key1```， 则结果为```['value1','value11', 'value111']```
#### 高级用法：
- 支持通过属性确定值，如果json是无序的，要获取key1值为value1所在节点的key3的值，则写法为```0.object.value[key1=value1].key3```
- 支持通过多属性确定值，比如要获取key1值为value1，key2值为value2，所在节点的key3的值，则写法为```0.object.value[key1=value1，key2=value2].key3```
- 支持多层属性，比如要获取name为myLittleObject的以上的值：则写法为```[name=myLittleObject].object.value[key1=value1].key3```


## 单测
- 100%文件覆盖率，77%的行覆盖率
