// 自定义字符串格式化
String.prototype.format = function (kwargs) {

    var ret = this.replace(/\{(\w+)\}/g,function (km, m) {
        return kwargs[m];
    });
    return ret;
};