let Utils = {};

function dateFormat(fmt, date) {
    date = date || new Date();
    let ret;
    const opt = {
        "Y+": date.getFullYear().toString(),        // 年
        "m+": (date.getMonth() + 1).toString(),     // 月
        "d+": date.getDate().toString(),            // 日
        "H+": date.getHours().toString(),           // 时
        "M+": date.getMinutes().toString(),         // 分
        "S+": date.getSeconds().toString()          // 秒
        // 有其他格式化字符需求可以继续添加，必须转化成字符串
    };
    for (let k in opt) {
        ret = new RegExp("(" + k + ")").exec(fmt);
        if (ret) {
            fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
        }
    }
    return fmt;
}

function ajax (key, data, toast) {
    return new Promise((resolve, reject) => {
        getCache('token', true).then(d => {
            if (d) data['token'] = d;
            uni.showLoading();
            uni.request({
                url: "/api" + key,
                dataType: 'json',
                data: data
            }).then(res => {
                // 处理系统定义的逻辑错误
                if (res[1].data.error) {
                    reject(res[1].data);
                    uni.showToast({
                        title: res[1].data.message,
                        icon: 'error',
                        mask: true,
                        duration: 1000
                    });

                } else {
                    resolve(res[1].data);

                    if (toast) {
                        uni.showToast({
                            title: toast,
                            icon: 'success',
                            mask: true,
                            duration: 1000
                        });
                    }
                }
                uni.hideLoading();
            }).catch(err => {
                reject(err);
                uni.showToast({
                    title: "请求失败！",
                    icon: 'none',
                    mask: true,
                    duration: 1000
                });
                uni.hideLoading();
            }); 
        });
    });
}

function setCache (key, value) {
    uni.setStorage({
        key: key,
        data: value,
        fail: () => {
            uni.showModal({
                title: '储存数据失败!',
                showCancel: false
            })
        }
    });    
}

function getCache (key, noError) {
    return new Promise((resolve, reject) => {
        uni.getStorage({
            key: key,
            success: (res) => {
                resolve(res.data);
            },
            fail: () => {
                if (noError) resolve(null); else reject(res.data);
            }
        })
    });
}




Utils.ajax = ajax;
Utils.setCache = setCache;
Utils.getCache = getCache;
Utils.dateFormat = dateFormat;

export default Utils;