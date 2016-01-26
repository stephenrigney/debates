xquery version "3.0";

(: Returns json representation of speech elements, with date, speaker and speech URI. Speech text is output as an array whereby the text of every <p> element of the speech :)

declare namespace akn="http://docs.oasis-open.org/legaldocml/ns/akn/3.0/CSD13";


declare namespace output = "http://www.w3.org/2010/xslt-xquery-serialization";
declare option output:method "json";
declare option output:media-type "application/json";


let $banking := collection("/db/apps/banking/data")

let $hearings :=
for $speech in $banking//akn:debateSection/akn:speech[1]

let $root := root($speech)
let $uri := $root//akn:FRBRExpression/akn:FRBRuri/@value
let $date := $root//akn:FRBRWork/akn:FRBRdate/@date
let $dsect := $speech/ancestor::akn:debateSection[1]/@eId
let $eId := $speech/@eId
let $spkr := $root//akn:TLCPerson[@eId eq substring($speech/@by, 2)]/@href
let $text := for $p in $speech/akn:p
        return <text>{string($p)}</text>

return
    <speeches>
        <uri>{concat($uri, "/", $dsect, "/", $eId)}</uri>
        <spkr>{xs:string($spkr)}</spkr>
        {$text}

    </speeches>

return $hearings
