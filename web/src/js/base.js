

function Options (params) {
    let Fields = [0, 0, 0, 0, 0, 0];
    params.forEach(e => {
        Fields[e[1]] = e[0];
    });
    return Fields
}

let Numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', 
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', 
    '二十', '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', 
    '二十七', '二十八', '二十九', '三十'
];

let Types = [
    {
        code: 0,
        name: '研发',
        options: Options([['项目', 0], ['模块', 1], ['任务', 2]]),
        value: 'project'
    }, {
        code: 1,
        name: '事务',
        options: Options([['事务', 0], ['子项', 1], ['任务', 2]]),
        value: 'business'
    }, {
        code: 2,
        name: '临时',
        options: Options([['任务', 2]]),
        value: 'temp'
    }, {
        code: 3,
        name: '外出',
        options: Options([['项目', 0], ['事项', 1], ['地点', 2]]),
        value: 'out'
    }, {
        code: 4,
        name: '其它',
        options: Options([['事项', 0], ['子项', 1], ['任务', 2]]),
        value: 'other'
    }
];

export {Numbers, Types};