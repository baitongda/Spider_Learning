function main(splash,args)
    treat = require("treat")
    splash:go("http://quotes.toscrape.com")
    local texts = splash:select_all(".quote .text")
    local results = {}
    for index,text in ipairs(texts) do
        results[index] = text 
    end
    return treat.as_array(results)
end