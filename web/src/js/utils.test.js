const rewire = require("rewire")
const utils = rewire("./utils")
const dateFormat = utils.__get__("dateFormat")
const setCache = utils.__get__("setCache")
const getCache = utils.__get__("getCache")
// @ponicode
describe("dateFormat", () => {
    test("0", () => {
        let callFunction = () => {
            dateFormat("01:04:03", "01-01-2020")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("1", () => {
        let callFunction = () => {
            dateFormat("2017-09-29T23:01:00.000Z", "01-01-2030")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("2", () => {
        let callFunction = () => {
            dateFormat("2017-09-29T19:01:00.000", "32-01-2020")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("3", () => {
        let callFunction = () => {
            dateFormat("2017-09-29T23:01:00.000Z", "01-01-2020")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("4", () => {
        let callFunction = () => {
            dateFormat("01:04:03", "01-01-2030")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("5", () => {
        let callFunction = () => {
            dateFormat(undefined, undefined)
        }
    
        expect(callFunction).not.toThrow()
    })
})

// @ponicode
describe("setCache", () => {
    test("0", () => {
        let callFunction = () => {
            setCache("Dillenberg", "Dillenberg")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("1", () => {
        let callFunction = () => {
            setCache("Dillenberg", "Elio")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("2", () => {
        let callFunction = () => {
            setCache("Dillenberg", "elio@example.com")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("3", () => {
        let callFunction = () => {
            setCache("Elio", "Dillenberg")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("4", () => {
        let callFunction = () => {
            setCache("elio@example.com", "Dillenberg")
        }
    
        expect(callFunction).not.toThrow()
    })

    test("5", () => {
        let callFunction = () => {
            setCache(undefined, undefined)
        }
    
        expect(callFunction).not.toThrow()
    })
})

// @ponicode
describe("getCache", () => {
    test("0", () => {
        let callFunction = () => {
            getCache("Elio", true)
        }
    
        expect(callFunction).not.toThrow()
    })

    test("1", () => {
        let callFunction = () => {
            getCache("elio@example.com", false)
        }
    
        expect(callFunction).not.toThrow()
    })

    test("2", () => {
        let callFunction = () => {
            getCache("Elio", false)
        }
    
        expect(callFunction).not.toThrow()
    })

    test("3", () => {
        let callFunction = () => {
            getCache("Dillenberg", false)
        }
    
        expect(callFunction).not.toThrow()
    })

    test("4", () => {
        let callFunction = () => {
            getCache("Dillenberg", true)
        }
    
        expect(callFunction).not.toThrow()
    })

    test("5", () => {
        let callFunction = () => {
            getCache(undefined, undefined)
        }
    
        expect(callFunction).not.toThrow()
    })
})
