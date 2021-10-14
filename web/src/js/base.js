

function Options (params) {
    let Fields = [0, 0, 0, 0, 0, 0];
    params.forEach(e => {
        Fields[e[1]] = e[0];
    });
    return Fields
}

function Limit (conf) {
    return conf.map(d => ({'must': d[0], 'select': d[1]}));
}

let Numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', 
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', 
    '二十', '二十一', '二十二', '二十三', '二十四', '二十五', '二十六', 
    '二十七', '二十八', '二十九', '三十'
];

// option: ["类别", "索引"]
// limit: [是否必填，是否只能选]
let Types = [
    {
        code: 0,
        name: '研发',
        options: Options([['项目', 0], ['模块', 1], ['任务', 2]]),
        limit: [[1, 1], [1, 1], [1, 1]],
        value: 'project'
    }, {
        code: 1,
        name: '事务',
        options: Options([['事务', 0], ['子项', 1], ['任务', 2]]),
        limit: [[1, 1], [0, 0], [1, 0]],
        value: 'business'
    }, {
        code: 2,
        name: '临时',
        options: Options([['项目', 0], ['任务', 2]]),
        limit: [[0, 0], [1, 0]],
        value: 'temp'
    }, {
        code: 3,
        name: '外出',
        options: Options([['项目', 0], ['地点', 1], ['事项', 2]]),
        limit: [[1, 0], [1, 0], [1, 0]],
        value: 'out'
    }, {
        code: 4,
        name: '其它',
        options: Options([['事项', 0], ['子项', 1], ['任务', 2]]),
        limit: [[1, 0], [0, 0], [1, 0]],
        value: 'other'
    }
];

export {Numbers, Types};