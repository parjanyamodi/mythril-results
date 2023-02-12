const fs = require('fs');
const cleanUp = require('./cleanUp')
const legit = require('./vulnerabilities.json')

const mapping = {
    112: "access_control",
    101: "arithmetic",
    107: "reentrancy",
    113: "denial_of_service",
    124: "access_control",
    110: "access_control",
    105: "access_control",
    115: "access_control",
    106: "access_control",
    116: "time_manipulation",
    120: "bad_randomness",
    104: "unchecked_low_level_calls",
    }


const timeParse = (str) => {
    var arr = str.split(':')
    // console.log(arr)
    var t = 0.0
    for(var i =arr.length-1; i >=0; i--){
        if(arr[i] === undefined || arr[i] === null || arr[i] === "")
        {break}
        t += parseFloat(arr[i])*Math.pow(60, arr.length-1-i)
        // console.log(t)
    }
    // console.log(t)
    return t
}

const isLegit = (data) => {
    
    return data.success
}

function union(setA, setB) {
    const _union = new Set(setA);
    for (const elem of setB) {
      _union.add(elem);
    }
    return _union;
  }

const processAllFiles = (dir) => {
    const types = fs.readdirSync(dir)
    var swcIds = new Set()
    for(var i =0; i <types.length; i++){
        var time = 0
        dir = types[i]
        var c = 0
        var t = 0
        const files = fs.readdirSync(`./oyente_results/${dir}`)
        for(var j =0; j <files.length; j++){
            var file = files[j]
            var data = cleanUp(`./oyente_results/${dir}/${file}`, dir, file)
            if (data && data.issues && data.issues.length > 0 && isLegit(data, dir, file))
            {
                // swcIds = union(swcIds, isLegit(data, dir, file))
                time += data.time
                // console.log(dir, file, data.time)
                c++
            }
            t++
        }
        console.log(`${dir}: ${c}/${t}`)
        console.log(`Time: ${time/c}`)
    }
}

processAllFiles('./oyente_results')