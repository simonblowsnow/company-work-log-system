const popup = require("./popup")
// @ponicode
describe("popup.default.data", () => {
    test("0", () => {
        let callFunction = () => {
            popup.default.data()
        }
    
        expect(callFunction).not.toThrow()
    })
})
